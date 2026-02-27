import { FormEvent, useEffect, useState } from 'react'
import { apiGet, apiPost } from '../api/client'

export function AssistantPage() {
  const [messages, setMessages] = useState<any[]>([])
  const [text, setText] = useState('')

  const load = () => apiGet<any[]>('/assistant/messages?limit=50').then(setMessages)
  useEffect(() => { load() }, [])

  const send = async (e: FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return
    await apiPost('/assistant/messages', { content: text })
    setText('')
    await load()
  }

  return <div>
    <h2>AI Assistant</h2>
    <p>Get automatic camera summaries and chat with the assistant instead of opening every feed.</p>
    <form onSubmit={send} style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
      <input value={text} onChange={(e)=>setText(e.target.value)} placeholder='Ask: What happened outside?' style={{ minWidth: 360 }} />
      <button type='submit'>Send</button>
    </form>
    {messages.map((m) => <div key={m.id}><strong>{m.role}:</strong> {m.content}</div>)}
  </div>
}
