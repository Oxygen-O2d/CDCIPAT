import React from 'react';

const IntermediateCode = ({ tac }) => {
  if (!tac || tac.length === 0) return <div className="p-4 text-white/40 text-sm">No intermediate code generated.</div>;

  return (
    <div className="w-full h-full bg-[#1c1c1e] rounded-2xl border border-white/5 p-6 shadow-sm overflow-auto font-mono text-sm leading-loose">
      {tac.map((line, i) => {
        const isLabel = line.endsWith(':');
        return (
          <div key={i} className={`flex items-center gap-4 ${isLabel ? 'mt-4 mb-2 text-[#ff9f0a] font-bold' : 'text-[#64d2ff]'}`}>
            {!isLabel && <span className="text-white/20 select-none w-6 text-right text-xs">{i + 1}</span>}
            <span className={isLabel ? '-ml-2' : ''}>{line}</span>
          </div>
        );
      })}
    </div>
  );
};

export default IntermediateCode;
