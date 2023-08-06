from cc_db.engines import *
from cc_db.session_handler import SessionHandler
from sqlalchemy import Column, String, Boolean, Integer

class Model(Base,SessionHandler):
  __tablename__ = 'model'
  Id = Column(Integer, primary_key=True)
  Name = Column(String)
  Description = Column(String)
  Combination = Column(Boolean)
  Recursive = Column(Boolean)
  Active = Column(Boolean)
  Creator = Column(String)
  
  def create_session(self):
    Session = sessionmaker(forecast_model_engine)
    return Session()
  
  def __repr__(self):
    return "<Model(Name='%s', Description='%s', Creator='%s', Combination='%s', Recursive='%s', Active='%s')>" % (self.Name, self.Description, self.Creator, self.Combination, self.Recursive, self.Recursive)
