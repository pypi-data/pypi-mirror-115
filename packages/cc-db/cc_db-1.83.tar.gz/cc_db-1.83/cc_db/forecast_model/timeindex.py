from cc_db.engines import *
from cc_db.session_handler import SessionHandler
from sqlalchemy import Column, String, Boolean

class TimeIndex(Base,SessionHandler):
  __tablename__ = 'timeindex'
  Id = Column(String, primary_key=True)
  Name = Column(String)
  Description = Column(String)

  def create_session(self):
    Session = sessionmaker(forecast_model_engine)
    return Session()
  
  
  def __repr__(self): 
    return "<TimeIndex(Id='%s', Name='%s', Description='%s')>" %(self.Id, self.Name, self.Description)
