import datetime
from sqlalchemy.orm import Query
from sqlalchemy.sql import null
from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy.orm import relationship as rs
from sqlalchemy import event
from sqlalchemy import inspect
import sqlalchemy as sa

class FillableMixin:
    fillable = []
    def fill(self, data):
        for key in self.fillable:
            if key in data:
                setattr(self, key, data[key])
                #print(key + " " + data[key])  

class TimestampMixin:
    created_at = sa.Column(sa.DateTime(), default=datetime.datetime.now)
    updated_at = sa.Column(sa.DateTime(), onupdate=datetime.datetime.now)

class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime(timezone=True), nullable=True)

    def delete(self, deleted_at=None):
        self.deleted_at = deleted_at or datetime.datetime.now()

    def restore(self):
        self.deleted_at = None
 
@event.listens_for(Query, 'before_compile', retval=True)
def before_compile(query):
    #print(str(query))
    include_deleted = query._execution_options.get('include_deleted', False)
    if include_deleted:
        return query

    for column in query.column_descriptions:
        entity = column['entity']
        if entity is None:
            continue

        inspector = inspect(column['entity'])
        mapper = getattr(inspector, 'mapper', None)
        if mapper and issubclass(mapper.class_, SoftDeleteMixin):
            query = query.enable_assertions(False).filter(
                entity.deleted_at.is_(None),
            )
        
    return query


@event.listens_for(SoftDeleteMixin, 'load', propagate=True)
def load(obj, context):
    include_deleted = context.query._execution_options.get('include_deleted', False)
    if obj.deleted_at and not include_deleted:
        raise TypeError('Deleted object '+str(obj)+' was loaded, did you use joined eager loading?')
    

def before_update( mapper, connection, instance):
    """ Make sure when we update this record the created fields stay unchanged!  """
    instance.updated_at = datetime.datetime.utcnow()

event.listen(TimestampMixin, 'before_update', before_update)
