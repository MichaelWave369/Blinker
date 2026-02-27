import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'

export function NotificationsPage() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { apiGet<any[]>('/notifications').then(setItems) }, [])
  return <div><h2>Notifications</h2>{items.map(n => <div key={n.id}>{n.created_at} - {n.title} - {n.body}</div>)}</div>
}
