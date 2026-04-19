import { useState } from "react";

export default function Sidebar({
  files = [],
  activeFile,
  onSelectFile,
  onNewFile,
  onDeleteRequest,
  onRenameFile,
}) {
  const [editing, setEditing] = useState(null);
  const [tempName, setTempName] = useState("");
  const [status, setStatus] = useState(null);

  const startEdit = (file) => {
    setEditing(file);
    setTempName(file);
    setStatus(null);
  };

  const cancelEdit = () => {
    setEditing(null);
    setTempName("");
    setStatus(null);
  };

  const showStatus = (file, type) => {
    setStatus({ file, type });
    setTimeout(() => setStatus(null), 800);
  };

  const saveEdit = (oldFile) => {
    let name = tempName.trim();

    if (!name) return showStatus(oldFile, "error");

    if (!name.endsWith(".vj")) {
      name = name.replace(/\..+$/, "") + ".vj";
    }

    if (files.includes(name) && name !== oldFile) {
      return showStatus(oldFile, "error");
    }

    if (name === oldFile) return cancelEdit();

    showStatus(oldFile, "success");

    setTimeout(() => {
      onRenameFile(oldFile, name);
      cancelEdit();
    }, 250);
  };

  return (
    <div className="w-64 max-w-[80vw] h-full flex flex-col bg-[#0d1117] border-r border-[#1f2937]">

      {/* HEADER */}
      <div className="h-11 px-3 flex items-center justify-between border-b border-[#1f2937] bg-[#161b22]">
        <span className="text-[11px] text-gray-400 tracking-widest uppercase">
          Explorer
        </span>

        <button
          onClick={onNewFile}
          className="text-[11px] px-2 py-[3px] border border-gray-700 rounded hover:bg-gray-800 active:scale-95 transition"
        >
          + New
        </button>
      </div>

      {/* FILE LIST */}
      <div className="flex-1 overflow-y-auto">
        {files.map((file) => {
          const active = file === activeFile;
          const editingNow = editing === file;

          const statusIcon =
            status?.file === file
              ? status.type === "success"
                ? "✔"
                : "✖"
              : null;

          return (
            <div
              key={file}
              className={`
                flex items-center justify-between px-3 py-2 text-sm cursor-pointer
                transition-all duration-150
                ${
                  active
                    ? "bg-[#161b22] text-white border-l-2 border-green-400"
                    : "text-gray-400 hover:bg-[#161b22]"
                }
              `}
            >
              {/* NAME */}
              {editingNow ? (
                <input
                  autoFocus
                  value={tempName}
                  onChange={(e) => setTempName(e.target.value)}
                  onBlur={() => saveEdit(file)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") saveEdit(file);
                    if (e.key === "Escape") cancelEdit();
                  }}
                  className="w-full text-xs px-2 py-1 bg-[#0a0f1a] border border-gray-700 rounded outline-none focus:border-blue-500"
                />
              ) : (
                <span
                  onClick={() => onSelectFile(file)}
                  onDoubleClick={() => startEdit(file)}
                  className="flex-1 truncate"
                >
                  {file}
                </span>
              )}

              {/* ACTIONS (🔥 ALWAYS VISIBLE) */}
              <div className="flex items-center gap-2 ml-2 text-xs">

                {statusIcon ? (
                  <span
                    className={
                      status.type === "success"
                        ? "text-green-400 font-bold"
                        : "text-red-400 font-bold"
                    }
                  >
                    {statusIcon}
                  </span>
                ) : (
                  !editingNow && (
                    <>
                      <button
                        onClick={() => startEdit(file)}
                        className="text-gray-500 hover:text-white active:scale-90 transition p-1"
                      >
                        ✎
                      </button>

                      <button
                        onClick={() => onDeleteRequest(file)}
                        className="text-gray-500 hover:text-red-400 active:scale-90 transition p-1"
                      >
                        ✕
                      </button>
                    </>
                  )
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* FOOTER */}
      <div className="px-3 py-2 text-[10px] text-gray-500 border-t border-[#1f2937] bg-[#0d1117]">
        Vijay++ Workspace
      </div>
    </div>
  );
}