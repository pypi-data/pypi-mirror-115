from sqlalchemy.sql.schema import MetaData
from sqlalchemy.orm import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_BINDS = {
    'cargoline':'mysql://root:RHyndmanfpp3@127.0.0.1:3306/cargoline',
    'usermanagement': 'mysql://root:RHyndmanfpp3@localhost/cargocast_usermanagement',
    'forecast': 'mysql://root:RHyndmanfpp3@localhost/consignment',
    'company':  'mysql://root:RHyndmanfpp3@localhost/company'
}



cargoline_engine = db.create_engine(SQLALCHEMY_BINDS["cargoline"])
usermanagement_engine = db.create_engine(SQLALCHEMY_BINDS["usermanagement"])
forecast_engine = db.create_engine(SQLALCHEMY_BINDS["forecast"])
company_engine = db.create_engine(SQLALCHEMY_BINDS["company"])

meta = MetaData()
Base = declarative_base(metadata = meta)

#***UPDATE***
# cd C:/Users/p.dietrich/Documents/CargoCast/cc_db
# python setup.py sdist
# twine upload --skip-existing dist/*
# source C:/Users/p.dietrich/Documents/CargoCast/cc-forecast/cc.forecast/virtualenv/.venv/Scripts/activate
# pip uninstall cc_db
# pip install cc_db==1.77

