import React, { useMemo } from 'react';
import Tree from 'react-d3-tree';

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
  const treeData = useMemo(() => {
    if (!data) return { name: 'Root' };
    return transformAST(data);
  }, [data]);

  const renderCustomNodeElement = ({ nodeDatum, toggleNode }) => (
    <g>
      <circle r="15" onClick={toggleNode} className="fill-[#1c1c1e] stroke-[#0a84ff] stroke-2" />
      <text 
        fill="#f5f5f7" 
        stroke="none"
        strokeWidth="0"
        x="20" 
        dy="4"
        style={{ fontSize: '14px', fontFamily: 'monospace' }}
      >
        {nodeDatum.name}
      </text>
      {nodeDatum.attributes && Object.entries(nodeDatum.attributes).map(([k, v], i) => (
        <text 
          key={k}
          fill="#8e8e93" 
          stroke="none"
          strokeWidth="0"
          x="20" 
          dy={20 + i * 14} 
          style={{ fontSize: '10px', fontFamily: 'monospace' }}
        >
          {k}: {v}
        </text>
      ))}
    </g>
  );

  return (
    <div className="w-full h-full bg-[#1c1c1e] border-l border-white/5 relative">
      <Tree
        data={treeData}
        orientation="vertical"
        pathFunc="step"
        translate={{ x: 300, y: 50 }}
        nodeSize={{ x: 200, y: 100 }}
        renderCustomNodeElement={renderCustomNodeElement}
        separation={{ siblings: 1.5, nonSiblings: 2 }}
      />
    </div>
  );
};

export default TreeVisualizer;
