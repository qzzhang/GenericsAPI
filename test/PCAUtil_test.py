# -*- coding: utf-8 -*-
import inspect
import os  # noqa: F401
import unittest
import time
import pandas as pd
import shutil
from configparser import ConfigParser

from GenericsAPI.Utils.PCAUtil import PCAUtil
from GenericsAPI.GenericsAPIImpl import GenericsAPI
from GenericsAPI.GenericsAPIServer import MethodContext
from GenericsAPI.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as workspaceService


class PCAUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
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
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.pca_util = PCAUtil(cls.cfg)

        suffix = int(time.time() * 1000)
        cls.wsName = "test_pca_util_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.wsId = ret[0]

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def getPCAUtil(self):
        return self.__class__.pca_util

    def loadExpressionMatrix(self):
        if hasattr(self.__class__, 'expr_matrix_ref'):
            return self.__class__.expr_matrix_ref

        matrix_file_name = 'test_import.xlsx'
        matrix_file_path = os.path.join(self.scratch, matrix_file_name)
        shutil.copy(os.path.join('data', matrix_file_name), matrix_file_path)

        obj_type = 'ExpressionMatrix'
        params = {'obj_type': obj_type,
                  'matrix_name': 'test_ExpressionMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': matrix_file_path,
                  'scale': "log2",
                  }
        expr_matrix_ref = self.serviceImpl.import_matrix_from_excel(
            self.ctx, params)[0].get('matrix_obj_ref')

        self.__class__.expr_matrix_ref = expr_matrix_ref
        print('Loaded ExpressionMatrix: ' + expr_matrix_ref)
        return expr_matrix_ref

    def fail_run_pca(self, params, error, exception=ValueError, contains=False):
        with self.assertRaises(exception) as context:
            self.getImpl().run_pca(self.ctx, params)
        if contains:
            self.assertIn(error, str(context.exception.args))
        else:
            self.assertEqual(error, str(context.exception.args[0]))

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    # def test_run_pca_fail(self):
    #     self.start_test()

    #     invalidate_params = {'missing_input_obj_ref': 'input_obj_ref',
    #                          'workspace_name': 'workspace_name'}
    #     error_msg = '"input_obj_ref" parameter is required, but missing'
    #     self.fail_run_pca(invalidate_params, error_msg)

    #     invalidate_params = {'input_obj_ref': 'input_obj_ref',
    #                          'missing_workspace_name': 'workspace_name'}
    #     error_msg = '"workspace_name" parameter is required, but missing'
    #     self.fail_run_pca(invalidate_params, error_msg)

    def test_run_pca_ok(self):
        self.start_test()

        expr_matrix_ref = self.loadExpressionMatrix()

        params = {'input_obj_ref': expr_matrix_ref,
                  'workspace_name': self.wsName,
                  'pca_matrix_name': 'test_pca_matrix_obj'}

        ret = self.getImpl().run_pca(self.ctx, params)[0]

        print(ret)

    # def test_init_ok(self):
    #     self.start_test()
    #     class_attri = ['scratch', 'token', 'callback_url', 'ws_url']

    #     network_util = self.getPCAUtil()
    #     self.assertTrue(set(class_attri) <= set(network_util.__dict__.keys()))
    #     self.assertEqual(network_util.scratch, self.cfg.get('scratch'))

    # def test__Matrix2D_to_df(self):

    #     corr_data = self.loadCorrData()

    #     df = self.getNetworkUtil()._Matrix2D_to_df(corr_data)

    #     self.assertCountEqual(df.index.tolist(), corr_data.get('row_ids'))
    #     self.assertCountEqual(df.columns.tolist(), corr_data.get('col_ids'))
    #     self.assertCountEqual(df.values.tolist(), corr_data.get('values'))

    # def test__trans_df_ok(self):
    #     corr_data = self.loadCorrData()

    #     df = self.getNetworkUtil()._Matrix2D_to_df(corr_data)

    #     links = self.getNetworkUtil()._trans_df(df)

    #     self.assertEqual(links.index.size, len(corr_data.get('row_ids'))**2)
    #     self.assertEqual(links.columns.size, 3)

    # def test_df_to_graph_ok(self):

    #     graph_df = self.loadGraphDF()

    #     graph = self.getNetworkUtil().df_to_graph(graph_df, 'source', 'target')

    #     expected_nodes = ['A', 'E', 'G', 'F', 'I', 'H', 'J']
    #     self.assertCountEqual(list(graph.nodes()), expected_nodes)

    # def test_draw_graph_ok(self):

    #     graph_df = self.loadGraphDF()
    #     graph = self.getNetworkUtil().df_to_graph(graph_df, 'source', 'target')

    #     graph_path = os.path.join(self.scratch, 'graph.png')

    #     self.getNetworkUtil().draw_graph(graph, graph_path)
    #     self.assertGreater(os.path.getsize(graph_path), 1024)  # file size greate than 1KB

    #     self.getNetworkUtil().draw_graph(graph, graph_path, graph_layout='spectral')
    #     self.assertGreater(os.path.getsize(graph_path), 1024)  # file size greate than 1KB
