import { useEffect, useState } from 'react'
import { apiGet, apiPost } from '../api/client'

export function DashboardPage() {
  const [cams, setCams] = useState<any[]>([])
  useEffect(() => { apiPost('/sync/now').then(()=>apiGet<any[]>('/cameras').then(setCams)) }, [])
  return <div><h2>Camera Dashboard</h2>{cams.map(c => <div key={c.id}>{c.name} | battery:{c.battery} | signal:{c.signal} | armed:{String(c.armed)}</div>)}</div>
}
