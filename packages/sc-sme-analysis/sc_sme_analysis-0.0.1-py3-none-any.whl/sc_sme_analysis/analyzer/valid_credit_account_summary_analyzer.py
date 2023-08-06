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

from sc_sme_analysis.analyzer.base_summary_analyzer import BaseSummaryAnalyzer
from sc_sme_analysis.utils import ConfigUtils, ManifestUtils


class ValidCreditAccountSummaryAnalyzer(BaseSummaryAnalyzer):
    """
    有效授信户总计分析
    """

    def __init__(self, *, excel_writer: pd.ExcelWriter):
        super().__init__(excel_writer=excel_writer)
        self._key_enabled = "sme.valid_credit_account_summary.enabled"
        self._key_business_type = "sme.valid_credit_account_summary.business_type"
        self._key_export_column_list = "sme.valid_credit_account_summary.sheet_config.export_column_list"

    def _read_config(self):
        config = ConfigUtils.get_config()
        # 生成的Excel中有效授信客户名称的列名
        self._target_client_name_column_name = config.get(
            "sme.valid_credit_account.sheet_config.target_client_name_column_name")
        # 生成的Excel中有效授信户数量的列名
        self._target_client_count_column_name = config.get(
            "sme.valid_credit_account.sheet_config.target_client_count_column_name")

    def _pre_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        # 按客户经理计数客户数（去重后的）
        group_by_manager = data.groupby(
            by=ManifestUtils.get_name_column_name()
        )[self._target_client_count_column_name].sum().to_dict()
        # 添加按客户经理计数列（列名为配置项）
        data[self._target_client_count_column_name] = data[ManifestUtils.get_name_column_name()].map(group_by_manager)

        data = data.drop(columns=[self._target_client_name_column_name])
        # 去除重复项
        data = data.drop_duplicates()
        return data
