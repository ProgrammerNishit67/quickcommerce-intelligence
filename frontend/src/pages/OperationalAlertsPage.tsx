import React, { useEffect, useState } from 'react';
import { fetchAPI } from '../api/client';
import { OperationalAlert } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  BellRing,
  AlertTriangle,
  CheckCircle2,
  Filter,
  ArrowRight,
  Clock,
  Store,
  Layers
} from 'lucide-react';

export const OperationalAlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<OperationalAlert[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');

  useEffect(() => {
    setLoading(true);
    fetchAPI<OperationalAlert[]>('/alerts')
      .then(res => setAlerts(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Scanning operational telemetry against anomaly thresholds..." />;

  const filteredAlerts = alerts.filter(a => {
    if (selectedSeverity === 'ALL') return true;
    return a.severity === selectedSeverity;
  });

  const criticalCount = alerts.filter(a => a.severity === 'CRITICAL').length;
  const warningCount = alerts.filter(a => a.severity === 'WARNING').length;

  return (
    <div className="p-8 space-y-6">
      {/* Alert Banner / Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-lg bg-rose-50 text-rose-600 border border-rose-100">
              <BellRing className="w-5 h-5 animate-bounce" />
            </span>
            <div>
              <h3 className="text-base font-bold text-slate-900 tracking-tight">
                Operational Anomaly Detection Engine
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Live automated alerts detecting delivery SLA overshoots, cancellation spikes, and stockout bottlenecks
              </p>
            </div>
          </div>
        </div>

        {/* Severity Filters */}
        <div className="flex items-center gap-2 bg-slate-50 p-1 rounded-lg border border-slate-200 text-xs font-semibold">
          {['ALL', 'CRITICAL', 'WARNING', 'INFO'].map(sev => (
            <button
              key={sev}
              onClick={() => setSelectedSeverity(sev)}
              className={`px-3 py-1.5 rounded-md transition-all ${
                selectedSeverity === sev
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {sev}
              {sev === 'CRITICAL' && criticalCount > 0 && ` (${criticalCount})`}
              {sev === 'WARNING' && warningCount > 0 && ` (${warningCount})`}
            </button>
          ))}
        </div>
      </div>

      {/* Alert Cards Feed */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-500">
            <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
            <p className="font-semibold text-sm text-slate-800">All Operations Functioning Normally</p>
            <p className="text-xs text-slate-400 mt-1">No active anomalies matching filter criteria.</p>
          </div>
        ) : (
          filteredAlerts.map(alert => (
            <div
              key={alert.id}
              className={`bg-white rounded-xl border p-5 shadow-sm transition-all hover:shadow-md ${
                alert.severity === 'CRITICAL'
                  ? 'border-rose-300 bg-rose-50/10'
                  : alert.severity === 'WARNING'
                  ? 'border-amber-300 bg-amber-50/10'
                  : 'border-slate-200'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
                <div className="flex items-center gap-3">
                  <StatusBadge status={alert.severity} variant="severity" />
                  <span className="text-xs font-bold text-slate-900 tracking-tight">
                    {alert.title}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium">
                  {alert.store_name && (
                    <span className="flex items-center gap-1 text-slate-700 bg-slate-100 px-2 py-0.5 rounded">
                      <Store className="w-3 h-3 text-slate-400" />
                      {alert.store_name}
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-400" />
                    {alert.detected_at}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-xs">
                <div>
                  <span className="text-slate-400 font-medium block mb-0.5">Observed Metric:</span>
                  <p className="font-bold text-slate-900 text-sm">{alert.metric_value}</p>
                  <span className="text-[11px] text-slate-500">Operating Limit: {alert.threshold}</span>
                </div>

                <div className="md:col-span-2">
                  <span className="text-slate-400 font-medium block mb-0.5">Diagnostic Description:</span>
                  <p className="text-slate-700 font-normal leading-relaxed">{alert.description}</p>
                </div>
              </div>

              {/* Recommended Action Box */}
              <div className="mt-4 pt-3 border-t border-slate-100/80 flex items-start sm:items-center justify-between gap-3 bg-slate-50/70 p-3 rounded-lg">
                <div className="flex items-start sm:items-center gap-2 text-xs">
                  <span className="font-bold text-slate-800 shrink-0">Action Protocol:</span>
                  <span className="text-slate-700">{alert.recommended_action}</span>
                </div>
                <button className="shrink-0 inline-flex items-center gap-1 text-xs font-semibold text-brand-600 hover:text-brand-700">
                  <span>Dispatch Fix</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
