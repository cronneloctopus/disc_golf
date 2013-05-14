import os
import requests
from functools import wraps
from flask import request, render_template, redirect, \
    url_for, session, g, flash, Blueprint
from disc_golf.models import Course, ScoreCard
from forms import LoginForm, ScoreForm

from flask.ext.openid import OpenID
from config import OPENID_PROVIDERS
from models import User

from config import app


index_page = Blueprint(
    'index_page', __name__,
    template_folder='templates'
)


@app.template_filter('divide')
def divide_filter(v, arg):
    return v / arg


@app.template_filter('subtract')
def subtract_filter(v, arg):
    return v - arg


############################ FUNTIONS ######################

# send mail function
def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests.post(
        "https://api.mailgun.net/v2/%s/messages" % app.config['MAILGUN_DOMAIN'],
        auth=("api", app.config['MAILGUN_KEY']),
        data={
            "from": from_address,
            "to": to_address,
            "subject": subject,
            "text": plaintext,
            "html": html
        }
    )
    return r


############################ OPENID ######################

basedir = os.path.abspath(os.path.dirname(__file__))
oid = OpenID(app, os.path.join(basedir, 'tmp'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/success', methods=['GET', 'POST'])
def success():
    return "success!"


@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = User.objects.get_or_404(email=session['email'])


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('posts.list'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(
            form.openid.data, ask_for=['nickname', 'email']
        )
    return render_template(
        'login.html',
        next=oid.get_next_url(),
        error=oid.fetch_error(),
        title='Sign In',
        form=form,
        providers=OPENID_PROVIDERS
    )


@oid.after_login
def after_login(resp):
    # if fields empty, flash error message
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    try:
        # get user object based on request
        user = User.objects.get(email=resp.email)
    except User.DoesNotExist:
        # add user to db!!
        # split on '@' and return first string
        # TODO: handle none unique usernames
        username = resp.email.split('@', 1)[0]
        user = User(
            username=username,
            email=resp.email
        )
        user.save()
        # send email confirmation to user
        send_mail(
            to_address=resp.email,
            from_address='discgolf-app@gmail.com',
            subject='Welcome to Disc Golf!',
            plaintext='Welcome to Disc Golf!',
            html='<b>Welcome to Disc Golf!</b>'
        )

    session['user'] = user
    session['email'] = resp.email
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    else:
        flash(u'Your credentials have not been recognized')
        return redirect(url_for('login'))
    return redirect(url_for('success', next=oid.get_next_url(),
                            username=resp.nickname,
                            email=resp.email))


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember_me', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())
    
######################## END OPENID ######################


@app.route('/test/')
#@login_required
def test():
    return render_template(
        'test.html',
    )


@index_page.route('/')
#@login_required
def index():
    courses = Course.objects.all()

    return render_template(
        'index.html',
        title='Disc Golf - Home',
        courses=courses
    )


@app.route('/course/<slug>/', methods=['GET', 'POST'])
def course_detail(slug):
    # check for map variable
    if request.method == "GET" and request.args.get("map"):
        session['map_provider'] = request.args.get("map")
    course = Course.objects.get(slug=slug)
    # score form
    form = ScoreForm(request.form)
    # validate and submit form data
    if request.method == 'POST' and form.validate():
        course_score = ScoreCard(
            user=g.user,
            score=form.score.data,
            baskets=form.baskets.data,
            course=course
        )
        if course_score.created:
            course_score.created = form.created.data
        course_score.save()

        flash('Thanks for submitting a score!')

        # TODO: send email to user
        # TODO: use celery to offload to queue
        send_mail(
            to_address=g.user.email,
            from_address='discgolf-app@gmail.com',
            subject='New Dsic Golf Scorecard Score.',
            plaintext='You just recorded a new score for ' + course.name,
            html='You just recorded a new score for <b>' + course.name + '</b>'
        )

    # get course data
    data = {'nine_sum': 0, 'eighteen_sum': 0}
    nine_count = 0
    eighteen_count = 0
    all_scores = ScoreCard.objects.all().filter(course=course).filter(
        user=g.user
    ).order_by('-created')
    # print all_scores

    nine_scores = []
    eighteen_scores = []

    if all_scores:
        # get data of last round
        data['last_round'] = all_scores[0]

        for card in all_scores:
            if card.baskets == 9 and card.score:
                nine_count += 1
                # make time tuple
                tt = card.created.timetuple()
                dt = (tt[0], tt[1], tt[2])
                # update dictionary
                nine_scores.append((dt, card.score))
                data['nine_sum'] += card.score
            elif card.baskets == 18 and card.score:
                eighteen_count += 1
                # make time tuple
                tt = card.created.timetuple()
                dt = (tt[0], tt[1], tt[2])
                # update dictionary
                eighteen_scores.append((dt, card.score))
                data['eighteen_sum'] += card.score

        # get avgs
        if data['nine_sum']:
            data['nine_avg'] = data['nine_sum'] / len(nine_scores)
        if data['eighteen_sum']:
            data['eighteen_avg'] = data['eighteen_sum'] / len(eighteen_scores)

        # get min, max
        if len(nine_scores) > 0:
            data['nine_max'] = map(max, zip(*nine_scores))
            data['nine_min'] = map(min, zip(*nine_scores))
        if len(eighteen_scores) > 0:
            data['eighteen_max'] = map(max, zip(*eighteen_scores))
            data['eighteen_min'] = map(min, zip(*eighteen_scores))

        # get start date, end date

    return render_template(
        'course_detail.html',
        title='Course Detail -' + course.name,
        course=course,
        form=form,
        data=data,
        all_scores=all_scores,
        nine_scores=nine_scores,
        eighteen_scores=eighteen_scores,
    )
