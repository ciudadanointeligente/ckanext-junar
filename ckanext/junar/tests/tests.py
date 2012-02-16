from ckanext.junar import Junar
import unittest
from ckan import plugins
from sqlalchemy import MetaData, __version__ as sqav
from nose.tools import assert_equal, raises

from ckan.tests import *
import ckan.model as model
from ckan.lib.create_test_data import CreateTestData
from ckanext.junar.model import ResourceRelatedElement

from ckanext.config import JUNAR_API_KEY

from ludibrio import Stub, Mock

from junar_api import junar_api


dictionary = {'category': '', 'subtitle': u'the title', 'description': u'lorem ipsum', 'title': u'the title', 'end_point': u'thaurl', 'tags': [], 'table_id': 0, 'author_notes': ''}

with Stub() as Junar:
    from junar_api import junar_api
    from ckanext.config import JUNAR_API_KEY
    junar_api_client = junar_api.Junar(JUNAR_API_KEY)

    junar_api_client.publish(dictionary) >> {
        'subtitle': u'the title',
        'description': u'lorem ipsum', 
        'title': u'the title', 
        'source': u'thaurl', 
        'link': 'http://www.junar.com/someurl/that/junar/gave/us', 
        'result': {
            'fLength': 0, 
            'fType': 'ARRAY', 
            'fTimestamp': 0, 
            'fArray': [ {'fStr': '', 'fType': 'TEXT'}, 
                        {'fStr': 'COBRE (1)', 'fType': 'TEXT'}, 
                        {'fStr': 'Enero', 'fType': 'TEXT'}, 
                        {'fStr': '364.8', 'fType': 'TEXT'}], 
            'fRows': 2, 
            'fCols': 2
        }, 
        'id': u'the-precious-guid'
    }
    
    
    
    datastream = junar_api_client.datastream('theguid')
    
    datastream.invoke(output = 'json_array') >> "{'subtitle': 'the title', 'description': 'lorem ipsum', 'title': 'the title', 'source': 'thaurl', 'link': 'http://www.junar.com/someurl/that/junar/gave/us', 'result': [['', 'COBRE (1)'], ['Enero', '364.8']], 'id': 'the-precious-guid'}"

    
    

class TestJunar(unittest.TestCase):
    
    @classmethod
    def setup_class(cls):
        plugins.load('junar')

    def setUp(self):
        self.pkgname = u'resourcetest'
        assert not model.Package.by_name(self.pkgname)
        assert model.Session.query(model.Resource).filter(model.Resource.name == u'resourcetest').count() == 0
        self.urls = [u'http://somewhere.com/', u'http://elsewhere.com/']
        self.format = u'csv'
        self.description = u'Important part.'
        self.hash = u'abc123'
        self.alt_url = u'http://alturl' 
        self.size = 200
        self.label = 'labeltest'
        self.sort_order = '1'
        rev = model.repo.new_revision()
        pkg = model.Package(name=self.pkgname)
        model.Session.add(pkg)
        rg = pkg.resource_groups[0]
        
        self.pr = model.Resource(url=u'thaurl',
                            name=u'the title',
                            format=u'csv',
                            description=u'lorem ipsum',
                            hash=u'12345',
                            alt_url=u'http://theurl.com',
                            extras={u'size':200},
                            )
        rg.resources.append(self.pr)
        model.repo.commit_and_remove()

    def teardown(self):
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        plugins.reset()
        
        
    def test_create_a_new_related_resource_element_create_automatically_one_with_junar(self):
        resource = model.Session.query(model.Resource).get(self.pr.id)
        assert len(resource.related_elements) == 1
        related_element = resource.related_elements[0]
        
        
class TestResourceRelatedElement(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        plugins.load('junar')
        
        
    def setUp(self):
        pass
    
    def teardown(self):
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        plugins.reset()

    def test_create_a_new_related_element_and_related_it_to_a_resource(self):
        pr = model.Resource(url=u'thaurl',
                            name=u'the title',
                            format=u'csv',
                            description=u'lorem ipsum',
                            hash=u'12345',
                            alt_url=u'http://theurl.com',
                            extras={u'size':200},
                            )
        model.Session.add(pr)
        rev = model.repo.new_revision()
        model.repo.commit_and_remove()
        resource_related_element = ResourceRelatedElement(name="elemento relacionado")
        resource_related_element.resource = pr
        resource_related_element.title = u'elemento relacionado'
        resource_related_element.url = u'http://www.ciudadanointeligente.cl'
        resource_related_element.embed_code = u'<iframe src="http://ciudadanointeligente.cl"></iframe>'
        model.Session.add(resource_related_element)
        model.repo.commit_and_remove()
        assert model.Session.query(ResourceRelatedElement).filter_by(resource=pr).count() == 2
        saved_element = model.Session.query(ResourceRelatedElement).get(resource_related_element.id)
        assert saved_element.name == u'elemento relacionado'
        
class TestGettingThingsFromJunarApi(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        plugins.load('junar')        
        
    def setUp(self):
        pass
        
        
    def test_get_guid_from_junar(self):        
        pr = model.Resource(url=u'thaurl',
                            name=u'the title',
                            format=u'csv',
                            description=u'lorem ipsum',
                            hash=u'12345',
                            alt_url=u'http://theurl.com',
                            extras={u'size':200},
                            )
        
        rev = model.repo.new_revision()
        model.Session.add(pr)
        model.repo.commit_and_remove()
        resource = model.Session.query(model.Resource).get(pr.id)
        
        related_element = resource.related_elements[0]
        assert related_element.name == u'the-precious-guid'
        assert related_element.url == u'http://www.junar.com/someurl/that/junar/gave/us'
        assert related_element.embed_code == u'<iframe title="the-precious-guid" width="400" height="175" src="http://www.junar.com/portal/DataServicesManager/actionEmbed?guid=the-precious-guid&amp;end_point=&amp;header_row=0" frameborder="0" style="border:1px solid #E2E0E0;padding:0;margin:0;"></iframe><p style="padding:3px 0 15px 0;margin:0;font:11px arial, helvetica, sans-serif;color:#999;">Powered by <a href="http://www.junar.com" title="Junar &middot; Discovering Data" style="color:#0862A2;">Junar</a></p>'
        
