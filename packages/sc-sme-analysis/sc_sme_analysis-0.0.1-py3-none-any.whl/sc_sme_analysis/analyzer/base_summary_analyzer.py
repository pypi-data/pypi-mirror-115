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

#  The MIT License (MIT)
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import logging

import pandas as pd
from pandas import ExcelWriter

from sc_sme_analysis.utils import ConfigUtils
from .base_analyzer import BaseAnalyzer


class BaseSummaryAnalyzer(BaseAnalyzer):
    """
    汇总分析基础类
    """

    def __init__(self, *, excel_writer: ExcelWriter):
        super().__init__(excel_writer=excel_writer)

    def analysis(self, *, manifest_data: pd.DataFrame) -> pd.DataFrame:
        """
        主分析流程分析

        :param manifest_data: 花名册数据
        :return: 与花名册合并后的分析结果
        """
        self._business_type = ConfigUtils.get_config().get(self._key_business_type)
        # 如果未启用，则直接返回花名册数据
        if not self._enabled():
            logging.getLogger(__name__).info("{} 分析未启用".format(self._business_type))
            return manifest_data
        # 读取业务类型
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))
        data = manifest_data.copy()
        # 重命名DataFrame相关列
        data = self._rename_target_columns(data=data)
        # 在数据透视之前做的操作
        data = self._pre_pivot_table(data=data)
        # 对DataFrame进行数据透视
        data = self._pivot_table(data=data)
        # 在数据透视之后做的操作
        if not data.empty:
            data = self._after_pivot_table(data=data)
        # 删除重复列
        data = self._drop_duplicated_columns(data=data)
        logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
        return data

    def write_report(self, data: pd.DataFrame):
        pass

    def write_origin_data(self):
        pass
