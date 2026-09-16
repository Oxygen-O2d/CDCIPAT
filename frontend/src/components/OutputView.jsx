import React from 'react';

const OutputView = ({ output }) => {
  if (!output || output.length === 0) {
    return (
      <div className="w-full h-full bg-[#000000] rounded-2xl border border-white/10 p-6 shadow-inner font-mono text-sm text-white/50 flex items-start">
        <span className="text-[#30d158] mr-2">➜</span> [Program exited with no output]
      </div>
    );
  }

  return (
    <div className="w-full h-full bg-[#000000] rounded-2xl border border-white/10 p-6 shadow-inner font-mono text-sm text-white/90 overflow-auto whitespace-pre-wrap">
      <div className="text-white/30 mb-4 select-none">--- Execution Started ---</div>
      {output.map((line, i) => (
        <div key={i} className="mb-1">{line}</div>
      ))}
      <div className="text-white/30 mt-4 select-none">--- Execution Finished ---</div>
    </div>
  );
};

export default OutputView;
