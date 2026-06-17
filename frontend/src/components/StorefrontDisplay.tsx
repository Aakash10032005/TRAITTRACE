"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { ShoppingCart } from "lucide-react";

interface StorefrontDisplayProps {
  persona: string;
  heroTitle: string;
  heroSubtitle: string;
  recommendedProductId: string;
  isInitial: boolean;
}

interface ProductDetails {
  id: string;
  name: string;
  price: string;
  description: string;
  tags: string[];
  specs: string[];
}

const PRODUCTS_MOCK: Record<string, ProductDetails> = {
  "prod_premium_minimal": {
    id: "prod_premium_minimal",
    name: "Monolith Slate Desk Organizer",
    price: "₹15,900.00",
    description: "Architectural grade desk tray milled from a single block of steel-anodized alloy. Zero distraction, pure alignment.",
    tags: ["Minimalist", "Premium", "Anodized"],
    specs: ["Milled metal block", "Magnetic guide paths", "Antistatic base pads"]
  },
  "prod_classic_standard": {
    id: "prod_classic_standard",
    name: "The Core Hybrid Chronograph",
    price: "₹20,900.00",
    description: "Classic design meeting modern telemetry alerts. Titanium housing with a tanned hide band and scratch-proof crystal.",
    tags: ["Classic", "Telemetry", "Standard"],
    specs: ["Japanese quartz core", "Genuine hide strap", "Waterproof to 5 ATM"]
  },
  "prod_budget_classic": {
    id: "prod_budget_classic",
    name: "Modular Eco-Canvas Commuter Pack",
    price: "₹7,500.00",
    description: "Sturdy daily utility pack constructed from 100% post-consumer recycled nylon. Optimized storage configurations.",
    tags: ["Recycled", "Utility", "Value"],
    specs: ["Post-consumer canvas", "15-inch storage sleeve", "Weatherproof bindings"]
  },
  "prod_outdoor_rugged": {
    id: "prod_outdoor_rugged",
    name: "Apex Solar Exploration Compass",
    price: "₹24,900.00",
    description: "Tough tracking compass with built-in solar battery extension, altimeter, barometer, and custom composite casing.",
    tags: ["Exploration", "Solar", "Rugged"],
    specs: ["Solar power collector", "IP68 dust protection", "Integrated GPS dials"]
  },
  "prod_tech_enthusiast": {
    id: "prod_tech_enthusiast",
    name: "AeroKey Custom Gasket Keyboard",
    price: "₹29,500.00",
    description: "Pro-grade mechanical keyboard featuring custom linear switches, hot-swappable PCB sockets, and gasket-mount sound isolation.",
    tags: ["Custom", "Mechanical", "Hot-Swap"],
    specs: ["Polycarbonate board base", "Gold-plated solder plates", "Custom mapping firmware"]
  }
};

export default function StorefrontDisplay({
  persona,
  heroTitle,
  heroSubtitle,
  recommendedProductId,
  isInitial
}: StorefrontDisplayProps) {
  // Resolve product or fallback to default
  let activeProduct = PRODUCTS_MOCK[recommendedProductId];
  
  if (!activeProduct) {
    const matchedKey = Object.keys(PRODUCTS_MOCK).find(key => 
      recommendedProductId.toLowerCase().includes(key.substring(5)) ||
      key.toLowerCase().includes(recommendedProductId.toLowerCase())
    );
    activeProduct = matchedKey ? PRODUCTS_MOCK[matchedKey] : PRODUCTS_MOCK["prod_classic_standard"];
  }

  return (
    <div className="w-full bg-[#fdfbf7] border-2 border-neutral-900 rounded-none overflow-hidden relative shadow-none">
      
      {/* Mock Store Header */}
      <div className="border-b border-neutral-900 bg-neutral-100 px-6 py-4 flex justify-between items-center z-10">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded-none bg-neutral-900 flex items-center justify-center font-bold text-white text-[10px] font-mono">
            E
          </div>
          <span className="font-bold tracking-tight text-neutral-900 text-xs font-mono uppercase">
            EPSILON CATALOGUE
          </span>
        </div>
        <div className="flex gap-4 text-[11px] font-mono text-neutral-500">
          <span className="hover:underline cursor-pointer">SHOP</span>
          <span className="hover:underline cursor-pointer">ARCHIVE</span>
          <span className="stamp-red-text font-bold">● ACTIVE INTAKE</span>
        </div>
      </div>

      {/* Main Dynamic Viewport */}
      <div className="p-6 md:p-8 flex flex-col justify-center min-h-[360px] z-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={persona + heroTitle}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="flex flex-col gap-6"
          >
            {/* Dynamic Persona Tracker Badge */}
            <div className="self-start">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 bg-transparent text-[11px] font-bold font-mono transition-all duration-350 border ${
                isInitial 
                  ? "text-neutral-500 border-neutral-400" 
                  : "stamp-red-text border-[#b91c1c] bg-[#b91c1c]/5"
              }`}>
                {isInitial ? "DETECTOR PATH: PENDING SWIPES" : `DETECTOR PATH: ${persona.toUpperCase()}`}
              </span>
            </div>

            {/* Dynamic Copywriting */}
            <div>
              <h1 className={`text-2xl font-bold tracking-tight uppercase font-mono leading-tight transition-colors duration-300 ${
                isInitial ? "text-neutral-900" : "stamp-red-text"
              }`}>
                {heroTitle}
              </h1>
              <p className="text-xs text-neutral-600 max-w-lg mt-2 leading-relaxed font-sans">
                {heroSubtitle}
              </p>
            </div>

            {/* Recommended Product Clip-Out */}
            <div className="mt-2">
              <div className="text-[10px] font-bold text-neutral-500 font-mono uppercase tracking-wider mb-2">
                ACTIVE RECOMMENDATION CARD
              </div>
              
              <div className={`border-2 p-4 flex flex-col md:flex-row gap-4 items-stretch relative transition-all duration-350 ${
                isInitial 
                  ? "border-neutral-900 bg-[#faf7f0]" 
                  : "border-[#b91c1c] bg-[#fffcf8] shadow-[4px_4px_0px_rgba(185,28,28,0.15)]"
              }`}>
                
                {/* Visual indicator stamp overlay — floats top-right, clear of price */}
                {!isInitial && (
                  <span className="absolute top-2 right-2 text-[8px] font-bold font-mono tracking-widest bg-[#b91c1c] text-white px-2 py-0.5 uppercase z-20">
                    ★ TAILORED RE-ROUTE SUCCESSFUL
                  </span>
                )}

                {/* Product Image Box */}
                <div className="w-24 h-24 border border-dashed border-neutral-400 bg-neutral-50 flex items-center justify-center flex-shrink-0 relative overflow-hidden">
                  <Image
                    src="/watch-chronograph.png"
                    alt="The Core Hybrid Chronograph"
                    width={88}
                    height={88}
                    className="object-contain w-full h-full p-1"
                  />
                  <span className="absolute bottom-1 right-1 px-1 rounded text-[7px] bg-neutral-900 text-white font-mono">
                    {activeProduct.id.replace("prod_", "")}
                  </span>
                </div>

                {/* Product Specs */}
                <div className="flex-1 flex flex-col justify-between gap-2">
                  <div>
                    {/* Push name+price below the stamp badge height (stamp is ~22px tall at top-2) */}
                    <div className={`flex justify-between items-start ${!isInitial ? "pt-6" : ""}`}>
                      <h3 className="font-bold text-neutral-900 text-sm font-mono leading-tight uppercase">
                        {activeProduct.name}
                      </h3>
                      <span className="text-sm font-extrabold text-neutral-900 font-mono whitespace-nowrap ml-2">
                        {activeProduct.price}
                      </span>
                    </div>
                    
                    <p className="text-[11px] text-neutral-600 mt-1 line-clamp-2 leading-normal">
                      {activeProduct.description}
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-1 mt-1">
                    {activeProduct.tags.map(t => (
                      <span key={t} className="text-[9px] font-mono border border-neutral-300 px-1.5 py-0.5 bg-white text-neutral-600 uppercase">
                        {t}
                      </span>
                    ))}
                  </div>

                  {/* Buy Button */}
                  <button className={`w-full mt-2 py-1.5 border transition-all font-bold text-[10px] text-white font-mono uppercase flex items-center justify-center gap-1 ${
                    isInitial 
                      ? "border-neutral-900 bg-neutral-900 hover:bg-neutral-800"
                      : "border-[#b91c1c] bg-[#b91c1c] hover:bg-[#991b1b]"
                  }`}>
                    <ShoppingCart className="w-3.5 h-3.5" />
                    Place Order
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* GDPR Footer */}
      <div className="border-t border-neutral-200 bg-neutral-50 px-6 py-3.5 flex flex-col sm:flex-row justify-between gap-2 items-center text-[9px] text-neutral-500 font-mono">
        <div className="flex gap-4">
          <span className="flex items-center gap-1 font-bold text-neutral-600">
            [+] EXPLICIT CONSENT
          </span>
          <span className="flex items-center gap-1">
            [+] COOKIE-FREE FILE
          </span>
        </div>
        <div>
          TRAITTRACE SYSTEM v1.0
        </div>
      </div>
    </div>
  );
}
