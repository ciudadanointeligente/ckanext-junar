from ckanext.junar import Junar
import unittest
from ckan import plugins
from sqlalchemy import MetaData, __version__ as sqav
from nose.tools import assert_equal, raises

from ckan.tests import *
import ckan.model as model
from ckan.lib.create_test_data import CreateTestData
from ckanext.junar.model import ResourceRelatedElement


class TestJunar(unittest.TestCase):
    
    @classmethod
    def setup_class(cls):
        plugins.load('junar')

    def setUp(self):
        self.pkgname = u'resourcetest'
        assert not model.Package.by_name(self.pkgname)
        assert model.Session.query(model.Resource).count() == 0
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
        
        self.pr = model.Resource(url=u'http://somewhere.com/',
                            format=self.format,
                            description=self.description,
                            hash=self.hash,
                            alt_url=self.alt_url,
                            extras={u'size':self.size},
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
        pr = model.Resource(url=u'http://somewhere.com/',
                            format=u'csv',
                            description=u'a description',
                            hash=u'abc123',
                            alt_url=u'http://alturl',
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
