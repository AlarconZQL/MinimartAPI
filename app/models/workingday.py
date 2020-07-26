from sqlalchemy import UniqueConstraint
from app.utils import Days
from app.models import db
from app.models.store_workingday import store_workingday


class WorkingDay(db.Model):
    '''Data model for working days'''
    __tablename__ = 'workingday'
    __table_args__ = (UniqueConstraint('day', 'starts_at', 'finishes_at',
                                       name='_workingday_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Enum(Days), nullable=False)
    starts_at = db.Column(db.Time, nullable=False)
    finishes_at = db.Column(db.Time, nullable=False)
    stores = db.relationship(
        'Store', secondary=store_workingday, back_populates='workingdays')

    def __repr__(self):
        return f'<WorkingDay {self.day} - {self.starts_at} - {self.finishes_at}>'
