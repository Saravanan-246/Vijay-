import { useEffect, useRef, useState } from "react";

export default function Editor({
  code,
  setCode,
  onRun,
  fileName = "test.vj",
  errorLine = null,
}) {
  const textareaRef = useRef(null);
  const gutterRef = useRef(null);
  const highlightRef = useRef(null);

  const [lineCount, setLineCount] = useState(1);
  const [scrollTop, setScrollTop] = useState(0);

  const LINE_HEIGHT = 22;
  const PADDING_TOP = 12;

  // =========================
  // 🔥 SYNTAX HIGHLIGHT
  // =========================
  const highlightCode = (text = "") => {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/("[^"]*")/g, '<span class="text-amber-300">$1</span>')
      .replace(/\b(Ghilli)\b/g, '<span class="text-sky-400">$1</span>')
      .replace(/\b(Headmaster)\b/g, '<span class="text-indigo-400">$1</span>')
      .replace(/\b(ImWaiting)\b/g, '<span class="text-emerald-400">$1</span>')
      .replace(/\b(Mudivu)\b/g, '<span class="text-violet-400">$1</span>')
      .replace(/\b(Vattam)\b/g, '<span class="text-rose-400">$1</span>');
  };

  // =========================
  // LINE COUNT
  // =========================
  useEffect(() => {
    setLineCount(code ? code.split("\n").length : 1);
  }, [code]);

  // =========================
  // 🔥 SCROLL FIX (MAIN FIX)
  // =========================
  const handleScroll = () => {
    const ta = textareaRef.current;
    if (!ta) return;

    const top = ta.scrollTop;
    const left = ta.scrollLeft;

    setScrollTop(top);

    // move highlight layer
    if (highlightRef.current) {
      highlightRef.current.style.transform = `translate(${-left}px, ${-top}px)`;
    }

    // sync gutter
    if (gutterRef.current) {
      gutterRef.current.scrollTop = top;
    }
  };

  // =========================
  // 🔥 AUTO SCROLL TO ERROR
  // =========================
  useEffect(() => {
    if (!errorLine || !textareaRef.current) return;

    const ta = textareaRef.current;

    const target =
      (errorLine - 1) * LINE_HEIGHT - ta.clientHeight / 2;

    ta.scrollTop = Math.max(target, 0);

    handleScroll();
  }, [errorLine]);

  // =========================
  // RUN SHORTCUT
  // =========================
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      onRun?.();
    }
  };

  return (
    <div className="h-full w-full bg-[#0B0E14] flex flex-col">

      {/* HEADER */}
      <div className="h-10 px-4 flex items-center justify-between border-b border-white/5 bg-[#0D1117]">
        <span className="text-xs text-gray-400 truncate">
          {fileName}
        </span>
        <span className="text-[11px] text-gray-500">
          Ctrl/Cmd + Enter
        </span>
      </div>

      {/* BODY */}
      <div className="flex flex-1 min-h-0">

        {/* GUTTER */}
        <div
          ref={gutterRef}
          className="w-14 bg-[#0D1117] border-r border-white/5 text-right pr-3 text-[12px] font-mono select-none overflow-hidden"
        >
          <div style={{ paddingTop: PADDING_TOP }}>
            {Array.from({ length: lineCount }).map((_, i) => {
              const line = i + 1;
              const isError = line === errorLine;

              return (
                <div
                  key={line}
                  style={{ height: LINE_HEIGHT }}
                  className={
                    isError
                      ? "text-red-400 bg-red-500/10 border-r-2 border-red-500"
                      : "text-gray-600"
                  }
                >
                  {line}
                </div>
              );
            })}
          </div>
        </div>

        {/* EDITOR */}
        <div className="relative flex-1 overflow-hidden">

          {/* 🔥 HIGHLIGHT LAYER */}
          <pre
            ref={highlightRef}
            className="absolute top-0 left-0 p-3 font-mono text-[13px] leading-[22px] text-gray-300 pointer-events-none"
            style={{
              whiteSpace: "pre",
              minWidth: "100%",
            }}
            dangerouslySetInnerHTML={{
              __html: highlightCode(code),
            }}
          />

          {/* 🔥 ERROR LINE */}
          {errorLine && (
            <div
              className="absolute left-0 right-0 bg-red-500/5 border-y border-red-500/20 pointer-events-none"
              style={{
                top: PADDING_TOP + (errorLine - 1) * LINE_HEIGHT - scrollTop,
                height: LINE_HEIGHT,
              }}
            />
          )}

          {/* 🔥 TEXTAREA */}
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onScroll={handleScroll}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            className="absolute top-0 left-0 w-full h-full bg-transparent text-transparent caret-blue-400 font-mono text-[13px] leading-[22px] outline-none resize-none p-3"
            style={{
              whiteSpace: "pre",
              overflow: "auto",
            }}
          />
        </div>
      </div>
    </div>
  );
}