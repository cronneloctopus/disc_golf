from application import db
import datetime
import re


ROLE_USER = 0
ROLE_ADMIN = 1

_punct_re = re.compile(
    r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+'
)


def slugify(text, delim=u'-'):
    """
    Generates an ASCII-only slug.
    """
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(word.split())
    return unicode(delim.join(result))


class User(db.DynamicDocument):
    #openid = db.IntField(primary_key=True)
    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    role = db.IntField(default=ROLE_USER)

    # speifics for OpenID
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #def get_id(self):
    #    return unicode(self.id)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % (self.username)


class Course(db.DynamicDocument):
    """
    Model for disc golf course detail.
    """
    name = db.StringField(max_length=255, required=True)
    location = db.GeoPointField()
    description = db.StringField(max_length=255, required=False)
    slug = db.StringField(max_length=255, required=False)
    par = db.StringField(max_length=255, required=False)
    #thumbnail = db.ImageField()

    def save(self, *args, **kwargs):
        # custom save method to create slug
        self.slug = slugify(text=self.name)
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_slug(self):
        slug = slugify(text=self.name)
        return slug


class ScoreCard(db.DynamicDocument):
    """
    Model for user scores by course.
    """
    user = db.ReferenceField(User)
    course = db.ReferenceField(Course)
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    score = db.IntField()
    baskets = db.IntField()
    handicap = db.IntField(default=0, required=False)

    def __unicode__(self):
        return "%s | %s | %s (%s)" % (
            self.user, self.course, self.score, self.baskets
        )
