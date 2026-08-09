import { useEffect, useState } from 'react';
import Plot from '../components/PlotComponent';
import { api, formatSalary } from '../api';
import { Loading, Card, StatCard } from '../components/UI';

const LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { family: 'Inter', color: '#94a3b8', size: 12 },
  margin: { t: 10, b: 60, l: 80, r: 10 },
  xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  yaxis: { gridcolor: 'rgba(255,255,255,0.05)', automargin: true },
};
const CONFIG = { displayModeBar: false, responsive: true };

export default function SalaryPage() {
  const [byRole, setByRole] = useState([]);
  const [byLocation, setByLocation] = useState([]);
  const [byExp, setByExp] = useState([]);
  const [byMode, setByMode] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getSalaryByRole(20),
      api.getSalaryByLocation(),
      api.getSalaryByExperience(),
      api.getSalaryByWorkMode(),
      api.getSalaryStats(),
    ]).then(([r, l, e, m, s]) => {
      setByRole(r);
      setByLocation(l);
      setByExp(e);
      setByMode(m);
      setStats(s);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loading />;

  const lpa = (v) => v ? (v / 100000).toFixed(1) : '0';

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          Salary <span className="gradient-text">Intelligence</span>
        </h1>
        <p className="page-subtitle">
          Compensation analysis across roles, cities, and experience levels
        </p>
      </div>

      {/* Stats */}
      <div className="stat-grid">
        <StatCard icon="📈" value={`${lpa(stats?.mean)} LPA`} label="Average Salary" color="#f59e0b" />
        <StatCard icon="⚖️" value={`${lpa(stats?.median)} LPA`} label="Median Salary" />
        <StatCard icon="📉" value={`${lpa(stats?.min)} LPA`} label="Entry Level" color="#10b981" />
        <StatCard icon="🚀" value={`${lpa(stats?.max)} LPA`} label="Senior Level" color="#ef4444" />
        <StatCard icon="📊" value={`${lpa(stats?.p25)} - ${lpa(stats?.p75)} LPA`} label="25th-75th Percentile" />
      </div>

      {/* Salary by Role */}
      <div style={{ marginBottom: 20 }}>
        <Card
          title="Average Salary by Job Role"
          subtitle="Top 20 roles sorted by average compensation (LPA)"
        >
          <Plot
            data={[
              {
                type: 'bar',
                name: 'Min',
                x: byRole.map(r => r.job_title),
                y: byRole.map(r => r.salary_min / 100000),
                marker: { color: 'rgba(16,185,129,0.6)', line: { width: 0 } },
                hovertemplate: '%{x}<br>Min: %{y:.1f} LPA<extra></extra>',
              },
              {
                type: 'bar',
                name: 'Avg',
                x: byRole.map(r => r.job_title),
                y: byRole.map(r => r.salary_avg / 100000),
                marker: { color: 'rgba(59,130,246,0.8)', line: { width: 0 } },
                hovertemplate: '%{x}<br>Avg: %{y:.1f} LPA<extra></extra>',
              },
              {
                type: 'bar',
                name: 'Max',
                x: byRole.map(r => r.job_title),
                y: byRole.map(r => r.salary_max / 100000),
                marker: { color: 'rgba(139,92,246,0.7)', line: { width: 0 } },
                hovertemplate: '%{x}<br>Max: %{y:.1f} LPA<extra></extra>',
              },
            ]}
            layout={{
              ...LAYOUT,
              barmode: 'group',
              height: 380,
              margin: { t: 10, b: 120, l: 60, r: 10 },
              xaxis: { ...LAYOUT.xaxis, tickangle: -40 },
              legend: { orientation: 'h', y: -0.45, font: { color: '#94a3b8', size: 11 } },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      <div className="chart-grid" style={{ marginBottom: 20 }}>
        {/* By Location */}
        <Card title="Salary by City" subtitle="Average compensation per location">
          <Plot
            data={[{
              type: 'bar',
              x: byLocation.map(l => l.location),
              y: byLocation.map(l => l.salary_avg / 100000),
              marker: {
                color: byLocation.map((_, i) => `hsl(${220 + i * 8}, 70%, 60%)`),
                line: { width: 0 },
              },
              hovertemplate: '<b>%{x}</b><br>Avg: %{y:.1f} LPA<extra></extra>',
            }]}
            layout={{
              ...LAYOUT,
              height: 300,
              margin: { t: 10, b: 90, l: 60, r: 10 },
              xaxis: { ...LAYOUT.xaxis, tickangle: -35 },
              yaxis: { ...LAYOUT.yaxis, title: 'LPA' },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>

        {/* By Work Mode */}
        <Card title="Salary by Work Mode" subtitle="Remote vs Hybrid vs Onsite compensation">
          <Plot
            data={[{
              type: 'bar',
              x: byMode.map(m => m.work_mode),
              y: byMode.map(m => m.salary_avg / 100000),
              marker: {
                color: ['#10b981', '#f59e0b', '#6366f1'],
                line: { width: 0 },
              },
              hovertemplate: '<b>%{x}</b><br>Avg: %{y:.1f} LPA<extra></extra>',
              text: byMode.map(m => `${(m.salary_avg / 100000).toFixed(1)} LPA`),
              textposition: 'outside',
              textfont: { color: '#f1f5f9', size: 13 },
            }]}
            layout={{
              ...LAYOUT,
              height: 300,
              margin: { t: 40, b: 50, l: 60, r: 10 },
              yaxis: { ...LAYOUT.yaxis, title: 'LPA' },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      {/* By Experience */}
      <Card title="Salary by Experience Level" subtitle="How compensation grows with years of experience">
        <Plot
          data={[{
            type: 'scatter',
            mode: 'lines+markers',
            x: byExp.map(e => e.exp_bracket),
            y: byExp.map(e => e.salary_avg / 100000),
            line: {
              color: '#3b82f6',
              width: 3,
              shape: 'spline',
            },
            marker: {
              color: '#60a5fa',
              size: 10,
              line: { color: '#07090f', width: 2 },
            },
            fill: 'tozeroy',
            fillcolor: 'rgba(59,130,246,0.08)',
            hovertemplate: '<b>%{x}</b><br>Avg Salary: %{y:.1f} LPA<extra></extra>',
          }]}
          layout={{
            ...LAYOUT,
            height: 280,
            margin: { t: 10, b: 50, l: 70, r: 20 },
            xaxis: { ...LAYOUT.xaxis, title: '' },
            yaxis: { ...LAYOUT.yaxis, title: 'LPA' },
          }}
          config={CONFIG}
          style={{ width: '100%' }}
        />
      </Card>
    </div>
  );
}
