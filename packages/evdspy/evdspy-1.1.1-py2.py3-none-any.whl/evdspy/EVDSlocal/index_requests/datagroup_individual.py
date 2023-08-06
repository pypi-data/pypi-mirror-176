import pandas as pd

from .datagroups_initial import data_models_dict, data_strategy
from .index_classes import GeneralIndexesDatagroups, GeneralIndexesDatagroupIndividual, \
    GeneralIndexesDatagroupSeriesList
from .error_classes_index import ContentFunctionError
from .df_operations import DFOperations
from .index_util_funcs import json_to_excel
from ..common.table import Table2_
from ..components.api_params import DateStart, DateEnd
from ..components.options_class import SingletonOptions
from ..config.apikey_class import ApikeyClass
from ..config.config import ConfigBase

config = ConfigBase()


# EVDSApiDomainDatagroupIndividual

def try_to_make_excel(json_content, file_name, try_float):
    try:
        json_to_excel(json_content, file_name, try_float=try_float)
        from ..common.colors import print_with_success_style
        print_with_success_style(f"{file_name} was created...")
    except:
        from ..common.colors import print_with_failure_style
        print_with_failure_style(f"{file_name} could not be created...")


def get_datagroup_individual_with_code(code_str: str):
    """get_datagroup_individual_with_code"""
    json_content = get_datagroup_individual_with_code_helper(code_str)
    file_name = rf"SeriesData\EVPY_Data_{code_str}.xlsx"
    if 'items' in json_content:
        json_content = json_content['items']
    try_to_make_excel(json_content, file_name, try_float=True)
    return json_content


def get_datagroup_individual_with_code_helper(code_str: str):
    """get_datagroup_individual_with_code_helper"""
    gid = GeneralIndexesDatagroupIndividual(code=0)  # this number will be overriten . does not matter what number
    gid.create_url_first_part()
    gid.add_extra_params(code=code_str)
    start_date = SingletonOptions().get_valid_value("default_start_date")
    end_date = SingletonOptions().get_valid_value("default_end_date")
    date_start: DateStart = DateStart(value=start_date)
    date_end: DateEnd = DateEnd(value=end_date)
    gid.complete_url_instance.add_item(date_start)
    gid.complete_url_instance.add_item(date_end)
    gid.complete_url_instance.refresh_url()
    gid.complete_url_instance.add_apikey()  # this will get apikey itself if None given
    json_content = gid.get_json()

    return json_content


def get_series_list_of_subject(code_str: str):
    # https://evds2.tcmb.gov.tr/service/evds/serieList/key=XXXXX&type=csv&code=bie_yssk
    gid = GeneralIndexesDatagroupSeriesList(code=0)  # this number will be overriten . does not matter what number
    gid.create_url_first_part()
    gid.add_extra_params(code=code_str)
    gid.complete_url_instance.refresh_url()
    json_content = gid.get_json()
    file_name = rf"SeriesData\EVPY_Data_{code_str}_EXPLANATION.xlsx"
    try_to_make_excel(json_content, file_name, try_float=False)

    return json_content
