from flask import url_for
from application import db


ROLE_USER = 0
ROLE_ADMIN = 1


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
    #location = db.GeoPointField()
    description = db.StringField(max_length=255, required=False)
    slug = db.StringField(max_length=255, required=True)
    #thumbnail = db.ImageField()

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.name


class ScoreCard(db.DynamicDocument):
    """
    Model for user scores by course.
    """
    user = db.ReferenceField(User)
    course = db.ReferenceField(Course)
    score = db.IntField()
    handicap = db.IntField(default=0)

    def __unicode__(self):
        return "%s | %s | %s" % (self.user, self.course, self.score)
