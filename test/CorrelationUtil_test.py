# -*- coding: utf-8 -*-
import inspect
import json  # noqa: F401
import os  # noqa: F401
import unittest

import pandas as pd
import numpy as np

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from GenericsAPI.Utils.CorrelationUtil import CorrelationUtil


class GenericsAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GenericsAPI'):
            cls.cfg[nameval[0]] = nameval[1]

        cls.corr_util = CorrelationUtil(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getCorrUtil(self):
        return self.__class__.corr_util

    def loadDF(self):

        if hasattr(self.__class__, 'test_random_df'):
            return self.__class__.test_random_df

        # Build test DF
        index = ['idx_{}'.format(idx) for idx in range(0, 6)]
        columns = ['col_{}'.format(idx) for idx in range(0, 10)]

        np.random.seed(0)
        test_random_df = pd.DataFrame(np.random.uniform(low=0, high=100,
                                                        size=(len(index), len(columns))),
                                      index=index, columns=columns)

        self.__class__.test_random_df = test_random_df
        print('Created Random DF:\n' + test_random_df.to_string())
        return test_random_df

    def fail_df_to_corr(self, df, error, method='pearson', dimension='col',
                        exception=ValueError, contains=False):
        with self.assertRaises(exception) as context:
            self.getCorrUtil().df_to_corr(df, method=method, dimension=dimension)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def fail_plot_scatter_matrix(self, df, error, alpha=0.2, dimension='col',
                                 exception=ValueError, contains=False):
        with self.assertRaises(exception) as context:
            self.getCorrUtil().plot_scatter_matrix(df, alpha=alpha, dimension=dimension)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def test_init_ok(self):
        self.start_test()
        class_attri = ['scratch']
        corr_util = self.getCorrUtil()
        self.assertItemsEqual(class_attri, corr_util.__dict__.keys())
        self.assertEqual(corr_util.scratch, self.cfg.get('scratch'))

    def test_df_to_corr_fail(self):
        self.start_test()
        df = self.loadDF()

        # unavailable correlation method
        self.fail_df_to_corr(df, 'Input correlation method', method='fake_method', contains=True)

        # unavailable dimension
        self.fail_df_to_corr(df, 'Input dimension', dimension='fake_dimension', contains=True)

    def test_df_to_corr_ok(self):
        self.start_test()
        df = self.loadDF()

        # test default
        corr_df = self.getCorrUtil().df_to_corr(df)
        self.assertItemsEqual(corr_df.index.tolist(), corr_df.columns.tolist())
        self.assertItemsEqual(corr_df.index.tolist(), df.columns.tolist())

        # test correlation on rows
        corr_df = self.getCorrUtil().df_to_corr(df, dimension='row')
        self.assertItemsEqual(corr_df.index.tolist(), corr_df.columns.tolist())
        self.assertItemsEqual(corr_df.index.tolist(), df.index.tolist())

    def test_plot_scatter_matrix_fail(self):
        self.start_test()
        df = self.loadDF()

        # unavailable dimension
        self.fail_plot_scatter_matrix(df, 'Input dimension', dimension='fake_dim', contains=True)

        # fail pd.plotting.scatter_matrix
        self.fail_plot_scatter_matrix(df, 'Running scatter_matrix returned an error', alpha=10, contains=True)

    def test_plot_scatter_matrix_ok(self):
        self.start_test()
        df = self.loadDF()

        # default
        scatter_plot_path = self.getCorrUtil().plot_scatter_matrix(df)
        self.assertTrue(os.path.isfile(scatter_plot_path))
        self.assertGreater(os.path.getsize(scatter_plot_path), 1024)  # file size greate than 1KB

        # scatter plot on rows
        scatter_plot_path = self.getCorrUtil().plot_scatter_matrix(df, dimension='row')
        self.assertTrue(os.path.isfile(scatter_plot_path))
        self.assertGreater(os.path.getsize(scatter_plot_path), 1024)  # file size greate than 1KB

    def test_plot_corr_matrix_ok(self):
        self.start_test()
        df = self.loadDF()
        corr_df = self.getCorrUtil().df_to_corr(df, dimension='col')

        # default
        corr_matrix_plot_path = self.getCorrUtil().plot_corr_matrix(corr_df)
        self.assertTrue(os.path.isfile(corr_matrix_plot_path))
        self.assertGreater(os.path.getsize(corr_matrix_plot_path), 1024)  # file size greate than 1KB
