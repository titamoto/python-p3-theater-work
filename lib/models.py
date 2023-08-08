from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

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

    def __repr__(self):
        return f'Role(id={self.id}, ' + \
            f'character_name={self.character_name}) '
