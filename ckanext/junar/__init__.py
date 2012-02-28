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


html.EMBED_IFRAME = '<div class="related_elements"><h3>Related Elements</h3><iframe title="%(name)s" width="400" height="175" src="%(embed)s" frameborder="0" style="border:1px solid #E2E0E0;padding:0;margin:0;"></iframe></div>'


class Junar(SingletonPlugin):
    
    implements(IMapper)
    implements(IConfigurable)
    implements(IDomainObjectModification)
    implements(IGenshiStreamFilter)
    
    def before_insert(self, mapper, connection, instance):
        if isinstance(instance,Resource):
            resource = instance
            related_element = ResourceRelatedElement()
            
            datastream = self.publish_resource_in_junar(resource)
            
            if datastream is not None:
                related_element.name = datastream.guid
                related_element.title = resource.name
                related_element.url = resource.url 
                related_element.embed_code = u'http://staging.junar.com/portal/DataServicesManager/actionEmbed?guid='+datastream.guid + u'&end_point='
                instance.related_elements.append(related_element)
            
            
        """
        Receive an object instance before that instance is INSERTed into its table.
        """
        
    def publish_resource_in_junar(self,resource):
        dictionary = {
                'source':resource.url,
                'title':resource.name.encode('utf-8'),
                'subtitle':(resource.name + u' - subtitle').encode('utf-8'),
                'description': resource.description.encode('utf-8'),
                'tags':'', #empty for now because resources do not have any tags
                'notes':'',#empty for now because resources do not have any author notes
                'table_id':'table0',
                'category':'world',
                'auth_key':JUNAR_API_KEY
            }
            
            
        from junar_api import junar_api
        
        junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')
        dataset = junar_api_client.publish(dictionary)   
        
        return dataset
        
            
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
        
        
    def filter(self, stream):
        from pylons import request, tmpl_context as c
        routes = request.environ.get('pylons.routes_dict')
        is_resource_view = routes.get('controller') == 'package' and routes.get('action') == 'resource_read'
        if is_resource_view and c.resource['id']:
            id = c.resource['id']
            related_elements = model.Session.query(ResourceRelatedElement).filter(ResourceRelatedElement.resource_id == id)
            if related_elements.count() > 0 :
                first_related_element = related_elements.first()
                
                data = {'embed': first_related_element.embed_code, 'name':first_related_element.name}
                
                stream = stream | Transformer('//div[@class=\'quick-info\']')\
                    .after(HTML(html.EMBED_IFRAME % data))
            stream = stream | Transformer('//div[@class=\'resource-preview\']').remove()
        return stream
