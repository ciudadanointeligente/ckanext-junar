# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)



import logging
log = logging.getLogger(__name__)

import html
from genshi.core import TEXT
from genshi.input import HTML
from genshi.filters import Transformer

from ckan.plugins.core import SingletonPlugin, implements
from ckan.plugins.interfaces import IMapper, IDomainObjectModification
from ckan.plugins.interfaces import IConfigurable, IGenshiStreamFilter
from ckan.model.resource import Resource
from ckanext.junar.model import setup, ResourceRelatedElement
import ckan.model as model

class Junar(SingletonPlugin):
    
    implements(IMapper)
    implements(IConfigurable)
    implements(IDomainObjectModification)
    
    def before_insert(self, mapper, connection, instance):
        """
        Receive an object instance before that instance is INSERTed into its table.
        """
        pass

    def before_update(self, mapper, connection, instance):
        """
        Receive an object instance before that instance is UPDATEed.
        """
        pass

    def before_delete(self, mapper, connection, instance):
        """
        Receive an object instance before that instance is DELETEed.
        """
        pass

    def after_insert(self, mapper, connection, instance):
        if isinstance(instance,Resource):
            print instance
                                     
    def after_update(self, mapper, connection, instance):
        """
        Receive an object instance after that instance is UPDATEed.
        """
        pass
    
    def after_delete(self, mapper, connection, instance):
        """
        Receive an object instance after that instance is DELETEed.
        """
        pass
    def notify(self, entity, operation):
        if isinstance(entity,Resource) and operation == "new":
            resource = entity
            related_element = ResourceRelatedElement(resource=resource,name=resource.name, title=resource.name,url=resource.url)
            model.Session.add(related_element)
            model.repo.commit_and_remove()
    
    
    def configure(self, config):
        setup()
