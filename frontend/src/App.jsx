import { useState } from 'react';
import Sidebar from './components/Sidebar';
import OverviewPage from './pages/OverviewPage';
import SkillsPage from './pages/SkillsPage';
import SalaryPage from './pages/SalaryPage';
import LocationsPage from './pages/LocationsPage';
import SkillGapPage from './pages/SkillGapPage';
import PredictorPage from './pages/PredictorPage';

const PAGES = {
  overview: OverviewPage,
  skills: SkillsPage,
  salary: SalaryPage,
  locations: LocationsPage,
  gap: SkillGapPage,
  predictor: PredictorPage,
};

export default function App() {
  const [page, setPage] = useState('overview');

  const PageComponent = PAGES[page] || OverviewPage;

  return (
    <div className="app-layout">
      <Sidebar active={page} onNavigate={setPage} />
      <main className="main-content">
        <PageComponent key={page} />
      </main>
    </div>
  );
}
