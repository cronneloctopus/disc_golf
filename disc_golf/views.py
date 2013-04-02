from flask import request, redirect, render_template, url_for, \
    session, g, flash, Blueprint
from config import app
from disc_golf.models import Course


index_page = Blueprint(
    'index_page', __name__,
    template_folder='templates'
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
