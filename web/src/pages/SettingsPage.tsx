import { useEffect, useState } from 'react'
import { apiGet, apiPost } from '../api/client'

export function SettingsPage() {
  const [rules, setRules] = useState<any[]>([])
  const [name, setName] = useState('Night important')

  const load = () => apiGet<any[]>('/rules').then(setRules)
  useEffect(() => { load() }, [])

  const createRule = async () => {
    await apiPost('/rules', {
      name,
      enabled: true,
      conditions: { tag_match: 'motion' },
      actions: { mark_important: true, create_notification: true, add_tags: ['important'] }
    })
    load()
  }

  return <div>
    <h2>Settings / Rules</h2>
    <input value={name} onChange={(e)=>setName(e.target.value)} />
    <button onClick={createRule}>Add Rule</button>
    {rules.map(r => <div key={r.id}>{r.name} (enabled: {String(r.enabled)})</div>)}
  </div>
}
