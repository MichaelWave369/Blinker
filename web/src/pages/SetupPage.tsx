import { useState } from 'react'
import { apiPost } from '../api/client'

export function SetupPage() {
  const [form, setForm] = useState({ username: '', password: '', pin: '' })
  const [status, setStatus] = useState('')

  return <div><h2>Setup / Auth</h2>
    <input placeholder="Email/Username" onChange={(e)=>setForm({...form, username:e.target.value})} />
    <input placeholder="Password" type="password" onChange={(e)=>setForm({...form, password:e.target.value})} />
    <input placeholder="2FA PIN" onChange={(e)=>setForm({...form, pin:e.target.value})} />
    <button onClick={async()=>{try{await apiPost('/auth/login', form);setStatus('Connected')}catch(err){setStatus(String(err))}}}>Test connection</button>
    <p>{status}</p>
  </div>
}
