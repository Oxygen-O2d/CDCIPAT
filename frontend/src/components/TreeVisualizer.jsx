import React, { useMemo, useState, useRef, useEffect } from 'react';
import Tree from 'react-d3-tree';

const getNodeCategoryColor = (name) => {
  const lower = name.toLowerCase();
  if (lower.includes('decl') || lower.includes('assign')) return { border: '#0a84ff', bg: '#0a84ff15', text: '#64d2ff' };
  if (lower.includes('while') || lower.includes('if') || lower.includes('block')) return { border: '#bf5af2', bg: '#bf5af215', text: '#da8fff' };
  if (lower.includes('binop') || lower.includes('op')) return { border: '#ff9f0a', bg: '#ff9f0a15', text: '#ffd60a' };
  if (lower.includes('int') || lower.includes('float') || lower.includes('ident')) return { border: '#30d158', bg: '#30d15815', text: '#30d158' };
  if (lower.includes('print')) return { border: '#ff375f', bg: '#ff375f15', text: '#ff6482' };
  return { border: '#ffffff30', bg: '#ffffff0a', text: '#ffffff' };
};

const transformAST = (node) => {
  if (!node) return null;
  if (Array.isArray(node)) {
    return { name: "List", children: node.map(transformAST).filter(Boolean) };
  }
  if (typeof node !== 'object') {
    return { name: String(node) };
  }

  const { type, ...rest } = node;
  const children = [];
  const attributes = {};

  for (const [key, value] of Object.entries(rest)) {
    if (value === null) continue;
    if (typeof value === 'object') {
      const child = transformAST(value);
      if (child) {
        if (!child.name.startsWith(key)) {
          child.name = `${key}: ${child.name}`;
        }
        children.push(child);
      }
    } else {
      attributes[key] = String(value);
    }
  }

  return {
    name: type || "Node",
    attributes: Object.keys(attributes).length > 0 ? attributes : undefined,
    children: children.length > 0 ? children : undefined
  };
};

const TreeVisualizer = ({ data }) => {
  const containerRef = useRef(null);
  const [orientation, setOrientation] = useState('horizontal');
  const [pathFunc, setPathFunc] = useState('diagonal');
  const [translate, setTranslate] = useState({ x: 90, y: 300 });

  const treeData = useMemo(() => {
    if (!data) return { name: 'Root' };
    return transformAST(data);
  }, [data]);

  const recenter = () => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      if (orientation === 'horizontal') {
        setTranslate({ x: 90, y: Math.max(height / 2, 200) });
      } else {
        setTranslate({ x: Math.max(width / 2, 200), y: 70 });
      }
    }
  };

  useEffect(() => {
    recenter();
  }, [orientation]);

  const renderCustomNodeElement = ({ nodeDatum, toggleNode }) => {
    const hasChildren = nodeDatum.children && nodeDatum.children.length > 0;
    const colors = getNodeCategoryColor(nodeDatum.name);
    
    // Prepare attributes subtitle string
    const attrEntries = nodeDatum.attributes ? Object.entries(nodeDatum.attributes) : [];
    const attrText = attrEntries.map(([k, v]) => `${k}=${v}`).join(', ');
    
    // Node width sizing
    const labelWidth = Math.max(140, Math.min(220, nodeDatum.name.length * 9 + 40));
    const height = attrText ? 44 : 32;

    return (
      <g>
        {/* Node card box */}
        <rect
          x={-12}
          y={-height / 2}
          width={labelWidth}
          height={height}
          rx={10}
          fill="#1c1c1e"
          stroke={colors.border}
          strokeWidth={1.5}
          onClick={toggleNode}
          className="cursor-pointer transition-all duration-200 hover:brightness-125"
          style={{ filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.5))' }}
        />
        
        {/* Category color indicator pill */}
        <circle
          cx={2}
          cy={attrText ? -6 : 0}
          r={4}
          fill={colors.border}
        />

        {/* Primary Title */}
        <text
          x={14}
          y={attrText ? -3 : 4}
          fill="#f5f5f7"
          stroke="none"
          strokeWidth={0}
          style={{ fontSize: '12px', fontWeight: 600, fontFamily: 'monospace' }}
          className="pointer-events-none select-none"
        >
          {nodeDatum.name.length > 20 ? `${nodeDatum.name.slice(0, 19)}…` : nodeDatum.name}
        </text>

        {/* Attribute details */}
        {attrText && (
          <text
            x={14}
            y={12}
            fill={colors.text}
            stroke="none"
            strokeWidth={0}
            style={{ fontSize: '10px', fontFamily: 'monospace', opacity: 0.85 }}
            className="pointer-events-none select-none"
          >
            {attrText.length > 24 ? `${attrText.slice(0, 23)}…` : attrText}
          </text>
        )}

        {/* Child count badge indicator */}
        {hasChildren && (
          <g transform={`translate(${labelWidth - 18}, 0)`} onClick={toggleNode} className="cursor-pointer">
            <circle r={7} fill="#2c2c2e" stroke={colors.border} strokeWidth={1} />
            <text
              textAnchor="middle"
              dy={3.5}
              fill="#8e8e93"
              style={{ fontSize: '9px', fontWeight: 'bold' }}
              stroke="none"
            >
              {nodeDatum.children.length}
            </text>
          </g>
        )}
      </g>
    );
  };

  return (
    <div ref={containerRef} className="w-full h-full relative overflow-hidden bg-black/30 select-none">
      {/* Floating View Controls (Apple HIG Glass Pill) */}
      <div className="absolute top-4 right-6 z-20 flex items-center gap-2 p-1.5 bg-black/60 backdrop-blur-2xl border border-white/10 rounded-full shadow-2xl ring-1 ring-white/5">
        <div className="flex bg-white/5 rounded-full p-0.5 border border-white/5">
          <button
            onClick={() => setOrientation('horizontal')}
            className={`px-3 py-1 text-xs font-medium rounded-full transition-all duration-200 ${
              orientation === 'horizontal' ? 'bg-white/20 text-white shadow-sm' : 'text-white/50 hover:text-white'
            }`}
            title="Horizontal (Left-to-Right)"
          >
            Horizontal
          </button>
          <button
            onClick={() => setOrientation('vertical')}
            className={`px-3 py-1 text-xs font-medium rounded-full transition-all duration-200 ${
              orientation === 'vertical' ? 'bg-white/20 text-white shadow-sm' : 'text-white/50 hover:text-white'
            }`}
            title="Vertical (Top-to-Bottom)"
          >
            Vertical
          </button>
        </div>

        <div className="w-[1px] h-4 bg-white/10 my-auto" />

        <button
          onClick={() => setPathFunc(p => p === 'diagonal' ? 'step' : 'diagonal')}
          className="px-2.5 py-1 text-xs text-white/60 hover:text-white bg-white/5 hover:bg-white/10 rounded-full transition-all border border-white/5"
          title="Toggle Line Style"
        >
          {pathFunc === 'diagonal' ? 'Curves' : 'Orthogonal'}
        </button>

        <button
          onClick={recenter}
          className="px-2.5 py-1 text-xs text-white/60 hover:text-white bg-white/5 hover:bg-white/10 rounded-full transition-all border border-white/5 flex items-center gap-1"
          title="Recenter Tree"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
          Center
        </button>
      </div>

      <Tree
        data={treeData}
        orientation={orientation}
        pathFunc={pathFunc}
        translate={translate}
        nodeSize={orientation === 'horizontal' ? { x: 240, y: 65 } : { x: 200, y: 90 }}
        renderCustomNodeElement={renderCustomNodeElement}
        separation={{ siblings: 1.1, nonSiblings: 1.5 }}
        zoom={0.85}
        enableLegacyTransitions={true}
        transitionDuration={350}
      />
    </div>
  );
};

export default TreeVisualizer;
