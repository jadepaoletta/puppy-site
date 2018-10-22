"""Models and database functions for NearSited"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions

class Dog(db.Model):
    """User of NearSited website."""

    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    # Define relationship to trip
    photo = db.relationship("DogPhoto",
                            backref=db.backref("dogs",
                                               order_by=dog_id))

    def __repr__(self):
        """Returns the id and name of the User object"""

        return "< id: {} name: {} {} >".format(self.dog_id, self.name)


class Prospect(db.Model):
    """Friend relationship in NearSited website."""

    __tablename__ = "prospects"

    prospect_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Returns the id and name of the User object"""

        return "< id: {} name: {} >".format(self.prospect_id, self.name)


class DogPhoto(db.Model):
    """Photo in NearSited website."""

    __tablename__ = "dog_photos"

    photo_id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.LargeBinary, nullable = False)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    dog = db.relationship("Dog", 
                            backref=db.backref("dog_photos", order_by=photo_id))

    def __repr__(self):
        """Returns details of photo."""

        return "< photo_id {} for dog: {}>".format(self.photo_id, self.dog_id)


class GenPhoto(db.Model):
    """Photo in NearSited website."""

    __tablename__ = "gen_photos"

    photo_id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.LargeBinary, nullable = False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Returns details of photo."""

        return "< photo_id {}>".format(self.photo_id)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bullpups'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."