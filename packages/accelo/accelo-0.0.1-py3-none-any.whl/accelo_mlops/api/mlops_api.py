import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from io import BytesIO
import pickle
from accelo_mlops.utils.errors import S3AccessValidationError, ENVValidationError
from accelo_mlops.utils.constants import (ACCELO_DATASTORE_NAME,
                                          CLOUD_ACCESS_KEY, CLOUD_SECRET_KEY,
                                          MANDATORY_ENV_VARS)
import logging
_logger = logging.getLogger(__name__)
env = os.environ


class MLOpsApi:

    @staticmethod
    def validate_env_vars():
        for var in MANDATORY_ENV_VARS:
            if not var:
                raise ENVValidationError('Please check the setup guide and set the required environment variables '
                                         'before using the API. ')

    @staticmethod
    def validate_aws_keys(workspace='test_acceldata'):
        s3 = boto3.client(service_name='s3',
                          aws_access_key_id=CLOUD_ACCESS_KEY,
                          aws_secret_access_key=CLOUD_SECRET_KEY)
        try:
            s3.put_object(Bucket='mlops-datastore', Key=f'{workspace}/')
        except ClientError as e:
            raise S3AccessValidationError(f'Some error occurred when creating the workspace. Error msg: {str(e)}')
        except NoCredentialsError as e:
            raise S3AccessValidationError(f'Some error occurred when creating the workspace. Error msg: {str(e)}')

    @staticmethod
    def _upload_dataframe_to_s3(dataframe, destination_file_path):
        """

        :param dataframe: The dataframe with original data + mlops columns for better searchability.
        :param destination_file_path: Path to which the data has to be uploaded.
        :return:
        """
        pandas_buffer = BytesIO()
        dataframe.to_parquet(pandas_buffer)
        s3_resource = boto3.resource(service_name='s3',
                                     aws_access_key_id=CLOUD_ACCESS_KEY,
                                     aws_secret_access_key=CLOUD_SECRET_KEY)
        try:
            _logger.debug(f'DEBUG: Uploading data to: {destination_file_path}')
            s3_resource.Object(ACCELO_DATASTORE_NAME, destination_file_path).put(Body=pandas_buffer.getvalue())
        except ClientError as e:
            _logger.exception(f'Some client error occurred. Error msg: {e}. ')
        except FileNotFoundError as e:
            _logger.exception(f'File not found. Error msg: {e}')
        except NoCredentialsError as e:
            _logger.exception(f'Credentials incorrect. Error msg: {e}')

    @classmethod
    def upload_data(cls, dataframe, file_path):
        cls._upload_dataframe_to_s3(dataframe, file_path.__str__())

    @classmethod
    def upload_model(cls, model_obj, file_path):
        pickle_obj = pickle.dumps(model_obj)
        s3_resource = boto3.resource(service_name='s3',
                                     aws_access_key_id=CLOUD_ACCESS_KEY,
                                     aws_secret_access_key=CLOUD_SECRET_KEY)
        try:
            _logger.debug(f'DEBUG: Uploading model to: {file_path}')
            s3_resource.Object(ACCELO_DATASTORE_NAME, file_path.__str__()).put(Body=pickle_obj)
        except ClientError as e:
            _logger.exception(f'Some client error occurred. Error msg: {e}. ')
        except FileNotFoundError as e:
            _logger.exception(f'File not found. Error msg: {e}')
        except NoCredentialsError as e:
            _logger.exception(f'Credentials incorrect. Error msg: {e}')

