import React from 'react';

const PipelineStatus = ({ stage, success }) => {
  const stages = [
    "Init",
    "Lexical Analysis",
    "Syntax Analysis",
    "Semantic Analysis",
    "Intermediate Code Gen",
    "Execution",
    "Completed"
  ];

  const currentIndex = stages.indexOf(stage);

  return (
    <div className="flex items-center justify-between w-full max-w-4xl overflow-x-auto no-scrollbar py-0.5">
      {stages.slice(1, -1).map((s, i) => {
        const stageIndex = i + 1;
        let state = "pending"; // gray
        if (currentIndex > stageIndex || currentIndex === stages.length - 1) state = "done"; // green
        if (currentIndex === stageIndex && success === false) state = "failed"; // red
        if (currentIndex === stageIndex && success !== false) state = "active"; // blue

        let colorClasses = "bg-white/5 text-white/40 border-transparent";
        if (state === "done") colorClasses = "bg-[#30d158]/10 text-[#30d158] border-[#30d158]/20";
        if (state === "failed") colorClasses = "bg-[#ff453a]/10 text-[#ff453a] border-[#ff453a]/20";
        if (state === "active") colorClasses = "bg-[#0a84ff]/10 text-[#0a84ff] border-[#0a84ff]/20 animate-pulse";

        return (
          <React.Fragment key={s}>
            <div className={`flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full border text-[11px] sm:text-xs font-semibold tracking-wide shrink-0 ${colorClasses} transition-all duration-300`}>
              {state === "done" && <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>}
              {state === "failed" && <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>}
              {s}
            </div>
            {i < stages.length - 3 && (
              <div className="flex-1 min-w-2 h-[1px] bg-white/10 mx-1.5 sm:mx-2 shrink" />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default PipelineStatus;
