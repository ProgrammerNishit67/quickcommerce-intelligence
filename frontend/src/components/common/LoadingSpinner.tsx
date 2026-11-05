import React from 'react';

export const LoadingSpinner: React.FC<{ message?: string }> = ({ message = 'Loading live analytics...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-slate-500">
      <div className="w-8 h-8 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mb-3"></div>
      <p className="text-xs font-medium text-slate-500 tracking-wide">{message}</p>
    </div>
  );
};
