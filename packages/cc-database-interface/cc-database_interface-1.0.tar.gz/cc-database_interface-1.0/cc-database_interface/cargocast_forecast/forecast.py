from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Date, Integer, Numeric
from ..engines import *
from ..cargoline.partner import Partner
from .timeindex import TimeIndex
from .forecastunit import ForecastUnit
from .model import Model
from ..session_handler import SessionHandler

class Forecast(Base,SessionHandler):
  __tablename__ = 'forecast'
  TimeIndexId = Column(String, ForeignKey('timeindex.Id'),primary_key=True)
  ForecastUnitId = Column(String,ForeignKey('forecastunit.Id'), primary_key=True)
  PartnerId = Column(String, ForeignKey('partner.Id'), primary_key=True)
  ModelId = Column(Integer, ForeignKey('model.Id'),primary_key=True)
  Date = Column(Date, primary_key=True)
  H = Column(Integer, primary_key=True)
  Forecast = Column(Numeric)
  
  
  def create_session(self):
    Session = sessionmaker(forecast_engine)
    return Session()

  def __repr__(self):
    return "<Forecast(TimeIndexId='%s', ForecastUnitId='%s', PartnerId='%s',ModelId='%s',Date='%s',H='%s',Forecast = '%s')>" % (self.TimeIndexId, self.ForecastUnitId, self.PartnerId, self.ModelId,self.Date,self.H,self.Forecast)
