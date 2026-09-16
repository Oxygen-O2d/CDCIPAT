import React from 'react';

const SemanticChecks = ({ issues }) => {
  if (!issues || issues.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-[#30d158]/80 space-y-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <span className="font-semibold tracking-wide">No Semantic Issues Found</span>
      </div>
    );
  }

  return (
    <div className="w-full space-y-3">
      {issues.map((issue, i) => {
        const isError = issue.type === "error";
        return (
          <div key={i} className={`flex items-start gap-4 p-4 rounded-2xl border shadow-sm ${
            isError ? 'bg-[#ff453a]/5 border-[#ff453a]/20' : 'bg-[#ffd60a]/5 border-[#ffd60a]/20'
          }`}>
            <div className={`mt-0.5 ${isError ? 'text-[#ff453a]' : 'text-[#ffd60a]'}`}>
              {isError ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              )}
            </div>
            <div>
              <div className="text-sm font-semibold text-white/90">Line {issue.line}</div>
              <div className={`text-sm mt-1 ${isError ? 'text-[#ff453a]/90' : 'text-[#ffd60a]/90'}`}>{issue.message}</div>
            </div>
          </div>
        )
      })}
    </div>
  );
};

export default SemanticChecks;
