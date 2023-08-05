# TODO: Documentation
# TODO: Specific exceptions


class DataValidationError(Exception):
    pass


class PredictionsValidationError(DataValidationError):
    pass


class ActualsValidationError(DataValidationError):
    pass


class PredictionsAndActualsValidationError(DataValidationError):
    pass


class BaselinesValidationError(DataValidationError):
    pass


class ModelValidationError(Exception):
    pass


class S3AccessValidationError(Exception):
    pass


class MLOpsAPIError(Exception):
    pass


class TorchAPIError(Exception):
    pass


class ProjectValidationError(MLOpsAPIError):
    pass


class ProjectExistsError(ProjectValidationError):
    pass


class MetadataValidationError(Exception):
    pass


class ENVValidationError(Exception):
    pass
