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
from scconfig.config import Config
from scutils import Singleton

from sc_retail_analysis.configs.default import DEFAULT_CONFIG


class ConfigUtils(metaclass=Singleton):
    """
    配置文件相关工具类
    """

    _config = None

    @classmethod
    def clear(cls):
        cls._config = None

    @classmethod
    def load_configurations(cls):
        """
        加载配置文件
        :return:
        """
        try:
            # load configurations
            cls._config = Config.create(project_name="sc-retail-analysis", defaults=DEFAULT_CONFIG)
        except Exception as error:
            cls._config = {}
            logging.getLogger(__name__).exception("failed to read configuration", exc_info=error)

    @classmethod
    def get_config(cls):
        """
        获取配置信息
        :return: 配置信息字典
        """
        if cls._config is None:
            cls.load_configurations()
        return cls._config


class BranchUtils(metaclass=Singleton):
    """
    机构相关工具类
    """
    _branch_name_mapping_loaded = False
    _branch_name_mapping = dict()
    _sales_performance_attribution_mapping_loaded = False
    _sales_performance_attribution_mapping = dict()
    # 公共户名关键字列表
    _common_account_keyword_list = list()
    # 所有会发生业务的机构列表
    _all_business_branch_list = list()
    _all_business_branch_list_loaded = False

    @classmethod
    def load_common_account_keyword_list(cls):
        """
        加载公共户关键字列表
        :return:
        """
        # 公共户名关键字
        common_account_keyword = ConfigUtils.get_config().get("branch.common_account_keyword")
        cls._common_account_keyword_list.clear()
        cls._common_account_keyword_list.extend(common_account_keyword)

    @classmethod
    def is_common_account(cls, name):
        """
        判断账户名称是否为公共户
        :param name: 账户名称
        :return: 账户名称是否为公共户
        """
        for common_account_keyword in cls._common_account_keyword_list:
            if common_account_keyword in name:
                return True
        return False

    @classmethod
    def get_branch_name_mapping(cls) -> dict:
        """
        机构对应关系表
        :return: 机构对应关系表
        """
        return cls._branch_name_mapping

    @classmethod
    def load_branch_name_mapping(cls):
        """
        加载机构对应关系表
        :return:
        """
        if cls._branch_name_mapping_loaded:
            return
        mapping = ConfigUtils.get_config().get("branch.name_mapping")
        cls._branch_name_mapping.update(mapping)
        cls._branch_name_mapping_loaded = True

    @classmethod
    def get_sales_performance_attribution_mapping(cls) -> dict:
        """
        业绩归属机构配置
        :return: 业绩归属机构配置
        """
        return cls._sales_performance_attribution_mapping

    @classmethod
    def load_sales_performance_attribution_mapping(cls):
        """
        加载业绩归属机构配置
        :return:
        """
        if cls._sales_performance_attribution_mapping_loaded:
            return
        mapping = ConfigUtils.get_config().get("branch.sales_performance_attribution_mapping")
        cls._sales_performance_attribution_mapping.update(mapping)
        cls._sales_performance_attribution_mapping_loaded = True

    @classmethod
    def load_all_business_branch_list(cls):
        """
        加载业绩归属机构配置
        :return:
        """
        if cls._all_business_branch_list_loaded:
            return
        cls.load_branch_name_mapping()
        cls.load_sales_performance_attribution_mapping()
        name_mapping = cls.get_branch_name_mapping()
        attribution_mapping = cls.get_sales_performance_attribution_mapping()
        cls._all_business_branch_list.clear()
        branch_list = set()
        for branch_name in set(name_mapping.values()):
            if branch_name in attribution_mapping:
                branch_name = attribution_mapping.get(branch_name)
            branch_list.add(branch_name)
        cls._all_business_branch_list.extend(branch_list)
        cls._all_business_branch_list_loaded = True

    @classmethod
    def get_all_business_branch_list(cls):
        return cls._all_business_branch_list

    @classmethod
    def replace_branch_name(cls, *, branch_name: str) -> str:
        """
        替换机构名称为通用机构名称
        :param branch_name: 原机构名称
        :return: 通用机构名称
        """
        if branch_name in cls.get_branch_name_mapping():
            return cls.get_branch_name_mapping().get(branch_name)
        return branch_name


class ManifestUtils(metaclass=Singleton):
    """
    花名册相关工具类
    """
    # 名单DataFrame
    _df: pd.DataFrame = None
    # 花名册姓名与所在部门对应关系DataFrame
    _name_branch_df: pd.DataFrame = None
    _id_column_name: str = ""
    _name_column_name: str = ""
    _branch_column_name: str = ""
    _sales_performance_attribution_column_name: str = ""
    # 离职人员调整表
    _leave_employee_mapping = dict()
    # （非息）离职人员归属机构表
    _non_interest_leave_employee_branch_mapping = dict()

    @classmethod
    def get_manifest_branch_column_name(cls):
        return "花名册" + cls.get_branch_column_name()

    @classmethod
    def get_name_branch_data_frame(cls) -> pd.DataFrame:
        """
        花名册姓名与所在部门对应关系
        :return:
        """
        return cls._name_branch_df

    @classmethod
    def get_id_column_name(cls) -> str:
        """
        工号列名
        :return: 工号列名
        """
        return cls._id_column_name

    @classmethod
    def get_name_column_name(cls) -> str:
        """
        姓名列名
        :return: 姓名列名
        """
        return cls._name_column_name

    @classmethod
    def get_branch_column_name(cls) -> str:
        """
        所属机构列名
        :return: 所属机构列名
        """
        return cls._branch_column_name

    @classmethod
    def get_sales_performance_attribution_column_name(cls) -> str:
        """
        业绩归属机构列名
        :return: 业绩归属机构列名
        """
        return cls._sales_performance_attribution_column_name

    @classmethod
    def get_leave_employee_mapping(cls) -> dict:
        """
        机构对应关系表
        :return: 机构对应关系表
        """
        return cls._leave_employee_mapping

    @classmethod
    def load_leave_employee_mapping(cls):
        """
        加载离职人员调整表
        :return:
        """
        mapping = ConfigUtils.get_config().get("manifest.leave_employee_mapping")
        cls._leave_employee_mapping.update(mapping)

    @classmethod
    def get_non_interest_leave_employee_branch_mapping(cls) -> dict:
        """
        （非息）离职人员归属机构表
        :return: （非息）离职人员归属机构表
        """
        return cls._non_interest_leave_employee_branch_mapping

    @classmethod
    def load_non_interest_leave_employee_branch_mapping(cls):
        """
        加载（非息）离职人员归属机构表
        :return:
        """
        mapping = ConfigUtils.get_config().get("manifest.non_interest_leave_employee_branch_mapping")
        cls._non_interest_leave_employee_branch_mapping.update(mapping)

    @classmethod
    def load_manifest(cls):
        """
        加载花名册
        :return:
        """
        config = ConfigUtils.get_config()
        src_file_path = config.get("manifest.source_file_path")
        # 业绩归属机构列名
        cls._sales_performance_attribution_column_name = config.get("branch.sales_performance_attribution_column_name")
        sheet_name = config.get("manifest.sheet_name")
        header_row = config.get("manifest.sheet_config.header_row")
        # 工号列索引
        id_column = config.get("manifest.sheet_config.id_column")
        # 姓名列索引
        name_column = config.get("manifest.sheet_config.name_column")
        # 所属机构列索引
        branch_column = config.get("manifest.sheet_config.branch_column")
        logging.getLogger(__name__).info("加载花名册：{}".format(src_file_path))
        df = pd.read_excel(src_file_path, sheet_name=sheet_name, header=header_row)
        df = df.iloc[:, [id_column, name_column, branch_column]]
        cls._id_column_name = df.columns[0]
        cls._name_column_name = df.columns[1]
        cls._branch_column_name = df.columns[2]
        # 添加公共户相关行
        for branch in set(BranchUtils.get_branch_name_mapping().values()):
            df = df.append({
                cls._id_column_name: 0,
                cls._name_column_name: branch,
                cls._branch_column_name: branch,
            }, ignore_index=True)

        mapping = BranchUtils.get_branch_name_mapping()
        # 替换机构名称
        df = df.replace({cls._branch_column_name: mapping})
        # 添加业绩归属列
        df[cls._sales_performance_attribution_column_name] = df[cls._branch_column_name]
        # 业绩归属机构配置
        mapping = BranchUtils.get_sales_performance_attribution_mapping()
        # 处理业绩归属机构
        result = df.replace({cls._sales_performance_attribution_column_name: mapping})
        # 花名册姓名与所在部门对应关系
        cls._name_branch_df = result[[cls._name_column_name, cls._branch_column_name]].copy()
        cls._name_branch_df.set_index(cls._name_column_name, inplace=True)
        cls._name_branch_df.rename(columns={
            cls._branch_column_name: ManifestUtils.get_manifest_branch_column_name(),
        }, inplace=True)
        cls._df = result

    @classmethod
    def fix_name_error(cls, data: pd.DataFrame, id_column_name: str, name_column_name: str) -> pd.DataFrame:
        """
        解决姓名与工号不匹配的问题

        :param data: 原始数据
        :param id_column_name: 工号列名称
        :param name_column_name: 姓名列名称
        :return: 解决姓名与工号不匹配的问题后的数据
        """
        for row_i, row in data.iterrows():
            id_value = row[id_column_name]
            if id_value == 0:
                continue
            name_in_manifest = cls._df.loc[cls._df[cls._id_column_name] == id_value][cls._name_column_name]
            if name_in_manifest.empty:
                continue
            name = row[name_column_name]
            if name != name_in_manifest.values[0]:
                data.at[row_i, name_column_name] = name_in_manifest.values[0]
        return data

    @classmethod
    def merge_with_manifest(cls, *,
                            manifest_data: pd.DataFrame,
                            data: pd.DataFrame,
                            id_column_name: str = None,
                            how: str = "left",
                            name_column_name: str = None) -> pd.DataFrame:
        """
        与花名册合并

        :param manifest_data: 花名册数据，左边表
        :param data: 待合并DataFrame，右边表
        :param how: 如何合并，即连接方式，默认使用left连接，即左连接，保证花名册的数据完整
        :param id_column_name: 工号列名称
        :param name_column_name: 姓名列名称
        :return: 花名册与目标DataFrame合并后的DataFrame
        """
        if id_column_name is None and name_column_name is None:
            # ID与名称列全为空，则返回原结果
            return data
        if id_column_name is None and name_column_name is not None:
            # 如果没有工号列，则按姓名列Join
            return manifest_data.merge(data, how=how, left_on=[cls._df.columns[1]], right_on=[name_column_name])
        if name_column_name is None and id_column_name is not None:
            # 如果没有姓名列，则按工号列Join
            return manifest_data.merge(data, how=how, left_on=[cls._df.columns[0]], right_on=[id_column_name])
        # ID与姓名都不为空，则按ID和姓名两列Join
        return manifest_data.merge(data, how=how, left_on=[cls._df.columns[0], cls._df.columns[1]],
                                   right_on=[id_column_name, name_column_name])

    @classmethod
    def get_manifest_df(cls) -> pd.DataFrame:
        return cls._df

    @classmethod
    def get_all_names_in_manifest(cls) -> list:
        return list(cls._df[cls._name_column_name].values)


__all__ = {
    "ConfigUtils",
    "BranchUtils",
    "ManifestUtils",
}
