import { useEffect, useState } from 'react';
import { api, CATEGORY_COLORS } from '../api';
import { Loading, Card } from '../components/UI';

export default function SkillGapPage() {
  const [roles, setRoles] = useState([]);
  const [targetRole, setTargetRole] = useState('Data Scientist');
  const [userInput, setUserInput] = useState('Python, SQL, Pandas, NumPy');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rolesLoading, setRolesLoading] = useState(true);

  useEffect(() => {
    api.getAvailableRoles().then(r => {
      setRoles(r.roles || []);
      setRolesLoading(false);
    });
  }, []);

  const analyze = async () => {
    const skills = userInput.split(',').map(s => s.trim()).filter(Boolean);
    if (!skills.length || !targetRole) return;
    setLoading(true);
    setResult(null);
    const res = await api.analyzeSkillGap(skills, targetRole);
    setResult(res);
    setLoading(false);
  };

  const matchColor = (pct) => {
    if (pct >= 80) return '#10b981';
    if (pct >= 50) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="page animate-fade-up">
      <div className="page-header">
        <h1 className="page-title">
          Skill <span className="gradient-text">Gap</span> Analyzer
        </h1>
        <p className="page-subtitle">
          Compare your skills against market requirements for any tech role
        </p>
      </div>

      <div className="chart-grid">
        {/* Input Card */}
        <Card title="Your Profile" subtitle="Enter your skills and target role">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div className="form-group">
              <label className="form-label">Your Current Skills</label>
              <textarea
                className="form-input"
                rows={4}
                value={userInput}
                onChange={e => setUserInput(e.target.value)}
                placeholder="Python, React, SQL, Docker, AWS..."
                style={{ resize: 'vertical', fontFamily: 'Inter' }}
              />
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                Separate skills with commas
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Target Role</label>
              {rolesLoading ? (
                <div className="form-input" style={{ color: 'var(--text-muted)' }}>Loading roles...</div>
              ) : (
                <select
                  className="form-select"
                  value={targetRole}
                  onChange={e => setTargetRole(e.target.value)}
                >
                  {roles.map(r => <option key={r} value={r}>{r}</option>)}
                </select>
              )}
            </div>

            <button
              className="btn btn-primary"
              onClick={analyze}
              disabled={loading}
              style={{ width: '100%', justifyContent: 'center', padding: '12px 20px' }}
            >
              {loading ? (
                <>
                  <div className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
                  Analyzing...
                </>
              ) : (
                <>🎯 Analyze My Skill Gap</>
              )}
            </button>
          </div>
        </Card>

        {/* Results */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {!result && !loading && (
            <Card>
              <div style={{
                textAlign: 'center',
                padding: '48px 0',
                color: 'var(--text-muted)',
                fontSize: 14,
              }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>🎯</div>
                <div>Enter your skills and click Analyze to see your gap analysis</div>
              </div>
            </Card>
          )}

          {loading && (
            <Card>
              <Loading text="Analyzing your skill profile..." />
            </Card>
          )}

          {result && !result.error && (
            <>
              {/* Match Score */}
              <Card>
                <div className="match-score">
                  <div
                    className="match-score-ring"
                    style={{ color: matchColor(result.match_percentage) }}
                  >
                    {result.match_percentage}%
                  </div>
                  <div className="match-score-label">
                    Match Rate for <strong style={{ color: 'var(--text-primary)' }}>{result.target_role}</strong>
                  </div>
                  <div style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 6 }}>
                    {result.user_match_count} of {result.role_skill_count} top skills matched
                  </div>

                  {/* Progress bar */}
                  <div style={{
                    margin: '20px auto 0',
                    maxWidth: 320,
                    height: 8,
                    background: 'rgba(255,255,255,0.08)',
                    borderRadius: 4,
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%',
                      width: `${result.match_percentage}%`,
                      background: matchColor(result.match_percentage),
                      borderRadius: 4,
                      transition: 'width 0.8s ease',
                    }} />
                  </div>
                </div>
              </Card>

              {/* Matched Skills */}
              {result.matched_skills.length > 0 && (
                <Card title="✅ Skills You Have" subtitle={`${result.matched_skills.length} matched`}>
                  <div className="skill-list">
                    {result.matched_skills.map(s => (
                      <span key={s} className="skill-tag skill-tag-green">✓ {s}</span>
                    ))}
                  </div>
                </Card>
              )}

              {/* Missing Skills */}
              {result.missing_skills.length > 0 && (
                <Card title="🚀 Skills to Learn" subtitle="Most impactful gaps — sorted by market demand">
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {result.missing_skills.map(s => (
                      <div key={s.skill_name} style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 12,
                      }}>
                        <div style={{ flex: 1 }}>
                          <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            marginBottom: 4,
                          }}>
                            <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
                              {s.skill_name}
                            </span>
                            <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                              <span style={{
                                fontSize: 11,
                                color: CATEGORY_COLORS[s.category] || '#3b82f6',
                              }}>
                                {s.category}
                              </span>
                              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                                {s.pct_jobs}% of jobs
                              </span>
                            </div>
                          </div>
                          <div style={{
                            height: 4,
                            background: 'rgba(255,255,255,0.06)',
                            borderRadius: 2,
                            overflow: 'hidden',
                          }}>
                            <div style={{
                              height: '100%',
                              width: `${s.pct_jobs}%`,
                              background: CATEGORY_COLORS[s.category] || '#3b82f6',
                              opacity: 0.7,
                              borderRadius: 2,
                            }} />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </>
          )}

          {result?.error && (
            <Card>
              <div style={{ textAlign: 'center', padding: '32px 0', color: '#ef4444' }}>
                ⚠️ {result.error}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
