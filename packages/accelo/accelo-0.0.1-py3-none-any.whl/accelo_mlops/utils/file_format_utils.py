from accelo_mlops.utils.constants import PQ_FILE_EXT, D_FILE_SEPARATOR, PKL_FILE_EXT
import pathlib
from accelo_mlops.utils.time_utils import get_timestamp


class FileFormatUtils:

    @classmethod
    def create_model_filepath(cls, workspace, entity, model_file_prefix='ADMLOPS'):
        now = get_timestamp(unit='s')
        fname = model_file_prefix + D_FILE_SEPARATOR + str(now) + PKL_FILE_EXT
        path = pathlib.Path().joinpath(workspace,
                                       entity.entity_type,
                                       f'model_id={str(entity.id)}',
                                       f'model_version={str(entity.version)}',
                                       fname)
        return path

    @classmethod
    def create_s3_path(cls, workspace, entity, partition_dt,
                       partition_hr, parquet_file_prefix='ADMLOPS'):
        """
        Description:
            This is a helper function that helps return a s3 filepath to which the data_entity will be uplaoded.
            The filepath may look something like:
                /<workspace_name>/<model_id>/<version>/<entity>/<sub-entity>/<YYYY-MM-DD>/<HOUR>/ADMLOPS_<timestamp>.parquet
            which would come up to:
                /client/1234/1/data/actuals/2021-01-01/17/ADMLOPS_1618937189.parquet

        :param workspace: This is the client workspace or namespace which will uniquely divide the tenants.
        :param entity: This can be baseline_data, prediction, actual
        :param partition_dt: The date when the entity was uploaded
        :param partition_hr: The atomic unit of partition is hour
        :param parquet_file_prefix: file_prefix that defaults to 'ADMLOPS'. This needs to change going forward.
        :return: the file path to which the data_entity will be uplaoded.
        """
        now = get_timestamp(unit='s')
        fname = parquet_file_prefix + D_FILE_SEPARATOR + str(now) + PQ_FILE_EXT
        if entity.sub_entity_type:
            path = pathlib.Path().joinpath(workspace,
                                           entity.entity_type, entity.sub_entity_type,
                                           f'model_id={str(entity.model_id)}',
                                           f'model_version={str(entity.model_version)}',
                                           f'date={partition_dt}', f'hour={partition_hr}',
                                           fname)
        else:
            path = pathlib.Path().joinpath(workspace,
                                           entity.entity_type,
                                           f'model_id={str(entity.model_id)}',
                                           f'model_version={str(entity.model_version)}',
                                           f'date={partition_dt}', f'hour={partition_hr}',
                                           fname)
        return path
