import React, { useEffect, useState } from 'react';
import { fetchAPI } from '../api/client';
import { BusinessInsight } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import {
  Lightbulb,
  MapPin,
  TrendingUp,
  Search,
  CheckCircle2,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export const BusinessInsightsPage: React.FC = () => {
  const [insights, setInsights] = useState<BusinessInsight[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    fetchAPI<BusinessInsight[]>('/insights')
      .then(res => setInsights(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Synthesizing multi-table root cause intelligence & operational playbook..." />;

  return (
    <div className="p-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-slate-900 text-white rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Operations Intelligence Engine</span>
          </div>
          <h2 className="text-lg font-bold text-white tracking-tight">
            Root Cause Operational Insights & Action Playbooks
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Each diagnosis below is algorithmically generated from live PostgreSQL/SQLite analytical tables, identifying what happened, the supporting metrics, root causes, and operations next steps.
          </p>
        </div>
        <span className="text-xs font-mono font-semibold px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">
          {insights.length} Diagnostic Playbooks Active
        </span>
      </div>

      {/* Insights Cards Grid */}
      <div className="space-y-6">
        {insights.map((insight, idx) => {
          const impactStyle =
            insight.impact_level === 'HIGH'
              ? 'bg-rose-50 text-rose-700 border-rose-200'
              : insight.impact_level === 'MEDIUM'
              ? 'bg-amber-50 text-amber-700 border-amber-200'
              : 'bg-emerald-50 text-emerald-700 border-emerald-200';

          return (
            <div
              key={insight.id || idx}
              className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow"
            >
              {/* Card Header */}
              <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-100 flex items-center justify-center shrink-0">
                    <Lightbulb className="w-4 h-4" />
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                      {insight.title}
                    </h3>
                    <p className="text-xs text-slate-500 font-medium flex items-center gap-1.5 mt-0.5">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      <span>{insight.where_it_happened}</span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-auto">
                  <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold border ${impactStyle}`}>
                    {insight.impact_level} IMPACT
                  </span>
                  <span className="text-[11px] font-mono text-slate-400 bg-white px-2 py-0.5 rounded border border-slate-200">
                    {insight.category}
                  </span>
                </div>
              </div>

              {/* Card Body */}
              <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                {/* Section 1: What Happened */}
                <div className="space-y-3">
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                      1. What Happened
                    </span>
                    <p className="text-slate-800 font-medium leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                      {insight.what_happened}
                    </p>
                  </div>

                  {/* Supporting Metrics */}
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                      Supporting Database Metrics
                    </span>
                    <ul className="space-y-1.5 text-slate-600">
                      {insight.supporting_metrics.map((metric, mIdx) => (
                        <li key={mIdx} className="flex items-start gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>
                          <span>{metric}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Section 2: Root Cause Analysis */}
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                    2. Root Cause Analysis (RCA)
                  </span>
                  <div className="p-3 bg-amber-50/50 rounded-lg border border-amber-100 text-slate-700 leading-relaxed font-normal">
                    <p>{insight.root_cause_analysis}</p>
                  </div>
                </div>

                {/* Section 3: Recommended Action Plan */}
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                    3. Recommended Next Steps
                  </span>
                  <div className="p-3 bg-emerald-50/50 rounded-lg border border-emerald-100 text-slate-800 leading-relaxed font-medium">
                    <p>{insight.recommended_action}</p>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
