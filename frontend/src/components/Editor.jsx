import React from 'react';

const Editor = ({ code, setCode, examples, onCompile }) => {
  return (
    <div className="flex flex-col h-full relative bg-transparent">
      <div className="px-8 py-4 flex gap-4 items-center justify-between z-10 border-b border-white/5 bg-white/[0.02]">
        <span className="text-[10px] font-bold text-white/40 tracking-widest uppercase">Source Code</span>
        <select 
          className="bg-black/30 hover:bg-black/50 transition-colors text-xs font-medium text-white/80 border border-white/10 rounded-xl px-4 py-2 outline-none cursor-pointer flex-1 appearance-none max-w-[220px] shadow-inner ring-1 ring-white/5"
          onChange={(e) => {
            if (e.target.value) setCode(examples[e.target.value].trim());
          }}
          value=""
        >
          <option value="" disabled>Load Example...</option>
          {Object.keys(examples).map(k => (
            <option key={k} value={k} className="bg-[#1c1c1e] text-white">{k}</option>
          ))}
        </select>
      </div>
      <div className="flex-1 p-8 relative">
        <textarea
          className="w-full h-full bg-transparent text-[#e5e5ea] font-mono text-sm leading-relaxed p-0 border-none focus:outline-none focus:ring-0 resize-none drop-shadow-sm"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder={`// Enter MiniLang code here...`}
          spellCheck="false"
        />
      </div>
      <div className="p-8 pt-0 mt-auto">
        <button
          onClick={onCompile}
          className="w-full bg-white hover:bg-gray-200 active:scale-95 text-black font-bold py-4 px-6 rounded-2xl transition-all duration-300 shadow-[0_4px_20px_rgba(255,255,255,0.3)] flex justify-center items-center gap-3 ring-1 ring-white/50"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          Initialize Sequence
        </button>
      </div>
    </div>
  );
};

export default Editor;
