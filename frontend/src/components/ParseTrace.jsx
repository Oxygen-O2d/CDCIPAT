import React from 'react';

const ParseTrace = ({ trace }) => {
  if (!trace || trace.length === 0) return <div className="p-4 text-gray-500">No trace available.</div>;

  return (
    <div className="w-full bg-[#1c1c1e] rounded-2xl border border-white/5 p-6 shadow-sm font-mono text-sm">
      <ul className="space-y-2">
        {trace.map((step, i) => (
          <li key={i} className="flex items-center gap-3 py-1 border-b border-white/5 last:border-0">
            <span className="text-white/30 text-xs w-6 text-right select-none">{i + 1}</span>
            <span className="text-[#bf5af2]">{step.split('->')[0].trim()}</span>
            <span className="text-white/20">→</span>
            <span className="text-[#64d2ff]">{step.split('->')[1]?.trim()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ParseTrace;
