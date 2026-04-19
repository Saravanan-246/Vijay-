from errors import VijayError as VJError


class Builtins:
    def __init__(self, input_provider=None):
        """
        input_provider: function(prompt) -> string
        Provided by runner / FastAPI
        """
        self.input_provider = input_provider

    # =========================
    # 🔥 PRINT
    # =========================
    def ImWaiting(self, *values):
        try:
            output = []

            for val in values:
                if hasattr(val, "value"):
                    output.append(str(val.value))
                else:
                    output.append(str(val))

            return " ".join(output) if output else ""

        except Exception as e:
            raise VJError(f"Print error: {str(e)}")

    # =========================
    # 🔥 INPUT
    # =========================
    def Solu(self, prompt=""):
        if not callable(self.input_provider):
            raise VJError("Input system not connected")

        try:
            result = self.input_provider(prompt)
            return "" if result is None else str(result)

        except Exception as e:
            raise VJError(f"Input error: {str(e)}")

    # =========================
    # 🔹 MULTI INPUT
    # =========================
    def SoluMulti(self, count, prompt=""):
        if not isinstance(count, int) or count < 0:
            raise VJError("Invalid input count")

        values = []
        for _ in range(count):
            values.append(self.Solu(prompt))

        return values