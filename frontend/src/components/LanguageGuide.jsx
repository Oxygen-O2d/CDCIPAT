import React from 'react';

const LanguageGuide = () => {
  return (
    <div className="w-full h-full p-6 sm:p-8 overflow-auto text-white/80 font-sans leading-relaxed">
      <h2 className="text-2xl font-bold text-white mb-6 tracking-tight">MiniLang Guide</h2>
      
      <div className="space-y-8">
        <section>
          <h3 className="text-sm font-bold text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Variables & Types</h3>
          <p className="text-sm mb-2">MiniLang is strictly typed. All variables must be declared with a type before use.</p>
          <ul className="list-disc list-inside text-sm space-y-1 text-white/60 font-mono">
            <li><span className="text-[#30d158]">num</span> - Integer numbers (e.g. 5, -10)</li>
            <li><span className="text-[#30d158]">dec</span> - Decimal/floating-point numbers (e.g. 3.14)</li>
          </ul>
          <div className="mt-3 bg-black/40 p-3 rounded-xl border border-white/5 font-mono text-sm text-[#64d2ff]">
            num count = 10;<br/>
            dec price = 19.99;
          </div>
        </section>

        <section>
          <h3 className="text-sm font-bold text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Control Flow</h3>
          <p className="text-sm mb-2">Conditional logic uses <code className="text-white bg-white/10 px-1 rounded">check</code> and <code className="text-white bg-white/10 px-1 rounded">otherwise</code>.</p>
          <div className="bg-black/40 p-3 rounded-xl border border-white/5 font-mono text-sm text-[#64d2ff]">
            check (count &gt; 5) {'{'}<br/>
            &nbsp;&nbsp;count = count - 1;<br/>
            {'}'} otherwise {'{'}<br/>
            &nbsp;&nbsp;count = count + 1;<br/>
            {'}'}
          </div>
        </section>

        <section>
          <h3 className="text-sm font-bold text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Loops</h3>
          <p className="text-sm mb-2">Loops are handled via the <code className="text-white bg-white/10 px-1 rounded">repeat</code> keyword.</p>
          <div className="bg-black/40 p-3 rounded-xl border border-white/5 font-mono text-sm text-[#64d2ff]">
            repeat (count &gt; 0) {'{'}<br/>
            &nbsp;&nbsp;count = count - 1;<br/>
            {'}'}
          </div>
        </section>

        <section>
          <h3 className="text-sm font-bold text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Output</h3>
          <p className="text-sm mb-2">Print results to the executor output using <code className="text-white bg-white/10 px-1 rounded">output()</code>.</p>
          <div className="bg-black/40 p-3 rounded-xl border border-white/5 font-mono text-sm text-[#64d2ff]">
            output(count);
          </div>
        </section>
      </div>
    </div>
  );
};

export default LanguageGuide;
