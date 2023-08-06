from cc_db.session_handler import SessionHandler
from sqlalchemy import Column
from sqlalchemy import String, Integer*
from cc_db.engines import *


class Company(Base,SessionHandler):
  __tablename__ = 'company'
  Id = Column(Integer, primary_key=True)
  Name = Column(String)

  def create_session(self):
    Session = sessionmaker(company_engine)
    return Session()
  
  
  def __repr__(self):
    return "<Company(Id='%s', Name='%s')>" % (self.Id, self.Name)
  
  
# C:/Users/p.dietrich/Documents/CargoCast/cc-forecast/cc.forecast/virtualenv/cc_db
