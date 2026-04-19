export default function Topbar({
  onRun,
  status = "idle",
  fileName = "test.vj",
  onToggleSidebar,
}) {
  const isRunning = status === "running";

  const statusConfig = {
    success: { text: "Success", color: "text-green-400", dot: "bg-green-500" },
    error: { text: "Error", color: "text-red-400", dot: "bg-red-500" },
    running: { text: "Running", color: "text-yellow-400", dot: "bg-yellow-400" },
    idle: { text: "Idle", color: "text-gray-400", dot: "bg-gray-500" },
  };

  const { text, color, dot } = statusConfig[status] || statusConfig.idle;

  return (
    <div className="h-12 bg-[#0d1117] border-b border-[#1f2937] flex items-center justify-between px-4">

      {/* LEFT */}
      <div className="flex items-center gap-4 min-w-0">

        {/* MOBILE MENU */}
        <button
          onClick={onToggleSidebar}
          className="md:hidden text-gray-400 text-lg hover:text-white transition"
        >
          ☰
        </button>

        {/* BRAND */}
        <div className="flex items-center gap-2">
          <span className="text-green-400 font-semibold text-sm tracking-wide">
            Vijay++
          </span>
          <span className="text-[10px] text-gray-600 hidden md:block">
            IDE
          </span>
        </div>

        {/* FILE TAB (PRO STYLE) */}
        <div className="hidden sm:flex items-center ml-2">
          <div className="relative px-4 py-1.5 text-xs bg-[#161b22] border border-[#30363d] rounded-t-md text-gray-200 max-w-[200px] truncate">
            {fileName}

            {/* subtle active underline */}
            <div className="absolute bottom-0 left-0 w-full h-[2px] bg-green-500" />
          </div>
        </div>
      </div>

      {/* CENTER STATUS */}
      <div className="hidden md:flex items-center text-xs text-gray-400 tracking-wide">
        {status === "idle" && "Ready"}
        {status === "running" && "Running code..."}
        {status === "success" && "Execution completed"}
        {status === "error" && "Execution failed"}
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-4">

        {/* STATUS INDICATOR */}
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${dot}`} />
          <span className={`text-[11px] font-medium ${color}`}>
            {text}
          </span>
        </div>

        {/* RUN BUTTON */}
        <button
          onClick={!isRunning ? onRun : undefined}
          disabled={isRunning}
          className="
            px-4 py-1.5
            text-xs font-medium
            rounded-md
            bg-green-500 text-black
            hover:bg-green-400
            disabled:bg-[#30363d] disabled:text-gray-500
            transition-all duration-150
            flex items-center gap-2
          "
        >
          {isRunning ? (
            <>
              <span className="w-3 h-3 border-2 border-black border-t-transparent rounded-full animate-spin" />
              Running
            </>
          ) : (
            <>
              <span className="w-0 h-0 border-l-[6px] border-l-black border-y-[4px] border-y-transparent" />
              Run
            </>
          )}
        </button>
      </div>
    </div>
  );
}