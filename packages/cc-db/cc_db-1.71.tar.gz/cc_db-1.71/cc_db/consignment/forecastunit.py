from cc_db.session_handler import SessionHandler
from cc_db.engines import *
from sqlalchemy import Column, String

class ForecastUnit(Base,SessionHandler):
  __tablename__ = 'forecastunit'
  Id = Column(String, primary_key=True)
  Name = Column(String)
  Description = Column(String)
  
  def create_session(self):
    Session = sessionmaker(forecast_engine)
    return Session()
  
  def __repr__(self): 
    return "<ForecastUnit(Id='%s', Name='%s', Description='%s')>" %(self.Id, self.Name, self.Description)
  
    
