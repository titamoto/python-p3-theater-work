from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'audition'

    id = Column(Integer(), primary_key = True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer(), ForeignKey('role.id'))

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        engine = create_engine('sqlite:///theater.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(Audition).filter(Audition.id == self.id).update({'hired' : True})
        session.commit()
        return session.query(Audition).filter(Audition.id == self.id).first()

    def __repr__(self):
        return f'Audition(id={self.id}, ' + \
            f'actor={self.actor}, ' + \
            f'location={self.location}) ' + \
            f'phone={self.phone}) ' + \
            f'hired={self.hired}) ' + \
            f'role_id={self.role_id}) '
 
class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer(), primary_key = True)
    character_name = Column(String())

    auditions = relationship('Audition', back_populates='role')
    actors = association_proxy('auditions', 'actor', creator=lambda actor : Audition(actor=actor))
    locations = association_proxy('auditions', 'location', creator=lambda location : Audition(location=location))

    def lead(self):
        engine = create_engine('sqlite:///theater.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        hired = session.query(Audition).filter(Audition.role_id == self.id, Audition.hired == True).first()
        if hired == None:
            return 'no actor has been hired for this role'
        return hired

    def understudy(self):
        engine = create_engine('sqlite:///theater.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        all_hired = session.query(Audition).filter(Audition.role_id == self.id, Audition.hired == True).all()
        if len(all_hired) < 2:
            return 'no actor has been hired for understudy for this role'
        return all_hired[1]


    def __repr__(self):
        return f'Role(id={self.id}, ' + \
            f'character_name={self.character_name}) '
