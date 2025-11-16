'use client'
import React, {useState} from 'react'
import axios from 'axios'
export default function FilePanel({session}){
  const [file, setFile] = useState(null); const [msg, setMsg] = useState('')
  async function upload(){
    if(!file) return
    const fd = new FormData(); fd.append('file', file); fd.append('session_id', session || 'demo')
    try{ const res = await axios.post((process.env.NEXT_PUBLIC_API_URL||'/api') + '/upload_document', fd, { headers: {'Content-Type':'multipart/form-data'} })
      setMsg('Uploaded — ' + (res.data.file||''))
    }catch(e){ setMsg('Upload failed') }
  }
  return (
    <div className="bg-white p-4 rounded-xl shadow mb-6">
      <h3 className="font-semibold">Upload Document</h3>
      <input type="file" accept="application/pdf" onChange={e=>setFile(e.target.files[0])} className="mt-3" />
      <div className="mt-3 flex gap-2"><button onClick={upload} className="px-3 py-2 rounded bg-sky-600 text-white">Upload</button>
        <button className="px-3 py-2 rounded border">View Files</button></div>
      {msg && <p className="text-sm mt-2 text-slate-500">{msg}</p>}
    </div>
  )
}
