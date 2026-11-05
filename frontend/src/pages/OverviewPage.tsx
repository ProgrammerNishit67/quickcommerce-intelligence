import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { OverviewResponse } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import {
  ShoppingBag,
  IndianRupee,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Building2,
  TrendingUp,
  Percent
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

export const OverviewPage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<OverviewResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    fetchAPI<OverviewResponse>('/overview', {
      start_date: filters.startDate,
      end_date: filters.endDate,
      store_id: filters.storeId,
    })
      .then(res => {
        if (isMounted) {
          setData(res);
          setError(null);
        }
      })
      .catch(err => {
        if (isMounted) setError(err.message);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [filters]);

  if (loading) return <LoadingSpinner message="Calculating database-backed executive KPIs..." />;
  if (error || !data) {
    return (
      <div className="p-8 text-center text-rose-600 bg-rose-50 rounded-xl m-8 border border-rose-200">
        <p className="font-semibold text-sm">Failed to load overview analytics</p>
        <p className="text-xs mt-1">{error}</p>
      </div>
    );
  }

  const { kpis, daily_trends, store_performance, category_performance } = data;

  const storeColumns: Column<(typeof store_performance)[0]>[] = [
    {
      header: 'Dark Store',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.store_name}</p>
          <p className="text-[11px] text-slate-400">{r.city} • {r.store_id}</p>
        </div>
      ),
      sortKey: 'store_name'
    },
    { header: 'Orders', accessor: r => r.orders.toLocaleString(), sortKey: 'orders', align: 'right' },
    {
      header: 'Net Revenue',
      accessor: r => `₹${r.revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'revenue',
      align: 'right'
    },
    {
      header: 'Avg Delivery',
      accessor: r => `${r.avg_delivery_time.toFixed(1)}m`,
      sortKey: 'avg_delivery_time',
      align: 'right'
    },
    {
      header: 'On-Time SLA',
      accessor: r => (
        <span className={`font-semibold ${r.on_time_rate >= 90 ? 'text-emerald-600' : 'text-amber-600'}`}>
          {r.on_time_rate.toFixed(1)}%
        </span>
      ),
      sortKey: 'on_time_rate',
      align: 'right'
    },
    {
      header: 'Cancellation',
      accessor: r => `${r.cancellation_rate.toFixed(1)}%`,
      sortKey: 'cancellation_rate',
      align: 'right'
    }
  ];

  const categoryColumns: Column<(typeof category_performance)[0]>[] = [
    { header: 'Category', accessor: 'category', sortKey: 'category' },
    { header: 'Units Sold', accessor: r => r.units_sold.toLocaleString(), sortKey: 'units_sold', align: 'right' },
    {
      header: 'Revenue',
      accessor: r => `₹${r.revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'revenue',
      align: 'right'
    },
    {
      header: 'Gross Margin %',
      accessor: r => (
        <span className="font-semibold text-slate-800">{r.gross_margin_pct.toFixed(1)}%</span>
      ),
      sortKey: 'gross_margin_pct',
      align: 'right'
    },
    {
      header: 'Revenue Share',
      accessor: r => `${r.share_pct.toFixed(1)}%`,
      sortKey: 'share_pct',
      align: 'right'
    }
  ];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards Header Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Orders"
          value={kpis.total_orders.toLocaleString()}
          subtitle="Placed across all dark stores"
          icon={ShoppingBag}
          badge="+8.4% WoW"
          badgeType="success"
        />
        <KPICard
          title="Gross Merchandise Value"
          value={`₹${(kpis.total_gmv / 100000).toFixed(2)} L`}
          subtitle={`₹${kpis.total_gmv.toLocaleString('en-IN', { maximumFractionDigits: 0 })} total order value`}
          icon={TrendingUp}
        />
        <KPICard
          title="Net Revenue Collected"
          value={`₹${(kpis.net_revenue / 100000).toFixed(2)} L`}
          subtitle="Net realized after discounts"
          icon={IndianRupee}
          badge="Excl. Cancellations"
          badgeType="neutral"
        />
        <KPICard
          title="Average Order Value (AOV)"
          value={`₹${kpis.average_order_value.toFixed(0)}`}
          subtitle="Realized basket size per delivery"
          icon={Percent}
        />
        <KPICard
          title="Average Delivery Time"
          value={`${kpis.average_delivery_time.toFixed(1)} min`}
          subtitle="SLA benchmark: 15.0 mins"
          icon={Clock}
          badge={kpis.average_delivery_time <= 15 ? 'Within SLA' : 'SLA Breach'}
          badgeType={kpis.average_delivery_time <= 15 ? 'success' : 'danger'}
        />
        <KPICard
          title="On-Time Delivery Rate"
          value={`${kpis.on_time_delivery_rate.toFixed(1)}%`}
          subtitle="Fulfillments delivered under 15m"
          icon={CheckCircle2}
          badge="Target >= 92%"
          badgeType={kpis.on_time_delivery_rate >= 90 ? 'success' : 'warning'}
        />
        <KPICard
          title="Cancellation Rate"
          value={`${kpis.cancellation_rate.toFixed(1)}%`}
          subtitle="Customer & store cancelled orders"
          icon={AlertTriangle}
          badge="Target <= 4.0%"
          badgeType={kpis.cancellation_rate <= 4.5 ? 'success' : 'danger'}
        />
        <KPICard
          title="Active Dark Stores"
          value={kpis.active_stores}
          subtitle="High-density micro-fulfillment hubs"
          icon={Building2}
          badge="100% Operational"
          badgeType="success"
        />
      </div>

      {/* Main Trajectory Chart */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-100 gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Daily Order Volume & Net Revenue Trajectory
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Daily revenue run rate contrasted against total order fulfillment volume
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 text-slate-700">
            60-Day Historical Trend
          </span>
        </div>

        <div className="h-80 mt-6">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={daily_trends} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748b' }} tickLine={false} />
              <YAxis
                yAxisId="left"
                tick={{ fontSize: 11, fill: '#64748b' }}
                tickLine={false}
                axisLine={false}
                tickFormatter={v => `₹${(v / 1000).toFixed(0)}k`}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                tick={{ fontSize: 11, fill: '#64748b' }}
                tickLine={false}
                axisLine={false}
                tickFormatter={v => `${v}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  color: '#fff',
                  borderRadius: '8px',
                  border: 'none',
                  fontSize: '12px',
                }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Bar
                yAxisId="right"
                dataKey="orders"
                name="Daily Orders"
                fill="#cbd5e1"
                radius={[4, 4, 0, 0]}
                barSize={12}
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="revenue"
                name="Net Revenue (₹)"
                stroke="#16a34a"
                strokeWidth={2.5}
                dot={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid: Store Benchmarking & Category Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Dark Store Operational Matrix</h3>
            <span className="text-xs text-slate-500 font-medium">{store_performance.length} Stores Tracked</span>
          </div>
          <DataTable
            columns={storeColumns}
            data={store_performance}
            searchPlaceholder="Filter store by name..."
            searchKey="store_name"
            rowsPerPage={5}
          />
        </div>

        <div>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Category Contribution & Margins</h3>
            <span className="text-xs text-slate-500 font-medium">FMCG Catalog Breakdown</span>
          </div>
          <DataTable
            columns={categoryColumns}
            data={category_performance}
            searchPlaceholder="Filter category..."
            searchKey="category"
            rowsPerPage={5}
          />
        </div>
      </div>
    </div>
  );
};
