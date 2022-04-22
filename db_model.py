import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlalchemy
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Character(Base):
    __tablename__ = 'Character'

    id = sq.Column(sq.Integer, primary_key=True)
    birth_year = sq.Column(sq.String)
    eye_color = sq.Column(sq.String)
    films = sq.Column(sq.String)
    gender = sq.Column(sq.String)
    hair_color = sq.Column(sq.String)
    height = sq.Column(sq.String)
    homeworld = sq.Column(sq.String)
    mass = sq.Column(sq.String)
    name = sq.Column(sq.String)
    skin_color = sq.Column(sq.String)
    species = sq.Column(sq.String)
    starships = sq.Column(sq.String)
    vehicles = sq.Column(sq.String)


class DbClass:
    def __init__(self, pg_url_connection):
        self.engine = sqlalchemy.create_engine(pg_url_connection)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.creation = Base.metadata.create_all(self.engine)

    def upload_to_db(self, data_dict):
        qty_before = len(self.session.query(Character).all())
        # print('Кол-во было', qty_before)
        print('_' * 20)
        for data in data_dict:
            if self.session.query(Character).filter_by(name=data.get('name')).first() is not None:
                print(f'''{data.get('name')} is existed''')
                continue
            new_data = Character(**data)
            self.session.add(new_data)
            self.session.commit()
            print(f'''{data.get('name')} was added to your DB''')
        print('_' * 20)
        print(len(self.session.query(Character).all()) - qty_before, ' was added by session')
        print('_' * 20)
