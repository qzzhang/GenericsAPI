import time
import pandas as pd
import os
import uuid
import errno
import traceback
from matplotlib import pyplot as plt

from GenericsAPI.Utils.DataUtil import DataUtil


def log(message, prefix_newline=False):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(('\n' if prefix_newline else '') + time_str + ': ' + message)

CORR_METHOD = ['pearson', 'kendall', 'spearman']   # correlation method


class CorrelationUtil:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def __init__(self, config):
        self.scratch = config['scratch']
        plt.switch_backend('agg')
        # self.data_util = DataUtil(config)

    def df_to_corr(self, df, method='pearson', dimension='col'):
        """
        Compute pairwise correlation of dimension (col or row)

        method: one of ['pearson', 'kendall', 'spearman']
        """

        log('Computing correlation matrix')

        if method not in CORR_METHOD:
            err_msg = 'Input correlation method [{}] is not available.\n'.format(method)
            err_msg += 'Please choose one of {}'.format(CORR_METHOD)
            raise ValueError(err_msg)

        if dimension == 'row':
            df = df.T
        elif dimension != 'col':
            err_msg = 'Input dimension [{}] is not available.\n'.format(dimension)
            err_msg += 'Please choose either "col" or "row"'
            raise ValueError(err_msg)

        corr_df = df.corr(method=method)

        return corr_df

    def plot_corr_matrix(self, corr_df):
        """
        plot_corr_matrix: genreate correlation matrix plot
        """
        log('Plotting matrix of correlation')

        result_dir = os.path.join(self.scratch, str(uuid.uuid4()) + '_corr_matrix_plots')
        self._mkdir_p(result_dir)

        try:
            plt.clf()
            matrix_size = corr_df.index.size
            figsize = 10 if matrix_size / 5 < 10 else matrix_size / 5
            fig, ax = plt.subplots(figsize=(figsize, figsize))
            cax = ax.matshow(corr_df)
            plt.xticks(range(len(corr_df.columns)), corr_df.columns, rotation='vertical',
                       fontstyle='italic')
            plt.yticks(range(len(corr_df.columns)), corr_df.columns, fontstyle='italic')
            plt.colorbar(cax)

            # ax = plt.gca()
            # for (i, j), z in np.ndenumerate(corr_df):
            #     ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center', color='white')
        except:
            err_msg = 'Running plot_corr_matrix returned an error:\n{}\n'.format(
                                                                    traceback.format_exc())
            raise ValueError(err_msg)
        else:
            corr_matrix_plot_path = os.path.join(result_dir, 'corr_matrix_plots.png')
            log('Saving plot to:\n{}'.format(corr_matrix_plot_path))
            plt.savefig(corr_matrix_plot_path)

        return corr_matrix_plot_path

    def plot_scatter_matrix(self, df, dimension='col', alpha=0.2, diagonal='kde', figsize=(10, 10)):
        """
        plot_scatter_matrix: generate scatter plot for dimension (col or row)
                             ref: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.plotting.scatter_matrix.html
        """
        log('Plotting matrix of scatter')

        result_dir = os.path.join(self.scratch, str(uuid.uuid4()) + '_scatter_plots')
        self._mkdir_p(result_dir)

        if dimension == 'row':
            df = df.T
        elif dimension != 'col':
            err_msg = 'Input dimension [{}] is not available.\n'.format(dimension)
            err_msg += 'Please choose either "col" or "row"'
            raise ValueError(err_msg)

        try:
            plt.clf()
            sm = pd.plotting.scatter_matrix(df, alpha=alpha, diagonal=diagonal, figsize=figsize)

            # Change label rotation
            [s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
            [s.yaxis.label.set_rotation(45) for s in sm.reshape(-1)]

            # # May need to offset label when rotating to prevent overlap of figure
            [s.get_yaxis().set_label_coords(-1.5, 0.5) for s in sm.reshape(-1)]

            # Hide all ticks
            [s.set_xticks(()) for s in sm.reshape(-1)]
            [s.set_yticks(()) for s in sm.reshape(-1)]
        except:
            err_msg = 'Running scatter_matrix returned an error:\n{}\n'.format(
                                                                    traceback.format_exc())
            raise ValueError(err_msg)
        else:
            scatter_plot_path = os.path.join(result_dir, 'scatter_plots.png')
            log('Saving plot to:\n{}'.format(scatter_plot_path))
            plt.savefig(scatter_plot_path)

        return scatter_plot_path
