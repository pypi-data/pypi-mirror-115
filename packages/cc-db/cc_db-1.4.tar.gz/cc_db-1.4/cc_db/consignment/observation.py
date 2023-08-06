from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Date, Integer, Numeric
from sqlalchemy.orm import relationship
from .timeindex import TimeIndex
from .forecastunit import ForecastUnit
from .model import Model
from cc_db.engines import *
from cc_db.cargoline.partner import Partner
from cc_db.session_handler import SessionHandler


class Observation(Base,SessionHandler):
  __tablename__ = 'observation'
  TimeIndexId = Column(String, ForeignKey('timeindex.Id'), primary_key=True)
  TimeIndex = relationship('TimeIndex',foreign_keys = [TimeIndexId])
  ForecastUnitId = Column(String,ForeignKey('forecastunit.Id'),primary_key=True)
  ForecastUnit = relationship('ForecastUnit', foreign_keys = [ForecastUnitId])
  PartnerId = Column(String, ForeignKey('partner.Id'),primary_key=True)
  # Partner = relationship('Partner', foreign_keys = [PartnerId])
  Date = Column(Date, primary_key=True)
  Value = Column(Numeric)

  def create_session(self):
    Session = sessionmaker(forecast_engine)
    return Session()

  def __repr__(self): 
    return "<Observation(TimeIndexId='%s', ForecastUnitId='%s', PartnerId='%s',Date='%s',Value = '%s')>" % (self.TimeIndexId, self.ForecastUnitId, self.PartnerId,self.Date,self.Value)



