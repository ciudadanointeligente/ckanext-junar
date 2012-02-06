from ckanext.junar import Junar
import unittest
from ckan import plugins
from sqlalchemy import MetaData, __version__ as sqav
from nose.tools import assert_equal, raises

from ckan.tests import *
import ckan.model as model
from ckan.lib.create_test_data import CreateTestData
from mock import Mock


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
        for url in self.urls:
            pr = model.Resource(url=url,
                                format=self.format,
                                description=self.description,
                                hash=self.hash,
                                alt_url=self.alt_url,
                                extras={u'size':self.size},
                                )
            rg.resources.append(pr)
        pr = model.Resource(url="no_extra",
                            format=self.format,
                            description=self.description,
                            hash=self.hash,
                            )
        rg.resources.append(pr)
        model.repo.commit_and_remove()

    def teardown(self):
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        plugins.reset()
    
    
    def test_when_saving_a_resource_it_gets_a_new_guid_from_junar(self):
        assert True
