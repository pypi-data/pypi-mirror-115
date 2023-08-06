from session_handler import SessionHandler
from engines import *
from company.company import Company
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from engines import *
from sqlalchemy.orm import relationship

class Partner(Base,SessionHandler):
  __tablename__ = 'partner'
  Id = Column(String, primary_key=True)
  CompanyId = Column(Integer, ForeignKey('company.Id'))
  Name = Column(String)
  Bundesland = Column(String)
  
  
  def create_session(self):
    Session = sessionmaker(cargoline_engine)
    return Session()

  def __repr__(self):
    return "<Partner(Id='%s', CompanyId='%s', Name='%s', Bundesland='%s')>" % (
    self.Id, self.CompanyId, self.Name,self.Bundesland)





