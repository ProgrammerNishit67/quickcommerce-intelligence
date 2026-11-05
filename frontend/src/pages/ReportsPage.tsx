import React, { useState, useEffect } from 'react';
import { useFilters } from '../context/FilterContext';
import { getExportUrl, fetchAPI } from '../api/client';
import { DataTable, Column } from '../components/common/DataTable';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import {
  FileSpreadsheet,
  Download,
  FileText,
  Calendar,
  Clock,
  Boxes,
  Store,
  TrendingUp,
  Eye
} from 'lucide-react';

interface ReportConfig {
  id: string;
  title: string;
  description: string;
  icon: any;
  category: string;
  cadence: string;
}

const REPORT_CATALOG: ReportConfig[] = [
  {
    id: 'daily_ops',
    title: 'Daily Operations & Fulfillment Report',
    description: 'Daily order volumes, delivered vs cancelled breakdowns, gross GMV, net cash receipts, and on-time SLA rates.',
    icon: Calendar,
    category: 'Executive Operations',
    cadence: 'Daily at 23:59 IST'
  },
  {
    id: 'delivery_sla',
    title: 'Delivery SLA Compliance & Breach Report',
    description: 'Detailed hub-by-hub breakdown of 15-minute SLA breach frequencies, average delivery durations, and delay severity.',
    icon: Clock,
    category: 'Logistics Fleet',
    cadence: 'Hourly & Daily'
  },
  {
    id: 'inventory_exception',
    title: 'Inventory Exception & Replenishment Report',
    description: 'Critical zero-stockout flags, safety-stock violations, suggested reorder purchase units, and procurement budget estimates.',
    icon: Boxes,
    category: 'Supply Chain & Procurement',
    cadence: 'Real-Time / Shift-End'
  },
  {
    id: 'store_performance',
    title: 'Dark Store Benchmarking & Scorecard Report',
    description: 'National and city store rankings, rider throughput, revenue velocity, capacity utilization, and composite efficiency.',
    icon: Store,
    category: 'Store Operations',
    cadence: 'Weekly & Monthly'
  },
  {
    id: 'revenue_analysis',
    title: 'Revenue Contribution & Discount Burn Report',
    description: 'Gross sales value, net realized revenue, discount subsidies, free delivery cost absorption, and contribution margins.',
    icon: TrendingUp,
    category: 'Commercial Finance',
    cadence: 'Monthly Closing'
  }
];

export const ReportsPage: React.FC = () => {
  const { filters } = useFilters();
  const [selectedReport, setSelectedReport] = useState<string>('daily_ops');
  const [previewData, setPreviewData] = useState<any[]>([]);
  const [previewLoading, setPreviewLoading] = useState<boolean>(false);

  // Load preview data when selected report changes
  useEffect(() => {
    setPreviewLoading(true);
    // In our backend, we can fetch preview by parsing a sample of the data or calling existing endpoints
    const endpointMap: Record<string, string> = {
      daily_ops: '/overview',
      delivery_sla: '/delivery',
      inventory_exception: '/inventory',
      store_performance: '/store-performance',
      revenue_analysis: '/revenue'
    };

    fetchAPI<any>(endpointMap[selectedReport] || '/overview', {
      start_date: filters.startDate,
      end_date: filters.endDate,
      store_id: filters.storeId
    })
      .then(res => {
        if (selectedReport === 'daily_ops') {
          setPreviewData(res.daily_trends || []);
        } else if (selectedReport === 'delivery_sla') {
          setPreviewData(res.store_delivery_performance || []);
        } else if (selectedReport === 'inventory_exception') {
          setPreviewData(res.replenishment_recommendations || []);
        } else if (selectedReport === 'store_performance') {
          setPreviewData(res || []);
        } else if (selectedReport === 'revenue_analysis') {
          setPreviewData(res.store_revenue || []);
        }
      })
      .catch(console.error)
      .finally(() => setPreviewLoading(false));
  }, [selectedReport, filters]);

  const activeReportObj = REPORT_CATALOG.find(r => r.id === selectedReport)!;

  // Construct dynamic columns for preview table
  const previewColumns: Column<any>[] = previewData.length > 0
    ? Object.keys(previewData[0])
        .filter(k => typeof previewData[0][k] !== 'object')
        .slice(0, 7)
        .map(key => ({
          header: key.replace(/_/g, ' ').toUpperCase(),
          accessor: r => {
            const val = r[key];
            if (typeof val === 'number') {
              return Number.isInteger(val) ? val.toLocaleString() : val.toFixed(1);
            }
            return String(val ?? '');
          },
          sortKey: key
        }))
    : [];

  return (
    <div className="p-8 space-y-8">
      {/* Header Info */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 tracking-tight">
            Enterprise Reporting & Data Export Center
          </h3>
          <p className="text-xs text-slate-500 font-medium">
            Generate scheduled and on-demand operational reports formatted for Excel (.xlsx) and CSV analysis
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
          <span>Active Filter:</span>
          <span className="font-semibold text-slate-800 bg-slate-100 px-2.5 py-1 rounded-md">
            {filters.preset} • {filters.storeId === 'all' ? 'All Stores' : filters.storeId}
          </span>
        </div>
      </div>

      {/* Report Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {REPORT_CATALOG.map(rep => {
          const Icon = rep.icon;
          const isSelected = selectedReport === rep.id;
          return (
            <div
              key={rep.id}
              onClick={() => setSelectedReport(rep.id)}
              className={`rounded-xl border p-5 shadow-sm cursor-pointer transition-all flex flex-col justify-between ${
                isSelected
                  ? 'border-brand-500 bg-emerald-50/20 ring-1 ring-brand-500/20'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-md'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="p-2 rounded-lg bg-slate-100 text-slate-800">
                    <Icon className="w-4 h-4" />
                  </span>
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    {rep.category}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-900">{rep.title}</h4>
                <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">{rep.description}</p>
              </div>

              {/* Action Buttons */}
              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <span className="text-[10px] text-slate-400 font-medium">{rep.cadence}</span>
                <div className="flex items-center gap-1.5" onClick={e => e.stopPropagation()}>
                  <a
                    href={getExportUrl(rep.id, 'csv', filters.storeId)}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors"
                    title="Export as CSV"
                  >
                    <Download className="w-3 h-3 text-slate-500" />
                    <span>CSV</span>
                  </a>
                  <a
                    href={getExportUrl(rep.id, 'excel', filters.storeId)}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition-colors shadow-sm"
                    title="Export as Excel .xlsx"
                  >
                    <FileSpreadsheet className="w-3 h-3 text-white" />
                    <span>Excel</span>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Live Preview Section */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-3">
          <div className="flex items-center gap-2">
            <Eye className="w-4 h-4 text-slate-500" />
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Live Preview: {activeReportObj.title}
            </h3>
          </div>

          <div className="flex items-center gap-2">
            <a
              href={getExportUrl(selectedReport, 'csv', filters.storeId)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-sm transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-slate-500" />
              <span>Download Full CSV</span>
            </a>
            <a
              href={getExportUrl(selectedReport, 'excel', filters.storeId)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-colors"
            >
              <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-400" />
              <span>Download Excel (.xlsx)</span>
            </a>
          </div>
        </div>

        {previewLoading ? (
          <LoadingSpinner message="Generating report preview..." />
        ) : previewData.length > 0 ? (
          <DataTable
            columns={previewColumns}
            data={previewData}
            searchPlaceholder="Filter preview records..."
            rowsPerPage={6}
          />
        ) : (
          <p className="text-xs text-slate-400 py-6 text-center">No preview records found.</p>
        )}
      </div>
    </div>
  );
};
