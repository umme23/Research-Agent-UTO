'use client'
import React, {useState} from 'react'
import Layout from './Layout'
import AgentConsole from './AgentConsole'
import FilePanel from './FilePanel'
import SummaryCards from './SummaryCards'

export default function AgentDashboard(){
  const [session, setSession] = useState(null)
  return (
    <Layout>
      <div className="p-6">
        <header className="flex items-center justify-between">
          <div><h1 className="text-3xl font-bold">Universal Task Orchestrator</h1>
            <p className="text-slate-500 mt-1">Multi-agent orchestration · Document Intelligence · Demo</p></div>
          <div className="space-x-2"><button className="btn">New Session</button>
            <button className="btn btn-primary">Publish</button></div>
        </header>
        <section className="mt-6 grid grid-cols-3 gap-6">
          <div className="col-span-2"><AgentConsole session={session} setSession={setSession} /></div>
          <div className="col-span-1"><FilePanel session={session} /><SummaryCards /></div>
        </section>
      </div>
    </Layout>
  )
    }
