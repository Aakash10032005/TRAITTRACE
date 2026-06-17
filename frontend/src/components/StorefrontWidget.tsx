"use client";

import React, { useState } from "react";
import { motion, AnimatePresence, useMotionValue, useTransform } from "framer-motion";
import { ChevronLeft, ChevronRight, RefreshCw, AlertCircle, ShoppingBag, ExternalLink, X } from "lucide-react";

interface StorefrontWidgetProps {
  onInteraction: (value: string, type: string) => void;
  isLoading: boolean;
}

const TRAIT_DECKS = [
  {
    id: "aesthetic",
    category: "01 // AESTHETIC",
    question: "Design your storefront visual identity:",
    leftLabel: "Minimalist",
    rightLabel: "Bold & Vibrant",
    leftDesc: "Sleek typography, structured grids, clean whitespace.",
    rightDesc: "High contrast colors, expressive layouts, dynamic motion.",
  },
  {
    id: "lifestyle",
    category: "02 // VALUE ALIGNMENT",
    question: "Select your primary spending priority:",
    leftLabel: "Eco-Friendly",
    rightLabel: "Luxe & Premium",
    leftDesc: "Ethically sourced materials, low impact carbon grids.",
    rightDesc: "Exceptional craftsmanship, limited editions, status-defining quality.",
  },
  {
    id: "pricing",
    category: "03 // TRANSACTION COMFORT",
    question: "Indicate your target budget segment:",
    leftLabel: "Budget",
    rightLabel: "Premium",
    leftDesc: "Cost efficiency, utility focus, essential components.",
    rightDesc: "Top-tier specifications, premium warranty, elite engineering.",
  },
  {
    id: "hobby",
    category: "04 // WEEKEND ENVIRONMENT",
    question: "Define your primary active habitat:",
    leftLabel: "Active Outdoor",
    rightLabel: "Tech Enthusiast",
    leftDesc: "Wilderness exploration, off-grid adventure, rugged gear sets.",
    rightDesc: "Algorithmic code labs, high refresh setups, custom mechanics.",
  }
];

// Subwatch option configurations based on zero-party traits selection
interface WatchOffer {
  name: string;
  price: string;
  category: string;
  description: string;
  bulletSpecs: string[];
  amazonLink: string;
  flipkartLink: string;
  googleLink: string;
}

const WATCH_OFFERS: Record<string, WatchOffer> = {
  "premium_outdoor": {
    name: "Garmin Fenix 7 Pro Sapphire Solar",
    price: "₹84,900.00",
    category: "Elite Rugged Sport",
    description: "Multi-sport solar tracker featuring scratch-resistant sapphire lenses, tactical mapping, and military durable composite construction.",
    bulletSpecs: ["Solar charged battery extension", "IP68 water resistant to 100m", "Sapphire crystal dome case"],
    amazonLink: "https://www.amazon.in/s?k=Garmin+Fenix+7+Pro+Sapphire+Solar",
    flipkartLink: "https://www.flipkart.com/search?q=Garmin+Fenix+7+Pro+Sapphire+Solar",
    googleLink: "https://www.google.com/search?tbm=shop&q=Garmin+Fenix+7+Pro+Sapphire+Solar"
  },
  "premium_tech": {
    name: "Samsung Galaxy Watch 6 Classic LTE",
    price: "₹42,900.00",
    category: "Premium Smart Companion",
    description: "Stainless steel smart wearable with rotating bezel ring, body impedance analysis sensors, and cellular LTE link.",
    bulletSpecs: ["Rotating mechanical dial ring", "BIA body structure analyzer", "Always-on sapphire OLED"],
    amazonLink: "https://www.amazon.in/s?k=Samsung+Galaxy+Watch+6+Classic+LTE",
    flipkartLink: "https://www.flipkart.com/search?q=Samsung+Galaxy+Watch+6+Classic+LTE",
    googleLink: "https://www.google.com/search?tbm=shop&q=Samsung+Galaxy+Watch+6+Classic+LTE"
  },
  "budget_outdoor": {
    name: "Amazfit T-Rex 2 Rugged GPS",
    price: "₹15,999.00",
    category: "Tactical Value Tracker",
    description: "Rugged high-utility sports tracker with dual-band GPS, 24-day battery charge lifespan, and extreme temperature operations.",
    bulletSpecs: ["Dual-band GPS route logging", "24-day battery charge span", "15 military grade certifications"],
    amazonLink: "https://www.amazon.in/s?k=Amazfit+T-Rex+2+Rugged",
    flipkartLink: "https://www.flipkart.com/search?q=Amazfit+T-Rex+2+Rugged",
    googleLink: "https://www.google.com/search?tbm=shop&q=Amazfit+T-Rex+2+Rugged"
  },
  "budget_tech": {
    name: "OnePlus Watch 2R Smartwatch",
    price: "₹17,999.00",
    category: "Performance Value Companion",
    description: "Google WearOS watch featuring dual-engine processor core, high resolution AMOLED screen, and fast wrap warp charge.",
    bulletSpecs: ["Google WearOS ecosystem", "Dual-engine battery optimizer", "Fast warp charge capabilities"],
    amazonLink: "https://www.amazon.in/s?k=OnePlus+Watch+2R",
    flipkartLink: "https://www.flipkart.com/search?q=OnePlus+Watch+2R",
    googleLink: "https://www.google.com/search?tbm=shop&q=OnePlus+Watch+2R"
  }
};

// ISOLATED COMPONENT: SwipeCard
// This encapsulates drag motion values to resolve stale bindings on cards 2-4
interface SwipeCardProps {
  card: typeof TRAIT_DECKS[0];
  onSwipe: (direction: "left" | "right") => void;
  isLoading: boolean;
}

function SwipeCard({ card, onSwipe, isLoading }: SwipeCardProps) {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-180, 180], [-10, 10]);
  const opacity = useTransform(x, [-180, -120, 0, 120, 180], [0.55, 1, 1, 1, 0.55]);
  const leftIndicatorOpacity = useTransform(x, [-110, -25], [1, 0]);
  const rightIndicatorOpacity = useTransform(x, [25, 110], [0, 1]);

  return (
    <motion.div
      style={{ x, rotate, opacity }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.6}
      onDragEnd={(_, info) => {
        if (info.offset.x < -80) {
          onSwipe("left");
        } else if (info.offset.x > 80) {
          onSwipe("right");
        }
      }}
      className="absolute w-full h-full rounded-none manila-card border-2 border-neutral-900 p-6 flex flex-col justify-between shadow-none cursor-grab active:cursor-grabbing overflow-hidden bg-[#faf7f0] z-10"
      exit={{
        y: 30,
        opacity: 0,
        transition: { duration: 0.2 }
      }}
    >
      {/* Swipe indicators overlay */}
      <motion.div 
        style={{ opacity: leftIndicatorOpacity }}
        className="absolute inset-0 bg-[#b91c1c]/5 border-l-8 border-[#b91c1c]/40 pointer-events-none"
      />
      <motion.div 
        style={{ opacity: rightIndicatorOpacity }}
        className="absolute inset-0 bg-neutral-900/5 border-r-8 border-neutral-900/40 pointer-events-none"
      />

      {/* Card category tab */}
      <div className="flex justify-between items-start">
        <span className="text-[10px] font-bold tracking-wider uppercase border border-neutral-900 px-2 py-0.5 bg-neutral-900 text-white font-mono">
          {card.category}
        </span>
        {isLoading && (
          <div className="flex items-center gap-1 text-[10px] font-bold uppercase font-mono stamp-red-text animate-pulse">
            <AlertCircle className="w-3 h-3" />
            SYNCHRONIZING...
          </div>
        )}
      </div>

      {/* Main Question block */}
      <div className="my-auto py-2">
        <h4 className="text-sm font-semibold text-neutral-850 font-mono tracking-tight leading-snug mb-3">
          {card.question}
        </h4>
        <div className="flex justify-between gap-4 mt-4 text-center select-none font-mono">
          <div className="flex-1 flex flex-col items-center border border-neutral-900 bg-neutral-100 p-2.5">
            <ChevronLeft className="w-4 h-4 text-neutral-700 mb-0.5" />
            <span className="text-xs font-bold text-neutral-900">{card.leftLabel}</span>
          </div>
          <div className="flex-1 flex flex-col items-center border border-neutral-900 bg-neutral-100 p-2.5">
            <ChevronRight className="w-4 h-4 text-neutral-700 mb-0.5" />
            <span className="text-xs font-bold text-neutral-900">{card.rightLabel}</span>
          </div>
        </div>
      </div>

      {/* Choice summaries footer */}
      <div className="border-t border-neutral-300 pt-3 flex gap-4 text-[10px] text-neutral-600 font-sans leading-relaxed">
        <div className="flex-1 text-left">
          <span className="font-bold font-mono text-neutral-800 block mb-0.5">← SWIPE LEFT</span>
          {card.leftDesc}
        </div>
        <div className="flex-1 text-right">
          <span className="font-bold font-mono text-neutral-800 block mb-0.5">SWIPE RIGHT →</span>
          {card.rightDesc}
        </div>
      </div>
    </motion.div>
  );
}

export default function StorefrontWidget({ onInteraction, isLoading }: StorefrontWidgetProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [choices, setChoices] = useState<string[]>([]);
  const [showModal, setShowModal] = useState(false);

  const activeCard = TRAIT_DECKS[currentIndex];

  const handleSwipe = (direction: "left" | "right") => {
    if (!activeCard || isLoading) return;

    const selectedValue = direction === "left" ? activeCard.leftLabel : activeCard.rightLabel;
    
    // Save selections local state to calculate smartwatch segment
    setChoices(prev => [...prev, selectedValue]);
    onInteraction(selectedValue, "swipe");

    setCurrentIndex((prev) => prev + 1);
  };

  const handleReset = () => {
    setCurrentIndex(0);
    setChoices([]);
    setShowModal(false);
  };

  // Determine smartwatch offer based on choices
  const getWatchRecommendation = (): WatchOffer => {
    const isPremium = choices.includes("Premium") || choices.includes("Luxe & Premium");
    const isOutdoor = choices.includes("Active Outdoor");

    if (isPremium) {
      return isOutdoor ? WATCH_OFFERS.premium_outdoor : WATCH_OFFERS.premium_tech;
    } else {
      return isOutdoor ? WATCH_OFFERS.budget_outdoor : WATCH_OFFERS.budget_tech;
    }
  };

  const recommendedWatch = getWatchRecommendation();

  return (
    <div className="flex flex-col w-full max-w-md mx-auto h-[460px] font-sans">
      
      {/* Widget Header progress count */}
      <div className="w-full flex justify-between items-center mb-3">
        <div>
          <span className="text-[10px] font-bold tracking-wider uppercase text-neutral-500">
            Consumer Profile Card Deck
          </span>
          <h3 className="text-xs font-semibold text-neutral-700 uppercase tracking-tight font-mono mt-0.5">
            Card {Math.min(currentIndex + 1, TRAIT_DECKS.length)} of {TRAIT_DECKS.length}
          </h3>
        </div>
        <button
          onClick={handleReset}
          className="flex items-center gap-1.5 px-3 py-1 bg-transparent hover:bg-neutral-200 border border-neutral-900 transition-all text-[11px] font-semibold text-neutral-900 tracking-tight"
        >
          <RefreshCw className="w-3 h-3" />
          Reset File Deck
        </button>
      </div>

      {/* Card Swipe Canvas wrapper */}
      <div className="relative w-full h-[340px] flex items-center justify-center select-none">
        <AnimatePresence mode="wait">
          {activeCard ? (
            <SwipeCard
              key={activeCard.id}
              card={activeCard}
              onSwipe={handleSwipe}
              isLoading={isLoading}
            />
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="w-full h-full rounded-none manila-card border-2 border-neutral-900 p-8 flex flex-col items-center justify-center text-center bg-[#faf7f0]"
            >
              <div className="w-12 h-12 border-2 border-dashed border-[#b91c1c] flex items-center justify-center mb-4">
                <FileTextIcon />
              </div>
              <h3 className="text-lg font-bold text-neutral-900 font-mono uppercase tracking-tight">FILE SYNTHESIZED</h3>
              <p className="text-xs text-neutral-600 font-sans max-w-xs mt-2 leading-relaxed">
                Your zero-party choices have been fully processed and synced with the active profile graph.
              </p>
              
              <div className="flex flex-col gap-2 mt-6 w-full max-w-[200px]">
                <button
                  onClick={() => setShowModal(true)}
                  className="w-full py-2 bg-[#b91c1c] hover:bg-[#991b1b] text-white text-xs font-bold uppercase font-mono border-2 border-neutral-900 tracking-wider flex items-center justify-center gap-1.5"
                >
                  <ShoppingBag className="w-3.5 h-3.5" />
                  View Smartwatches
                </button>
                <button
                  onClick={handleReset}
                  className="w-full py-2 border border-neutral-900 hover:bg-neutral-200 bg-transparent text-xs font-bold uppercase text-neutral-900 font-mono transition-all"
                >
                  Reset Cards Deck
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Manual Button Fallbacks */}
      {activeCard && (
        <div className="flex gap-4 mt-3 w-full font-mono">
          <button
            onClick={() => handleSwipe("left")}
            disabled={isLoading}
            className="flex-1 py-2 border border-neutral-900 hover:bg-neutral-200 transition-all font-bold text-xs text-neutral-900 flex items-center justify-center gap-1"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            CHOOSE {activeCard.leftLabel.toUpperCase()}
          </button>
          <button
            onClick={() => handleSwipe("right")}
            disabled={isLoading}
            className="flex-1 py-2 border border-neutral-900 hover:bg-neutral-200 transition-all font-bold text-xs text-neutral-900 flex items-center justify-center gap-1"
          >
            CHOOSE {activeCard.rightLabel.toUpperCase()}
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* OVERLAY POPUP MODAL: Smartwatch Marketplace Offers */}
      <AnimatePresence>
        {showModal && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-[999]">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="w-full max-w-lg manila-card border-2 border-neutral-900 rounded-none bg-[#fdfbf7] p-6 font-mono text-neutral-900 shadow-2xl relative"
            >
              {/* Close Button */}
              <button
                onClick={() => setShowModal(false)}
                className="absolute top-4 right-4 text-neutral-500 hover:text-neutral-900 border border-neutral-900 p-1 bg-[#faf7f0] transition-all"
              >
                <X className="w-4 h-4" />
              </button>

              <div className="flex items-center gap-2 mb-3 border-b border-neutral-300 pb-3">
                <ShoppingBag className="w-5 h-5 stamp-red-text" />
                <h3 className="font-extrabold text-sm uppercase tracking-wider text-neutral-800">
                  Tailored Marketplace offers
                </h3>
              </div>

              {/* Dynamic recommendation details */}
              <div className="flex flex-col gap-4">
                <div>
                  <span className="text-[10px] font-bold bg-[#b91c1c] text-white px-2 py-0.5 uppercase">
                    Profile Category Match: {recommendedWatch.category}
                  </span>
                  <h2 className="text-lg font-black text-neutral-900 mt-2 tracking-tight">
                    {recommendedWatch.name}
                  </h2>
                  <div className="text-md font-extrabold stamp-red-text mt-0.5">
                    {recommendedWatch.price}
                  </div>
                </div>

                <p className="text-xs text-neutral-600 font-sans leading-relaxed">
                  {recommendedWatch.description}
                </p>

                {/* Specs Clipout */}
                <div className="bg-[#faf7f0] border border-neutral-300 p-3">
                  <span className="text-[9px] font-bold text-neutral-400 block uppercase tracking-wider mb-1.5">
                    Hardware spec checklist
                  </span>
                  <ul className="text-[10px] text-neutral-700 flex flex-col gap-1.5 list-disc pl-4 font-sans">
                    {recommendedWatch.bulletSpecs.map((s, idx) => (
                      <li key={idx} className="leading-tight">{s}</li>
                    ))}
                  </ul>
                </div>

                {/* Purchase links with icons */}
                <div className="mt-2 border-t border-neutral-300 pt-4">
                  <span className="text-[9px] font-bold text-neutral-400 block uppercase tracking-wider mb-2">
                    Purchase on local marketplaces
                  </span>
                  
                  <div className="flex flex-col sm:flex-row gap-3">
                    <a
                      href={recommendedWatch.amazonLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 py-2 border border-neutral-900 bg-[#faf7f0] hover:bg-neutral-200 transition-all font-bold text-[10px] uppercase text-neutral-900 text-center flex items-center justify-center gap-1"
                    >
                      Amazon.in
                      <ExternalLink className="w-3 h-3 text-neutral-600" />
                    </a>
                    <a
                      href={recommendedWatch.flipkartLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 py-2 border border-neutral-900 bg-[#faf7f0] hover:bg-neutral-200 transition-all font-bold text-[10px] uppercase text-neutral-900 text-center flex items-center justify-center gap-1"
                    >
                      Flipkart
                      <ExternalLink className="w-3 h-3 text-neutral-600" />
                    </a>
                    <a
                      href={recommendedWatch.googleLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 py-2 border border-neutral-900 bg-[#faf7f0] hover:bg-neutral-200 transition-all font-bold text-[10px] uppercase text-neutral-900 text-center flex items-center justify-center gap-1"
                    >
                      Google Shop
                      <ExternalLink className="w-3 h-3 text-neutral-600" />
                    </a>
                  </div>
                </div>

              </div>

            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  );
}

function FileTextIcon() {
  return (
    <svg className="w-6 h-6 text-[#b91c1c]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"></path>
    </svg>
  );
}
