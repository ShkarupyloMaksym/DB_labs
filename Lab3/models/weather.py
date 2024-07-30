from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WindDirection(Enum):
    N = 'N'
    NNE = 'NNE'
    NE = 'NE'
    ENE = 'ENE'
    E = 'E'
    ESE = 'ESE'
    SE = 'SE'
    SSE = 'SSE'
    S = 'S'
    SSW = 'SSW'
    SW = 'SW'
    WSW = 'WSW'
    W = 'W'
    WNW = 'WNW'
    NW = 'NW'
    NNW = 'NNW'


class Weather(Base):
    __tablename__ = 'weather_db'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, unique=True)
    country = sa.Column(sa.String)
    wind_degree = sa.Column(sa.Integer)
    wind_kph = sa.Column(sa.Float)
    wind_direction = sa.Column(sa.Enum(WindDirection))
    last_updated = sa.Column(sa.Date)
    sunrise = sa.Column(sa.Time)
    pressure_mb = sa.Column(sa.Float)
    pressure_in = sa.Column(sa.Float)
    precip_mm = sa.Column(sa.Float)
    precip_in = sa.Column(sa.Float)
    humidity = sa.Column(sa.Integer)
    cloud = sa.Column(sa.Integer)
