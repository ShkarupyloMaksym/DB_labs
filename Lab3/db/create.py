import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models.weather import Weather
from data.dataProcessing import DataImporter


def create_database():
    df = DataImporter().get_data()

    engine = sa.create_engine('postgresql://Shkarupylo:Shkarupylo@localhost/lab3')

    Weather.metadata.drop_all(engine)
    Weather.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        weather_record = Weather(**row.to_dict())
        session.add(weather_record)

    session.commit()
    session.close()


if __name__ == '__main__':
    create_database()
