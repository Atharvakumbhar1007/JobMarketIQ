import React from 'react';
import createPlotlyComponent from 'react-plotly.js/factory';

// Uses the window.Plotly object injected by the CDN script in index.html
// This avoids Vite's 'global is not defined' issue when bundling plotly.js
const Plot = createPlotlyComponent(window.Plotly);

export default function PlotComponent(props) {
  // If window.Plotly is somehow not available, show a fallback
  if (!window.Plotly) {
    return <div style={{ color: '#ef4444', padding: 20 }}>Plotly failed to load. Check your network or index.html.</div>;
  }
  return <Plot {...props} />;
}
