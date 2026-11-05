import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { RevenueAnalyticsResponse } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import { IndianRupee, TrendingUp, Percent, Tag, CreditCard } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';

export const RevenuePage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<RevenueAnalyticsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<RevenueAnalyticsResponse>('/revenue', {
      start_date: filters.startDate,
      end_date: filters.endDate,
      store_id: filters.storeId,
    })
      .then(res => setData(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters]);

  if (loading) return <LoadingSpinner message="Reconciling financial metrics, discounts & margin structures..." />;
  if (!data) return null;

  const {
    total_gmv,
    net_revenue,
    avg_order_value,
    total_discounts,
    discount_burn_rate,
    revenue_trends,
    category_revenue,
    store_revenue,
    top_products,
    payment_mode_split
  } = data;

  const storeColumns: Column<(typeof store_revenue)[0]>[] = [
    {
      header: 'Dark Store',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.store_name}</p>
          <p className="text-[11px] text-slate-400">{r.city}</p>
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
      header: 'Realized AOV',
      accessor: r => `₹${r.aov.toFixed(0)}`,
      sortKey: 'aov',
      align: 'right'
    },
    {
      header: 'Discounts Granted',
      accessor: r => `₹${r.discounts.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'discounts',
      align: 'right'
    }
  ];

  const topProductColumns: Column<(typeof top_products)[0]>[] = [
    {
      header: 'Product Name',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.name}</p>
          <p className="text-[11px] text-slate-400">{r.category}</p>
        </div>
      ),
      sortKey: 'name'
    },
    { header: 'MRP', accessor: r => `₹${r.mrp}`, sortKey: 'mrp', align: 'right' },
    { header: 'Units Sold', accessor: r => r.units_sold.toLocaleString(), sortKey: 'units_sold', align: 'right' },
    {
      header: 'Gross Revenue',
      accessor: r => `₹${r.revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'revenue',
      align: 'right'
    }
  ];

  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899'];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Gross Merchandise Value (GMV)"
          value={`₹${(total_gmv / 100000).toFixed(2)} L`}
          subtitle="Pre-discount aggregate basket value"
          icon={TrendingUp}
        />
        <KPICard
          title="Net Cash Realized"
          value={`₹${(net_revenue / 100000).toFixed(2)} L`}
          subtitle="Delivered customer payment receipts"
          icon={IndianRupee}
          badge="Delivered Only"
          badgeType="success"
        />
        <KPICard
          title="Promotional Discounts"
          value={`₹${total_discounts.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`}
          subtitle={`${discount_burn_rate}% burn rate against GMV`}
          icon={Tag}
          badge={discount_burn_rate <= 12 ? 'Controlled' : 'High Burn'}
          badgeType={discount_burn_rate <= 12 ? 'neutral' : 'warning'}
        />
        <KPICard
          title="Average Order Value"
          value={`₹${avg_order_value.toFixed(0)}`}
          subtitle="Basket ticket size per delivery"
          icon={Percent}
        />
      </div>

      {/* Daily GMV vs Net Revenue Area Chart */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="pb-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Daily Revenue Flow & Discount Spread
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Illustrates daily gap between gross GMV and net collected cash
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
            Realized Net: ₹{(net_revenue / 100000).toFixed(2)} Lakhs
          </span>
        </div>

        <div className="h-80 mt-6">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={revenue_trends} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <defs>
                <linearGradient id="colorGmv" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="colorNet" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748b' }} tickLine={false} />
              <YAxis
                tick={{ fontSize: 11, fill: '#64748b' }}
                tickLine={false}
                axisLine={false}
                tickFormatter={v => `₹${(v / 1000).toFixed(0)}k`}
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
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Area
                type="monotone"
                dataKey="gmv"
                name="Gross GMV (₹)"
                stroke="#3b82f6"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorGmv)"
              />
              <Area
                type="monotone"
                dataKey="net_revenue"
                name="Net Revenue (₹)"
                stroke="#10b981"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#colorNet)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid: Payment Mode Split & Store Revenue Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Payment Split */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Payment Channel Split</h3>
            <p className="text-xs text-slate-500 font-medium mb-4">UPI dominance vs Cards & COD</p>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={payment_mode_split}
                    dataKey="revenue"
                    nameKey="mode"
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={3}
                  >
                    {payment_mode_split.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={val => `₹${Number(val).toLocaleString('en-IN')}`}
                    contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-100">
            {payment_mode_split.map((p, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-slate-700">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                  ></span>
                  {p.mode}
                </span>
                <span className="font-semibold text-slate-900">
                  ₹{(p.revenue / 1000).toFixed(1)}k ({((p.revenue / (net_revenue || 1)) * 100).toFixed(0)}%)
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Store Revenue Table */}
        <div className="lg:col-span-2">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Dark Store Revenue Breakdown</h3>
            <span className="text-xs text-slate-500 font-medium">Ranked by Net Realized Volume</span>
          </div>
          <DataTable
            columns={storeColumns}
            data={store_revenue}
            searchPlaceholder="Filter store..."
            searchKey="store_name"
            rowsPerPage={5}
          />
        </div>
      </div>

      {/* Top 10 Hero SKUs Table */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight">Top 10 Hero Revenue Generators</h3>
          <span className="text-xs text-slate-500 font-medium">Highest Gross Sales Contribution</span>
        </div>
        <DataTable
          columns={topProductColumns}
          data={top_products}
          searchPlaceholder="Filter hero product..."
          searchKey="name"
          rowsPerPage={10}
        />
      </div>
    </div>
  );
};
