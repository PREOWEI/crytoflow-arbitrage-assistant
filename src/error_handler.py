class ErrorHandler:
    """Central helper for stable error responses."""

    @staticmethod
    def handle_invalid_pair(pair):
        return {
            "status": "error",
            "message": f"Invalid or unsupported cryptocurrency pair: {pair}",
        }

    @staticmethod
    def handle_invalid_exchange(exchange):
        return {
            "status": "error",
            "message": f"Unsupported exchange requested: {exchange}",
        }

    @staticmethod
    def handle_api_error(error):
        return {
            "status": "error",
            "message": f"API error occurred: {error}",
        }

    @staticmethod
    def handle_network_error(error=None):
        message = "Network error occurred."
        if error:
            message = f"{message} {error}"
        return {
            "status": "error",
            "message": message,
        }

    @staticmethod
    def handle_processing_error(error):
        return {
            "status": "error",
            "message": f"Processing error occurred: {error}",
        }

    @staticmethod
    def safe_execute(function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            return ErrorHandler.handle_processing_error(error)
