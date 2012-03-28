# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)



import logging
log = logging.getLogger(__name__)


from genshi.core import TEXT
from genshi.input import HTML
from genshi.filters import Transformer

from ckan.plugins.core import SingletonPlugin, implements
from ckan.plugins.interfaces import IMapper, IConfigurable, IGenshiStreamFilter, IConfigurer
from ckan.model.resource import Resource
from ckanext.junar.model import setup, ResourceRelatedElement
import ckan.model as model

import html


html.EMBED_IFRAME = '<div class="related_elements"><h3>Related Elements</h3><iframe title="%(name)s" width="400" height="175" src="%(embed)s" frameborder="0" style="border:1px solid #E2E0E0;padding:0;margin:0;"></iframe></div>'


class Junar(SingletonPlugin):
    
    implements(IConfigurer, inherit=False)
    implements(IMapper, inherit=True)
    implements(IGenshiStreamFilter)
    
    def update_config(self, config):
        self.api_url = config.get('junar_api_url', None)
        self.base_url = config.get('junar_base_url', None)
        self.api_key = config.get('junar_api_key', None)


    def before_insert(self, mapper, connection, instance):

        if isinstance(instance,Resource):
            resource = instance
            related_element = ResourceRelatedElement()
            
            datastream = self.publish_resource_in_junar(resource)
            if datastream is not None:
                related_element.name = datastream.guid
                related_element.title = resource.name
                related_element.url = resource.url 
                related_element.embed_code = self.base_url + u'/portal/DataServicesManager/actionEmbed?guid='+datastream.guid + u'&end_point='
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
                'tags':'datos,ciudadanointeligente,transparencia', #empty for now because resources do not have any tags
                'notes':'',#empty for now because resources do not have any author notes
                'table_id':'table0',
                'category':'world',
                'auth_key': self.api_key
            }
            
            
        from junar_api import junar_api
        junar_api_client = junar_api.Junar(self.api_key , base_uri = self.api_url)

        dataset = junar_api_client.publish(dictionary)   
        
        return dataset
        
        
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
