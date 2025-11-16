'use client'
import React, {useState, useEffect, useRef} from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'

function MessageBubble({m, from}){
  const isAgent = from === 'agent'
  return (<div className={`flex ${isAgent? 'justify-start' : 'justify-end'}`}>
      <div className={`p-4 rounded-2xl max-w-[70%] ${isAgent? 'bg-white shadow' : 'bg-sky-600 text-white'}`}><div className="text-sm">{m}</div></div>
    </div>)
}

export default function AgentConsole({session, setSession}){
  const [messages, setMessages] = useState([{id:1, text: 'Hello — I am UTO. Describe your goal.', from: 'agent'}])
  const [input, setInput] = useState(''); const [loading, setLoading] = useState(false)
  const endRef = useRef()
  useEffect(()=>{ endRef.current?.scrollIntoView({behavior:'smooth'}) },[messages])

  async function send(){
    if(!input) return
    const userMsg = {id: Date.now(), text: input, from: 'user'}
    setMessages(prev=>[...prev, userMsg]); setInput(''); setLoading(true)
    try{
      const res = await axios.post((process.env.NEXT_PUBLIC_API_URL||'/api') + '/agent', {goal: userMsg.text})
      const agentText = res.data?.response || 'Agent produced no response (demo)'
      setMessages(prev=>[...prev, {id:Date.now()+1, text: agentText, from:'agent'}])
    }catch(err){ setMessages(prev=>[...prev, {id:Date.now()+2, text: 'Error from server', from: 'agent'}]) }
    finally{ setLoading(false) }
  }

  return (
    <div className="bg-gradient-to-b from-slate-50 to-white p-4 rounded-xl shadow">
      <div className="h-[520px] overflow-auto p-4 space-y-4">
        <AnimatePresence>{messages.map(m=> (<motion.div key={m.id} initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} exit={{opacity:0}}><MessageBubble m={m.text} from={m.from} /></motion.div>))}</AnimatePresence>
        <div ref={endRef} />
      </div>
      <div className="mt-3 flex gap-3">
        <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 p-3 rounded-lg border" placeholder="E.g., 'Summarize this PDF and create slides'"/>
        <button onClick={send} className="px-4 py-2 rounded-lg bg-sky-600 text-white">{loading? 'Working...' : 'Send'}</button>
      </div>
    </div>
  )
}
