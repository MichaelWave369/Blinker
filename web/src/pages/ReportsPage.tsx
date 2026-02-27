export function ReportsPage() {
  return <div>
    <h2>Reports</h2>
    <a href="/api/snapshot.png" download>Generate Snapshot PNG</a>
    <br />
    <a href="/api/reports/daily" target="_blank" rel="noreferrer">Open Daily Digest JSON</a>
  </div>
}
