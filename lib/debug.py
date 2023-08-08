from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Role, Audition

if __name__ == '__main__':
    engine = create_engine('sqlite:///theater.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    import ipdb; ipdb.set_trace()