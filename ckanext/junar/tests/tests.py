from ckanext.junar import Junar
import unittest
from ckan import plugins
from sqlalchemy import MetaData, __version__ as sqav
from nose.tools import assert_equal, raises

from ckan.tests import *
import ckan.model as model
from ckan.lib.create_test_data import CreateTestData
from ckanext.junar.model import ResourceRelatedElement

from ludibrio import Stub
from ludibrio.matcher import *



from junar_api import junar_api
from ckanext.config import JUNAR_API_KEY

from junar_api.junar_api import DataStream



    
    

class TestJunar(unittest.TestCase):
    
    @classmethod
    def setup_class(cls):
        plugins.load('junar')
        with Stub() as DataStream:
            DataStream.info() >> {'subtitle': 'mock information', 'description': 'The population rate per province in the Netherlands', 'title': 'Population rate', 'source': 'User Uploaded Data', 'link': 'http://www.junar.com/someurl/that/junar/gave/us', 'result': {'fLength': 0, 'fType': 'ARRAY', 'fTimestamp': 1330368967241L, 'fArray': [], 'fRows': 2, 'fCols': 13}, 'id': 'the-precious-guid'}
            
        with Stub() as Junar:
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')

            junar_api_client.publish(kind_of(dict)) >> DataStream

    def setUp(self):
        self.prepareStub()
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
        
    def prepareStub(self):
        with Stub() as DataStream:
            DataStream.info() >> {'subtitle': 'mock information', 'description': 'The population rate per province in the Netherlands', 'title': 'Population rate', 'source': 'User Uploaded Data', 'link': 'http://www.junar.com/someurl/that/junar/gave/us', 'result': {'fLength': 0, 'fType': 'ARRAY', 'fTimestamp': 1330368967241L, 'fArray': [], 'fRows': 2, 'fCols': 13}, 'id': 'the-precious-guid'}
            
        with Stub() as Junar:
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')

            junar_api_client.publish(kind_of(dict)) >> DataStream

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
        with Stub() as DataStream:
            DataStream.info() >> {'subtitle': 'mock information', 'description': 'The population rate per province in the Netherlands', 'title': 'Population rate', 'source': 'User Uploaded Data', 'link': 'http://www.junar.com/someurl/that/junar/gave/us', 'result': {'fLength': 0, 'fType': 'ARRAY', 'fTimestamp': 1330368967241L, 'fArray': [], 'fRows': 2, 'fCols': 13}, 'id': 'the-precious-guid'}
            
        with Stub() as Junar:
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')

            junar_api_client.publish(kind_of(dict)) >> DataStream
        
        
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
        with Stub() as DataStream:
            DataStream.info() >> {'subtitle': 'mock information', 'description': 'The population rate per province in the Netherlands', 'title': 'Population rate', 'source': 'User Uploaded Data', 'link': 'http://www.junar.com/someurl/that/junar/gave/us', 'result': {'fLength': 0, 'fType': 'ARRAY', 'fTimestamp': 1330368967241L, 'fArray': [], 'fRows': 2, 'fCols': 13}, 'id': 'the-precious-guid'}
            
        with Stub() as Junar:
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')

            junar_api_client.publish(kind_of(dict)) >> DataStream   
        
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
        assert related_element.embed_code == u'http://staging.junar.com/portal/DataServicesManager/actionEmbed?guid=the-precious-guid&end_point='
        

    def test_when_junar_sends_us_an_error_message_we_do_not_create_any_related_element(self):
        with Stub() as Junar:
            from junar_api import junar_api
            junar_api_client = junar_api.Junar(JUNAR_API_KEY, base_uri = 'http://api.staging.junar.com')
            #it is very important to define what this method will return on error
            junar_api_client.publish(kind_of(dict)) >> None
            
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
            
        assert resource.related_elements.__len__() == 0
        
    
        
