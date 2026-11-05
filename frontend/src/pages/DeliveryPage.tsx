import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { DeliveryAnalyticsResponse } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import { StatusBadge } from '../components/common/StatusBadge';
import { Clock, ShieldAlert, Award, Zap } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  Line,
  ComposedChart
} from 'recharts';

export const DeliveryPage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<DeliveryAnalyticsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<DeliveryAnalyticsResponse>('/delivery', {
      start_date: filters.startDate,
      end_date: filters.endDate,
      store_id: filters.storeId,
    })
      .then(res => setData(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters]);

  if (loading) return <LoadingSpinner message="Calculating delivery fleet metrics & SLA distributions..." />;
  if (!data) return null;

  const {
    avg_delivery_time,
    on_time_rate,
    sla_breaches,
    sla_breach_rate,
    hourly_trends,
    store_delivery_performance,
    delay_breakdown,
    partner_performance
  } = data;

  const storeColumns: Column<(typeof store_delivery_performance)[0]>[] = [
    {
      header: 'Store Hub',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.store_name}</p>
          <p className="text-[11px] text-slate-400">{r.city}</p>
        </div>
      ),
      sortKey: 'store_name'
    },
    { header: 'Allocated Riders', accessor: 'riders', sortKey: 'riders', align: 'center' },
    { header: 'Completed Trips', accessor: r => r.total_orders.toLocaleString(), sortKey: 'total_orders', align: 'right' },
    {
      header: 'Avg Delivery Time',
      accessor: r => `${r.avg_time.toFixed(1)} mins`,
      sortKey: 'avg_time',
      align: 'right'
    },
    {
      header: 'SLA Breaches',
      accessor: r => (
        <span className={r.breaches > 80 ? 'text-rose-600 font-semibold' : 'text-slate-600'}>
          {r.breaches}
        </span>
      ),
      sortKey: 'breaches',
      align: 'right'
    },
    {
      header: 'On-Time SLA Rate',
      accessor: r => (
        <span className={`font-semibold ${r.on_time_rate >= 90 ? 'text-emerald-600' : 'text-rose-600'}`}>
          {r.on_time_rate.toFixed(1)}%
        </span>
      ),
      sortKey: 'on_time_rate',
      align: 'right'
    }
  ];

  const partnerColumns: Column<(typeof partner_performance)[0]>[] = [
    {
      header: 'Delivery Partner',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.name}</p>
          <p className="text-[11px] text-slate-400">{r.partner_id} • {r.vehicle_type}</p>
        </div>
      ),
      sortKey: 'name'
    },
    {
      header: 'Rating',
      accessor: r => (
        <span className="inline-flex items-center gap-1 font-semibold text-slate-800">
          ★ {r.rating.toFixed(2)}
        </span>
      ),
      sortKey: 'rating',
      align: 'center'
    },
    { header: 'Total Trips', accessor: 'trips', sortKey: 'trips', align: 'right' },
    {
      header: 'Avg Delivery',
      accessor: r => `${r.avg_time.toFixed(1)}m`,
      sortKey: 'avg_time',
      align: 'right'
    },
    {
      header: 'SLA Adherence',
      accessor: r => (
        <StatusBadge
          status={r.sla_compliance_pct >= 92 ? `${r.sla_compliance_pct.toFixed(0)}% On-Time` : `${r.sla_compliance_pct.toFixed(0)}% Sub-Par`}
        />
      ),
      sortKey: 'sla_compliance_pct',
      align: 'right'
    }
  ];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Average Delivery Duration"
          value={`${avg_delivery_time.toFixed(1)} min`}
          subtitle="Target: <= 14.5 mins"
          icon={Clock}
          badge={avg_delivery_time <= 15.0 ? 'Optimal' : 'SLA Breach'}
          badgeType={avg_delivery_time <= 15.0 ? 'success' : 'danger'}
        />
        <KPICard
          title="On-Time Delivery Rate"
          value={`${on_time_rate.toFixed(1)}%`}
          subtitle="Orders fulfilled within 15 mins"
          icon={Zap}
          badge="15-Min Promise"
          badgeType="success"
        />
        <KPICard
          title="Total SLA Breaches"
          value={sla_breaches.toLocaleString()}
          subtitle="Orders delivered past 15 mins"
          icon={ShieldAlert}
          badge={`${sla_breach_rate.toFixed(1)}% breach rate`}
          badgeType="warning"
        />
        <KPICard
          title="Top Performing Fleet"
          value="EV 2-Wheelers"
          subtitle="Fastest average turnaround (11.8m)"
          icon={Award}
          badge="Lowest Cost/Trip"
          badgeType="neutral"
        />
      </div>

      {/* Hourly Congestion Chart */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="pb-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Hourly Order Volume & Delivery Time Heatmap
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Identifies peak fleet bottleneck hours (Morning Rush: 7-10 AM, Late Night Munchies: 8-11 PM)
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 border border-amber-200">
            Peak Bottleneck: 20:00 - 22:00
          </span>
        </div>

        <div className="h-80 mt-6">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={hourly_trends} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="hour" tick={{ fontSize: 11, fill: '#64748b' }} tickLine={false} />
              <YAxis
                yAxisId="left"
                tick={{ fontSize: 11, fill: '#64748b' }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                tick={{ fontSize: 11, fill: '#64748b' }}
                tickLine={false}
                axisLine={false}
                tickFormatter={v => `${v}m`}
                domain={[0, 25]}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  color: '#fff',
                  borderRadius: '8px',
                  border: 'none',
                  fontSize: '12px'
                }}
              />
              <Bar yAxisId="left" dataKey="orders" name="Order Volume" fill="#cbd5e1" radius={[4, 4, 0, 0]} />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="avg_time"
                name="Avg Delivery Time (mins)"
                stroke="#f59e0b"
                strokeWidth={3}
                dot={{ r: 3 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid: Delay Breakdown & Partner Leaderboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Delay Buckets */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight">Delivery Duration Distribution</h3>
          <p className="text-xs text-slate-500 font-medium mb-6">Fulfillment breakdown into SLA brackets</p>
          <div className="space-y-4">
            {delay_breakdown.map((item, idx) => (
              <div key={idx}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="font-medium text-slate-700">{item.tier}</span>
                  <span className="font-semibold text-slate-900">
                    {item.orders.toLocaleString()} ({item.percentage}%)
                  </span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      item.tier.includes('Fast')
                        ? 'bg-emerald-500'
                        : item.tier.includes('Standard')
                        ? 'bg-emerald-400'
                        : item.tier.includes('Minor')
                        ? 'bg-amber-400'
                        : 'bg-rose-500'
                    }`}
                    style={{ width: `${Math.min(100, item.percentage * 2.2)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Partner Leaderboard */}
        <div className="lg:col-span-2">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Rider Speed & Adherence Matrix</h3>
            <span className="text-xs text-slate-500 font-medium">Top active partners</span>
          </div>
          <DataTable
            columns={partnerColumns}
            data={partner_performance}
            searchPlaceholder="Search rider..."
            searchKey="name"
            rowsPerPage={5}
          />
        </div>
      </div>

      {/* Store Delivery Performance Table */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight">Dark Store Delivery Performance</h3>
          <span className="text-xs text-slate-500 font-medium">Ranked by On-Time SLA Adherence</span>
        </div>
        <DataTable
          columns={storeColumns}
          data={store_delivery_performance}
          searchPlaceholder="Search store..."
          searchKey="store_name"
          rowsPerPage={10}
        />
      </div>
    </div>
  );
};
