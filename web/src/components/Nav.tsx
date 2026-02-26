import { Link } from 'react-router-dom'

export function Nav() {
  return (
    <nav style={{ display: 'flex', gap: 12, padding: 12, borderBottom: '1px solid #ddd' }}>
      <Link to="/setup">Setup</Link>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/timeline">Timeline</Link>
      <Link to="/settings">Settings</Link>
      <Link to="/reports">Reports</Link>
    </nav>
  )
}
