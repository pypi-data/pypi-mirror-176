from .index_classes import GeneralIndexesDatagroups
from evdspy.EVDSlocal.common.files import Write, Read
from .data_models import DataModel, DataModelCSV, DataModelJSON
from .df_operations import DFOperations
from .error_classes_index import ContentFunctionError


# GID_csv = lambda x: GeneralIndexesDatagroups().get_csv
# GID_json = lambda x: GeneralIndexesDatagroups().get_json
data_strategy = {"csv": GeneralIndexesDatagroups().get_csv , "json": GeneralIndexesDatagroups().get_json }
data_models_dict = {"csv": DataModelCSV, "json": DataModelJSON}
