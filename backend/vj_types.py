from errors import TypeErrorVJ, MathError


# =========================
# 🔹 BASE VALUE
# =========================
class VJValue:
    def __init__(self, value):
        self.value = value

    def type_name(self):
        return "value"

    def __repr__(self):
        return str(self.value)

    # 🔹 DEFAULT OPS
    def add(self, other):
        raise TypeErrorVJ(f"Cannot add {self.type_name()} with {other.type_name()}")

    def sub(self, other):
        raise TypeErrorVJ(f"Cannot subtract {self.type_name()} with {other.type_name()}")

    def mul(self, other):
        raise TypeErrorVJ(f"Cannot multiply {self.type_name()} with {other.type_name()}")

    def div(self, other):
        raise TypeErrorVJ(f"Cannot divide {self.type_name()} with {other.type_name()}")


# =========================
# 🔹 NUMBER (INT + FLOAT BASE)
# =========================
class VJNumber(VJValue):
    def type_name(self):
        return "number"

    def add(self, other):
        if isinstance(other, (VJNumber, VJFloat)):
            return create_value(self.value + other.value)
        if isinstance(other, VJString):
            return VJString(str(self.value) + other.value)
        return super().add(other)

    def sub(self, other):
        if isinstance(other, (VJNumber, VJFloat)):
            return create_value(self.value - other.value)
        return super().sub(other)

    def mul(self, other):
        if isinstance(other, (VJNumber, VJFloat)):
            return create_value(self.value * other.value)
        if isinstance(other, VJString):
            return VJString(other.value * int(self.value))
        return super().mul(other)

    def div(self, other):
        if isinstance(other, (VJNumber, VJFloat)):
            if other.value == 0:
                raise MathError("Division by zero")
            return VJFloat(self.value / other.value)
        return super().div(other)


# =========================
# 🔹 FLOAT
# =========================
class VJFloat(VJNumber):
    def type_name(self):
        return "float"


# =========================
# 🔹 STRING
# =========================
class VJString(VJValue):
    def type_name(self):
        return "string"

    def add(self, other):
        if isinstance(other, VJValue):
            return VJString(self.value + str(other.value))
        return super().add(other)

    def mul(self, other):
        if isinstance(other, VJNumber):
            return VJString(self.value * int(other.value))
        return super().mul(other)


# =========================
# 🔹 FACTORY
# =========================
def create_value(raw):
    if isinstance(raw, bool):
        return VJNumber(1 if raw else 0)

    if isinstance(raw, int):
        return VJNumber(raw)

    if isinstance(raw, float):
        return VJFloat(raw)

    if isinstance(raw, str):
        return VJString(raw)

    raise TypeErrorVJ(f"Unsupported type: {type(raw)}")