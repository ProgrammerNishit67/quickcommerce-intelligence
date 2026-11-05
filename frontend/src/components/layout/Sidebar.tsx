import React from 'react';
import {
  LayoutDashboard,
  Truck,
  Boxes,
  TrendingUp,
  AlertCircle,
  Store,
  BellRing,
  Lightbulb,
  Database,
  FileSpreadsheet,
  Zap
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  alertCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, alertCount = 0 }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'delivery', label: 'Delivery Analytics', icon: Truck },
    { id: 'inventory', label: 'Inventory Intelligence', icon: Boxes },
    { id: 'revenue', label: 'Revenue Analytics', icon: TrendingUp },
    { id: 'order-quality', label: 'Order Quality', icon: AlertCircle },
    { id: 'store-performance', label: 'Store Performance', icon: Store },
    { id: 'alerts', label: 'Operational Alerts', icon: BellRing, badge: alertCount },
    { id: 'insights', label: 'Business Insights', icon: Lightbulb },
    { id: 'data-management', label: 'Data Management', icon: Database },
    { id: 'reports', label: 'Reports', icon: FileSpreadsheet },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 border-r border-slate-800 select-none">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 gap-3 border-b border-slate-800/80 bg-slate-950/40">
        <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-950 shadow-md shadow-emerald-500/20">
          <Zap className="w-5 h-5 fill-current" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-white tracking-tight leading-none">
            QuickCommerce
          </h1>
          <span className="text-[10px] font-medium text-emerald-400 tracking-wider uppercase">
            Intelligence OS
          </span>
        </div>
      </div>

      {/* Nav Menu */}
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold tracking-wider text-slate-500 uppercase">
          Analytics & Operations
        </div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && item.badge > 0 && (
                <span className="px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500 text-white animate-pulse">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer System Status */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/20 text-xs">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[11px] text-slate-400">Database Engine</span>
          <span className="inline-flex items-center gap-1.5 text-[10px] font-medium text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            PostgreSQL / SQLite Live
          </span>
        </div>
        <p className="text-[10px] text-slate-500">
          Dark Store Catchment: 10 Hubs Active
        </p>
      </div>
    </aside>
  );
};
