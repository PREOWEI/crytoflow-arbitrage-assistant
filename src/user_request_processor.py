class UserRequestProcessor:
    """Validates user input and starts natural language interpretation."""

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def process_request(self, user_input):
        if user_input is None or not isinstance(user_input, str):
            return self._invalid_request()

        cleaned_input = user_input.strip()
        if not cleaned_input or len(cleaned_input) < 5:
            return self._invalid_request()

        interpretation = self.interpreter.interpret(cleaned_input)
        if interpretation.get("status") != "success":
            return interpretation

        return {
            "status": "success",
            "data": interpretation,
        }

    def _invalid_request(self):
        return {
            "status": "error",
            "message": "Invalid request. Please enter a valid cryptocurrency analysis request.",
        }
