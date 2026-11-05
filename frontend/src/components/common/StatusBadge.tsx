import React from 'react';

interface StatusBadgeProps {
  status: string;
  variant?: 'status' | 'severity' | 'tier';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, variant = 'status' }) => {
  const normalized = status.toUpperCase().replace(/\s+/g, '_');

  let style = 'bg-slate-100 text-slate-700 border-slate-200';

  if (variant === 'severity') {
    if (normalized.includes('CRITICAL')) {
      style = 'bg-rose-50 text-rose-700 border-rose-200 font-semibold';
    } else if (normalized.includes('WARNING')) {
      style = 'bg-amber-50 text-amber-700 border-amber-200 font-semibold';
    } else {
      style = 'bg-blue-50 text-blue-700 border-blue-200';
    }
  } else {
    if (['DELIVERED', 'ACTIVE', 'HEALTHY', 'STAR_RIDER', 'HIGH_VELOCITY'].some(k => normalized.includes(k))) {
      style = 'bg-emerald-50 text-emerald-700 border-emerald-200';
    } else if (['CANCELLED', 'OUT_OF_STOCK', 'CRITICAL', 'BREACH', 'SEVERE'].some(k => normalized.includes(k))) {
      style = 'bg-rose-50 text-rose-700 border-rose-200';
    } else if (['REORDER', 'DELAY', 'LOW_STOCK', 'WARNING'].some(k => normalized.includes(k))) {
      style = 'bg-amber-50 text-amber-700 border-amber-200';
    }
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${style}`}>
      {status}
    </span>
  );
};
