import React from 'react';

const SymbolTable = ({ symbols }) => {
  if (!symbols || symbols.length === 0) return <div className="p-4 text-white/40 text-sm">Symbol table is empty.</div>;

  return (
    <div className="w-full bg-[#1c1c1e] rounded-2xl border border-white/5 overflow-hidden shadow-sm">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-white/[0.03] text-xs font-semibold text-white/50 border-b border-white/5">
          <tr>
            <th className="px-6 py-3 font-medium tracking-wide">Identifier</th>
            <th className="px-6 py-3 font-medium tracking-wide">Type</th>
            <th className="px-6 py-3 font-medium tracking-wide">Declared Line</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {symbols.map((sym, i) => (
            <tr key={i} className="hover:bg-white/[0.02] transition-colors">
              <td className="px-6 py-3 font-mono text-[#0a84ff] text-sm">{sym.name}</td>
              <td className="px-6 py-3 font-mono text-[#bf5af2] text-xs">{sym.type}</td>
              <td className="px-6 py-3 text-white/60">{sym.line}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SymbolTable;
