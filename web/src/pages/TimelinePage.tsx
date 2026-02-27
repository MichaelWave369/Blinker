import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'

export function TimelinePage() {
  const [events, setEvents] = useState<any[]>([])
  const [q, setQ] = useState('')
  const [tag, setTag] = useState('')

  const load = () => {
    const params = new URLSearchParams()
    if (q) params.set('q', q)
    if (tag) params.set('tag', tag)
    apiGet<any[]>(`/events/search?${params.toString()}`).then(setEvents)
  }

  useEffect(() => { load() }, [])

  return <div>
    <h2>Timeline</h2>
    <div style={{ display: 'flex', gap: 8 }}>
      <input placeholder='Search summary/camera/tags' value={q} onChange={(e)=>setQ(e.target.value)} />
      <input placeholder='Tag (e.g. motion)' value={tag} onChange={(e)=>setTag(e.target.value)} />
      <button onClick={load}>Search</button>
    </div>
    {events.map((item) => <div key={item.event.id}>{item.event.created_at} - {item.camera_name} - {item.event.summary} [{item.tags.join(', ')}]</div>)}
  </div>
}
