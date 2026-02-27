import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiGet } from '../api/client'

export function CameraPage() {
  const { id } = useParams()
  const [events, setEvents] = useState<any[]>([])
  useEffect(() => { apiGet<any[]>(`/events?camera_id=${id}`).then(setEvents) }, [id])
  return <div><h2>Camera {id}</h2>{events.map(e => <div key={e.id}>{e.created_at} - {e.summary}</div>)}</div>
}
