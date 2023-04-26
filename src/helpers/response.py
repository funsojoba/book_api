from flask import jsonify


def api_response(status, message=None, data=None, errors=None):

    response = jsonify(
        {
            "status": "success" if status in [200, 201] else "failure",
            "message": message,
            "data": data,
            "errors": errors,
        }
    )
    response.status_code = status
    return response
