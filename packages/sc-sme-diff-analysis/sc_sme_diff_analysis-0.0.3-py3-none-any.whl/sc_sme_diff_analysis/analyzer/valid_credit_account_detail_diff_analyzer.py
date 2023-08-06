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

import pandas as pd

from sc_sme_diff_analysis.utils import ConfigUtils
from .base_summary_diff_analyzer import BaseSummaryDiffAnalyzer


class ValidCreditAccountDetailDiffAnalyzer(BaseSummaryDiffAnalyzer):
    """
    有效授信户-客户经理明细-差异分析
    """

    def __init__(self):
        super().__init__()

    def _read_config(self):
        super()._read_config()
        config = ConfigUtils.get_config()

        # 生成的Excel中Sheet的名称
        self._target_sheet_name = config.get("diff.valid_credit_account_detail.target_sheet_name")
        # 指标名称列名称
        self._target_compare_item_column_name = config.get(
            "diff.valid_credit_account_detail.target_compare_item_column_name")
        # Sheet名称
        self._sheet_name = config.get("diff.valid_credit_account_detail.sheet_name")
        # 表头行索引
        self._header_row = config.get("diff.valid_credit_account_detail.header_row")
        # 索引列名称（Excel中列名必须唯一）
        self._index_column_name = config.get("diff.valid_credit_account_detail.manager_name_column_name")
        # 有效授信客户名称的列名
        self._client_name_column_name = config.get("diff.valid_credit_account_detail.client_name_column_name")
        # 待分析差异列名称列表（Excel中列名必须唯一）
        diff_column_list: list = config.get("diff.valid_credit_account_detail.diff_column_list")
        if diff_column_list is not None and type(diff_column_list) is list:
            self._diff_column_list.extend(diff_column_list)

    def _read_src_file(
            self,
            source_file_path: str,
    ) -> (bool, pd.DataFrame):
        contains_data, data = super()._read_src_file(source_file_path)
        if contains_data:
            data = data.fillna("")
        return contains_data, data

    def _calculate_diff_according_to_type(
            self,
            result: pd.DataFrame,
            contains_data: bool,
            current_day_data: pd.DataFrame,
            compare_type: str,
            compare_data: pd.DataFrame,
    ):
        if not contains_data:
            return
        for row_i, row in result.iterrows():
            target_cmp_type = row[self._target_compare_type_column_name]
            if target_cmp_type != compare_type:
                continue
            index_value = row[self._index_column_name]
            current_day_selection = current_day_data.loc[current_day_data[self._index_column_name] == index_value]
            # 过滤空的客户名称
            current_day_selection = current_day_selection.loc[
                current_day_selection[self._client_name_column_name] != ""]
            compare_data_selection = compare_data.loc[compare_data[self._index_column_name] == index_value]
            # 过滤空的客户名称
            compare_data_selection = compare_data_selection.loc[
                compare_data_selection[self._client_name_column_name] != ""]
            # 当天的客户清单
            client_list_current = current_day_selection.to_dict(orient='list')[self._client_name_column_name]
            # 待比较的客户清单
            client_list_compare = compare_data_selection.to_dict(orient='list')[self._client_name_column_name]

            # 这里的结果是跟比较时期比增加的
            diff_current = set(client_list_current).difference(client_list_compare)
            if len(diff_current) > 0:
                result.at[row_i, '新增'] = ", \n".join(diff_current)
            # 这里的结果是跟比较时期比减少的
            diff_compare = set(client_list_compare).difference(client_list_current)
            if len(diff_compare) > 0:
                result.at[row_i, '减少'] = ", \n".join(diff_compare)

    def _calculate_difference(
            self, *,
            current_day_data: pd.DataFrame,
            yesterday_data: pd.DataFrame,
            last_week_data: pd.DataFrame,
            monthly_base_data: pd.DataFrame,
            seasonal_base_data: pd.DataFrame,
            yearly_base_data: pd.DataFrame,
    ) -> pd.DataFrame:
        # 所有列
        all_columns = list()
        all_columns.append(self._index_column_name)
        all_columns.append(self._target_compare_type_column_name)
        all_columns.extend(self._diff_column_list)
        result = pd.DataFrame(columns=all_columns)
        # 所有索引值
        all_index_values = set(list(current_day_data[self._index_column_name].values))

        compare_types = list()
        manager_order = dict()
        if self._contains_current_day_data:
            compare_types.append(self._target_current_day_column_name)
            manager_order[self._target_current_day_column_name] = 0
        if self._contains_yearly_base_data:
            compare_types.append(self._target_yearly_base_compare_column_name)
            manager_order[self._target_yearly_base_compare_column_name] = 0
        if self._contains_seasonal_base_data:
            compare_types.append(self._target_seasonal_base_compare_column_name)
            manager_order[self._target_seasonal_base_compare_column_name] = 0
        if self._contains_monthly_base_data:
            compare_types.append(self._target_monthly_base_compare_column_name)
            manager_order[self._target_monthly_base_compare_column_name] = 0
        if self._contains_last_week_data:
            compare_types.append(self._target_last_week_compare_column_name)
            manager_order[self._target_last_week_compare_column_name] = 0
        if self._contains_yesterday_data:
            compare_types.append(self._target_yesterday_compare_column_name)
            manager_order[self._target_yesterday_compare_column_name] = 0

        # 初始化基础数据
        for index_value in all_index_values:
            for key in compare_types:
                result = result.append({
                    self._index_column_name: index_value,
                    self._target_compare_type_column_name: key,
                }, ignore_index=True)
        # 分析较年初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yearly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_yearly_base_compare_column_name,
            compare_data=yearly_base_data,
        )
        # 分析较季度初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_seasonal_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_seasonal_base_compare_column_name,
            compare_data=seasonal_base_data,
        )
        # 分析较月初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_monthly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_monthly_base_compare_column_name,
            compare_data=monthly_base_data,
        )
        # 分析较上周
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_last_week_data,
            current_day_data=current_day_data,
            compare_type=self._target_last_week_compare_column_name,
            compare_data=last_week_data,
        )
        # 分析较昨日
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yesterday_data,
            current_day_data=current_day_data,
            compare_type=self._target_yesterday_compare_column_name,
            compare_data=yesterday_data,
        )
        # 当前时点数
        self._deal_with_current_data(result=result, current_day_data=current_day_data)
        # 没有的数据填充"-"
        result.fillna("", inplace=True)
        # 处理比较类型的排序
        result[self._target_compare_type_column_name] = pd.Categorical(
            result[self._target_compare_type_column_name],
            manager_order.keys()
        )
        result.set_index([self._index_column_name], inplace=True)
        return result

    def _deal_with_current_data(
            self, *,
            result: pd.DataFrame,
            current_day_data: pd.DataFrame,
    ):
        pass
