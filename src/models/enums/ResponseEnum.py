from enum import Enum

class ResponseEnum(Enum):

    FILE_VALIDATED_SUCCESS = 'file_validate_successfully'
    FILE_UPLOAD_SUCCESS = 'file_uploaded_successfully'
    FILE_UPLOAD_FAIL = 'file_upload_failed'
    FILE_TYPE_NOT_SUPPORTED = 'file_type_not_supported'
    FILE_SIZE_EXCEED = 'file_size_exceeded'
    PROCESSING_FAIL = 'file_processing_failed'
    PROCESSING_SUCCESS = 'file_processing_success'
