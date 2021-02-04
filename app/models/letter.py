from sqlalchemy.orm.exc import NoResultFound

from app import db


class Letter(db.Model):
    __tablename__ = "letter"

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(256))
    status = db.Column(db.String(191))

    # Gets letter object from database.
    @classmethod
    def get(cls, track_number):
        try:
            letter = db.session.query(cls).filter_by(
                tracking_number=track_number).one()
            return letter
        except NoResultFound as err:
            return None

    # Creates a letter in database.
    @classmethod
    def create_letter(cls, tracking_number, status):
        """
        Create a new Letter entry in database.

        :param tracking_number: Letter tracking number
        :type tracking_number:  str
        :param status:          Letter status
        :type status:           str
        :rtype:     json
        """
        letter = cls(tracking_number=tracking_number, status=status)
        letter.add()

    # Gets all letters in database.
    @classmethod
    def get_all(cls):
        letters = db.session.query(cls).all()
        return letters
