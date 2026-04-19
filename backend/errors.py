# =========================
# 🔴 BASE ERROR
# =========================
class VijayError(Exception):
    def __init__(self, message, line=None, code="GENERAL_ERROR"):
        self.message = str(message)
        self.line = line if isinstance(line, int) else None
        self.code = code

        super().__init__(self._format())

    # =========================
    # FORMAT MESSAGE
    # =========================
    def _format(self):
        prefix = "Bayam ⚠️"
        if self.line is not None:
            return f"{prefix} [Line {self.line}]: {self.message}"
        return f"{prefix}: {self.message}"

    def __str__(self):
        return self._format()

    # =========================
    # API RESPONSE
    # =========================
    def to_dict(self):
        return {
            "error": self.message,
            "line": self.line,
            "code": self.code,
        }


# =========================
# 🔴 PARSER ERRORS
# =========================
class SyntaxErrorVJ(VijayError):
    def __init__(self, message="Invalid syntax", line=None):
        super().__init__(f"Syntax error: {message}", line, "SYNTAX_ERROR")


class IndentationErrorVJ(VijayError):
    def __init__(self, line=None):
        super().__init__("Invalid indentation", line, "INDENTATION_ERROR")


class UnknownCommandError(VijayError):
    def __init__(self, command, line=None):
        super().__init__(f"Unknown command '{command}'", line, "UNKNOWN_COMMAND")


# =========================
# 🔴 RUNTIME ERRORS
# =========================
class RuntimeErrorVJ(VijayError):
    def __init__(self, message="Runtime error", line=None):
        super().__init__(message, line, "RUNTIME_ERROR")


class VariableError(VijayError):
    def __init__(self, name, message="Variable error", line=None):
        super().__init__(f"{message}: '{name}'", line, "VARIABLE_ERROR")


class TypeErrorVJ(VijayError):
    def __init__(self, message="Type mismatch", line=None):
        super().__init__(message, line, "TYPE_ERROR")


class InputError(VijayError):
    def __init__(self, message="Invalid input", line=None):
        super().__init__(message, line, "INPUT_ERROR")


class MathError(VijayError):
    def __init__(self, message="Math error", line=None):
        super().__init__(message, line, "MATH_ERROR")


# =========================
# 🔴 EXECUTION FLOW ERRORS
# =========================
class InvalidOperationError(VijayError):
    def __init__(self, message="Invalid operation", line=None):
        super().__init__(message, line, "INVALID_OPERATION")


class ConditionError(VijayError):
    def __init__(self, message="Invalid condition", line=None):
        super().__init__(message, line, "CONDITION_ERROR")