import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { StorePerformanceRanking } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import { Store, Trophy, Target, Gauge } from 'lucide-react';

export const StorePerformancePage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<StorePerformanceRanking[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<StorePerformanceRanking[]>('/store-performance', {
      start_date: filters.startDate,
      end_date: filters.endDate,
    })
      .then(res => setData(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters.startDate, filters.endDate]);

  if (loading) return <LoadingSpinner message="Benchmarking dark store composite scorecard & national rankings..." />;

  const columns: Column<StorePerformanceRanking>[] = [
    {
      header: 'Rank',
      accessor: r => (
        <div className="flex items-center gap-1.5 font-bold">
          {r.national_rank === 1 ? (
            <span className="w-6 h-6 rounded-full bg-amber-400 text-slate-950 flex items-center justify-center text-xs shadow-sm">
              🥇
            </span>
          ) : r.national_rank === 2 ? (
            <span className="w-6 h-6 rounded-full bg-slate-300 text-slate-900 flex items-center justify-center text-xs">
              🥈
            </span>
          ) : r.national_rank === 3 ? (
            <span className="w-6 h-6 rounded-full bg-amber-700 text-white flex items-center justify-center text-xs">
              🥉
            </span>
          ) : (
            <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs">
              #{r.national_rank}
            </span>
          )}
        </div>
      ),
      sortKey: 'national_rank',
      align: 'center'
    },
    {
      header: 'Dark Store Facility',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.store_name}</p>
          <p className="text-[11px] text-slate-400">{r.locality}, {r.city}</p>
        </div>
      ),
      sortKey: 'store_name'
    },
    {
      header: 'Scorecard',
      accessor: r => (
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900 text-white font-mono font-bold text-xs">
          <Gauge className="w-3.5 h-3.5 text-emerald-400" />
          <span>{r.composite_score.toFixed(1)}</span>
        </div>
      ),
      sortKey: 'composite_score',
      align: 'center'
    },
    {
      header: 'Delivered Revenue',
      accessor: r => `₹${r.net_revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'net_revenue',
      align: 'right'
    },
    {
      header: 'Total Orders',
      accessor: r => r.total_orders.toLocaleString(),
      sortKey: 'total_orders',
      align: 'right'
    },
    {
      header: 'On-Time SLA %',
      accessor: r => (
        <span className={`font-semibold ${r.sla_adherence_pct >= 90 ? 'text-emerald-600' : 'text-amber-600'}`}>
          {r.sla_adherence_pct.toFixed(1)}%
        </span>
      ),
      sortKey: 'sla_adherence_pct',
      align: 'right'
    },
    {
      header: 'Avg Delivery',
      accessor: r => `${r.avg_delivery_time.toFixed(1)}m`,
      sortKey: 'avg_delivery_time',
      align: 'right'
    },
    {
      header: 'Cancel %',
      accessor: r => `${r.cancellation_rate_pct.toFixed(1)}%`,
      sortKey: 'cancellation_rate_pct',
      align: 'right'
    },
    {
      header: 'In-Stock %',
      accessor: r => `${r.in_stock_rate_pct.toFixed(1)}%`,
      sortKey: 'in_stock_rate_pct',
      align: 'right'
    }
  ];

  const topStore = data[0];
  const lowestStore = data[data.length - 1];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="National #1 Dark Store"
          value={topStore ? topStore.store_name : 'Loading...'}
          subtitle={`Score: ${topStore ? topStore.composite_score : 0}/100 • ${topStore ? topStore.city : ''}`}
          icon={Trophy}
          badge="Gold Standard"
          badgeType="success"
        />
        <KPICard
          title="Operational Capacity"
          value="1,460 Orders/Hr"
          subtitle="Designed platform peak throughput"
          icon={Store}
          badge="Aggregate"
          badgeType="neutral"
        />
        <KPICard
          title="Average Fleet Size"
          value="22 Riders"
          subtitle="Dedicated delivery partners per hub"
          icon={Target}
        />
        <KPICard
          title="Focus Facility for Improvement"
          value={lowestStore ? lowestStore.store_name : 'Loading...'}
          subtitle={`Lagging on delivery duration (${lowestStore ? lowestStore.avg_delivery_time.toFixed(1) : 0}m)`}
          icon={Gauge}
          badge="RCA Required"
          badgeType="danger"
        />
      </div>

      {/* Benchmarking Methodology Explainer Card */}
      <div className="bg-slate-900 text-white p-5 rounded-xl border border-slate-800 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h4 className="text-sm font-bold tracking-tight text-white flex items-center gap-2">
            <Gauge className="w-4 h-4 text-emerald-400" />
            Composite Operational Scoring Methodology
          </h4>
          <p className="text-xs text-slate-400 mt-1">
            Scores are normalized across: Delivered Revenue Volume (35%) + On-Time 15-Minute SLA % (30%) + Low Cancellation % (20%) + Catalog In-Stock Health % (15%).
          </p>
        </div>
        <span className="shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
          Multi-Factor Objective Model
        </span>
      </div>

      {/* Main Ranking Table */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight">National Dark Store Leaderboard</h3>
          <span className="text-xs text-slate-500 font-medium">Ranked by Balanced Scorecard</span>
        </div>
        <DataTable
          columns={columns}
          data={data}
          searchPlaceholder="Search dark store..."
          searchKey="store_name"
          rowsPerPage={10}
        />
      </div>
    </div>
  );
};
