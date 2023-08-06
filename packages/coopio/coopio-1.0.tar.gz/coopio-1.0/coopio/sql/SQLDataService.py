from typing import List, Dict
from abc import ABC, abstractmethod
from coopio.IDataService import IDataService, T
import logging
import sqlalchemy as db
from sqlalchemy.orm import Session
import pandas as pd
from mapper.object_mapper import ObjectMapper

def create_a_db_connection_string(server_name: str,
                                  db_name: str):
    return 'mssql+pyodbc://@' + server_name + '/' + db_name + '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server'


def get_sql_connection(servername: str, db_name: str, echo: bool = False):
    # Update connection to newly created db
    return db.create_engine(create_a_db_connection_string(servername, db_name)
                            , connect_args={'autocommit': True}
                            , echo=echo)


def get_session(servername: str, db_name: str):
    sqlcon = get_sql_connection(servername, db_name)

    return Session(sqlcon)

def recreate_db(servername: str, db_name: str, echo: bool = False):
    # init connection to master
    sqlcon = get_sql_connection(servername, "master", echo)

    # create the db
    create_db_sql = f"DROP DATABASE IF EXISTS {db_name}; CREATE DATABASE {db_name};"
    deb = sqlcon.execute(create_db_sql)

    # Update connection to newly created db
    return get_sql_connection(servername, db_name, echo)

class SqlDataService(IDataService):

    def __init__(self,
                 servername: str,
                 db_name: str,
                 base: db.orm.decl_api.DeclarativeMeta,
                 orm_obj_mapping_factory: ObjectMapper):

        self.servername = servername
        self.db_name = db_name
        self.base = base
        self.orm_obj_mapping_factory = orm_obj_mapping_factory
        super().__init__()

        # recreate db
        sqlcon = recreate_db(servername, db_name)

        # Create defined tables
        self.base.metadata.create_all(sqlcon)


    @staticmethod
    def _commit(session):
        try:
            session.commit()
            return True
        except db.exc.SQLAlchemyError as e:
            logging.error(e.args)
            session.rollback()
            return False

    def add_or_update(self, type: T, objs: List[T], **kwargs) -> List[T]:

        entries_to_update = []
        entries_to_put = []

        orm_type = list(self.orm_obj_mapping_factory.mappings[type].keys())[0]

        with get_session(self.servername, self.db_name) as session:
            # must batch since there is a max length of 1000 on the .in_ function
            for ii in range(0, len(objs) % 1000, 1000):
                batch = objs[ii: ii + 1000]

                # Find all objects that needs to be updated
                for each in (
                        session.query(orm_type.id).filter(orm_type.id.in_([obj.id for obj in batch])).all()
                ):
                    obj = objs.pop(each.id)
                    entries_to_update.append(obj)

            # Bulk mappings for everything that needs to be inserted
            for obj in objs:
                entries_to_put.append(obj)

            # bulk save
            puts = [self.orm_obj_mapping_factory.map(x) for x in entries_to_put]
            session.bulk_save_objects(puts)

            # merge objects that were already in db
            updts = [self.orm_obj_mapping_factory.map(x) for x in entries_to_update]
            for obj in updts:
                session.merge(obj)

            # commit
            self._commit(session)

            # return
            return self.retrieve_objs(type, [obj.id for obj in objs])

    def retrieve_objs(self, type: T, ids: List[str] = None) -> List[T]:

        orm_type = list(self.orm_obj_mapping_factory.mappings[type].keys())[0]

        with get_session(self.servername, self.db_name) as session:
            # query
            if ids is not None:
                orm_results = session.query(orm_type).filter(orm_type.id in ids)
            else:
                orm_results = session.query(orm_type)

            # map and return
            return [self.orm_obj_mapping_factory.map(x) for x in orm_results]

    def delete(self, type: T, ids: List[str]) -> Dict[str, bool]:
        with get_session(self.servername, self.db_name) as session:
            objs = self.retrieve_objs(type, ids)

            for obj in objs:
                session.delete(obj)

            self._commit(session)

            return {id: True for id in ids}

    def retrieve_as_df(self, ids: List[str] = None) -> pd.DataFrame:
        objs = self.retrieve_objs(ids)
        df = pd.DataFrame(objs)
        return df

    def translate_from_data_rows(self, df: pd.DataFrame) -> List[T]:
        raise NotImplementedError()
