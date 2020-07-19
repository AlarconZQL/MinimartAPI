from . import db

store_workingday = db.Table('store_workingday',
                            db.Column('store_id', db.Integer,
                                      db.ForeignKey('store.id'), primary_key=True),
                            db.Column('workingday_id', db.Integer,
                                      db.ForeignKey('workingday.id'), primary_key=True))
