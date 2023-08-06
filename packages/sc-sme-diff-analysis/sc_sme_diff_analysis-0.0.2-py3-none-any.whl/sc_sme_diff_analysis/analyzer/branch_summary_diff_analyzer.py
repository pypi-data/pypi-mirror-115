#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging

import pandas as pd

from sc_sme_diff_analysis.utils import ConfigUtils
from .base_summary_diff_analyzer import BaseSummaryDiffAnalyzer


class BranchSummaryDiffAnalyzer(BaseSummaryDiffAnalyzer):
    """
    机构汇总差异分析类
    """

    def __init__(self):
        super().__init__()

    def _read_config(self):
        super()._read_config()
        config = ConfigUtils.get_config()
        # 选中需要处理的机构清单
        self._branch_selected_list = config.get("branch.selected_list")
        # 生成的Excel中Sheet的名称
        self._target_sheet_name = config.get("diff.branch_summary.target_sheet_name")
        # Sheet名称
        self._sheet_name = config.get("diff.branch_summary.sheet_name")
        # 表头行索引
        self._header_row = config.get("diff.branch_summary.header_row")
        # 所属机构列名称（Excel中列名必须唯一）
        self._index_column_name = config.get("diff.branch_summary.branch_column_name")
        # 待分析差异列名称列表（Excel中列名必须唯一）
        diff_column_dict: dict = config.get("diff.branch_summary.diff_column_list")
        if diff_column_dict is not None and type(diff_column_dict) is dict:
            self._diff_column_dict.update(diff_column_dict)

    def _read_src_file(
            self,
            source_file_path: str,
    ) -> (bool, pd.DataFrame):
        """
        读取原始数据，获取DataFrame

        :param source_file_path: 源文件路径
        :return: (bool, pd.DataFrame), 1、是否包含数据，2、读取的数据
        """
        logging.getLogger(__name__).info("读取源文件：{}".format(source_file_path))
        try:
            data = pd.read_excel(source_file_path, sheet_name=self._sheet_name, header=self._header_row)
            # 筛选指定部门，删除合计行
            data = data[data[self._index_column_name].isin(self._branch_selected_list)]
            # 按机构排序
            data = data.sort_values(
                by=[self._index_column_name],
                ascending=True
            )
            return True, data
        except Exception as e:
            logging.getLogger(__name__).error("读取文件失败：{}".format(e))
            return False, pd.DataFrame()
