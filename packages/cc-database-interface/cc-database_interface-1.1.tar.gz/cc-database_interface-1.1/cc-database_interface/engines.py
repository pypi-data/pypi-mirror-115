from sqlalchemy.sql.schema import MetaData
from sqlalchemy.orm import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_BINDS = {
    'cargoline':'mysql://root:RHyndmanfpp3@127.0.0.1:3306/cargoline',
    'usermanagement': 'mysql://root:RHyndmanfpp3@localhost/cargocast_usermanagement',
    'forecast': 'mysql://root:RHyndmanfpp3@localhost/cargocast_forecast',
    'company':  'mysql://root:RHyndmanfpp3@localhost/company'
}



cargoline_engine = db.create_engine(SQLALCHEMY_BINDS["cargoline"])
usermanagement_engine = db.create_engine(SQLALCHEMY_BINDS["usermanagement"])
forecast_engine = db.create_engine(SQLALCHEMY_BINDS["forecast"])
company_engine = db.create_engine(SQLALCHEMY_BINDS["company"])

meta = MetaData()
Base = declarative_base(metadata = meta)


# Cargoline_Base = declarative_base(bind = cargoline_engine,metadata = meta)
# Usermanagement_Base = declarative_base(bind = usermanagement_engine,metadata = meta)
# Forecast_Base = declarative_base(bind = forecast_engine,metadata = meta)
# Company_Base = declarative_base(bind = company_engine,metadata = meta)
