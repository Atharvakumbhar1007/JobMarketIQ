import { useState } from 'react';

const NAV_ITEMS = [
  { id: 'overview', icon: '📊', label: 'Dashboard' },
  { id: 'skills', icon: '🧠', label: 'Skill Demand' },
  { id: 'salary', icon: '💰', label: 'Salary Intel' },
  { id: 'locations', icon: '📍', label: 'Locations' },
  { id: 'gap', icon: '🎯', label: 'Skill Gap' },
  { id: 'predictor', icon: '🤖', label: 'Salary Predictor' },
];

export default function Sidebar({ active, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-title">JobMarketIQ</div>
        <div className="sidebar-logo-sub">AI Intelligence Platform</div>
      </div>
      <nav className="sidebar-nav">
        <div className="nav-section-label">Analytics</div>
        {NAV_ITEMS.map(item => (
          <button
            key={item.id}
            className={`nav-item ${active === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
            style={{ width: '100%', textAlign: 'left' }}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div style={{ padding: '16px 24px', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: 1.8 }}>
          <div style={{ fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 4 }}>Data Source</div>
          <div>5,000 synthetic job listings</div>
          <div>Indian tech market · 2026</div>
        </div>
      </div>
    </aside>
  );
}
