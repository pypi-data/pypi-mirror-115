from sqlalchemy.sql.schema import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.inspection import inspect
from sqlalchemy import *
import pandas as pd

class SessionHandler():

  # def create_session(self):
  #   Session = sessionmaker(self.metadata.bind)
  #   return Session()
  
  def to_database(self, overwrite = False):
    session = self.create_session()
    obj = self
    if overwrite == True: obj = self.get_or_create(session, obj)
    session.add(obj)
    self.commit(session)
    return(self)
  
  def all_to_database(self, obj_list, overwrite = False):
    session = self.create_session()
    for obj in obj_list:
      if overwrite == True:
        session = self.get_or_create(session, obj)
      else:
        session.add(obj)
    return self.commit(session)
  
  def get_or_create(self,session, obj):
    keys = [key.name for key in inspect(obj.__class__).primary_key]
    key_values = {k: v for k, v in obj.__dict__.items() if v and k in keys}
    params = {k: v for k, v in obj.__dict__.items() if v and k.startswith("_") == False and k not in keys}
    instance = session.query(obj.__class__).filter_by(**key_values).first()
    if instance:
      instance.update(**params)
    else:
      session.add(obj)
    return session
      
  
  def get_all(self, classname):
    session = self.create_session()   
    object_list = []
    for obj in session.query(classname).order_by(classname.Id):
      object_list.append(obj)
    return object_list


  def get(self, classname, id):
    session = self.create_session()   
    obj = session.query(classname).get(id)
    session.close()
    return obj

  def execute(self, stmt):
    session = self.create_session()   
    result = session.execute(stmt)
    return result
      
  def commit(self,session):
    try:
      session.commit()
      return True
    except Exception as inst:
      print(type(inst))   
      print(inst.args)             
      return False            
    finally:
      if inspect(self).persistent == True: session.refresh(self)
      session.close()
      
  def delete_from_object_params(self,unique = True):
    session = self.create_session()
    params = {k: v for k, v in self.__dict__.items() if v and k.startswith("_") == False}
    q = session.query(self.__class__).filter_by(**params)
    if q.count()==1 or unique == False:
      # only if query identifies a unique database entry
      q.delete()
      self.commit(session)
      res = self.commit(session)
    else:
      session.close()
      res = "no unique object could be identified for deletion!"
    return res
  
  def get_matchings(self, pandas = True):
    session = self.create_session()
    params = {k: v for k, v in self.__dict__.items() if v and k.startswith("_") == False}
    q = session.query(self.__class__).filter_by(**params)
    if pandas == True: q = pd.read_sql(q.statement,q.session.bind)
    return q

  def delete(self):
    session = self.create_session()
    session.delete(self)
    return(self.commit(session))

  def update(self, stmt):
    session = self.create_session()
    result = session.execute(stmt)
    return self.commit(session) and result.rowcount == 1
