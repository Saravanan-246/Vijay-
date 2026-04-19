import { useState, useEffect } from "react";
import Topbar from "../components/Topbar";
import Sidebar from "../components/Sidebar";
import Editor from "../components/Editor";
import Terminal from "../components/Terminal";
import { runCode } from "../services/api";

export default function Home() {
  const [files, setFiles] = useState(["test.vj"]);
  const [activeFile, setActiveFile] = useState("test.vj");

  const [fileContents, setFileContents] = useState({
    "test.vj": `Ghilli

Solu "Enter name: " name
Solu "Enter score: " score

ImWaiting "Hello " + name
ImWaiting score + 10`,
  });

  const [output, setOutput] = useState([]);
  const [status, setStatus] = useState("idle");
  const [errorLine, setErrorLine] = useState(null);

  const [showSidebar, setShowSidebar] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState(null);

  // 🔥 INPUT SYSTEM
  const [waitingInput, setWaitingInput] = useState(false);
  const [inputQueue, setInputQueue] = useState([]);
  const [inputPrompts, setInputPrompts] = useState([]);
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);

  // =========================
  // SHORTCUT
  // =========================
  useEffect(() => {
    const handleShortcut = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        if (status !== "running") handleRun();
      }
    };

    window.addEventListener("keydown", handleShortcut);
    return () => window.removeEventListener("keydown", handleShortcut);
  }, [status, activeFile, fileContents]);

  // =========================
  // ESC MODAL
  // =========================
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") setDeleteTarget(null);
    };

    if (deleteTarget) window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [deleteTarget]);

  // =========================
  // CODE CHANGE
  // =========================
  const handleCodeChange = (newCode) => {
    setFileContents((prev) => ({
      ...prev,
      [activeFile]: newCode,
    }));
  };

  // =========================
  // 🚀 RUN
  // =========================
  const handleRun = () => {
    if (status === "running") return;

    const code = fileContents[activeFile];

    setStatus("running");
    setOutput([]);
    setErrorLine(null);
    setInputQueue([]);
    setCurrentPromptIndex(0);

    // 🔥 extract prompts
    const matches = [...code.matchAll(/Solu\s+"([^"]+)"/g)];
    const prompts = matches.map((m) => m[1]);

    if (prompts.length > 0) {
      setInputPrompts(prompts);
      setWaitingInput(true);

      // show first prompt
      setOutput([prompts[0]]);
      return;
    }

    runWithInput("");
  };

  // =========================
  // 🚀 EXECUTION
  // =========================
  const runWithInput = async (input) => {
    try {
      const res = await runCode({
        code: fileContents[activeFile],
        input,
      });

      const out = Array.isArray(res.output)
        ? res.output.filter((l) => l && l.trim())
        : ["No output"];

      setOutput((prev) => [...prev, ...out]);
      setStatus(res.status === "error" ? "error" : "success");
      setErrorLine(typeof res.line === "number" ? res.line : null);

      setWaitingInput(false);
      setInputPrompts([]);
      setCurrentPromptIndex(0);
    } catch (err) {
      console.error(err);

      setOutput(["Bayam ⚠️: Backend not reachable"]);
      setStatus("error");
      setWaitingInput(false);
    }
  };

  // =========================
  // 🔥 INPUT SUBMIT (ORDER FIX)
  // =========================
  const handleInputSubmit = (value) => {
    if (!value.trim()) return;

    const updated = [...inputQueue, value];
    setInputQueue(updated);

    // show typed input
    setOutput((prev) => [...prev, `> ${value}`]);

    const nextIndex = currentPromptIndex + 1;

    // show next prompt
    if (nextIndex < inputPrompts.length) {
      setCurrentPromptIndex(nextIndex);
      setOutput((prev) => [...prev, inputPrompts[nextIndex]]);
      return;
    }

    // 🔥 all inputs done
    const formatted = updated.join("\n");

    setWaitingInput(false);
    runWithInput(formatted);
  };

  // =========================
  // FILE SYSTEM
  // =========================
  const handleNewFile = () => {
    let index = files.length + 1;
    let name = `file${index}.vj`;

    while (files.includes(name)) {
      index++;
      name = `file${index}.vj`;
    }

    setFiles((prev) => [...prev, name]);
    setActiveFile(name);

    setFileContents((prev) => ({
      ...prev,
      [name]: `Ghilli\n\nImWaiting "New file"`,
    }));
  };

  const handleDeleteFile = (file) => {
    const updated = files.filter((f) => f !== file);

    if (updated.length === 0) {
      const defaultFile = "main.vj";

      setFiles([defaultFile]);
      setActiveFile(defaultFile);

      setFileContents({
        [defaultFile]: `Ghilli\n\nImWaiting "Welcome to Vijay++"`,
      });

      return;
    }

    setFiles(updated);

    setFileContents((prev) => {
      const copy = { ...prev };
      delete copy[file];
      return copy;
    });

    if (activeFile === file) {
      setActiveFile(updated[0]);
    }
  };

  const handleRenameFile = (oldName, newName) => {
    if (!newName.endsWith(".vj")) {
      newName = newName.replace(/\..+$/, "") + ".vj";
    }

    if (files.includes(newName)) return;

    setFiles((prev) =>
      prev.map((f) => (f === oldName ? newName : f))
    );

    setFileContents((prev) => {
      const copy = { ...prev };
      copy[newName] = copy[oldName];
      delete copy[oldName];
      return copy;
    });

    if (activeFile === oldName) {
      setActiveFile(newName);
    }
  };

  // =========================
  // UI
  // =========================
  return (
    <div className="h-screen flex flex-col bg-[#0f0f0f] text-white">

      <Topbar
        onRun={handleRun}
        status={status}
        fileName={activeFile}
        onToggleSidebar={() => setShowSidebar(!showSidebar)}
      />

      <div className="flex flex-1 overflow-hidden">

        {showSidebar && (
          <div
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
            onClick={() => setShowSidebar(false)}
          />
        )}

        <div
          className={`fixed md:static z-50 h-full transform ${
            showSidebar ? "translate-x-0" : "-translate-x-full"
          } md:translate-x-0 transition`}
        >
          <Sidebar
            files={files}
            activeFile={activeFile}
            onSelectFile={(file) => {
              setActiveFile(file);
              setShowSidebar(false);
            }}
            onNewFile={handleNewFile}
            onDeleteRequest={setDeleteTarget}
            onRenameFile={handleRenameFile}
          />
        </div>

        <div className="flex flex-col flex-1 min-h-0">

          <div className="flex-1 min-h-0">
            <Editor
              code={fileContents[activeFile]}
              setCode={handleCodeChange}
              onRun={handleRun}
              fileName={activeFile}
              errorLine={errorLine}
            />
          </div>

          <Terminal
            output={output}
            status={status}
            waitingInput={waitingInput}
            onInputSubmit={handleInputSubmit}
          />
        </div>
      </div>

      {deleteTarget && (
        <div
          className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={() => setDeleteTarget(null)}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="w-[90%] max-w-sm bg-[#161b22] border border-[#30363d] rounded-xl shadow-2xl p-5"
          >
            <h2 className="text-sm text-white font-medium mb-2">
              Delete file?
            </h2>

            <p className="text-xs text-gray-400 mb-5">
              Delete{" "}
              <span className="text-red-400 font-medium">
                {deleteTarget}
              </span>
              ?
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setDeleteTarget(null)}
                className="px-3 py-1.5 text-xs border border-gray-600 rounded-md hover:bg-[#21262d]"
              >
                Cancel
              </button>

              <button
                onClick={() => {
                  handleDeleteFile(deleteTarget);
                  setDeleteTarget(null);
                }}
                className="px-3 py-1.5 text-xs bg-red-600 rounded-md hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}