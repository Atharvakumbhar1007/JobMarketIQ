import { useEffect, useState } from 'react';
import Plot from '../components/PlotComponent';
import { api, CATEGORY_COLORS } from '../api';
import { Loading, Card } from '../components/UI';
import { ProgressBar } from '../components/UI';

const CHART_LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { family: 'Inter', color: '#94a3b8', size: 12 },
  margin: { t: 10, b: 40, l: 130, r: 60 },
  xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  yaxis: { gridcolor: 'rgba(255,255,255,0.05)', automargin: true },
};
const CONFIG = { displayModeBar: false, responsive: true };

export default function SkillsPage() {
  const [topSkills, setTopSkills] = useState([]);
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedLoc, setSelectedLoc] = useState('Bangalore');
  const [selectedRole, setSelectedRole] = useState('Data Scientist');
  const [locSkills, setLocSkills] = useState([]);
  const [roleSkills, setRoleSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getTopSkills(25),
      api.getSkillCategories(),
      api.getAvailableLocations(),
      api.getAvailableRoles(),
    ]).then(([sk, cat, locs, rl]) => {
      setTopSkills(sk);
      setCategories(cat);
      setLocations(locs.locations || []);
      setRoles(rl.roles || []);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (!selectedLoc) return;
    api.getSkillsByLocation(selectedLoc).then(setLocSkills);
  }, [selectedLoc]);

  useEffect(() => {
    if (!selectedRole) return;
    api.getSkillsByRole(selectedRole).then(setRoleSkills);
  }, [selectedRole]);

  if (loading) return <Loading />;

  const maxDemand = topSkills[0]?.demand_count || 1;

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          Skill <span className="gradient-text">Demand</span> Analysis
        </h1>
        <p className="page-subtitle">
          Discover the most in-demand tech skills across {topSkills.length > 0 ? topSkills.length + '+' : ''} tracked technologies
        </p>
      </div>

      <div className="chart-grid" style={{ marginBottom: 20 }}>
        {/* Top 25 Skills Bar Chart */}
        <Card title="Top 25 Most Demanded Skills" subtitle="Global demand across all job postings">
          <Plot
            data={[{
              type: 'bar',
              x: topSkills.map(s => s.demand_count),
              y: topSkills.map(s => s.skill_name),
              orientation: 'h',
              marker: {
                color: topSkills.map(s => CATEGORY_COLORS[s.category] || '#3b82f6'),
                opacity: 0.85,
                line: { width: 0 },
              },
              hovertemplate: '<b>%{y}</b><br>Demand: %{x:,}<extra></extra>',
            }]}
            layout={{
              ...CHART_LAYOUT,
              height: 540,
              margin: { t: 10, b: 30, l: 140, r: 60 },
            }}
            config={CONFIG}
            style={{ width: '100%' }}
          />
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Category Donut */}
          <Card title="Demand by Category" subtitle="Skill category distribution">
            <Plot
              data={[{
                type: 'pie',
                labels: categories.map(c => c.category),
                values: categories.map(c => c.total_mentions),
                hole: 0.55,
                marker: {
                  colors: categories.map(c => CATEGORY_COLORS[c.category] || '#64748b'),
                  line: { color: '#07090f', width: 3 },
                },
                textinfo: 'label+percent',
                textfont: { color: '#f1f5f9', size: 11 },
                hovertemplate: '%{label}<br>%{value:,} mentions<extra></extra>',
              }]}
              layout={{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { family: 'Inter', color: '#94a3b8', size: 12 },
                height: 240,
                showlegend: false,
                margin: { t: 10, b: 10, l: 10, r: 10 },
              }}
              config={CONFIG}
              style={{ width: '100%' }}
            />
          </Card>

          {/* Top Skills List with Progress Bars */}
          <Card title="Quick Reference" subtitle="Top 8 skills">
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {topSkills.slice(0, 8).map((skill, i) => (
                <div key={skill.skill_name}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4, fontSize: 13 }}>
                    <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{skill.skill_name}</span>
                    <span style={{ color: CATEGORY_COLORS[skill.category] || '#3b82f6', fontSize: 11 }}>
                      {skill.category}
                    </span>
                  </div>
                  <ProgressBar value={skill.demand_count} max={maxDemand} color={CATEGORY_COLORS[skill.category]} />
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* By Location & Role */}
      <div className="chart-grid">
        <Card title="Skills by City" subtitle="Filter top skills for a specific location">
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <select
              className="form-select"
              value={selectedLoc}
              onChange={e => setSelectedLoc(e.target.value)}
            >
              {locations.map(l => (
                <option key={l} value={l}>{l}</option>
              ))}
            </select>
          </div>
          {locSkills.length > 0 ? (
            <Plot
              data={[{
                type: 'bar',
                x: locSkills.map(s => s.count),
                y: locSkills.map(s => s.skill_name),
                orientation: 'h',
                marker: {
                  color: locSkills.map(s => CATEGORY_COLORS[s.category] || '#8b5cf6'),
                  line: { width: 0 },
                },
                hovertemplate: '<b>%{y}</b><br>%{x} jobs<extra></extra>',
              }]}
              layout={{
                ...CHART_LAYOUT,
                height: 360,
              }}
              config={CONFIG}
              style={{ width: '100%' }}
            />
          ) : <Loading text="Loading city skills..." />}
        </Card>

        <Card title="Skills by Job Role" subtitle="Most required skills for a specific role">
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <select
              className="form-select"
              value={selectedRole}
              onChange={e => setSelectedRole(e.target.value)}
            >
              {roles.map(r => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>
          {roleSkills.length > 0 ? (
            <Plot
              data={[{
                type: 'bar',
                x: roleSkills.map(s => s.count),
                y: roleSkills.map(s => s.skill_name),
                orientation: 'h',
                marker: {
                  color: roleSkills.map(s => CATEGORY_COLORS[s.category] || '#10b981'),
                  line: { width: 0 },
                },
                hovertemplate: '<b>%{y}</b><br>%{x} jobs<extra></extra>',
              }]}
              layout={{
                ...CHART_LAYOUT,
                height: 360,
              }}
              config={CONFIG}
              style={{ width: '100%' }}
            />
          ) : <Loading text="Loading role skills..." />}
        </Card>
      </div>
    </div>
  );
}
