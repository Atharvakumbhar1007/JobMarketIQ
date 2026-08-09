const API_BASE = 'http://localhost:8000';

export const api = {
  // Analytics
  getOverview: () => fetch(`${API_BASE}/api/analytics/overview`).then(r => r.json()),
  getLocations: () => fetch(`${API_BASE}/api/analytics/locations`).then(r => r.json()),
  getRemoteRatio: () => fetch(`${API_BASE}/api/analytics/remote-ratio`).then(r => r.json()),
  getTopCompanies: (n = 15) => fetch(`${API_BASE}/api/analytics/top-companies?n=${n}`).then(r => r.json()),
  getEmploymentTypes: () => fetch(`${API_BASE}/api/analytics/employment-types`).then(r => r.json()),

  // Skills
  getTopSkills: (n = 25) => fetch(`${API_BASE}/api/skills/top?n=${n}`).then(r => r.json()),
  getSkillsByLocation: (location, n = 15) =>
    fetch(`${API_BASE}/api/skills/by-location?location=${encodeURIComponent(location)}&n=${n}`).then(r => r.json()),
  getSkillsByRole: (role, n = 15) =>
    fetch(`${API_BASE}/api/skills/by-role?role=${encodeURIComponent(role)}&n=${n}`).then(r => r.json()),
  getSkillCategories: () => fetch(`${API_BASE}/api/skills/categories`).then(r => r.json()),
  getAvailableLocations: () => fetch(`${API_BASE}/api/skills/locations`).then(r => r.json()),
  getAvailableRoles: () => fetch(`${API_BASE}/api/skills/roles`).then(r => r.json()),
  analyzeSkillGap: (userSkills, targetRole, topN = 15) => {
    const params = new URLSearchParams({ target_role: targetRole, top_n: topN });
    return fetch(`${API_BASE}/api/skills/gap?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userSkills),
    }).then(r => r.json());
  },

  // Salary
  getSalaryByRole: (n = 20) => fetch(`${API_BASE}/api/salary/by-role?n=${n}`).then(r => r.json()),
  getSalaryByLocation: () => fetch(`${API_BASE}/api/salary/by-location`).then(r => r.json()),
  getSalaryByExperience: () => fetch(`${API_BASE}/api/salary/by-experience`).then(r => r.json()),
  getSalaryByWorkMode: () => fetch(`${API_BASE}/api/salary/by-work-mode`).then(r => r.json()),
  getSalaryStats: () => fetch(`${API_BASE}/api/salary/stats`).then(r => r.json()),
  predictSalary: (payload) =>
    fetch(`${API_BASE}/api/salary/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).then(r => r.json()),
  getPredictOptions: () => fetch(`${API_BASE}/api/salary/predict/options`).then(r => r.json()),

  // Jobs
  getJobs: (params = {}) => {
    const q = new URLSearchParams(params);
    return fetch(`${API_BASE}/api/jobs?${q}`).then(r => r.json());
  },
};

export const formatSalary = (val) => {
  if (!val) return '—';
  const lpa = val / 100000;
  return `${lpa.toFixed(1)} LPA`;
};

export const formatNumber = (n) =>
  n ? n.toLocaleString('en-IN') : '0';

export const CATEGORY_COLORS = {
  'Languages': '#3b82f6',
  'Frameworks': '#8b5cf6',
  'Databases': '#10b981',
  'Cloud': '#f59e0b',
  'ML & AI': '#ef4444',
  'DevOps': '#06b6d4',
  'BI & Analytics': '#ec4899',
};
