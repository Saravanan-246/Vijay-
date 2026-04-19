from environment import Environment
from vj_types import create_value
from vj_builtins import Builtins
from errors import VijayError, RuntimeErrorVJ


class Executor:
    def __init__(self, input_provider=None):
        self.env = Environment()
        self.builtins = Builtins(input_provider)

    # =========================
    # EXECUTE
    # =========================
    def execute(self, ast):
        try:
            outputs = []

            for node in ast:
                result = self.visit(node)

                if result is None:
                    continue

                if isinstance(result, list):
                    outputs.extend(result)
                else:
                    outputs.append(result)

            return outputs if outputs else ["AllIsWell ✅"]

        except VijayError as e:
            return [str(e)]
        except Exception as e:
            return [f"Bayam ⚠️: {str(e)}"]

    # =========================
    # VISIT
    # =========================
    def visit(self, node):
        t = node.get("type")
        line = node.get("line")

        try:
            if t == "START":
                return None

            elif t == "VAR":
                val = self.evaluate(node["expr"], line)
                self.env.define(node["name"], val)

            elif t == "ASSIGN":
                val = self.evaluate(node["expr"], line)
                self.env.assign(node["name"], val)

            elif t == "PRINT":
                val = self.evaluate(node["expr"], line)
                return self.builtins.ImWaiting(val)

            elif t == "INPUT":
                self.handle_input(node)

            elif t == "IF":
                cond = self.evaluate(node["condition"], line)

                if self.is_truthy(cond):
                    return self.run_block(node["body"])
                elif node.get("else"):
                    return self.run_block(node["else"])

            elif t == "LOOP":
                count = self.evaluate(node["count"], line)

                outputs = []
                for _ in range(int(count.value)):
                    res = self.run_block(node["body"])
                    if res:
                        outputs.extend(res)

                return outputs

            elif t == "ERROR":
                raise RuntimeErrorVJ(node.get("message"), line)

        except VijayError:
            raise
        except Exception as e:
            raise RuntimeErrorVJ(str(e), line)

    # =========================
    # BLOCK
    # =========================
    def run_block(self, block):
        outputs = []

        for stmt in block:
            res = self.visit(stmt)

            if res is None:
                continue

            if isinstance(res, list):
                outputs.extend(res)
            else:
                outputs.append(res)

        return outputs

    # =========================
    # 🔥 INPUT HANDLER (IMPROVED)
    # =========================
    def handle_input(self, node):
        name = node["name"]

        prompt = ""
        if node.get("prompt"):
            prompt = node["prompt"].strip('"')

        user_input = self.builtins.Solu(prompt)

        if user_input is None:
            user_input = ""

        value = self.auto_convert(user_input)

        self.env.define(name, create_value(value))

    # =========================
    # 🔥 SMART TYPE CONVERSION
    # =========================
    def auto_convert(self, val):
        if not isinstance(val, str):
            return val

        val = val.strip()

        # INT
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
            return int(val)

        # FLOAT
        try:
            if "." in val:
                return float(val)
        except:
            pass

        # BOOLEAN
        if val.lower() == "true":
            return True
        if val.lower() == "false":
            return False

        # STRING (default)
        return val

    # =========================
    # EVALUATE
    # =========================
    def evaluate(self, expr, line=None):
        try:
            if hasattr(expr, "value"):
                return expr

            if isinstance(expr, str):
                expr = expr.strip()

                # ()
                if expr.startswith("(") and expr.endswith(")"):
                    return self.evaluate(expr[1:-1], line)

                # LOGICAL
                if " AND " in expr:
                    l, r = expr.split(" AND ", 1)
                    return create_value(
                        self.is_truthy(self.evaluate(l, line)) and
                        self.is_truthy(self.evaluate(r, line))
                    )

                if " OR " in expr:
                    l, r = expr.split(" OR ", 1)
                    return create_value(
                        self.is_truthy(self.evaluate(l, line)) or
                        self.is_truthy(self.evaluate(r, line))
                    )

                # COMPARISON
                for op in ["==", "!=", ">=", "<=", ">", "<"]:
                    if op in expr:
                        l, r = expr.split(op, 1)
                        lv = self.evaluate(l, line).value
                        rv = self.evaluate(r, line).value
                        return create_value(eval(f"{lv} {op} {rv}"))

                # + -
                parts = self._split(expr, ["+", "-"])
                if parts:
                    l = self.evaluate(parts[0], line).value
                    r = self.evaluate(parts[2], line).value

                    # 🔥 STRING + NUMBER SAFE
                    if parts[1] == "+":
                        if isinstance(l, str) or isinstance(r, str):
                            return create_value(str(l) + str(r))
                        return create_value(l + r)

                    return create_value(l - r)

                # * /
                parts = self._split(expr, ["*", "/"])
                if parts:
                    l = self.evaluate(parts[0], line).value
                    r = self.evaluate(parts[2], line).value

                    if parts[1] == "/" and r == 0:
                        raise RuntimeErrorVJ("Division by zero", line)

                    return create_value(l * r if parts[1] == "*" else l / r)

                # STRING
                if expr.startswith('"') and expr.endswith('"'):
                    return create_value(expr[1:-1])

                # NUMBER
                try:
                    return create_value(int(expr))
                except:
                    try:
                        return create_value(float(expr))
                    except:
                        pass

                # BOOLEAN
                if expr.lower() == "true":
                    return create_value(True)
                if expr.lower() == "false":
                    return create_value(False)

                # VARIABLE
                return self.env.get(expr)

            raise RuntimeErrorVJ(f"Invalid expression -> {expr}", line)

        except VijayError:
            raise
        except Exception as e:
            raise RuntimeErrorVJ(str(e), line)

    # =========================
    # SPLIT
    # =========================
    def _split(self, expr, ops):
        depth = 0

        for i in range(len(expr) - 1, -1, -1):
            c = expr[i]

            if c == ")":
                depth += 1
            elif c == "(":
                depth -= 1
            elif c in ops and depth == 0:
                return (expr[:i].strip(), c, expr[i + 1:].strip())

        return None

    # =========================
    # TRUTHY
    # =========================
    def is_truthy(self, val):
        return bool(val.value if hasattr(val, "value") else val)