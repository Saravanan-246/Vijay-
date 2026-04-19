from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from runner import run_code_string


app = FastAPI(title="Vijay++ API")


# =========================
# 🔥 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 📦 REQUEST MODEL
# =========================
class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1)
    input: str = ""   # 🔥 input passed from frontend


# =========================
# 🔍 HEALTH
# =========================
@app.get("/")
def health():
    return {"status": "Vijay++ API running 🚀"}


# =========================
# 🚀 RUN CODE (FINAL)
# =========================
@app.post("/run")
def run_code(req: CodeRequest):
    code = req.code.strip()

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Bayam ⚠️: Empty code"
        )

    try:
        # 🔥 PASS INPUT DIRECTLY (NO BLOCKING)
        result = run_code_string(code, req.input)

        # =========================
        # 🔹 SAFE RESPONSE FORMAT
        # =========================
        status = result.get("status", "error")
        output = result.get("output", [])
        line = result.get("line", None)

        # normalize output
        if not isinstance(output, list):
            output = [str(output)]

        output = [str(x) for x in output if str(x).strip()]

        if not output:
            output = ["No output"]

        return {
            "status": status,
            "output": output,
            "line": line,
        }

    except Exception as e:
        return {
            "status": "error",
            "output": [f"Bayam ⚠️: {str(e)}"],
            "line": None,
        }