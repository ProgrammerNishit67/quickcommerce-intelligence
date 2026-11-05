import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badge?: string;
  badgeType?: 'success' | 'danger' | 'warning' | 'neutral';
  tooltip?: string;
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  badgeType = 'neutral',
  tooltip
}) => {
  const badgeStyles = {
    success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    danger: 'bg-rose-50 text-rose-700 border-rose-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    neutral: 'bg-slate-100 text-slate-700 border-slate-200'
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider" title={tooltip}>
          {title}
        </p>
        <div className="p-2 rounded-lg bg-slate-50 text-slate-700 border border-slate-100 group-hover:bg-slate-100 transition-colors">
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline gap-2">
        <h3 className="text-2xl font-bold text-slate-900 tracking-tight">{value}</h3>
        {badge && (
          <span className={`text-xs px-2 py-0.5 rounded-md font-medium border ${badgeStyles[badgeType]}`}>
            {badge}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-1.5 text-xs text-slate-500 font-medium">
          {subtitle}
        </p>
      )}
    </div>
  );
};
