import { useEffect, useState } from 'react';
import Plot from '../components/PlotComponent';
import { api, formatSalary, formatNumber } from '../api';
import { Loading, StatCard, Card } from '../components/UI';

const CHART_LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { family: 'Inter', color: '#94a3b8', size: 12 },
  margin: { t: 10, b: 60, l: 80, r: 10 },
  xaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.08)' },
  yaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.08)' },
};

const CONFIG = { displayModeBar: false, responsive: true };

export default function OverviewPage() {
  const [stats, setStats] = useState(null);
  const [locations, setLocations] = useState([]);
  const [remotePie, setRemotePie] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [empTypes, setEmpTypes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getOverview(),
      api.getLocations(),
      api.getRemoteRatio(),
      api.getTopCompanies(12),
      api.getEmploymentTypes(),
    ]).then(([s, l, r, c, e]) => {
      setStats(s);
      setLocations(l);
      setRemotePie(r);
      setCompanies(c);
      setEmpTypes(e);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loading />;

  const COLORS_WORK = { remote: '#10b981', hybrid: '#f59e0b', onsite: '#6366f1' };

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          Job Market <span className="gradient-text">Dashboard</span>
        </h1>
        <p className="page-subtitle">
          Live intelligence across {stats?.total_locations} cities · {formatNumber(stats?.total_jobs)} job listings
        </p>
      </div>

      {/* Stat Cards */}
      <div className="stat-grid">
        <StatCard icon="💼" value={formatNumber(stats?.total_jobs)} label="Total Jobs" change="↑ Active listings" />
        <StatCard icon="🏢" value={formatNumber(stats?.total_companies)} label="Companies Hiring" />
        <StatCard icon="📍" value={stats?.total_locations} label="Cities" />
        <StatCard icon="🌐" value={formatNumber(stats?.remote_jobs)} label="Remote Jobs" color="#10b981" />
        <StatCard
          icon="💰"
          value={`${stats?.avg_salary_lpa} LPA`}
          label="Avg Salary"
          color="#f59e0b"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="chart-grid" style={{ marginBottom: 20 }}>
        {/* Jobs by City */}
        <Card title="Jobs by City" subtitle="Total job listings per location">
          <Plot
            data={[{
              type: 'bar',
              x: locations.map(l => l.job_count),
              y: locations.map(l => l.location),
              orientation: 'h',
              marker: {
                color: locations.map((_, i) =>
                  `hsl(${210 + i * 12}, 70%, ${60 - i * 1.5}%)`
                ),
                line: { width: 0 },
              },
              hovertemplate: '%{y}<br>%{x} jobs<extra></extra>',
            }]}
            layout={{
              ...CHART_LAYOUT,
              height: 320,
              margin: { t: 10, b: 30, l: 100, r: 10 },
              xaxis: { ...CHART_LAYOUT.xaxis, title: '' },
              yaxis: { ...CHART_LAYOUT.yaxis, automargin: true },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>

        {/* Work Mode Donut */}
        <Card title="Work Mode Distribution" subtitle="Remote vs Hybrid vs Onsite">
          <Plot
            data={[{
              type: 'pie',
              labels: remotePie.map(r => r.work_mode),
              values: remotePie.map(r => r.count),
              hole: 0.55,
              marker: {
                colors: remotePie.map(r => COLORS_WORK[r.work_mode] || '#64748b'),
                line: { color: '#07090f', width: 3 },
              },
              textinfo: 'label+percent',
              textfont: { color: '#f1f5f9', size: 12 },
              hovertemplate: '%{label}<br>%{value:,} jobs (%{percent})<extra></extra>',
            }]}
            layout={{
              ...CHART_LAYOUT,
              height: 320,
              showlegend: false,
              margin: { t: 20, b: 20, l: 20, r: 20 },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="chart-grid">
        {/* Top Companies */}
        <Card title="Top Hiring Companies" subtitle="Companies with most job postings">
          <Plot
            data={[{
              type: 'bar',
              x: companies.map(c => c.company),
              y: companies.map(c => c.job_count),
              marker: {
                color: '#3b82f6',
                opacity: 0.85,
                line: { width: 0 },
              },
              hovertemplate: '%{x}<br>%{y} jobs<extra></extra>',
            }]}
            layout={{
              ...CHART_LAYOUT,
              height: 280,
              margin: { t: 10, b: 80, l: 40, r: 10 },
              xaxis: { ...CHART_LAYOUT.xaxis, tickangle: -40 },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>

        {/* Employment Types */}
        <Card title="Employment Types" subtitle="Full-time, Contract, Internship split">
          <Plot
            data={[{
              type: 'pie',
              labels: empTypes.map(e => e.employment_type),
              values: empTypes.map(e => e.count),
              hole: 0.45,
              marker: {
                colors: ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'],
                line: { color: '#07090f', width: 3 },
              },
              textinfo: 'label+percent',
              textfont: { color: '#f1f5f9', size: 12 },
              hovertemplate: '%{label}<br>%{value:,} jobs<extra></extra>',
            }]}
            layout={{
              ...CHART_LAYOUT,
              height: 280,
              showlegend: false,
              margin: { t: 20, b: 20, l: 20, r: 20 },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>
      </div>
    </div>
  );
}
