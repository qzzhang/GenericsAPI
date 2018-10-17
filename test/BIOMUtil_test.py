# -*- coding: utf-8 -*-
import inspect
import os
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ

from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenericsAPI.GenericsAPIImpl import GenericsAPI
from GenericsAPI.GenericsAPIServer import MethodContext
from GenericsAPI.authclient import KBaseAuth as _KBaseAuth
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from Workspace.WorkspaceClient import Workspace as workspaceService


class GenericsAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GenericsAPI'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'GenericsAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = GenericsAPI(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)

        suffix = int(time.time() * 1000)
        cls.wsName = "test_GenericsAPI_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        pass #shutil.copytree('data', os.path.join(cls.scratch, 'data'))

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def test_import_matrix_from_biom_1_0(self):
        self.start_test()

        params = {'obj_type': 'AmpliconMatrix',
                  'matrix_name': 'test_AmpliconMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': os.path.join('data', 'phyloseq_test.biom'),
                  'scale': 'raw',
                  'description': "OTU data",
                  }
        returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]
        self.assertIn('matrix_obj_ref', returnVal)
        self.assertIn('report_name', returnVal)
        self.assertIn('report_ref', returnVal)
        obj = self.dfu.get_objects(
            {'object_refs': [returnVal['matrix_obj_ref']]}
        )['data'][0]['data']
        self.assertIn('description', obj)
        self.assertEqual(obj['description'], 'OTU data')
        self.assertIn('attributes', obj)
        self.assertEqual(obj['attributes'], {'generated_by': 'QIIME revision XYZ'})
        self.assertIn('row_attributemapping_ref', obj)
        self.assertIn('col_attributemapping_ref', obj)

    def test_import_matrix_from_biom_2_1(self):
        self.start_test()

        params = {'obj_type': 'AmpliconMatrix',
                  'matrix_name': 'test_AmpliconMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': os.path.join('data', 'v2.1example.biom'),
                  'scale': 'raw',
                  'description': "OTU data",
                  }
        returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]
        self.assertIn('matrix_obj_ref', returnVal)
        self.assertIn('report_name', returnVal)
        self.assertIn('report_ref', returnVal)
        obj = self.dfu.get_objects(
            {'object_refs': [returnVal['matrix_obj_ref']]}
        )['data'][0]['data']
        self.assertIn('description', obj)
        self.assertEqual(obj['description'], 'OTU data')
        self.assertIn('attributes', obj)
        self.assertEqual(obj['attributes'], {'generated_by': 'QIIME 1.9.1',
                                             'create_date': '2017-05-22T11:07:28.478444',
                                             })
        self.assertIn('row_attributemapping_ref', obj)

    def test_import_matrix_from_tsv(self):
        self.start_test()

        params = {'obj_type': 'AmpliconMatrix',
                  'matrix_name': 'test_AmpliconMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': os.path.join('data', 'v2.1example.biom'),
                  'scale': 'raw',
                  'description': "OTU data",
                  }
        returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]
        self.assertIn('matrix_obj_ref', returnVal)
        self.assertIn('report_name', returnVal)
        self.assertIn('report_ref', returnVal)
        obj = self.dfu.get_objects(
            {'object_refs': [returnVal['matrix_obj_ref']]}
        )['data'][0]['data']
        self.assertIn('description', obj)
        self.assertEqual(obj['description'], 'OTU data')
        self.assertIn('attributes', obj)

    def test_bad_import_matrix_params(self):
        self.start_test()

        with self.assertRaisesRegex(ValueError, "parameter is required, but missing"):
            params = {'obj_type': 'AmpliconMatrix',
                      'matrix_name': 'test_AmpliconMatrix',
                      'workspace_name': self.wsName,
                      'input_file_path': os.path.join('data', 'test_import.xlsx'),
                      }
            returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]

        with self.assertRaisesRegex(ValueError, "Unknown matrix object type"):
            params = {'obj_type': 'foo',
                      'matrix_name': 'test_AmpliconMatrix',
                      'workspace_name': self.wsName,
                      'input_file_path': os.path.join('data', 'test_import.xlsx'),
                      'scale': 'log2'
                      }
            returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]

        with self.assertRaisesRegex(ValueError, "Unknown scale type"):
            params = {'obj_type': 'AmpliconMatrix',
                      'matrix_name': 'test_AmpliconMatrix',
                      'workspace_name': self.wsName,
                      'input_file_path': os.path.join('data', 'test_import.xlsx'),
                      'scale': 'foo'
                      }
            returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]

        with self.assertRaisesRegex(ValueError, "input_shock_id or input_file_path"):
            params = {'obj_type': 'AmpliconMatrix',
                      'matrix_name': 'test_AmpliconMatrix',
                      'workspace_name': self.wsName,
                      'scale': 'log2'
                      }
            returnVal = self.getImpl().import_matrix_from_biom(self.ctx, params)[0]
