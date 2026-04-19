import sys
import os

from runner import run_file


def main():
    try:
        # =========================
        # 📁 GET FILE PATH
        # =========================
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = os.path.join("examples", "test.vj")
            print("⚡ Vijay++ Running Default File...\n")

        # =========================
        # ❌ FILE VALIDATION
        # =========================
        if not os.path.exists(file_path):
            print(f"Bayam ⚠️: File not found -> {file_path}")
            return

        if not file_path.endswith(".vj"):
            print("Bayam ⚠️: Invalid file type (only .vj allowed)")
            return

        # =========================
        # 🔥 EXECUTE FILE
        # =========================
        result = run_file(file_path)

        # =========================
        # 🔥 NORMALIZE OUTPUT
        # =========================
        if isinstance(result, dict):
            output = result.get("output", [])
        elif isinstance(result, list):
            output = result
        else:
            output = [str(result)]

        # =========================
        # 🖨 PRINT OUTPUT
        # =========================
        has_output = False

        for line in output:
            if line is None:
                continue

            line = str(line).strip()

            if line:
                print(line)
                has_output = True

        # =========================
        # 🔹 EMPTY OUTPUT HANDLING
        # =========================
        if not has_output:
            print("No output")

    except Exception as e:
        print(f"Bayam ⚠️: {str(e)}")


if __name__ == "__main__":
    main()