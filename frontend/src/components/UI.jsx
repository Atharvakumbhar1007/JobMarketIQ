export function Loading({ text = 'Loading data...' }) {
  return (
    <div className="loading-spinner">
      <div className="spinner" />
      <span>{text}</span>
    </div>
  );
}

export function StatCard({ icon, value, label, change, color }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-value" style={color ? { color } : {}}>
        {value}
      </div>
      <div className="stat-label">{label}</div>
      {change && <div className="stat-change">{change}</div>}
    </div>
  );
}

export function Card({ title, subtitle, children, style }) {
  return (
    <div className="card" style={style}>
      {title && (
        <div style={{ marginBottom: 16 }}>
          <div className="chart-title">{title}</div>
          {subtitle && <div className="chart-subtitle">{subtitle}</div>}
        </div>
      )}
      {children}
    </div>
  );
}

export function Badge({ mode }) {
  const cls = {
    remote: 'badge-remote',
    hybrid: 'badge-hybrid',
    onsite: 'badge-onsite',
  }[mode?.toLowerCase()] || 'badge-onsite';
  return <span className={`badge ${cls}`}>{mode}</span>;
}

export function ProgressBar({ value, max, color }) {
  const pct = max ? Math.min((value / max) * 100, 100) : 0;
  return (
    <div className="progress-bar-wrap">
      <div
        className="progress-bar-fill"
        style={{
          width: `${pct}%`,
          background: color || 'var(--gradient-primary)',
        }}
      />
    </div>
  );
}
