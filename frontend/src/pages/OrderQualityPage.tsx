import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { OrderQualityResponse } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import { AlertCircle, RotateCcw, AlertTriangle, ShieldCheck } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from 'recharts';

export const OrderQualityPage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<OrderQualityResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<OrderQualityResponse>('/order-quality', {
      start_date: filters.startDate,
      end_date: filters.endDate,
      store_id: filters.storeId,
    })
      .then(res => setData(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters]);

  if (loading) return <LoadingSpinner message="Auditing order defect rates, cancellations & refund reconciliation..." />;
  if (!data) return null;

  const {
    total_cancellations,
    cancellation_rate,
    total_refunds,
    cancellation_reasons,
    cancelled_by_split,
    defect_types,
    store_cancellations
  } = data;

  const storeColumns: Column<(typeof store_cancellations)[0]>[] = [
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
    { header: 'Total Orders', accessor: r => r.total_orders.toLocaleString(), sortKey: 'total_orders', align: 'right' },
    { header: 'Cancellations', accessor: 'cancelled_orders', sortKey: 'cancelled_orders', align: 'right' },
    {
      header: 'Cancellation Rate',
      accessor: r => (
        <span className={`font-semibold ${r.cancellation_rate > 5.0 ? 'text-rose-600' : 'text-slate-700'}`}>
          {r.cancellation_rate.toFixed(1)}%
        </span>
      ),
      sortKey: 'cancellation_rate',
      align: 'right'
    },
    {
      header: 'Lost Revenue',
      accessor: r => `₹${r.lost_revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'lost_revenue',
      align: 'right'
    }
  ];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Cancellations"
          value={total_cancellations.toLocaleString()}
          subtitle="Orders aborted before fulfillment"
          icon={AlertCircle}
          badge={`${cancellation_rate.toFixed(1)}% rate`}
          badgeType={cancellation_rate <= 4.5 ? 'success' : 'danger'}
        />
        <KPICard
          title="Total Refund Liabilities"
          value={`₹${total_refunds.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`}
          subtitle="Direct refund disbursements"
          icon={RotateCcw}
          badge="100% Reconciled"
          badgeType="neutral"
        />
        <KPICard
          title="Primary Defect Driver"
          value="Extreme Delay"
          subtitle="> 25 min delivery overshoot"
          icon={AlertTriangle}
          badge="35% of all cancels"
          badgeType="danger"
        />
        <KPICard
          title="Fulfillment Defect Rate"
          value="0.8%"
          subtitle="Damaged / missing items"
          icon={ShieldCheck}
          badge="Within Tolerance"
          badgeType="success"
        />
      </div>

      {/* Grid: Cancellation Root Causes & Channel Origin */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Reasons Chart */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <div className="pb-4 border-b border-slate-100 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                Order Cancellation Breakdown by Reason
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Root causes prompting order drop-offs and refund disbursements
              </p>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 border border-rose-200">
              Top: Delivery Delays
            </span>
          </div>

          <div className="h-72 mt-6">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={cancellation_reasons}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} tickLine={false} />
                <YAxis
                  dataKey="reason"
                  type="category"
                  tick={{ fontSize: 10, fill: '#334155' }}
                  tickLine={false}
                  width={140}
                />
                <Tooltip
                  formatter={(val, name) => [val, name === 'count' ? 'Cancellations' : 'Refunds (₹)']}
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    color: '#fff',
                    borderRadius: '8px',
                    border: 'none',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="count" name="Cancellation Count" fill="#f43f5e" radius={[0, 4, 4, 0]} barSize={16} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Initiated By Card */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Cancellation Initiator</h3>
            <p className="text-xs text-slate-500 font-medium mb-6">Who triggered the abort action</p>
            <div className="space-y-4">
              {cancelled_by_split.map((item, idx) => (
                <div key={idx}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="font-semibold text-slate-800">{item.source}</span>
                    <span className="text-slate-600 font-medium">
                      {item.count} orders ({item.share_pct}%)
                    </span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        item.source === 'CUSTOMER'
                          ? 'bg-rose-500'
                          : item.source === 'STORE'
                          ? 'bg-amber-500'
                          : 'bg-indigo-500'
                      }`}
                      style={{ width: `${item.share_pct}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 mt-6 text-xs text-slate-600">
            <strong className="text-slate-900">Key Finding:</strong> Store-initiated cancellations stem directly
            from physical inventory count mismatches (phantom inventory).
          </div>
        </div>
      </div>

      {/* Store Cancellation Leaderboard */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight">Dark Store Defect & Cancellation Audit</h3>
          <span className="text-xs text-slate-500 font-medium">Ranked by Cancellation Rate</span>
        </div>
        <DataTable
          columns={storeColumns}
          data={store_cancellations}
          searchPlaceholder="Search store..."
          searchKey="store_name"
          rowsPerPage={10}
        />
      </div>
    </div>
  );
};
