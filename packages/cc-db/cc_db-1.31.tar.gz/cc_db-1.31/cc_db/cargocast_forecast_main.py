from .cargocast_forecast.forecastunit import ForecastUnit
from .cargocast_forecast.model import Model
from .cargocast_forecast.timeindex import TimeIndex
from .cargocast_forecast.observation import Observation
from .cargocast_forecast.forecast import Forecast
from .cargocast_forecast.weight import Weight
from .cargoline.partner import Partner
from .company.company import Company
from datetime import date
from .engines import *
from .session_handler import SessionHandler
import pandas as pd

# insert new forecastunit
fc = ForecastUnit(Id = 'NEW_FC_UNIT_TEST67' ,Name = "Test", Description = 'F').to_database()
fc.delete()

p=Partner(Id = '1234', CompanyId = 1, Name = "test", Bundesland = "Sachsen").to_database()
p.delete()


# delete forecastunit --> query from object
ForecastUnit(Id = 'NEW_FC_UNIT_TEST3').delete_from_object_params()


m=Model(Name = "Test_Model",Description = "recursive ARIMA Model", Combination = False, Recursive = True,Active = True, Creator = "Dietrich").to_database()
m.delete()

ti=TimeIndex(Id = "W",Name = "Week", Description = "Weekly Forecast" ).to_database()
ti.delete()


ob=Observation(TimeIndexId = "D",ForecastUnitId = "SE_PIECE", PartnerId = '4144',Date = date.today(), Value = 1234).to_database()
ob.delete()


fc=Forecast(TimeIndexId = "D",ForecastUnitId = "SE_PIECE", PartnerId = '4144',ModelId = 6,Date = date.today(), H = 1,Forecast = 1234).to_database()
fc.delete()


p=Partner(Id = '1234', CompanyId = 1, Name = "test", Bundesland = "Sachsen")
p.to_database()

# test delete all forecast from specic model
m=Model(Name = "Test_Model",Description = "recursive ARIMA Model", Combination = False, Recursive = True,Active = True, Creator = "Dietrich").to_database()
fc1 = Forecast(TimeIndexId = "D",ForecastUnitId = "SE_PIECE", PartnerId = '4144',ModelId = m.Id,Date = date.today(), H = 1,Forecast = 1234).to_database()
fc2 = Forecast(TimeIndexId = "D",ForecastUnitId = "SE_PIECE", PartnerId = '4144',ModelId = m.Id,Date = date.today(), H = 2,Forecast = 1234).to_database()
dt_fc = Forecast(ModelId = m.Id).get_matchings()
Forecast(ModelId = m.Id).delete_from_object_params(unique = False)
m.delete()



