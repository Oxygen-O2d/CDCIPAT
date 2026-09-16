import React from 'react';

const ParsingTable = ({ tableData }) => {
  if (!tableData) return <div className="p-4 text-gray-500">Parsing table data not available.</div>;

  const { grammar, first_sets, follow_sets, parsing_table } = tableData;

  // Extract all unique terminals from the parsing table
  const terminals = new Set();
  Object.values(parsing_table).forEach(row => {
    Object.keys(row).forEach(t => terminals.add(t));
  });
  const terminalList = Array.from(terminals).sort();
  const nonTerminals = Object.keys(parsing_table);

  return (
    <div className="w-full space-y-8">
      
      <div className="bg-[#1c1c1e] rounded-2xl border border-white/5 p-6 shadow-sm">
        <h3 className="text-sm font-semibold tracking-wide text-white/80 mb-4 uppercase">FIRST & FOLLOW Sets</h3>
        <div className="grid grid-cols-2 gap-8 text-sm font-mono">
          <div>
            <h4 className="text-[#0a84ff] border-b border-white/10 pb-2 mb-3">FIRST Sets</h4>
            <ul className="space-y-1.5 text-xs">
              {Object.entries(first_sets).map(([nt, set]) => (
                <li key={nt}><span className="text-[#bf5af2]">{nt}</span>: <span className="text-white/60">{`{ ${set.join(', ')} }`}</span></li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-[#30d158] border-b border-white/10 pb-2 mb-3">FOLLOW Sets</h4>
            <ul className="space-y-1.5 text-xs">
              {Object.entries(follow_sets).map(([nt, set]) => (
                <li key={nt}><span className="text-[#bf5af2]">{nt}</span>: <span className="text-white/60">{`{ ${set.join(', ')} }`}</span></li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-[#1c1c1e] rounded-2xl border border-white/5 p-6 shadow-sm">
        <h3 className="text-sm font-semibold tracking-wide text-white/80 mb-4 uppercase">LL(1) Parsing Table</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-white/[0.03] text-xs font-semibold text-white/50 border-y border-white/5">
              <tr>
                <th className="px-4 py-3 border-r border-white/5">Non-Terminal</th>
                {terminalList.map(t => (
                  <th key={t} className="px-4 py-3 border-r border-white/5 text-[#30d158] font-mono">{t}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {nonTerminals.map(nt => (
                <tr key={nt} className="hover:bg-white/[0.02] transition-colors">
                  <td className="px-4 py-3 font-mono text-[#bf5af2] border-r border-white/5 font-semibold text-xs whitespace-nowrap">{nt}</td>
                  {terminalList.map(t => (
                    <td key={t} className="px-4 py-3 font-mono border-r border-white/5 text-[10px] text-white/70 whitespace-nowrap">
                      {parsing_table[nt]?.[t] || ''}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default ParsingTable;
