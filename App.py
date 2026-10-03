import React, { useState } from 'react';
import { RotateCcw, Flag, MapPin, Target } from 'lucide-react';

export default function GolfShotTracker() {
  // Current Hole Metadata
  const [holeInfo] = useState({
    number: 7,
    par: 4,
    yardage: 415,
    handicap: 5,
  });

  // Shot history stack: stores GPS coordinates/pixels for each plotted shot
  const [shotHistory, setShotHistory] = useState([]);

  // Handle plotting a new shot via click/tap
  const handleMapClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const newShot = {
      id: Date.now(),
      shotNumber: shotHistory.length + 1,
      x,
      y,
    };

    setShotHistory((prev) => [...prev, newShot]);
  };

  // Undo last shot
  const handleUndo = () => {
    if (shotHistory.length === 0) return;
    setShotHistory((prev) => prev.slice(0, -1));
  };

  // Clear all shots for reset
  const handleReset = () => {
    setShotHistory([]);
  };

  return (
    <div className="flex flex-col h-screen w-full bg-slate-900 text-white font-sans select-none overflow-hidden">
      
      {/* 1. TOP HOLE INFO HUD */}
      <header className="bg-slate-800 border-b border-slate-700 px-4 py-3 shadow-lg z-10 flex items-center justify-between">
        <div className="flex items-center space-x-4 md:space-x-8">
          
          {/* Hole Number */}
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Hole</span>
            <span className="text-2xl font-black text-emerald-400">{holeInfo.number}</span>
          </div>

          {/* Par */}
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Par</span>
            <span className="text-xl font-bold text-slate-200">{holeInfo.par}</span>
          </div>

          {/* Total Yardage */}
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Yards</span>
            <span className="text-xl font-bold text-slate-100">{holeInfo.yardage}</span>
          </div>

          {/* Hole Handicap */}
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">HCP</span>
            <span className="text-xl font-bold text-amber-400">{holeInfo.handicap}</span>
          </div>
        </div>

        {/* Action Controls: Undo & Shot Counter */}
        <div className="flex items-center space-x-3">
          <div className="hidden sm:flex flex-col text-right mr-2">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Shots</span>
            <span className="text-lg font-bold text-slate-200">{shotHistory.length}</span>
          </div>

          {/* UNDO BUTTON */}
          <button
            onClick={handleUndo}
            disabled={shotHistory.length === 0}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all duration-150 ${
              shotHistory.length > 0
                ? 'bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-md active:scale-95 cursor-pointer'
                : 'bg-slate-700 text-slate-500 cursor-not-allowed opacity-50'
            }`}
            title="Undo last shot"
          >
            <RotateCcw size={16} className={shotHistory.length > 0 ? 'animate-spin-once' : ''} />
            <span>Undo</span>
          </button>
        </div>
      </header>

      {/* 2. MAP / SHOT PLOTTING AREA */}
      <main className="relative flex-1 bg-emerald-900/40 overflow-hidden cursor-crosshair">
        <div
          className="absolute inset-0 w-full h-full"
          onClick={handleMapClick}
        >
          {/* Simulated Hole Background (Replace with Map/GPS component) */}
          <div className="absolute inset-0 bg-gradient-to-b from-emerald-800 via-emerald-900 to-emerald-950 opacity-90" />
          
          {/* Green / Pin Indicator Target */}
          <div className="absolute top-12 left-1/2 -translate-x-1/2 flex flex-col items-center">
            <Flag size={28} className="text-red-500 fill-red-500 animate-bounce" />
            <span className="bg-slate-900/80 text-white text-[10px] px-2 py-0.5 rounded-full border border-slate-700">
              Pin
            </span>
          </div>

          {/* Tee Box Indicator */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center">
            <div className="w-8 h-2 bg-slate-200 rounded-full shadow-lg" />
            <span className="text-[10px] text-slate-300 font-medium mt-1">Tee Box</span>
          </div>

          {/* Plotted Shots Markers & Trajectory Lines */}
          {shotHistory.map((shot, index) => {
            const prevShot = index > 0 ? shotHistory[index - 1] : null;

            return (
              <React.Fragment key={shot.id}>
                {/* SVG Line connecting previous shot to current shot */}
                {prevShot && (
                  <svg className="absolute inset-0 w-full h-full pointer-events-none">
                    <line
                      x1={prevShot.x}
                      y1={prevShot.y}
                      x2={shot.x}
                      y2={shot.y}
                      stroke="#f59e0b"
                      strokeWidth="2"
                      strokeDasharray="4 4"
                    />
                  </svg>
                )}

                {/* Shot Location Marker */}
                <div
                  className="absolute transform -translate-x-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none"
                  style={{ left: shot.x, top: shot.y }}
                >
                  <div className="relative flex items-center justify-center">
                    <div className="w-7 h-7 bg-amber-500 rounded-full flex items-center justify-center text-slate-950 font-black text-xs shadow-lg ring-2 ring-white">
                      {shot.shotNumber}
                    </div>
                  </div>
                </div>
              </React.Fragment>
            );
          })}

          {/* Empty State Prompt */}
          {shotHistory.length === 0 && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="bg-slate-900/80 backdrop-blur border border-slate-700 px-4 py-2.5 rounded-xl flex items-center space-x-2 text-slate-300 text-sm shadow-xl">
                <Target size={18} className="text-emerald-400" />
                <span>Tap anywhere on the hole to plot Shot 1</span>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* 3. BOTTOM HUD FOOTER */}
      <footer className="bg-slate-800 border-t border-slate-700 px-4 py-2.5 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center space-x-2">
          <MapPin size={14} className="text-emerald-400" />
          <span>GPS Active</span>
        </div>

        {shotHistory.length > 0 && (
          <button
            onClick={handleReset}
            className="text-xs text-rose-400 hover:text-rose-300 underline font-medium cursor-pointer"
          >
            Reset Hole
          </button>
        )}
      </footer>

    </div>
  );
}

