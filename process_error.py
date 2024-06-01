import sys
import traceback
import json

def process_error() -> dict:
    # Get information about the exception that occurred
    ex_type, ex_value, ex_traceback = sys.exc_info()
    
    # Format the traceback information as a string
    traceback_string = traceback.format_exception(ex_type, ex_value, ex_traceback)
    
    # Create a JSON-formatted error message
    error_msg = json.dumps(
        {
            "errorType": ex_type.__name__,
            "errorMessage": str(ex_value),
            "stackTrace": traceback_string,
        }
    )
    
    # Return the error message as a dictionary
    return error_msg