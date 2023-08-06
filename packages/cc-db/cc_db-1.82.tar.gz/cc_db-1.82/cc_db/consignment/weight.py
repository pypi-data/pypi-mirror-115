from cc_db.engines import *
from cc_db.session_handler import SessionHandler
from sqlalchemy import Column, ForeignKey, String, Integer, Numeric
from .timeindex import TimeIndex
from .forecastunit import ForecastUnit
from .model import Model
from cc_db.cargoline.partner import Partner

class Weight(Base,SessionHandler):
  __tablename__ = 'weight'
  TimeIndexId = Column(String,  ForeignKey('timeindex.Id'), primary_key=True)
  ForecastUnitId = Column(String,  ForeignKey('forecastunit.Id'), primary_key=True)
  ModelId = Column(Integer, ForeignKey('model.Id'), primary_key=True)
  WeightedModelId = Column(Integer,  ForeignKey('model.Id'), primary_key=True)
  PartnerId= Column(String,  ForeignKey('partner.Id'),primary_key=True)
  H = Column(Integer)
  Weight = Column(Numeric)
  
  def create_session(self):
    Session = sessionmaker(forecast_engine)
    return Session()
  
  
  
  def __repr__(self):
    return "<Weight(TimeIndexId='%s', ForecastUnitId='%s', ModelId='%s', WeightedModelId='%s', PartnerId='%s', H='%s',Weight='%s')>" % (self.TimeIndexId, self.ForecastUnitId, self.ModelId, self.WeightedModelId, self.PartnerId, self.H, self.Weight)
