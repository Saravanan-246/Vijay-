import { useEffect, useRef, useState } from "react";

export default function Terminal({
  output = [],
  status = "idle",
  waitingInput = false,
  onInputSubmit = () => {},
  onRun = () => {},
}) {
  const containerRef = useRef(null);
  const inputRef = useRef(null);

  const [height, setHeight] = useState(220);
  const [isDragging, setIsDragging] = useState(false);

  const startY = useRef(0);
  const startHeight = useRef(220);

  const [autoScroll, setAutoScroll] = useState(true);
  const [inputValue, setInputValue] = useState("");

  // =========================
  // OUTPUT CLEAN
  // =========================
  const processedOutput = output
    .filter((line) => line && line.trim() !== "")
    .map((line) => ({
      text: line,
      isError: line.toLowerCase().includes("bayam"),
    }));

  // =========================
  // AUTO SCROLL
  // =========================
  useEffect(() => {
    const el = containerRef.current;
    if (!el || !autoScroll) return;

    requestAnimationFrame(() => {
      el.scrollTop = el.scrollHeight;
    });
  }, [processedOutput, waitingInput]);

  const handleScroll = () => {
    const el = containerRef.current;
    if (!el) return;

    const nearBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight < 30;

    setAutoScroll(nearBottom);
  };

  // =========================
  // INPUT FOCUS
  // =========================
  useEffect(() => {
    if (waitingInput) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }
  }, [waitingInput]);

  // =========================
  // 🔥 INPUT SUBMIT
  // =========================
  const handleInputKey = (e) => {
    if (e.key === "Enter") {
      if (!inputValue.trim()) return;

      const value = inputValue.trim();
      setInputValue("");

      onInputSubmit(value);
    }
  };

  // =========================
  // GLOBAL RUN SHORTCUT
  // =========================
  useEffect(() => {
    const handler = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        onRun();
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onRun]);

  // =========================
  // RESIZE
  // =========================
  const handleMouseDown = (e) => {
    setIsDragging(true);
    startY.current = e.clientY;
    startHeight.current = height;

    document.body.style.cursor = "row-resize";
    document.body.style.userSelect = "none";
  };

  useEffect(() => {
    const move = (e) => {
      if (!isDragging) return;

      const delta = startY.current - e.clientY;
      let newHeight = startHeight.current + delta;

      newHeight = Math.max(140, newHeight);
      newHeight = Math.min(window.innerHeight * 0.8, newHeight);

      setHeight(newHeight);
    };

    const up = () => {
      setIsDragging(false);
      document.body.style.cursor = "default";
      document.body.style.userSelect = "auto";
    };

    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);

    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
  }, [isDragging]);

  // =========================
  // STATUS
  // =========================
  const statusMap = {
    success: ["Success", "text-green-400", "bg-green-500"],
    error: ["Error", "text-red-400", "bg-red-500"],
    running: ["Running", "text-yellow-400", "bg-yellow-400"],
    idle: ["Idle", "text-gray-400", "bg-gray-500"],
  };

  const [text, color, dot] = statusMap[status] || statusMap.idle;

  return (
    <div
      style={{ height }}
      className="flex flex-col bg-[#0a0f1a] border-t border-[#1f2937]"
    >
      {/* RESIZE */}
      <div
        onMouseDown={handleMouseDown}
        className="h-[4px] cursor-row-resize bg-[#1f2937] hover:bg-blue-500"
      />

      {/* HEADER */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#111827] border-b border-[#1f2937]">
        <span className="text-[11px] text-gray-400 uppercase">Terminal</span>

        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${dot}`} />
          <span className={`text-[11px] ${color}`}>{text}</span>
        </div>
      </div>

      {/* BODY */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-4 py-3 font-mono text-[13px] text-gray-200 space-y-1"
      >
        {/* EMPTY */}
        {processedOutput.length === 0 && !waitingInput && (
          <div className="text-gray-500 italic">
            &gt; Run your code (Ctrl + Enter)
          </div>
        )}

        {/* OUTPUT */}
        {processedOutput.map((line, i) => (
          <div key={i} className="flex items-start">
            <span
              className={`mr-2 ${
                line.isError ? "text-red-400" : "text-green-400"
              }`}
            >
              &gt;
            </span>

            <span
              className={`whitespace-pre-wrap ${
                line.isError ? "text-red-400" : ""
              }`}
            >
              {line.text}
            </span>
          </div>
        ))}

        {/* INPUT */}
        {waitingInput && (
          <div className="flex items-center mt-2">
            <span className="text-green-400 mr-2">&gt;</span>

            <input
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleInputKey}
              className="flex-1 bg-transparent outline-none text-white border-b border-gray-700 focus:border-blue-500"
              placeholder="Type and press Enter..."
              autoFocus
            />
          </div>
        )}

        {/* SUCCESS */}
        {status === "success" && processedOutput.length > 0 && (
          <div className="mt-2 text-green-400 text-xs opacity-70">
            ✔ Execution completed
          </div>
        )}
      </div>
    </div>
  );
}