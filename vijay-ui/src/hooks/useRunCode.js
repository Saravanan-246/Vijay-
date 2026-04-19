import { useState } from "react";
import { runCode as apiRun } from "../services/api";

export default function useRunCode() {
  const [output, setOutput] = useState([]);
  const [status, setStatus] = useState("idle");
  const [errorLine, setErrorLine] = useState(null);

  const [inputs, setInputs] = useState([]);
  const [currentCode, setCurrentCode] = useState("");

  // =========================
  // RUN
  // =========================
  const runCode = async (code) => {
    setInputs([]);
    setOutput([]);
    setCurrentCode(code);

    await execute(code, []);
  };

  // =========================
  // EXECUTE
  // =========================
  const execute = async (code, inputList) => {
    try {
      setStatus("running");

      const data = await apiRun({
        code,
        input: inputList.join("\n"), // 🔥 FIX
      });

      setOutput(data.output || []);
      setStatus(data.status);

      if (data.status === "error") {
        setErrorLine(data.line || null);
      }

    } catch (err) {
      setStatus("error");
      setOutput([`Bayam ⚠️: ${err.message}`]);
    }
  };

  // =========================
  // INPUT SUBMIT
  // =========================
  const submitInput = async (value) => {
    if (!value.trim()) return;

    const updated = [...inputs, value];

    setInputs(updated);

    setOutput((prev) => [...prev, `> ${value}`]);

    await execute(currentCode, updated); // 🔥 FIX
  };

  return {
    runCode,
    submitInput,
    output,
    status,
    errorLine,
    waitingInput: true,
  };
}