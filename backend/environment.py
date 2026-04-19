from errors import VariableError, TypeErrorVJ


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    # =========================
    # DEFINE (Headmaster)
    # =========================
    def define(self, name, value, line=None):
        self._validate_name(name, line)

        if name in self.variables:
            raise VariableError(name, "Already declared", line)

        self.variables[name] = value

    # =========================
    # ASSIGN
    # =========================
    def assign(self, name, value, line=None):
        self._validate_name(name, line)

        # 🔥 search current + parent
        env = self._find_env(name)

        if not env:
            raise VariableError(name, "Not defined", line)

        old_value = env.variables[name]

        # 🔥 TYPE SAFETY (only if both have type)
        if hasattr(old_value, "type_name") and hasattr(value, "type_name"):
            if old_value.type_name() != value.type_name():
                raise TypeErrorVJ(
                    f"Cannot change type of '{name}' "
                    f"({old_value.type_name()} → {value.type_name()})",
                    line,
                )

        env.variables[name] = value

    # =========================
    # GET
    # =========================
    def get(self, name, line=None):
        self._validate_name(name, line)

        env = self._find_env(name)

        if env:
            return env.variables[name]

        raise VariableError(name, "Not defined", line)

    # =========================
    # EXISTS
    # =========================
    def exists(self, name):
        return self._find_env(name) is not None

    # =========================
    # CHILD SCOPE
    # =========================
    def create_child(self):
        return Environment(parent=self)

    # =========================
    # 🔥 FAST LOOKUP (IMPORTANT)
    # =========================
    def _find_env(self, name):
        current = self

        while current:
            if name in current.variables:
                return current
            current = current.parent

        return None

    # =========================
    # VALIDATE NAME
    # =========================
    def _validate_name(self, name, line=None):
        if not isinstance(name, str) or not name.strip():
            raise VariableError(name, "Invalid variable name", line)

        # 🔥 faster than replace + isalnum
        if not name.replace("_", "").isalnum():
            raise VariableError(name, "Invalid variable name format", line)

    # =========================
    # DEBUG
    # =========================
    def dump(self):
        return {
            k: getattr(v, "value", v)
            for k, v in self.variables.items()
        }