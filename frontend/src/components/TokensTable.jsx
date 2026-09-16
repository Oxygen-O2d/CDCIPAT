import React from 'react';

const TokensTable = ({ tokens }) => {
  if (!tokens || tokens.length === 0) return <div className="p-4 text-gray-500">No tokens to display.</div>;

  return (
    <div className="w-full bg-[#1c1c1e] rounded-2xl border border-white/5 overflow-hidden shadow-sm">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-white/[0.03] text-xs font-semibold text-white/50 border-b border-white/5">
          <tr>
            <th className="px-6 py-3 font-medium tracking-wide">Type</th>
            <th className="px-6 py-3 font-medium tracking-wide">Value</th>
            <th className="px-6 py-3 font-medium tracking-wide">Line</th>
            <th className="px-6 py-3 font-medium tracking-wide">Col</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {tokens.map((t, i) => (
            <tr key={i} className="hover:bg-white/[0.02] transition-colors">
              <td className="px-6 py-3 font-mono text-[#0a84ff] text-xs">{t.type}</td>
              <td className="px-6 py-3 font-mono text-[#30d158] text-xs">{t.value || 'ε'}</td>
              <td className="px-6 py-3 text-white/60">{t.line}</td>
              <td className="px-6 py-3 text-white/60">{t.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TokensTable;
