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


dictionary = {
            'subtitle': u'the title',
            'description': u'lorem ipsum',
            'tags': [],
            'url': u'thaurl',
            'title': u'the title',
            'from': 0,
            'author_notes': ''}

with Stub() as Junar:
    from junar_api import junar_api
    from ckanext.config import JUNAR_API_KEY
    junar_api_client = junar_api.Junar(JUNAR_API_KEY)

    junar_api_client.publish(dictionary) >> {'guid':'theguid','url':'theurl'}
    datastream = junar_api_client.datastream('theguid')
    
    datastream.invoke(output = 'json_array') >> "{'subtitle': 'Enero 2012', 'description': 'Precio del Cobre para Enero 2012', 'title': 'Precio del Cobre Chile', 'source': 'http://www.bcentral.cl/estadisticas-economicas/series-indicadores/xls/Precio_Cobre__HPescado_Petrol_Celulosa%20.xls', 'link': 'http://www.junar.com/datastreams/68312/precio-del-cobre-chile-enero-2012/', 'result': [['', 'COBRE (1)'], ['Enero', '364.8']], 'id': 'PRECI-DEL-COBRE-ENERO-2012'}{'subtitle': 'Enero 2012', 'description': 'Precio del Cobre para Enero 2012', 'title': 'Precio del Cobre Chile', 'source': 'http://www.bcentral.cl/estadisticas-economicas/series-indicadores/xls/Precio_Cobre__HPescado_Petrol_Celulosa%20.xls', 'link': 'http://www.junar.com/datastreams/68312/precio-del-cobre-chile-enero-2012/', 'result': [['', 'COBRE (1)'], ['Enero', '364.8']], 'id': 'PRECI-DEL-COBRE-ENERO-2012'}"

    
    

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
        assert related_element.name == u'theguid'
        assert related_element.url == u'theurl'
        
