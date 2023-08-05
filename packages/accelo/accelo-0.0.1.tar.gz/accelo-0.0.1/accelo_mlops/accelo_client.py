import pandas as pd
import numpy as np
from typing import Union, List
import uuid
import logging
import urllib3
import json
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from accelo_mlops.utils.time_utils import (get_timestamp, get_formatted_time, get_now, get_now_hour)
from accelo_mlops.utils.file_format_utils import FileFormatUtils
from accelo_mlops.entities.prediction import Predictions
from accelo_mlops.entities.actual import Actuals
from accelo_mlops.entities.baseline import Baseline
from accelo_mlops.entities.assembly import Assembly, SourceType, AssemblyToProjectResponse
from accelo_mlops.entities.snapshot import Snapshot
from accelo_mlops.entities.asset import Asset, AssetToModelResponse
from accelo_mlops.entities.metadata import Metadata
from accelo_mlops.entities.model import Model
from accelo_mlops.utils.errors import (PredictionsValidationError, ActualsValidationError,
                                       PredictionsAndActualsValidationError, BaselinesValidationError,
                                       ModelValidationError, ProjectValidationError, ProjectExistsError,
                                       MetadataValidationError)
from accelo_mlops.utils.api_utils import generate_uuid
from accelo_mlops.utils.constants import MLOPS_MANDATORY_METADATA
from accelo_mlops.api import MLOpsApi
from accelo_mlops.api import TorchApi
from accelo_mlops.utils.constants import (MLOPS_METASTORE)
from accelo_mlops.utils.UserResponsePrettify import prettify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_logger = logging.getLogger(__name__)


class AcceloClient:
    project_id = None
    model_id = None

    def __init__(self, workspace):
        self._validate_env()
        self._set_timestamp_date()
        self.workspace = workspace
        self._validate_keys()
        self.data_path_prefix = 'data'
        self.prediction_path_prefix = 'predictions'
        self.actuals_path_prefix = 'actuals'
        _logger.debug(f'Initialized the workspace: {self.workspace}')

    def _validate_keys(self):
        MLOpsApi.validate_aws_keys(workspace=self.workspace)

    @staticmethod
    def _validate_env():
        MLOpsApi.validate_env_vars()

    def _check_model_exists(self, model_id, project_id, engine):
        query = "SELECT * from ad_catalog.mlops_model_config " \
                f"WHERE model_id=\'{model_id}\' AND project_id=\'{project_id}\'"
        with engine.connect() as conn:
            result = conn.execute(query)
        if result.fetchall():
            return True
        return False

    def _update_model_configs_table(self,
                                    project_id,
                                    model_id,
                                    model_name,
                                    model_version,
                                    model_type,
                                    frequency_type):
        engine_string = f'postgresql+psycopg2://admin:admin@{MLOPS_METASTORE}:5432/ad_catalog'
        engine = create_engine(engine_string)
        if self._check_model_exists(model_id, project_id, engine):
            _logger.debug(f'DEBUG: Model configurations already saved for project_id={project_id} '
                          f'and model_id={model_id}')
            return
        services_enabled = ['detect', 'analyze']
        _logger.debug('DEBUG: Writing data to "MLOPS Config" Table. ')
        try:
            with engine.connect() as conn:
                for service_type in services_enabled:
                    query = 'INSERT INTO ' \
                            '   ad_catalog.mlops_model_config ' \
                            '(project_id, workspace, model_id, model_name, model_version, ' \
                            'model_type, service_type, service_enabled, frequency_type) ' \
                            '   VALUES ' \
                            f'(\'{project_id}\', \'{self.workspace}\',\'{model_id}\', \'{model_name}\', \'{model_version}\', ' \
                            f'\'{model_type.upper()}\', \'{service_type}\', \'{True}\', \'{frequency_type.upper()}\')'
                    conn.execute(query)
        except SQLAlchemyError as sqe:
            _logger.debug(f'Error writing to mlops_config table: {sqe}')

    @classmethod
    def _create_project(cls, name, description):
        source_type = SourceType()
        assembly = Assembly(name=name, sourceType=source_type, description=description)
        assembly_response = TorchApi.create_assembly(assembly)
        return assembly_response

    @classmethod
    def _init_snapshot(cls, assembly_response):
        _uuid = generate_uuid()
        snapshot = Snapshot(assembly_response.get('data').get('id'), _uuid)
        TorchApi.initialize_snapshot(snapshot)

    def create_project(self, name, description='Default Description. '):
        _logger.debug(f'INFO: Creating project = "{name}"')
        if TorchApi.is_assembly_exists(assembly_name=name):
            assembly_response = TorchApi.get_assembly_by_name(name)
            assembly_response_mini = AssemblyToProjectResponse.convert(assembly_response)
            prettify(jsonobject=assembly_response_mini)
            self.project_id = assembly_response_mini.get('project_id')
            raise ProjectExistsError(f'Project with name="{name}" already exists. '
                                     f'Please choose a different name or use the existing and create models. ')
        else:
            assembly_response = self._create_project(name, description)
            self.project_id = assembly_response.get('data').get('id')
            self._init_snapshot(assembly_response)
            prettify(jsonobject=AssemblyToProjectResponse.convert(assembly_response))
        return assembly_response

    @classmethod
    def _validate_model_exists(cls, model_id):
        """ Throws ERROR if the 'model' is not registered in Acceldata platform. """
        if not TorchApi.is_asset_exists(model_id):
            raise ModelValidationError(f'Model with id={model_id} not registered in Acceldata platform. '
                                       f'Register the model first to carry out any operation. ')

    @classmethod
    def _update_metadata(cls, model_id, metadata):
        """
        Based on the model_id, get the metadata.
        Add new changes to the metadata and do a POST call to
        """
        _logger.debug(f'DEBUG: Update Metadata for model id = {model_id}')
        if isinstance(metadata, list):
            TorchApi.update_asset_metadata(model_id, metadata)
        else:
            TorchApi.update_asset_metadata(model_id, [metadata])

    def _upload_model_object(self, model):
        filepath = FileFormatUtils.create_model_filepath(
            self.workspace,
            model,
            model_file_prefix=model.name
        )
        MLOpsApi.upload_model(model.model_object, filepath)
        return filepath

    @classmethod
    def _validate_model_metadata(cls, metadata_dict):
        remaining_fields = [field for field in MLOPS_MANDATORY_METADATA if field not in metadata_dict.keys()]
        if len(remaining_fields) >= 1:
            raise MetadataValidationError(f'Some fields from metadata_dict are required to perform '
                                          f'background tasks. Fields: {remaining_fields}. Please '
                                          f'add them and reregister the model. ')

    def register_model(self, project_id: int,
                       model_name: str,
                       model_version: str,
                       model_metadata: dict,
                       **params):
        """
        Users will be able to register a model to MLOps backend using this method. The metadata_dict is
        a dictionary/hashmap of key values with below required parameters.
        -  'frequency' -> how often to schedule the performance runs, options are: 'daily', 'hourly', etc
        - 'model_type' -> binary/multiclass classification (for now, only classification is supported)
        - 'performance_metric' -> The metric used to measure the model performance on test/validation data
        - 'model_obj' -> The model object used for training

        :param project_id: can be accessed using client.project_id where client is the object for the AcceloClient class
        :param model_name: name of the model that is unique per project, can be same across projects
        :param model_version: version of the model
        :param model_metadata: please see description above
        :param params: any other parameters that the users would like to add, key:value pairs
        """
        _logger.info('INFO: Register Model: START')
        model_version = str(model_version)
        if not TorchApi.is_assembly_exists(assembly_id=project_id):
            raise ProjectValidationError(f'Project with id={project_id} does not exist. Please recheck the id. ')
        self._validate_model_metadata(model_metadata)
        all_metadata = {**model_metadata, **params}
        metadata = [Metadata(key=key, value=str(value)) for key, value in all_metadata.items() if key != 'model_obj']
        metadata.append(Metadata(key='model_version', value=model_version))
        metadata.append(Metadata(key='workspace', value=self.workspace))
        current_snapshot = TorchApi.current_snapshot(project_id)
        assembly_name = TorchApi.get_assembly_name(project_id)
        asset = Asset(
            name=model_name,
            uid=f'{assembly_name}.{model_name}',
            assemblyId=project_id,
            currentSnapshot=current_snapshot,
            metadata=metadata
        )
        asset_response = TorchApi.register_asset(asset)
        model_response = AssetToModelResponse.convert(asset_response)
        self.model_id = model_response.get('model_id')
        model = Model(
            id=model_response.get('model_id'),
            name=model_name,
            version=model_version,
            project_id=project_id,
            model_object=model_metadata.get('model_obj')
        )
        filepath = self._upload_model_object(model)
        new_metadata = Metadata(key='ADMLOPS_model_location', value=str(filepath))
        self._update_metadata(model_response.get('model_id'), new_metadata)
        self._update_model_configs_table(
            project_id=project_id,
            model_id=model_response.get('model_id'),
            model_name=model_name,
            model_version=model_version,
            model_type=model_metadata.get('model_type') or 'UNKNOWN',
            frequency_type=params.get('frequency') or 'DAILY'
        )
        prettify(model_response)
        _logger.info('INFO: Register Model: COMPLETE')
        return model_response

    @staticmethod
    def _validate_predictions(prediction: Predictions):
        """
        Description:
            Validations should be both "client" and "server" side.

        Client:
            - length of feture_data and predictions is same
            - predictions must be dataframe, numpy array, list, series
        Server:
            - model_id, model_version exist
        """
        model_id = prediction.model_id
        feature_data = prediction.feature_data
        predictions = prediction.predictions

        if not feature_data.empty:
            if not isinstance(feature_data, pd.DataFrame):
                raise PredictionsValidationError(f'Feature data must of type "pandas.dataframe" '
                                                 f'but the type is {type(feature_data)}')

            if not len(feature_data) == len(predictions):
                raise PredictionsValidationError(f'Features and Predictions length do not match. '
                                                 f'Feature data has length: {len(feature_data)}, '
                                                 f'Predictions have length: {len(predictions)}')
        if not isinstance(predictions, (pd.DataFrame, pd.Series, np.ndarray, list)):
            raise PredictionsValidationError('Predictions need to be of type: '
                                             '"pandas DataFrome/Series", "numpy ndarray", '
                                             'or "python list"')

        AcceloClient._validate_model_exists(model_id)

    def _prepare_predictions(self, feature_data, prediction):
        feature_df = feature_data.copy()
        feature_df.loc[:, 'ADMLOPS_model_id'] = prediction.model_id
        feature_df.loc[:, 'ADMLOPS_model_version'] = prediction.model_version
        feature_df.loc[:, 'ADMLOPS_log_time'] = self.timestamp
        feature_df.loc[:, 'predictions'] = prediction.predictions
        feature_df.loc[:, 'ADMLOPS_ids'] = prediction.prediction_ids
        return feature_df

    @staticmethod
    def _id_cols_in_metadata(model_id):
        metadata = TorchApi.get_asset_metadata(asset_id=model_id)
        items = metadata.get('data').get('items')
        for item in items:
            if 'id_cols' == item.get('key'):
                return item.get('value').split(',')

    @staticmethod
    def _id_cols_in_prediction_df(id_cols, prediction_cols):
        if len(id_cols) == sum([1 for col in id_cols if col in prediction_cols]):
            return True
        return False

    def log_predictions(self,
                        model_id: Union[int, str],
                        model_version: Union[int, str],
                        feature_data: pd.DataFrame,
                        predictions: Union[List, pd.Series],
                        publish_date=None):
        """
        Description:
            Accepts predictions and feature_data for which the predictions were made.
            Adds additional required fields used by API.

        Validations:
            _validate_predictions()

        :param feature_data: should have fields 'id' and 'label' which will be used for logging.
        :param predictions: predictions about the feature data should be passed as a dataframe or a list (vector)
        :param model_id: the id received by the users when they register a model, this is a candidate key
        :param model_version: the id received by the users when they update a model, this in combination with
        model_id is a composite key
        :param publish_date:
        :return prediction_ids: these ids can be used by the users to map their predictions to the actuals at a later
        point in time
        """
        id_cols = self._id_cols_in_metadata(model_id)
        feature_cols = feature_data.columns.tolist()
        if id_cols and not self._id_cols_in_prediction_df(id_cols, feature_cols):
            raise PredictionsValidationError(f'The "id_cols" specified for dataframes are: {id_cols} '
                                             f'whereas the columns in the "feature_dataframe" are: {feature_cols}')
        published_dt = publish_date if publish_date else self.published_dt
        prediction_ids = [str(uuid.uuid4()) for _ in range(len(predictions))]
        prediction = Predictions(model_id=model_id,
                                 model_version=model_version,
                                 prediction_ids=prediction_ids,
                                 feature_data=feature_data,
                                 predictions=predictions)
        self._validate_predictions(prediction)
        feature_data = self._prepare_predictions(feature_data, prediction)
        filepath = FileFormatUtils.create_s3_path(self.workspace,
                                                  prediction,
                                                  published_dt,
                                                  self._get_current_hour())
        _logger.debug(f'DEBUG: The s3 path to upload predictions: {filepath}')
        MLOpsApi.upload_data(feature_data, filepath)

        return feature_data['ADMLOPS_ids'].tolist()

    @staticmethod
    def _validate_actuals(model_id, actual: Actuals):
        """
        Description:
            Validations should be both "client" and "server" side.

        Client:
            - length of actuals and ids is same

        Server:
            - model_id, model_version exist
        """
        if len(actual.actual_ids) != len(actual.actuals):
            raise ActualsValidationError(f'The length of actuals and actual_ids should match. '
                                         f'Predictions length: {len(actual.actual_ids)}, '
                                         f'Actuals length: {len(actual.actuals)}')

        if not isinstance(actual.actuals, (pd.Series, np.ndarray, list)):
            raise ActualsValidationError(f'Actuals need to be of type: '
                                         '"pandas Series", "numpy ndarray", '
                                         'or "python list"')

        AcceloClient._validate_model_exists(model_id)

    def _prepare_actuals(self, actual):
        actuals = pd.DataFrame(
            {
                'ADMLOPS_model_id': actual.model_id,
                'ADMLOPS_log_time': self.timestamp,
                'actuals': actual.actuals,
                'ADMLOPS_ids': actual.actual_ids
            }
        )
        return actuals

    @staticmethod
    def _validate_id_cols_present_for_actuals(model_id, id_cols):
        metadata = TorchApi.get_asset_metadata(asset_id=model_id)
        items = metadata.get('data').get('items')
        id_cols_in_db = list()
        for item in items:
            if 'id_cols' == item.get('key'):
                id_cols_in_db = item.get('value').split(',')
                break
        if sorted(id_cols) != sorted(id_cols_in_db):
            raise ActualsValidationError(f'The id_cols passed when logging actuals and one passed when '
                                         f'logging baselines are different. '
                                         f'Baseline id_cols: {id_cols_in_db}. '
                                         f'Actuals id_cols: {id_cols}')

    def log_actuals(self,
                    model_id: Union[int, str],
                    model_version: Union[int, str],
                    actuals: Union[pd.Series, List, np.ndarray],
                    actual_ids: List = None,
                    id_cols_df: pd.DataFrame = None,
                    publish_date=None):
        """
        Description:
            The actuals if individually logged require ids to be passed by the users.
            The generation part is taken care of by this thin client.
            If actuals are logged along with predictions, they are auto-passed in the code
            and the customer need not keep track of the mapping but the dependency is on
            the availability of the actuals.

        :param publish_date: By default uses current date, but user can provide a date from past
        :param actuals: actual labels for the serving data, this mostly is received late
        :param actual_ids: ids that are used for 1:1 mapping the serving feature data to the actuals
        this can be optional in case user/customer has added the id columns in the baseline data logging call/pipeline
        :param model_id: the model against which the serving pipeline is run, this is geneted by our
        service backend the returned to user when they register a model in our registry for the
        first time
        :param model_version: this version for now will be maintained by the customer, later. a decision
        on whether run id should be mapped to model versions can be taken (eg: mlflow)
        :param id_cols_df: if id_cols are logged as part of baseline, this is a mandatory field.
        :return:
        """
        if not actual_ids and id_cols_df.empty:
            raise ActualsValidationError('Either one of "actual_ids" OR "id_cols_df" is required to link '
                                         'predictions with actuals and compute results. ')
        actual = None
        if id_cols_df and not id_cols_df.empty:
            self._validate_id_cols_present_for_actuals(model_id, id_cols_df.columns.tolist())
            actual = Actuals(model_id=model_id,
                             model_version=model_version,
                             actual_ids=id_cols_df.values.tolist(),
                             actuals=actuals,
                             label_col=None)
        elif actual_ids:
            actual = Actuals(model_id=model_id,
                             model_version=model_version,
                             actual_ids=actual_ids,
                             actuals=actuals,
                             label_col=None)
            self._validate_actuals(model_id, actual)

        published_dt = publish_date if publish_date else self.published_dt
        actuals_data = self._prepare_actuals(actual)
        filepath = FileFormatUtils.create_s3_path(self.workspace,
                                                  actual,
                                                  published_dt,
                                                  self._get_current_hour())
        _logger.debug(f'The s3 path to upload predictions: {filepath}')
        MLOpsApi.upload_data(actuals_data, filepath)

    @staticmethod
    def _validate_predictions_and_actuals(model_id, predictions, actuals):
        """
        Description:
            Validations should be both "client" and "server" side.

        Client:
            - length of actuals and predictions is same

        Server:
            - model_id, model_version exist
        """
        if len(predictions) != len(actuals):
            raise PredictionsAndActualsValidationError(f'The length of predictions and actuals should match. '
                                                       f'Predictions length: {len(predictions)}, '
                                                       f'Actuals length: {len(actuals)}')

        AcceloClient._validate_model_exists(model_id)

    def log_predictions_and_actuals(self,
                                    model_id: Union[int, str],
                                    model_version: Union[int, str],
                                    feature_data: pd.DataFrame,
                                    predictions: Union[List, pd.DataFrame],
                                    actuals: Union[pd.DataFrame, List],
                                    publish_date=None):
        """
        Description:
            This method is invoked when the user has actuals and prediction and wants to
            log both at the same time. This is the recommended way to make sure there
            are no inconsistencies in mapping the predictions and actuals.

        :param publish_date:  By default uses current date, but user can provide a date from past
        :param model_id: the model against which the serving pipeline is run, this is geneted by our
        service backend the returned to user when they register a model in our registry for the
        first time
        :param model_version: this version for now will be maintained by the customer, later. a decision
        on whether run id should be mapped to model versions can be taken (eg: mlflow)
        :param feature_data: The feature data is the serving data on which the serving predictions are done
        :param predictions: predictions of the model
        :param actuals: actuals as collected by the users
        :return:
        """
        self._validate_predictions_and_actuals(model_id, predictions, actuals)
        unique_ids = self.log_predictions(model_id=model_id, model_version=model_version,
                                          feature_data=feature_data, predictions=predictions,
                                          publish_date=publish_date)
        self.log_actuals(model_id=model_id, model_version=model_version,
                         actuals=actuals, actual_ids=unique_ids, publish_date=publish_date)

    @staticmethod
    def _validate_id_cols(baseline: Baseline, id_cols):
        _columns = baseline.baseline_data.columns.tolist()
        for col in id_cols:
            if col not in _columns:
                raise BaselinesValidationError(f'{col} is specified as an id_col but not present in baseline data. '
                                               f'Baseline data has columns: {_columns}')

    @staticmethod
    def _validate_baseline(baseline: Baseline):
        """
        Description:
            Validations should be both "client" and "server" side.

        Client:
            - length of baselines and labels is same
            - type checking for baselines and predictions
            - data validity
        Server:
            - model_id, model_version exist
        """
        if not isinstance(baseline.baseline_data, pd.DataFrame):
            raise BaselinesValidationError(f'Baseline data is expected to be a dataframe. '
                                           f'The type provided is {type(baseline.baseline_data)}')

        if baseline.baseline_data.empty:
            raise BaselinesValidationError(f'Baseline data is empty. Not uploading data. '
                                           f'Please check if data is present. ')

        if not len(baseline.labels) == len(baseline.baseline_data):
            raise BaselinesValidationError(f'Length of features and labels must be same. '
                                           f'Length of baseline: {len(baseline.baseline_data)}, '
                                           f'Length of labels: {len(baseline.labels)}')

        if not TorchApi.is_asset_exists(baseline.model_id):
            raise ModelValidationError(f'The model with id={baseline.model_id} '
                                       'has not yet been registered. A model has to '
                                       'be registered to be able to log data against it. ')

    def _prepare_baselines(self, baseline_data, baseline):
        baseline_data_copy = baseline_data.copy()
        baseline_data_copy.loc[:, 'ADMLOPS_model_id'] = baseline.model_id
        baseline_data_copy.loc[:, 'ADMLOPS_model_version'] = baseline.model_version
        baseline_data_copy.loc[:, 'ADMLOPS_log_time'] = self.timestamp
        baseline_data_copy.loc[:, 'ADMLOPS_index'] = baseline_data_copy.index
        baseline_data_copy.reset_index(inplace=True)
        return baseline_data_copy

    @classmethod
    def _calculate_metadata_from_baseline(cls, baseline: Baseline, id_cols):
        """
        Calculate all the possbile fields from baseline data
        Add the ADMLOPS_ prefix and create a list of Metadata
        """
        if id_cols:
            data = baseline.baseline_data.drop(id_cols, axis=1)
        else:
            data = baseline.baseline_data
        total_cols = len(data.columns)
        numeric_cols = len(data._get_numeric_data().columns)
        features = [feature for feature in data.columns.tolist() if feature not in id_cols]
        metadata = [
            Metadata(key='ADMLOPS_features', value=json.dumps(features), dataType='JSON_OBJECT'),
            Metadata(key='ADMLOPS_total_features', value=str(total_cols)),
            Metadata(key='ADMLOPS_numerical_features', value=str(numeric_cols)),
            Metadata(key='ADMLOPS_categorical_features', value=str(total_cols - numeric_cols))
        ]
        return metadata

    def log_baseline(self,
                     model_id: Union[int, str],
                     model_version: Union[int, str],
                     baseline_data: pd.DataFrame,
                     labels: Union[pd.Series, np.ndarray, list],
                     label_name: str,
                     id_cols=None,
                     publish_date=None):
        """
            For data drift policies to take effect, users will be required to log baseline data.
            The underlying analysis can be run at the feature level or composite feature level.
            Recommended but optional.

        :param label_name: name of the field which is used as label for the model
        :param model_id: the model against which the serving pipeline is run, this is geneted by our
        service backend the returned to user when they register a model in our registry for the
        first time
        :param model_version: this version for now will be maintained by the customer, later. a decision
        on whether run id should be mapped to model versions can be taken (eg: mlflow)
        :param baseline_data: The training data.
        :param publish_date: By default uses current date, but user can provide a date from past
        :param labels: The labels fed into the model corresponding to the training data
        :param id_cols: The columns/features that are unique identifiers for a data point
        :return:
        """
        published_dt = publish_date if publish_date else self.published_dt
        baseline = Baseline(model_id=model_id,
                            model_version=model_version,
                            baseline_data=baseline_data,
                            labels=labels,
                            label_name=label_name)
        self._validate_baseline(baseline)
        metadata = self._calculate_metadata_from_baseline(baseline, id_cols)
        if id_cols:
            self._validate_id_cols(baseline, id_cols)
            metadata.append(
                Metadata(key='id_cols', value=','.join(id_cols))
            )
        baseline_data_cp = self._prepare_baselines(baseline_data, baseline)
        filepath = FileFormatUtils.create_s3_path(self.workspace,
                                                  baseline,
                                                  published_dt,
                                                  self._get_current_hour())
        _logger.debug(f'The s3 path to upload baseline: {str(filepath)}')
        MLOpsApi.upload_data(baseline_data_cp, str(filepath))
        self._update_metadata(model_id, metadata)

    def _set_timestamp_date(self):
        now = get_now()
        self.timestamp = get_timestamp(now, unit='s')
        self.published_dt = get_formatted_time(now, '%Y-%m-%d')

    @staticmethod
    def _get_current_hour():
        now = get_now()
        return str(get_now_hour(now))
