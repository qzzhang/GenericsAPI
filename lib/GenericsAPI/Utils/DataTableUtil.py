import logging
import uuid
import os
import json

from installed_clients.DataFileUtilClient import DataFileUtil
from GenericsAPI.Utils.AttributeUtils import AttributesUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from installed_clients.KBaseReportClient import KBaseReport


class DataTableUtil:

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.data_util = DataUtil(config)
        self.attr_util = AttributesUtil(config)
        self.matrix_types = [x.split(".")[1].split('-')[0]
                             for x in self.data_util.list_generic_types()]

    def _build_table_content(self, output_directory, input_matrix_ref, with_attribute_info):
        """
        _build_table_content: generate HTML table content for FloatMatrix2D object
        """

        page_content = """\n"""

        table_file_name = 'matrix_data_viewer.html'
        data_file_name = 'matrix_data.json'

        page_content += """<iframe height="900px" width="100%" """
        page_content += """src="{}" """.format(table_file_name)
        page_content += """style="border:none;"></iframe>\n"""

        # row_ids = matrix_2D.get('row_ids')
        # col_ids = matrix_2D.get('col_ids')
        # values = matrix_2D.get('values')

        # df = pd.DataFrame(values, index=row_ids, columns=col_ids)
        # df = df.T
        matrix_df = df.stack().reset_index()

        table_headers = matrix_df.columns.tolist()
        table_content = """\n"""
        # build header and footer
        table_content += """\n<thead>\n<tr>\n"""
        for table_header in table_headers:
            table_content += """\n <th>{}</th>\n""".format(table_header)
        table_content += """\n</tr>\n</thead>\n"""

        table_content += """\n<tfoot>\n<tr>\n"""
        for table_header in table_headers:
            table_content += """\n <th>{}</th>\n""".format(table_header)
        table_content += """\n</tr>\n</tfoot>\n"""

        logging.info('start generating table json file')
        data_array = matrix_df.values.tolist()

        total_rec = len(data_array)
        json_dict = {'draw': 1,
                     'recordsTotal': total_rec,
                     'recordsFiltered': total_rec,
                     'data': data_array}

        with open(os.path.join(output_directory, data_file_name), 'w') as fp:
            json.dump(json_dict, fp)

        logging.info('start generating table html')
        with open(os.path.join(output_directory, table_file_name), 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'templates', 'table_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>table_header</p>',
                                                          table_content)
                report_template = report_template.replace('ajax_file_path',
                                                          data_file_name)
                report_template = report_template.replace('deferLoading_size',
                                                          str(total_rec))
                result_file.write(report_template)

        return page_content

    def _generate_visualization_content(self, output_directory, input_matrix_ref,
                                        with_attribute_info):

        tab_def_content = ''
        tab_content = ''

        tab_def_content += """\n<div class="tab">\n"""
        tab_def_content += """
        <button class="tablinks" onclick="openTab(event, 'MatrixData')" id="defaultOpen">Matrix Data</button>
        """

        corr_table_content = self._build_table_content(output_directory, input_matrix_ref,
                                                       with_attribute_info)
        tab_content += """\n<div id="MatrixData" class="tabcontent">{}</div>\n""".format(
                                                                                corr_table_content)

        tab_def_content += """\n</div>\n"""

        return tab_def_content + tab_content

    def _generate_matrix_html_report(self, input_matrix_ref, with_attribute_info):

        """
        _generate_matrix_html_report: generate html summary report for matrix
        """

        logging.info('Start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'matrix_report.html')

        visualization_content = self._generate_visualization_content(output_directory,
                                                                     input_matrix_ref,
                                                                     with_attribute_info)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'templates', 'matrix_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Visualization_Content</p>',
                                                          visualization_content)
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_directory,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Compute Correlation App'
                            })
        return html_report

    def _generate_corr_report(self, workspace_name, input_matrix_ref, with_attribute_info):
        """
        _generate_report: generate summary report
        """
        logging.info('Start creating report')

        output_html_files = self._generate_matrix_html_report(input_matrix_ref,
                                                              with_attribute_info)

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 666,
                         'report_object_name': 'matrix_viewer_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def view_matrix_as_table(self, params):
        input_matrix_ref = params.get('input_matrix_ref')
        workspace_name = params.get('workspace_name')
        with_attribute_info = params.get('with_attribute_info', 1)

        if not isinstance(workspace_name, int):
            workspace_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            workspace_id = workspace_name

        returnVal = dict()
        report_output = self._generate_corr_report(workspace_name, input_matrix_ref,
                                                   with_attribute_info)

        returnVal.update(report_output)

        return returnVal
