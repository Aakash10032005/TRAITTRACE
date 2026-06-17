"use client";

import React, { useRef, useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { GraphSnapshot } from "../lib/api";
import { GitCommit, Circle, Activity } from "lucide-react";

// Dynamically import force graph to prevent Next.js SSR build failures
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), { ssr: false });

interface AnalyticsDashboardProps {
  graphData: GraphSnapshot;
  sessionId: string;
}

// Flat ink colors matching our typewriter control board theme
const CATEGORY_COLORS = {
  user: "#b91c1c",         // Stamp red for active visitor root
  aesthetic: "#c084fc",    // Soft purple
  lifestyle: "#34d399",    // Emerald green
  pricing: "#fbbf24",      // Amber
  hobby: "#38bdf8",        // Cyan blue
  preference: "#94a3b8"    // Slate gray
};

export default function AnalyticsDashboard({ graphData, sessionId }: AnalyticsDashboardProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 450, height: 260 });

  useEffect(() => {
    if (!containerRef.current) return;
    
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth - 32,
          height: 260
        });
      }
    };

    handleResize();
    const observer = new ResizeObserver(handleResize);
    observer.observe(containerRef.current);

    return () => {
      observer.disconnect();
    };
  }, []);

  const traitNodes = graphData.nodes.filter(n => n.type === "trait");

  return (
    <div ref={containerRef} className="w-full h-full control-card p-6 flex flex-col justify-between font-mono">
      
      {/* Dashboard Metadata */}
      <div>
        <div className="flex justify-between items-center mb-1">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 stamp-red-text animate-pulse" />
            Graph compilation path
          </span>
          <span className="text-[9px] text-slate-500 border border-slate-800 px-2 py-0.5 bg-black">
            NODES={graphData.nodes.length} EDGES={graphData.links.length}
          </span>
        </div>
        <h2 className="text-lg font-bold text-slate-200 uppercase tracking-tight">Active session mapping</h2>
        <p className="text-[11px] text-slate-400 leading-relaxed font-sans mb-3 mt-1">
          This model represents consumer traits mapped directly from physical swipes. No cookies, no third-party matching.
        </p>
      </div>

      {/* Force graph Canvas */}
      <div className="w-full h-[260px] bg-black/40 border border-slate-900 overflow-hidden flex items-center justify-center relative">
        {graphData.nodes.length <= 1 ? (
          <div className="flex flex-col items-center justify-center p-6 text-center select-none z-10">
            <Circle className="w-6 h-6 text-slate-800 animate-pulse mb-2.5" />
            <p className="text-[10px] text-slate-500 font-mono">
              WAITING FOR VISITOR CARD INPUTS...
            </p>
          </div>
        ) : (
          <ForceGraph2D
            width={dimensions.width}
            height={dimensions.height}
            graphData={graphData}
            backgroundColor="transparent"
            nodeRelSize={6}
            nodeVal={(node: any) => (node.type === "user" ? 12 : 7)}
            linkWidth={(link: any) => (link.weight ? link.weight * 2.0 : 1.5)}
            linkColor={() => "#2e3137"}
            linkDirectionalArrowLength={4.0}
            linkDirectionalArrowRelPos={1}
            linkDirectionalParticles={1}
            linkDirectionalParticleSpeed={0.012}
            cooldownTicks={80}
            nodeCanvasObject={(node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
              const label = node.id;
              const isUser = node.type === "user";
              const size = isUser ? 8 : 6;
              
              // Draw outer solid border
              ctx.beginPath();
              ctx.arc(node.x, node.y, size + 1.5, 0, 2 * Math.PI, false);
              ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
              ctx.fill();

              // Draw node circle
              ctx.beginPath();
              ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
              ctx.fillStyle = isUser 
                ? CATEGORY_COLORS.user 
                : CATEGORY_COLORS[node.category as keyof typeof CATEGORY_COLORS] || CATEGORY_COLORS.preference;
              ctx.fill();

              // Border stroke
              ctx.lineWidth = 1.0;
              ctx.strokeStyle = "#ffffff";
              ctx.stroke();

              // Text labeling (IBM Plex Mono)
              const fontSize = isUser ? 4.5 : 4.0;
              ctx.font = `bold ${fontSize}px "IBM Plex Mono", monospace`;
              ctx.textAlign = "center";
              ctx.textBaseline = "middle";
              ctx.fillStyle = isUser ? "#ffffff" : "#cbd5e1";
              
              const displayText = isUser ? "Visitor" : label.toUpperCase();
              ctx.fillText(displayText, node.x, node.y + size + 4.0);
            }}
          />
        )}
      </div>

      {/* Legend layout */}
      <div className="mt-4 pt-4 border-t border-slate-900 grid grid-cols-2 gap-4 text-[10px]">
        <div>
          <div className="font-bold text-slate-500 uppercase mb-2">
            Categories index
          </div>
          <div className="flex flex-wrap gap-x-3 gap-y-1.5">
            {Object.entries(CATEGORY_COLORS).map(([cat, color]) => (
              <span key={cat} className="flex items-center gap-1 text-slate-400">
                <span className="w-2 h-2 border border-black" style={{ backgroundColor: color }} />
                {cat.toUpperCase()}
              </span>
            ))}
          </div>
        </div>

        <div>
          <div className="font-bold text-slate-500 uppercase mb-2">
            Mapped Attributes ({traitNodes.length})
          </div>
          {traitNodes.length === 0 ? (
            <div className="text-slate-650 italic">None.</div>
          ) : (
            <div className="flex flex-wrap gap-1 max-h-[44px] overflow-y-auto">
              {traitNodes.map(node => (
                <span key={node.id} className="inline-flex items-center gap-0.5 px-1 bg-black border border-slate-800 text-slate-300">
                  <GitCommit className="w-2 h-2 text-[#b91c1c]" />
                  {node.id.toUpperCase()}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
