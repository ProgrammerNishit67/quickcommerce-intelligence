import React, { createContext, useContext, useState, useEffect } from 'react';
import { FilterState } from '../types';
import { fetchAPI } from '../api/client';

interface FilterContextType {
  filters: FilterState;
  setFilters: React.Dispatch<React.SetStateAction<FilterState>>;
  setPreset: (preset: string) => void;
  availableStores: { store_id: string; store_name: string; city: string }[];
  availableCategories: string[];
  refreshMetadata: () => void;
}

const defaultFilters: FilterState = {
  startDate: '2026-01-01',
  endDate: '2026-03-02',
  storeId: 'all',
  category: 'all',
  preset: 'All 60 Days',
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

export const FilterProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [availableStores, setAvailableStores] = useState<{ store_id: string; store_name: string; city: string }[]>([]);
  const [availableCategories, setAvailableCategories] = useState<string[]>([]);

  const fetchMeta = async () => {
    try {
      const data = await fetchAPI<{
        stores: { store_id: string; store_name: string; city: string }[];
        categories: string[];
      }>('/metadata/filters');
      setAvailableStores(data.stores || []);
      setAvailableCategories(data.categories || []);
    } catch (err) {
      console.error('Failed to load filter metadata', err);
    }
  };

  useEffect(() => {
    fetchMeta();
  }, []);

  const setPreset = (preset: string) => {
    // Current simulated baseline anchor: 2026-03-02
    if (preset === 'Last 7 Days') {
      setFilters(prev => ({ ...prev, preset, startDate: '2026-02-23', endDate: '2026-03-02' }));
    } else if (preset === 'Last 14 Days') {
      setFilters(prev => ({ ...prev, preset, startDate: '2026-02-16', endDate: '2026-03-02' }));
    } else if (preset === 'Last 30 Days') {
      setFilters(prev => ({ ...prev, preset, startDate: '2026-01-31', endDate: '2026-03-02' }));
    } else {
      setFilters(prev => ({ ...prev, preset: 'All 60 Days', startDate: '2026-01-01', endDate: '2026-03-02' }));
    }
  };

  return (
    <FilterContext.Provider value={{
      filters,
      setFilters,
      setPreset,
      availableStores,
      availableCategories,
      refreshMetadata: fetchMeta
    }}>
      {children}
    </FilterContext.Provider>
  );
};

export const useFilters = () => {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error('useFilters must be used within a FilterProvider');
  }
  return context;
};
