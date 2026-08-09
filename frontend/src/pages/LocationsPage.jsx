import { useEffect, useState } from 'react';
import Plot from '../components/PlotComponent';
import { api } from '../api';
import { Loading, Card, Badge, StatCard } from '../components/UI';

const CONFIG = { displayModeBar: false, responsive: true };

export default function LocationsPage() {
  const [locations, setLocations] = useState([]);
  const [remoteData, setRemoteData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getLocations(),
      api.getRemoteRatio(),
    ]).then(([l, r]) => {
      setLocations(l);
      setRemoteData(r);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loading />;

  const total = locations.reduce((s, l) => s + l.job_count, 0);

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          Location <span className="gradient-text">Explorer</span>
        </h1>
        <p className="page-subtitle">
          Geographic job market analysis across {locations.length} Indian tech hubs
        </p>
      </div>

      {/* City Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: 16,
        marginBottom: 28,
      }}>
        {locations.map((loc, i) => {
          const pct = ((loc.job_count / total) * 100).toFixed(1);
          const hue = 210 + i * 15;
          return (
            <div
              key={loc.location}
              className="card"
              style={{ cursor: 'default', position: 'relative', overflow: 'hidden' }}
            >
              <div style={{
                position: 'absolute', top: 0, left: 0, right: 0, height: 3,
                background: `hsl(${hue}, 70%, 60%)`,
              }} />
              <div style={{ fontSize: 24, marginBottom: 8 }}>
                {['🏙️','🌆','🌇','🌃','🌉','🏗️','🌁','🏢','🌐','🗺️','🏘️','🌍','🏛️','🌄','🏔️'][i % 15]}
              </div>
              <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>
                {loc.location}
              </div>
              <div style={{ fontSize: 26, fontWeight: 800, color: `hsl(${hue}, 70%, 65%)`, lineHeight: 1 }}>
                {loc.job_count.toLocaleString()}
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                jobs · {pct}% of total
              </div>
              <div style={{
                marginTop: 10,
                height: 4,
                background: 'rgba(255,255,255,0.06)',
                borderRadius: 2,
                overflow: 'hidden',
              }}>
                <div style={{
                  height: '100%',
                  width: `${pct}%`,
                  background: `hsl(${hue}, 70%, 60%)`,
                  borderRadius: 2,
                  transition: 'width 0.8s ease',
                }} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="chart-grid">
        {/* Treemap */}
        <Card title="Job Distribution Treemap" subtitle="Visual size = number of jobs">
          <Plot
            data={[{
              type: 'treemap',
              labels: locations.map(l => l.location),
              values: locations.map(l => l.job_count),
              parents: locations.map(() => ''),
              marker: {
                colors: locations.map((_, i) => `hsl(${210 + i * 15}, 65%, 45%)`),
                line: { color: '#07090f', width: 2 },
              },
              textinfo: 'label+value',
              textfont: { color: 'white', size: 12, family: 'Inter' },
              hovertemplate: '<b>%{label}</b><br>%{value:,} jobs<extra></extra>',
            }]}
            layout={{
              paper_bgcolor: 'transparent',
              font: { family: 'Inter', color: '#f1f5f9' },
              height: 380,
              margin: { t: 10, b: 10, l: 10, r: 10 },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>

        {/* Work Mode By City stacked bar */}
        <Card title="Work Mode Summary" subtitle="Remote · Hybrid · Onsite across the platform">
          <Plot
            data={[
              {
                type: 'bar',
                name: 'Remote',
                x: remoteData.map(r => r.work_mode),
                y: remoteData.map(r => r.count),
                marker: {
                  color: remoteData.map(r => ({
                    remote: '#10b981',
                    hybrid: '#f59e0b',
                    onsite: '#6366f1',
                  }[r.work_mode] || '#64748b')),
                  line: { width: 0 },
                },
                text: remoteData.map(r => `${r.percentage}%`),
                textposition: 'outside',
                textfont: { color: '#f1f5f9', size: 13 },
                hovertemplate: '<b>%{x}</b><br>%{y:,} jobs<extra></extra>',
              }
            ]}
            layout={{
              paper_bgcolor: 'transparent',
              plot_bgcolor: 'transparent',
              font: { family: 'Inter', color: '#94a3b8', size: 12 },
              height: 380,
              margin: { t: 50, b: 50, l: 70, r: 20 },
              yaxis: { gridcolor: 'rgba(255,255,255,0.05)', title: 'Number of Jobs' },
              xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
              showlegend: false,
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>
      </div>
    </div>
  );
}
