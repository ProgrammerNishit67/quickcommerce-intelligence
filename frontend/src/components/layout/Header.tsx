import React from 'react';
import { Clock, ShieldCheck, Activity } from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle: string;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle }) => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between shrink-0">
      <div>
        <h2 className="text-base font-bold text-slate-900 tracking-tight">{title}</h2>
        <p className="text-xs text-slate-500 font-medium">{subtitle}</p>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-50 border border-slate-200 text-xs text-slate-600">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>Promised SLA: <strong className="text-slate-900">15 Mins</strong></span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800">
          <Activity className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
          <span>Real-Time Fleet Active</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs text-slate-700">
          <ShieldCheck className="w-3.5 h-3.5 text-slate-600" />
          <span>Blinkit / Zepto Spec</span>
        </div>
      </div>
    </header>
  );
};
