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

from ckanext.config import JUNAR_API_KEY

class Junar(SingletonPlugin):
    
    implements(IMapper)
    implements(IConfigurable)
    implements(IDomainObjectModification)
    
    def before_insert(self, mapper, connection, instance):
        if isinstance(instance,Resource):
            resource = instance
            related_element = ResourceRelatedElement()
            dictionary = {
                'url':resource.url,
                'title':resource.name,
                'subtitle':resource.name,
                'description': resource.description,
                'tags':[], #empty for now because resources do not have any tags
                'author_notes':'',#empty for now because resources do not have any author notes
                'from':0
            }
            #aqui obtengo el guid de junar
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY)
            response = junar_api_client.publish(dictionary)
            
            #
            
            related_element.name = response['guid']
            related_element.title = resource.name
            related_element.url = response['url']
            instance.related_elements.append(related_element)
            #model.Session.commit()
            #trans.commit()
        """
        Receive an object instance before that instance is INSERTed into its table.
        """
        #pass

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
        pass
                                     
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
        pass
    
    
    def configure(self, config):
        setup()
