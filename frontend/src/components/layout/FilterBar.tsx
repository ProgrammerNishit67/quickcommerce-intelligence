import React from 'react';
import { useFilters } from '../../context/FilterContext';
import { Calendar, Store, RotateCcw } from 'lucide-react';

export const FilterBar: React.FC = () => {
  const { filters, setFilters, setPreset, availableStores } = useFilters();

  const presets = ['Last 7 Days', 'Last 14 Days', 'Last 30 Days', 'All 60 Days'];

  const handleReset = () => {
    setPreset('All 60 Days');
    setFilters(prev => ({
      ...prev,
      storeId: 'all',
      category: 'all',
    }));
  };

  return (
    <div className="bg-white border-b border-slate-200 px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      <div className="flex flex-wrap items-center gap-3">
        {/* Preset Buttons */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-medium">
          {presets.map(p => (
            <button
              key={p}
              onClick={() => setPreset(p)}
              className={`px-3 py-1 rounded-md transition-all ${
                filters.preset === p
                  ? 'bg-white text-slate-900 shadow-sm font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {p}
            </button>
          ))}
        </div>

        {/* Date Inputs */}
        <div className="flex items-center gap-2 bg-slate-50 px-3 py-1 rounded-lg border border-slate-200 text-xs text-slate-700">
          <Calendar className="w-3.5 h-3.5 text-slate-400" />
          <input
            type="date"
            value={filters.startDate}
            onChange={e => setFilters(prev => ({ ...prev, startDate: e.target.value, preset: 'Custom' }))}
            className="bg-transparent border-none text-xs focus:outline-none text-slate-800"
          />
          <span className="text-slate-400">to</span>
          <input
            type="date"
            value={filters.endDate}
            onChange={e => setFilters(prev => ({ ...prev, endDate: e.target.value, preset: 'Custom' }))}
            className="bg-transparent border-none text-xs focus:outline-none text-slate-800"
          />
        </div>

        {/* Store Selector */}
        <div className="flex items-center gap-2 bg-slate-50 px-3 py-1 rounded-lg border border-slate-200 text-xs text-slate-700">
          <Store className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={filters.storeId}
            onChange={e => setFilters(prev => ({ ...prev, storeId: e.target.value }))}
            className="bg-transparent border-none text-xs text-slate-800 focus:outline-none cursor-pointer pr-2"
          >
            <option value="all">All Dark Stores ({availableStores.length} Hubs)</option>
            {availableStores.map(s => (
              <option key={s.store_id} value={s.store_id}>
                {s.city} - {s.store_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Reset */}
      <button
        onClick={handleReset}
        className="flex items-center gap-1.5 px-3 py-1 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors border border-transparent hover:border-slate-200"
      >
        <RotateCcw className="w-3.5 h-3.5 text-slate-400" />
        <span>Reset Filters</span>
      </button>
    </div>
  );
};
