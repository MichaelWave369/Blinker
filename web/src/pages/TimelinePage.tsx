import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'

export function TimelinePage() {
  const [events, setEvents] = useState<any[]>([])
  useEffect(() => { apiGet<any[]>('/events').then(setEvents) }, [])
  return <div><h2>Timeline</h2>{events.map(e => <div key={e.id}>{e.created_at} - {e.camera_id} - {e.summary}</div>)}</div>
}
