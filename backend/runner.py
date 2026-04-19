from lexer import tokenize
from parser import parse
from executor import Executor
from errors import VijayError as VJError

import re


# =========================
# 🔹 RUN FILE
# =========================
def run_file(path, input_data=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return run_code_string(f.read(), input_data)

    except FileNotFoundError:
        return {
            "status": "error",
            "output": [f"Bayam ⚠️: File not found -> {path}"],
            "line": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "output": [f"Bayam ⚠️: {str(e)}"],
            "line": None,
        }


# =========================
# 🔥 MAIN EXECUTION
# =========================
def run_code_string(code, input_data=""):
    try:
        # 🔍 LEXER + PARSER
        tokens = tokenize(code)
        ast = parse(tokens)

        # ❌ STOP IF PARSER ERROR
        for node in ast:
            if node.get("type") == "ERROR":
                return {
                    "status": "error",
                    "output": [node.get("message")],
                    "line": node.get("line"),
                }

        # =========================
        # 🔥 INPUT SYSTEM (SMART)
        # =========================
        inputs = []
        if isinstance(input_data, str) and input_data.strip():
            inputs = [x.strip() for x in input_data.split("\n")]

        input_index = 0

        def input_provider(prompt=""):
            nonlocal input_index

            # ✅ use provided input
            if input_index < len(inputs):
                value = inputs[input_index]
                input_index += 1
                return value

            # 🔥 SMART DEFAULT (FIX)
            prompt_lower = (prompt or "").lower()

            if "number" in prompt_lower or "count" in prompt_lower:
                return "0"

            return ""  # string default

        # =========================
        # 🔥 EXECUTE
        # =========================
        executor = Executor(input_provider=input_provider)
        result = executor.execute(ast)

        # =========================
        # 🔥 NORMALIZE OUTPUT
        # =========================
        output = []

        if isinstance(result, list):
            for item in result:
                if item is None:
                    continue

                s = str(item).strip()
                if s:
                    output.append(s)

        elif result is not None:
            s = str(result).strip()
            if s:
                output.append(s)

        # 🔥 EMPTY OUTPUT FIX
        if not output:
            output = ["No output"]

        # =========================
        # 🔥 DETECT ERROR
        # =========================
        is_error = any("Bayam" in line for line in output)

        # =========================
        # 🔥 EXTRACT LINE NUMBER
        # =========================
        line = None
        joined = " ".join(output)

        match = re.search(r"Line\s+(\d+)", joined, re.IGNORECASE)
        if match:
            line = int(match.group(1))

        return {
            "status": "error" if is_error else "success",
            "output": output,
            "line": line,
        }

    except VJError as e:
        msg = str(e)

        match = re.search(r"Line\s+(\d+)", msg, re.IGNORECASE)
        line = int(match.group(1)) if match else None

        return {
            "status": "error",
            "output": [msg],
            "line": line,
        }

    except Exception as e:
        return {
            "status": "error",
            "output": [f"Bayam ⚠️: {str(e)}"],
            "line": None,
        }