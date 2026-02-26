import { Navigate, Route, Routes } from 'react-router-dom'
import { Nav } from './components/Nav'
import { SetupPage } from './pages/SetupPage'
import { DashboardPage } from './pages/DashboardPage'
import { TimelinePage } from './pages/TimelinePage'
import { CameraPage } from './pages/CameraPage'
import { SettingsPage } from './pages/SettingsPage'
import { ReportsPage } from './pages/ReportsPage'

export default function App() {
  return <div>
    <h1>Blinker</h1>
    <Nav />
    <Routes>
      <Route path="/" element={<Navigate to="/setup" />} />
      <Route path="/setup" element={<SetupPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/timeline" element={<TimelinePage />} />
      <Route path="/camera/:id" element={<CameraPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="/reports" element={<ReportsPage />} />
    </Routes>
  </div>
}
