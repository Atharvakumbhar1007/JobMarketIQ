import { useEffect, useState } from 'react';
import { api } from '../api';
import { Loading, Card } from '../components/UI';

const WORK_MODES = ['remote', 'hybrid', 'onsite'];
const EMP_TYPES = ['Full-time', 'Part-time', 'Contract', 'Internship'];

export default function PredictorPage() {
  const [roles, setRoles] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    job_title: 'Data Scientist',
    location: 'Bangalore',
    employment_type: 'Full-time',
    experience_min: 2,
    experience_max: 5,
    skill_count: 6,
    work_mode: 'hybrid',
    company: 'Unknown',
  });

  useEffect(() => {
    Promise.all([
      api.getAvailableRoles(),
      api.getAvailableLocations(),
    ]).then(([r, l]) => {
      setRoles(r.roles || []);
      setLocations(l.locations || []);
      setOptionsLoading(false);
    });
  }, []);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const predict = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.predictSalary({
        ...form,
        experience_min: Number(form.experience_min),
        experience_max: Number(form.experience_max),
        skill_count: Number(form.skill_count),
      });
      if (res.detail) {
        setError(res.detail);
      } else {
        setResult(res);
      }
    } catch {
      setError('Failed to reach the prediction service. Make sure the backend is running.');
    }
    setLoading(false);
  };

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          AI Salary <span className="gradient-text">Predictor</span>
        </h1>
        <p className="page-subtitle">
          ML-powered salary estimation (RandomForest · R² = 0.98)
        </p>
      </div>

      <div className="chart-grid">
        {/* Form */}
        <Card title="Job Configuration" subtitle="Fill in the details to get a salary prediction">
          {optionsLoading ? (
            <Loading text="Loading options..." />
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div className="predict-form-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
                <div className="form-group">
                  <label className="form-label">Job Title</label>
                  <select className="form-select" value={form.job_title} onChange={e => set('job_title', e.target.value)}>
                    {roles.map(r => <option key={r} value={r}>{r}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Location</label>
                  <select className="form-select" value={form.location} onChange={e => set('location', e.target.value)}>
                    {locations.map(l => <option key={l} value={l}>{l}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Work Mode</label>
                  <select className="form-select" value={form.work_mode} onChange={e => set('work_mode', e.target.value)}>
                    {WORK_MODES.map(m => <option key={m} value={m}>{m.charAt(0).toUpperCase() + m.slice(1)}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Employment Type</label>
                  <select className="form-select" value={form.employment_type} onChange={e => set('employment_type', e.target.value)}>
                    {EMP_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Min Experience (years)</label>
                  <input
                    type="number"
                    className="form-input"
                    min={0}
                    max={30}
                    value={form.experience_min}
                    onChange={e => set('experience_min', e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Max Experience (years)</label>
                  <input
                    type="number"
                    className="form-input"
                    min={0}
                    max={30}
                    value={form.experience_max}
                    onChange={e => set('experience_max', e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Number of Skills</label>
                  <input
                    type="number"
                    className="form-input"
                    min={1}
                    max={20}
                    value={form.skill_count}
                    onChange={e => set('skill_count', e.target.value)}
                  />
                </div>
              </div>

              <button
                className="btn btn-primary"
                onClick={predict}
                disabled={loading}
                style={{ width: '100%', justifyContent: 'center', padding: '14px 20px', fontSize: 15 }}
              >
                {loading ? (
                  <>
                    <div className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
                    Predicting...
                  </>
                ) : (
                  <>🤖 Predict My Salary</>
                )}
              </button>
            </div>
          )}
        </Card>

        {/* Result */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {!result && !loading && !error && (
            <Card>
              <div style={{
                textAlign: 'center',
                padding: '48px 0',
                color: 'var(--text-muted)',
              }}>
                <div style={{ fontSize: 56, marginBottom: 16 }}>🤖</div>
                <div style={{ fontSize: 15, marginBottom: 8, color: 'var(--text-secondary)' }}>
                  AI Salary Prediction
                </div>
                <div style={{ fontSize: 13 }}>
                  Configure the job details and click Predict to see an AI-powered salary estimate
                </div>
              </div>
            </Card>
          )}

          {loading && (
            <Card>
              <Loading text="Running ML inference..." />
            </Card>
          )}

          {error && (
            <Card>
              <div style={{ textAlign: 'center', padding: '32px 0' }}>
                <div style={{ fontSize: 36, marginBottom: 12 }}>⚠️</div>
                <div style={{ color: '#f87171', fontSize: 14 }}>{error}</div>
              </div>
            </Card>
          )}

          {result && (
            <>
              <div className="predict-result">
                <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>
                  Predicted Annual Salary
                </div>
                <div className="predict-amount">
                  {result.predicted_salary_lpa} LPA
                </div>
                <div className="predict-lpa" style={{ marginTop: 8 }}>
                  ≈ INR {result.predicted_salary.toLocaleString('en-IN')} per year
                </div>
                <div className="predict-range">
                  Estimated range: {result.salary_range_min_lpa} – {result.salary_range_max_lpa} LPA
                </div>
              </div>

              <Card title="Breakdown" subtitle="What went into this prediction">
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: 13 }}>
                  {[
                    { label: 'Role', value: form.job_title },
                    { label: 'Location', value: form.location },
                    { label: 'Work Mode', value: form.work_mode },
                    { label: 'Experience', value: `${form.experience_min}–${form.experience_max} years` },
                    { label: 'Skills', value: `${form.skill_count} skills` },
                    { label: 'Employment', value: form.employment_type },
                  ].map(item => (
                    <div key={item.label} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      paddingBottom: 10,
                      borderBottom: '1px solid var(--color-border)',
                    }}>
                      <span style={{ color: 'var(--text-muted)' }}>{item.label}</span>
                      <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card style={{ background: 'rgba(59,130,246,0.05)', borderColor: 'rgba(59,130,246,0.2)' }}>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.8 }}>
                  <span style={{ color: 'var(--color-primary-light)', fontWeight: 600 }}>🤖 Model Info:</span>{' '}
                  RandomForest Regressor trained on 5,000 Indian tech job listings.
                  R² = 0.9819 · MAE ≈ 1.15 LPA · 5-Fold CV R² = 0.9775
                </div>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
