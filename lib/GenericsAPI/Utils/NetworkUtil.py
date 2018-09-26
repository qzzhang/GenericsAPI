import time
import pandas as pd
import os
import uuid
import errno
import networkx as nx
from matplotlib import pyplot as plt
import json
import shutil

from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.CorrelationUtil import CorrelationUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(('\n' if prefix_newline else '') + time_str + ': ' + message)


class NetworkUtil:

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

    def _Matrix2D_to_df(self, Matrix2D):
        """
        _Matrix2D_to_df: transform a FloatMatrix2D to data frame
        """

        index = Matrix2D.get('row_ids')
        columns = Matrix2D.get('col_ids')
        values = Matrix2D.get('values')

        df = pd.DataFrame(values, index=index, columns=columns)

        return df

    def _trans_df(self, df):
        """
        _trans_df: transform DF in a links data frame (3 columns only)
        """

        links = df.stack().reset_index()
        links.columns = ['source', 'target', 'value']

        return links

    def _generate_visualization_content(self, graph):
        """
        _generate_visualization_content: generate visualization html content
        """

        graph_nodes_content = str(graph.nodes()).replace('u', '')
        graph_edges_content = str([list(edge) for edge in graph.edges()]).replace('u', '')

        return graph_nodes_content, graph_edges_content

    def _generate_network_html_report(self, graph):
        """
        _generate_network_html_report: generate html summary report
        """

        log('Start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'network_report.html')

        print 'fdsafds'
        print result_file_path

        graph_nodes_content, graph_edges_content = self._generate_visualization_content(graph)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'network_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('//GRAPH_NODES',
                                                          graph_nodes_content)
                report_template = report_template.replace('//GRAPH_EDGES',
                                                          graph_edges_content)
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_directory,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Build Network App'
                            })
        return html_report

    def _generate_network_report(self, graph, network_obj_ref, workspace_name):
        """
        _generate_report: generate summary report
        """
        log('Start creating report')

        output_html_files = self._generate_network_html_report(graph)

        report_params = {'message': '',
                         'objects_created': [{'ref': network_obj_ref,
                                              'description': 'Network'}],
                         'workspace_name': workspace_name,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'build_network_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _filter_links_threshold(self, links, threshold):
        """
        _filter_links_threshold: filetre links df over a threshold and remove self correlation (cor(A,A)=1)
        """

        links_filtered = links.loc[(links['value'] >= threshold) & (links['source'] != links['target'])]

        return links_filtered

    def _build_network_object(self, graph, workspace_name, network_obj_name):
        """
        _build_network_object: tansform graph to KBbase network object
        """

        if not isinstance(workspace_name, int):
            ws_name_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            ws_name_id = workspace_name

        network_data = {'description': 'Correlation Network'}

        nodes_list = list(graph.nodes())
        nodes = dict()
        for node in nodes_list:
            nodes.update({node: {'label': node}})
        network_data.update({'nodes': nodes})

        edges = list()
        for edge in list(graph.edges()):
            edges.append({'node_1_id': edge[0],
                          'node_2_id': edge[1]})
        network_data.update({'edges': edges})

        obj_type = 'KBaseExperiments.Network'
        info = self.dfu.save_objects({
            "id": ws_name_id,
            "objects": [{
                "type": obj_type,
                "data": network_data,
                "name": network_obj_name
            }]
        })[0]

        return "%s/%s/%s" % (info[6], info[0], info[4])

    def _process_build_nx_params(self, params):

        log('start validating build_network params')

        params = params.copy()

        # check for required parameters
        for p in ['corr_matrix_ref', 'workspace_name', 'network_obj_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        if not params['filter_on_threshold']:
            raise ValueError('Must choose either filter_on_threshold or ...')
        # params['filter_on_threshold'] = True

        return params

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']

        self.data_util = DataUtil(config)
        self.corr_util = CorrelationUtil(config)
        self.dfu = DataFileUtil(self.callback_url)

        plt.switch_backend('agg')

    @staticmethod
    def draw_graph(graph, path, graph_layout='shell', node_size=400, node_color='blue',
                   edge_color='green', font_color='black', alpha=0.3, font_size=15, linewidths=1):

        plt.clf()

        # network layouts
        if graph_layout == 'spring':
            graph_pos = nx.spring_layout(graph)
        elif graph_layout == 'spectral':
            graph_pos = nx.spectral_layout(graph)
        elif graph_layout == 'random':
            graph_pos = nx.random_layout(graph)
        else:
            graph_pos = nx.shell_layout(graph)

        nx.draw(graph, pos=graph_pos, with_labels=True, node_color=node_color, node_size=node_size,
                edge_color=edge_color, alpha=alpha, font_color=font_color, linewidths=linewidths,
                font_size=font_size)

        plt.savefig(path)

    def df_to_graph(self, graph_df, source, target):
        """
        _df_to_graph: a graph from Pandas DataFrame containing an edge list
        """

        graph = nx.from_pandas_edgelist(graph_df, source=source, target=target)

        return graph

    def build_network(self, params):
        """
        build_network: filter correlation matrix and build network on filtered correlation matrix
        """

        log('--->\nrunning NetworkUtil.build_network\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        params = self._process_build_nx_params(params)

        corr_matrix_ref = params.get('corr_matrix_ref')
        workspace_name = params.get('workspace_name')
        network_obj_name = params.get('network_obj_name')
        corr_data = self.dfu.get_objects({'object_refs': [corr_matrix_ref]})['data'][0]['data']

        coefficient_data = corr_data.get('coefficient_data')
        significance_data = corr_data.get('significance_data')

        if params.get('filter_on_threshold'):
            coefficient_threshold = params.get('filter_on_threshold').get('coefficient_threshold')
            corr_df = self._Matrix2D_to_df(coefficient_data)
            links = self._trans_df(corr_df)
            links_filtered = self._filter_links_threshold(links, coefficient_threshold)
            graph = self.df_to_graph(links_filtered, source='source', target='target')

            # result_dir = os.path.join(self.scratch, str(uuid.uuid4()) + '_network_plots')
            # self._mkdir_p(result_dir)
            # graph_path = os.path.join(result_dir, 'network_plot.png')
            # self.draw_graph(graph, graph_path)

        network_obj_ref = self._build_network_object(graph, workspace_name, network_obj_name)

        returnVal = {'network_obj_ref': network_obj_ref}
        report_output = self._generate_network_report(graph, network_obj_ref, workspace_name)

        returnVal.update(report_output)
        return returnVal
