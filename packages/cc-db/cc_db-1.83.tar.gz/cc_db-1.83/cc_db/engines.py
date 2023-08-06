from sqlalchemy.sql.schema import MetaData
from sqlalchemy.orm import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_BINDS = {
    'cargoline':'mysql://root:RHyndmanfpp3@127.0.0.1:3306/cargoline',
    'usermanagement': 'mysql://root:RHyndmanfpp3@localhost/cargocast_usermanagement',
    'forecast_model': 'mysql://root:RHyndmanfpp3@localhost/forecast_model',
    'company':  'mysql://root:RHyndmanfpp3@localhost/company'
}

# pool_size=20, max_overflow=0

cargoline_engine = db.create_engine(SQLALCHEMY_BINDS["cargoline"])
usermanagement_engine = db.create_engine(SQLALCHEMY_BINDS["usermanagement"])
forecast_model_engine = db.create_engine(SQLALCHEMY_BINDS["forecast_model"],pool_size=20, max_overflow=0)
company_engine = db.create_engine(SQLALCHEMY_BINDS["company"])

meta = MetaData()
Base = declarative_base(metadata = meta)

#***UPDATE***
# cd C:/Users/p.dietrich/Documents/CargoCast/cc_db
# python setup.py sdist
# twine upload --skip-existing dist/*
# source C:/Users/p.dietrich/Documents/CargoCast/cc-forecast/cc.forecast/virtualenv/.venv/Scripts/activate
# pip uninstall cc_db
# pip install cc_db==1.82


#***TEST***
# import cc_db.forecast_model.observation as o
# from sqlalchemy.inspection import inspect
# obj = o.Observation(TimeIndexId = "D",ForecastUnitId = "SE_PIECE", PartnerId = '4144', Value = 1234)

