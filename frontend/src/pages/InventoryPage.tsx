import React, { useEffect, useState } from 'react';
import { useFilters } from '../context/FilterContext';
import { fetchAPI } from '../api/client';
import { InventoryIntelligenceResponse } from '../types';
import { KPICard } from '../components/common/KPICard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { DataTable, Column } from '../components/common/DataTable';
import { StatusBadge } from '../components/common/StatusBadge';
import { Boxes, AlertOctagon, RotateCw, AlertTriangle } from 'lucide-react';
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

export const InventoryPage: React.FC = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<InventoryIntelligenceResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<InventoryIntelligenceResponse>('/inventory', {
      store_id: filters.storeId,
      category: filters.category,
    })
      .then(res => setData(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters.storeId, filters.category]);

  if (loading) return <LoadingSpinner message="Evaluating dark store inventory levels & replenishment triggers..." />;
  if (!data) return null;

  const {
    total_skus,
    stockout_count,
    stockout_rate,
    low_stock_count,
    overall_turnover_ratio,
    category_inventory,
    fast_moving_products,
    slow_moving_products,
    replenishment_recommendations
  } = data;

  const replenishColumns: Column<(typeof replenishment_recommendations)[0]>[] = [
    {
      header: 'Store Hub',
      accessor: 'store_name',
      sortKey: 'store_name'
    },
    {
      header: 'Product SKU',
      accessor: r => (
        <div>
          <p className="font-semibold text-slate-900">{r.name}</p>
          <p className="text-[11px] text-slate-400">{r.category} • {r.sku_id}</p>
        </div>
      ),
      sortKey: 'name'
    },
    {
      header: 'Stock Levels',
      accessor: r => (
        <span className="text-xs">
          <strong className={r.current_stock === 0 ? 'text-rose-600 font-bold' : 'text-slate-800'}>
            {r.current_stock}
          </strong> / Safety: {r.safety_stock}
        </span>
      ),
      sortKey: 'current_stock',
      align: 'center'
    },
    {
      header: 'Order Units',
      accessor: r => (
        <span className="font-bold text-slate-900">+{r.suggested_units} pcs</span>
      ),
      sortKey: 'suggested_units',
      align: 'right'
    },
    {
      header: 'Est. Procurement Cost',
      accessor: r => `₹${r.estimated_cost.toLocaleString('en-IN')}`,
      sortKey: 'estimated_cost',
      align: 'right'
    },
    {
      header: 'Urgency',
      accessor: r => (
        <StatusBadge
          status={r.urgency === 'URGENT_STOCKOUT' ? 'CRITICAL STOCKOUT' : 'SCHEDULED REORDER'}
          variant="severity"
        />
      ),
      sortKey: 'urgency',
      align: 'right'
    }
  ];

  const fastMovingColumns: Column<(typeof fast_moving_products)[0]>[] = [
    { header: 'Item Name', accessor: 'name', sortKey: 'name' },
    { header: 'Category', accessor: 'category', sortKey: 'category' },
    { header: 'MRP', accessor: r => `₹${r.mrp}`, sortKey: 'mrp', align: 'right' },
    { header: 'Units Sold', accessor: r => r.units_sold.toLocaleString(), sortKey: 'units_sold', align: 'right' },
    {
      header: 'Revenue',
      accessor: r => `₹${r.revenue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
      sortKey: 'revenue',
      align: 'right'
    }
  ];

  const slowMovingColumns: Column<(typeof slow_moving_products)[0]>[] = [
    { header: 'Item Name', accessor: 'name', sortKey: 'name' },
    { header: 'Category', accessor: 'category', sortKey: 'category' },
    { header: 'MRP', accessor: r => `₹${r.mrp}`, sortKey: 'mrp', align: 'right' },
    { header: 'Units Sold', accessor: r => r.units_sold.toLocaleString(), sortKey: 'units_sold', align: 'right' },
    {
      header: 'Action',
      accessor: () => <span className="text-[11px] font-medium text-amber-600">Review Depth</span>,
      align: 'right'
    }
  ];

  return (
    <div className="p-8 space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Catalog Tracked"
          value={total_skus.toLocaleString()}
          subtitle="SKU store allocations"
          icon={Boxes}
        />
        <KPICard
          title="Zero Stockouts"
          value={stockout_count}
          subtitle={`${stockout_rate}% catalog unavailable`}
          icon={AlertOctagon}
          badge={stockout_count === 0 ? 'Optimal' : 'Immediate Restock'}
          badgeType={stockout_count === 0 ? 'success' : 'danger'}
        />
        <KPICard
          title="Critical Low Stock"
          value={low_stock_count}
          subtitle="Items at or below safety stock"
          icon={AlertTriangle}
          badge="Trigger Level"
          badgeType="warning"
        />
        <KPICard
          title="Inventory Turnover"
          value={`${overall_turnover_ratio}x`}
          subtitle="Annualized working capital velocity"
          icon={RotateCw}
          badge="High Velocity"
          badgeType="success"
        />
      </div>

      {/* Category Stock Level Chart */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="pb-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Category Holding Value & Critical Shortages
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Identifies inventory capital tied up across FMCG categories
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 text-slate-700">
            Total Capital: ₹
            {(
              category_inventory.reduce((acc, c) => acc + c.holding_value, 0) / 100000
            ).toFixed(2)}{' '}
            Lakhs
          </span>
        </div>

        <div className="h-80 mt-6">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={category_inventory} margin={{ top: 10, right: 20, left: 10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis
                dataKey="category"
                tick={{ fontSize: 10, fill: '#64748b' }}
                interval={0}
                angle={-15}
                textAnchor="end"
                tickLine={false}
              />
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
              <Bar dataKey="holding_value" name="Holding Value (₹)" radius={[4, 4, 0, 0]}>
                {category_inventory.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.critical_items > 0 ? '#f59e0b' : '#10b981'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Replenishment Recommendation Engine Table */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Automated Dark Store Replenishment Queue
            </h3>
            <p className="text-xs text-slate-500">
              Procurement quantities dynamically calculated based on 2.5x reorder thresholds
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 border border-rose-200">
            {replenishment_recommendations.length} Immediate POs Suggested
          </span>
        </div>
        <DataTable
          columns={replenishColumns}
          data={replenishment_recommendations}
          searchPlaceholder="Filter SKU..."
          searchKey="name"
          rowsPerPage={8}
        />
      </div>

      {/* Fast vs Slow Moving SKUs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Hero SKUs (Top 10 Fast-Moving)
            </h3>
            <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
              High Turnover
            </span>
          </div>
          <DataTable
            columns={fastMovingColumns}
            data={fast_moving_products}
            searchPlaceholder="Search fast SKU..."
            searchKey="name"
            rowsPerPage={5}
          />
        </div>

        <div>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Lagging SKUs (Slow-Moving)
            </h3>
            <span className="text-xs font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
              Dead Stock Risk
            </span>
          </div>
          <DataTable
            columns={slowMovingColumns}
            data={slow_moving_products}
            searchPlaceholder="Search slow SKU..."
            searchKey="name"
            rowsPerPage={5}
          />
        </div>
      </div>
    </div>
  );
};
