import os
env = os.environ


# constants
D_FILE_SEPARATOR = "__"
PQ_FILE_EXT = '.parquet'
PKL_FILE_EXT = '.pkl'
TZ = "UTC"
ACCELO_LOG_LEVEL = 'debug'
ERRORS = 'errors'
MLOPS_MANDATORY_METADATA = ['frequency', 'model_type', 'performance_metric', 'model_obj']


# API
ACCELO_DATASTORE_NAME = 'mlops-datastore'
ACCELO_API_ENDPOINT = env.get('ACCELO_API_ENDPOINT') or 'torch.acceldata.local'
MLOPS_METASTORE = env.get('MLOPS_METASTORE') or 'torch.acceldata.local'
ACCELO_API_ACCESS_KEY = env.get('ACCELO_API_ACCESS_KEY')
ACCELO_API_SECRET_KEY = env.get('ACCELO_API_SECRET_KEY')
CLOUD_ACCESS_KEY = env.get('CLOUD_ACCESS_KEY')
CLOUD_SECRET_KEY = env.get('CLOUD_SECRET_KEY')
MANDATORY_ENV_VARS = [ACCELO_API_ACCESS_KEY, ACCELO_API_SECRET_KEY, CLOUD_ACCESS_KEY, CLOUD_SECRET_KEY, ACCELO_API_ENDPOINT]
