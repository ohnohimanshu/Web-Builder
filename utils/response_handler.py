"""
Utilities for handling API responses and errors.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST framework that returns
    detailed error messages.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, there was an unhandled exception
    if response is None:
        return None
    
    # Format the response data
    error_data = {
        'status': 'error',
        'code': response.status_code,
        'detail': str(exc) if hasattr(exc, '__str__') else 'An error occurred',
    }
    
    if hasattr(response, 'data') and isinstance(response.data, dict):
        if 'detail' in response.data:
            error_data['detail'] = response.data['detail']
        else:
            error_data['errors'] = response.data
    
    response.data = error_data
    
    return response


def build_error_response(message, status_code=status.HTTP_400_BAD_REQUEST, details=None):
    """
    Build a standardized error response.
    """
    response_data = {
        'status': 'error',
        'code': status_code,
        'detail': message
    }
    
    if details:
        response_data['errors'] = details
    
    return Response(response_data, status=status_code)


def build_success_response(data=None, message=None, status_code=status.HTTP_200_OK):
    """
    Build a standardized success response.
    """
    response_data = {
        'status': 'success',
        'code': status_code
    }
    
    if message:
        response_data['message'] = message
    
    if data:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)