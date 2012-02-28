import logging
from datetime import datetime

from ckan.lib.munge import munge_title_to_name
from ckan.model.meta import *
from ckan.model.types import make_uuid
from ckan.model.core import *
from ckan.model.resource import Resource
from ckan.model.domain_object import DomainObject

from sqlalchemy.orm import backref, relation

__all__ = [
    'ResourceRelatedElement', 'resource_related_element_table',
]

resource_related_element_table = None

def setup():
    if resource_related_element_table is None:
        create_apps_tables()
    metadata.create_all()

class ResourceRelatedElement(DomainObject):
    @classmethod
    def generate_name(cls, title):
        return _generate_name(cls,title)
    
def create_apps_tables():
    global resource_related_element_table
    
    resource_related_element_table = Table('resource_related_element',metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('resource_id', types.UnicodeText,
            ForeignKey('resource.id')),
        Column('name', types.Unicode(), nullable=True),
        Column('title', types.Unicode(), nullable=True),        
        Column('url', types.UnicodeText, nullable=True),
        Column('embed_code', types.UnicodeText),
        Column('created', DateTime, default=datetime.datetime.now),
        Column('updated', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now),
    )
    ## Mappers

    mapper(ResourceRelatedElement, resource_related_element_table, properties={
        'resource':orm.relation(Resource,
            # all resources including deleted
            # formally resource_related_stuff
            backref=orm.backref('related_elements',
                                cascade='all, delete',
                                ),
                           )
        },
    )
    
    

