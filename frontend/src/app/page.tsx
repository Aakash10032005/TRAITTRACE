"use client";

import React, { useState, useEffect } from "react";
import StorefrontWidget from "../components/StorefrontWidget";
import StorefrontDisplay from "../components/StorefrontDisplay";
import AnalyticsDashboard from "../components/AnalyticsDashboard";
import { submitInteraction, GraphSnapshot } from "../lib/api";
import { RefreshCw, FileText, Activity } from "lucide-react";

const INITIAL_PERSONA = {
  persona: "Unknown Consumer",
  hero_title: "A Storefront Tailored by Consent.",
  hero_subtitle: "Interact with the index cards below. As you tell us what you prefer, this page adapts to your traits in real-time. No cookies, no stealth tracking.",
  recommended_product_id: "prod_classic_standard"
};

export default function Home() {
  const [sessionId, setSessionId] = useState<string>("");
  const [personaData, setPersonaData] = useState(INITIAL_PERSONA);
  const [graphData, setGraphData] = useState<GraphSnapshot>({ nodes: [], links: [] });
  const [isLoading, setIsLoading] = useState(false);
  const [isInitial, setIsInitial] = useState(true);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    initNewFile();
  }, []);

  const initNewFile = () => {
    let uuid = "";
    try {
      uuid = crypto.randomUUID();
    } catch {
      uuid = "file-" + Math.random().toString(36).substring(2, 11);
    }
    setSessionId(uuid);
    setPersonaData(INITIAL_PERSONA);
    setGraphData({
      nodes: [{ id: uuid, type: "user", category: "user" }],
      links: []
    });
    setIsInitial(true);
    setLogs([]);
    addLog(`Opened intake file: ${uuid}`);
  };

  const addLog = (msg: string) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [`[${time}] ${msg}`, ...prev.slice(0, 12)]);
  };

  const handleInteraction = async (value: string, type: string) => {
    if (!sessionId) return;
    
    setIsLoading(true);
    addLog(`Captured trait: '${value}' via ${type}`);

    try {
      const response = await submitInteraction({
        session_id: sessionId,
        interaction_type: type,
        value: value
      });

      setPersonaData({
        persona: response.persona,
        hero_title: response.hero_title,
        hero_subtitle: response.hero_subtitle,
        recommended_product_id: response.recommended_product_id
      });
      setGraphData(response.graph_snapshot);
      setIsInitial(false);
      addLog(`Knowledge graph updated -> Category mapped successfully`);
      addLog(`Groq served persona: "${response.persona}"`);
      addLog(`Serving product id: ${response.recommended_product_id}`);

    } catch (err: any) {
      addLog(`Backend exception caught: ${err.message}`);
      addLog("Loaded fallback persona configuration.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen grid grid-cols-1 lg:grid-cols-2">
      
      {/* LEFT SIDE: VISITOR'S CASE FILE (Manila Paper Theme) */}
      <section className="bg-[#f4eee1] p-6 sm:p-10 lg:p-14 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-[#d4c5ab]">
        
        {/* Header Block */}
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 stamp-red-text" />
              <span className="font-semibold tracking-wider text-xs uppercase text-neutral-850">
                TRAITTRACE // INTAKE FILE
              </span>
            </div>
            <button
              onClick={initNewFile}
              className="flex items-center gap-1.5 px-3 py-1 bg-transparent hover:bg-neutral-200 border border-neutral-900 transition-all font-semibold text-xs text-neutral-900 tracking-tight"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Start a new file
            </button>
          </div>

          <div className="border-b-2 border-neutral-900 pb-4">
            <h1 className="text-3xl font-extrabold tracking-tight uppercase text-neutral-900">
              What you tell us
            </h1>
            <p className="text-xs text-neutral-600 mt-2 leading-relaxed font-sans max-w-lg">
              This panel represents a live, zero-party storefront. As you flip the preference cards below, you build a temporary profile. This storefront adapts to your choices instantly.
            </p>
          </div>
        </div>

        {/* Dynamic Store View Mockup */}
        <div className="my-10 flex flex-col gap-8">
          <StorefrontDisplay
            persona={personaData.persona}
            heroTitle={personaData.hero_title}
            heroSubtitle={personaData.hero_subtitle}
            recommendedProductId={personaData.recommended_product_id}
            isInitial={isInitial}
          />

          <StorefrontWidget
            onInteraction={handleInteraction}
            isLoading={isLoading}
          />
        </div>

      </section>

      {/* RIGHT SIDE: MARKETER'S CONTROL ROOM (Inverted Near-Black) */}
      <section className="control-room p-6 sm:p-10 lg:p-14 flex flex-col justify-between relative">
        
        {/* Header Block */}
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-center">
            <span className="font-semibold tracking-wider text-xs uppercase text-slate-500 flex items-center gap-1.5">
              <Activity className="w-4 h-4 text-slate-500 animate-pulse" />
              Telemetry / Analytics Room
            </span>
            <span className="text-[10px] font-mono text-slate-500 px-2 py-0.5 border border-slate-800 rounded bg-slate-900">
              STATE: EPHEMERAL
            </span>
          </div>

          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-3xl font-extrabold tracking-tight uppercase text-slate-100">
              What we do with it
            </h2>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed font-sans max-w-lg">
              This panel represents the marketer's control tower. Every action is mapped into a NetworkX knowledge graph. Groq translates the resulting graph paths into a structured buyer persona.
            </p>
          </div>
        </div>

        {/* Graphs and Logs */}
        <div className="my-10 flex flex-col gap-8 flex-1 justify-center">
          
          <AnalyticsDashboard
            graphData={graphData}
            sessionId={sessionId}
          />

          {/* Typewriter Printed telemetry log cards */}
          <div className="control-card p-5 flex flex-col gap-3 min-h-[200px]">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                Console Logs
              </span>
              <h3 className="text-xs font-semibold text-slate-300">
                Active Consumer Path Handshakes
              </h3>
            </div>
            
            <div className="flex-1 bg-black/50 border border-slate-900 p-4 font-mono text-[10px] leading-relaxed text-red-500 overflow-y-auto max-h-[140px] flex flex-col-reverse gap-1.5 shadow-inner">
              {logs.length === 0 ? (
                <div className="text-slate-700 italic">No entries in the active case file. Swipe index cards to generate logs.</div>
              ) : (
                logs.map((log, i) => (
                  <div key={i} className="border-b border-slate-900/40 pb-1 last:border-b-0">
                    {log}
                  </div>
                ))
              )}
            </div>
          </div>

        </div>

      </section>

    </main>
  );
}
