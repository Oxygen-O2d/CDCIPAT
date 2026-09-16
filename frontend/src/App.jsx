import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Editor from './components/Editor';
import TokensTable from './components/TokensTable';
import TreeVisualizer from './components/TreeVisualizer';
import SymbolTable from './components/SymbolTable';
import SemanticChecks from './components/SemanticChecks';
import IntermediateCode from './components/IntermediateCode';
import OutputView from './components/OutputView';
import PipelineStatus from './components/PipelineStatus';
import LanguageGuide from './components/LanguageGuide';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [code, setCode] = useState('');
  const [examples, setExamples] = useState({});
  const [compileRes, setCompileRes] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('guide');

  useEffect(() => {
    axios.get(`${API_URL}/examples`)
      .then(res => setExamples(res.data))
      .catch(err => console.error("Failed to load examples", err));
  }, []);

  const handleCompile = async () => {
    setError(null);
    setCompileRes(null);
    setActiveTab('tokens');

    if (!code.trim()) {
      setError("Please enter some MiniLang code.");
      return;
    }

    try {
      const res = await axios.post(`${API_URL}/compile`, { code });
      setCompileRes(res.data);
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setActiveTab('output');
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Network error");
    }
  };

  const tabs = [
    { id: 'guide', label: 'Guide' },
    { id: 'tokens', label: 'Tokens' },
    { id: 'ast', label: 'AST' },
    { id: 'symbols', label: 'Symbols' },
    { id: 'semantic', label: 'Semantic' },
    { id: 'tac', label: 'IR Code' },
    { id: 'output', label: 'Output' }
  ];

  return (
    <div className="flex h-screen bg-black text-[#f5f5f7] overflow-hidden font-sans selection:bg-blue-500/30 p-6 gap-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1c1e] via-black to-black">
      
      {/* Left Panel - Editor (Floating Glass) */}
      <div className="w-1/3 min-w-[350px] flex flex-col bg-white/5 backdrop-blur-3xl rounded-[2rem] border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.4)] overflow-hidden relative z-10 ring-1 ring-inset ring-white/5">
        <div className="px-8 py-6 flex items-center justify-between border-b border-white/5 bg-white/[0.02]">
          <h1 className="text-2xl font-bold tracking-tight text-white/90 drop-shadow-md">MiniLang</h1>
          <span className="text-[10px] font-bold uppercase tracking-widest bg-white/10 text-white/80 px-3 py-1.5 rounded-full shadow-inner ring-1 ring-white/10">Compiler</span>
        </div>
        <div className="flex-1 overflow-hidden">
          <Editor code={code} setCode={setCode} examples={examples} onCompile={handleCompile} />
        </div>
        {error && (
          <div className="absolute bottom-6 left-6 right-6 p-4 bg-red-500/20 backdrop-blur-xl border border-red-500/30 text-red-200 font-medium text-sm rounded-2xl shadow-2xl ring-1 ring-red-500/20">
            {error}
          </div>
        )}
      </div>

      {/* Right Panel - Visualization & Tabs (Floating Glass) */}
      <div className="w-2/3 flex flex-col relative bg-white/5 backdrop-blur-3xl rounded-[2rem] border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.4)] overflow-hidden ring-1 ring-inset ring-white/5">
        
        {/* Pipeline Status Strip */}
        <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02] z-10 flex justify-center">
           <PipelineStatus stage={compileRes?.stage} success={compileRes?.success} />
        </div>

        {/* Tabs Header */}
        <div className="absolute top-[96px] left-1/2 -translate-x-1/2 z-20 flex items-center p-1.5 bg-black/40 backdrop-blur-2xl border border-white/10 rounded-full shadow-2xl ring-1 ring-white/5">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2 text-sm font-semibold rounded-full transition-all duration-400 ease-out ${
                activeTab === tab.id 
                  ? 'bg-white text-black shadow-[0_2px_10px_rgba(255,255,255,0.3)] scale-105' 
                  : 'text-white/60 hover:text-white hover:bg-white/10 active:scale-95'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="flex-1 w-full h-full relative overflow-hidden bg-black/20">
          {activeTab === 'guide' && <LanguageGuide />}
          {activeTab !== 'guide' && !compileRes ? (
            <div className="h-full flex items-center justify-center text-white/30 text-lg font-medium tracking-wide">
              Initialize compilation sequence
            </div>
          ) : (
            <>
              {activeTab === 'tokens' && <div className="h-full pt-20 px-8 pb-8 overflow-auto"><TokensTable tokens={compileRes.tokens || []} /></div>}
              {activeTab === 'ast' && compileRes.ast && <TreeVisualizer data={compileRes.ast} />}
              {activeTab === 'symbols' && <div className="h-full pt-20 px-8 pb-8 overflow-auto"><SymbolTable symbols={compileRes.symbol_table || []} /></div>}
              {activeTab === 'semantic' && <div className="h-full pt-20 px-8 pb-8 overflow-auto"><SemanticChecks issues={compileRes.semantic_issues || []} /></div>}
              {activeTab === 'tac' && <div className="h-full pt-20 px-8 pb-8 overflow-auto"><IntermediateCode tac={compileRes.tac || []} /></div>}
              {activeTab === 'output' && <div className="h-full pt-20 px-8 pb-8 overflow-auto"><OutputView output={compileRes.output || []} /></div>}
            </>
          )}
        </div>

      </div>

    </div>
  );
}

export default App;
