import React, { useEffect, useState } from 'react';
import { fetchAPI, uploadCSV, getSampleCsvUrl } from '../api/client';
import { DataQualityReport } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  Download,
  Database,
  Layers,
  Sparkles,
  FileCheck
} from 'lucide-react';

interface DataSummary {
  total_orders: number;
  total_products: number;
  total_stores: number;
  total_partners: number;
  total_customers: number;
  total_inventory_records: number;
  total_cancellations: number;
  data_sources: {
    public_benchmark: number;
    synthetic_operational: number;
    csv_uploaded: number;
  };
}

export const DataManagementPage: React.FC = () => {
  const [summary, setSummary] = useState<DataSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [uploading, setUploading] = useState<boolean>(false);
  const [qualityReport, setQualityReport] = useState<DataQualityReport | null>(null);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadSummary = () => {
    setLoading(true);
    fetchAPI<DataSummary>('/data-management/summary')
      .then(res => setSummary(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadSummary();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    setUploadMessage(null);

    try {
      const res = await uploadCSV(file);
      setQualityReport(res.quality_report);
      setUploadMessage(`Successfully processed '${file.name}' with ${res.metadata.ingested_records} new records ingested into database.`);
      loadSummary();
    } catch (err: any) {
      setError(err.message || 'File upload failed');
    } finally {
      setUploading(false);
    }
  };

  if (loading && !summary) return <LoadingSpinner message="Auditing relational tables and data quality pipeline..." />;

  return (
    <div className="p-8 space-y-8">
      {/* Upload Zone & Actions */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="pb-4 border-b border-slate-100 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Operational CSV Ingestion & Data Validation Pipeline
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Upload orders CSV for schema validation, missing-value imputation, deduplication, and PostgreSQL ingestion
            </p>
          </div>
          <a
            href={getSampleCsvUrl()}
            download="sample_orders_template.csv"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" />
            <span>Download Sample CSV Template</span>
          </a>
        </div>

        {/* Upload Box */}
        <div className="mt-6 border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-brand-500 transition-colors bg-slate-50/50">
          <UploadCloud className="w-10 h-10 text-slate-400 mx-auto mb-3" />
          <p className="text-xs font-semibold text-slate-800">
            Upload new quick commerce order batches (.csv)
          </p>
          <p className="text-[11px] text-slate-400 mt-1 max-w-sm mx-auto">
            Automated primary key deduplication, date sanitization, and database integrity checks will execute upon upload.
          </p>

          <label className="mt-4 inline-block">
            <span className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold cursor-pointer shadow-sm transition-colors">
              {uploading ? 'Processing Data Pipeline...' : 'Select CSV File'}
            </span>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              disabled={uploading}
              className="hidden"
            />
          </label>
        </div>

        {uploadMessage && (
          <div className="mt-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs font-medium text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{uploadMessage}</span>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs font-medium text-rose-800 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Live Data Quality Report */}
      {qualityReport && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-emerald-600" />
              <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                Data Quality & Ingestion Audit Report
              </h3>
            </div>
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Quality Score: {qualityReport.data_quality_score}/100
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-[11px] text-slate-400 font-medium block">Total Raw Rows</span>
              <p className="text-base font-bold text-slate-900 mt-1">{qualityReport.total_records}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-[11px] text-slate-400 font-medium block">Valid Clean Rows</span>
              <p className="text-base font-bold text-slate-900 mt-1">{qualityReport.valid_records}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-[11px] text-slate-400 font-medium block">Duplicates Handled</span>
              <p className="text-base font-bold text-slate-900 mt-1">{qualityReport.duplicates_detected}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-[11px] text-slate-400 font-medium block">Missing Values Imputed</span>
              <p className="text-base font-bold text-slate-900 mt-1">{qualityReport.missing_values_count}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-[11px] text-slate-400 font-medium block">Anomalies Detected</span>
              <p className="text-base font-bold text-slate-900 mt-1">{qualityReport.anomalies_detected}</p>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              Validation & Cleaning Log Details
            </h4>
            <div className="bg-slate-50 rounded-lg p-3 border border-slate-200 text-xs text-slate-700 font-mono space-y-1">
              {qualityReport.issues_summary.map((iss, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className="text-emerald-500">✓</span>
                  <span>{iss}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Relational Database Inventory & Dataset Lineage */}
      {summary && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <div className="pb-4 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-slate-700" />
              <div>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                  Relational Storage & Dataset Lineage
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  Clearly distinguishing verified public FMCG catalog data from synthetic operational records
                </p>
              </div>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
              PostgreSQL Relational Schema
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
            <div className="p-4 rounded-xl border border-slate-200 bg-white">
              <span className="text-xs text-slate-500 font-medium">Orders Stored</span>
              <p className="text-xl font-bold text-slate-900 mt-1">{summary.total_orders.toLocaleString()}</p>
              <span className="text-[10px] text-slate-400 block mt-0.5">Transactional records</span>
            </div>
            <div className="p-4 rounded-xl border border-slate-200 bg-white">
              <span className="text-xs text-slate-500 font-medium">Catalog SKUs</span>
              <p className="text-xl font-bold text-slate-900 mt-1">{summary.total_products}</p>
              <span className="text-[10px] text-emerald-600 font-semibold block mt-0.5">Public FMCG Benchmark</span>
            </div>
            <div className="p-4 rounded-xl border border-slate-200 bg-white">
              <span className="text-xs text-slate-500 font-medium">Dark Stores</span>
              <p className="text-xl font-bold text-slate-900 mt-1">{summary.total_stores}</p>
              <span className="text-[10px] text-slate-400 block mt-0.5">Micro-fulfillment hubs</span>
            </div>
            <div className="p-4 rounded-xl border border-slate-200 bg-white">
              <span className="text-xs text-slate-500 font-medium">Delivery Fleet</span>
              <p className="text-xl font-bold text-slate-900 mt-1">{summary.total_partners}</p>
              <span className="text-[10px] text-slate-400 block mt-0.5">Active delivery partners</span>
            </div>
          </div>

          {/* Lineage Table */}
          <div className="mt-6 pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">
              Data Lineage & Provenance Metadata
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="font-bold text-emerald-700 block mb-1">
                  Tag: public_benchmark
                </span>
                <p className="text-slate-600">
                  Products, categories, real Indian FMCG MRPs (Amul, Maggi, Coca-Cola, Lay's), and product shelf-life.
                </p>
                <span className="mt-2 text-[11px] font-semibold text-slate-800 block">
                  Records: {summary.data_sources.public_benchmark} verified SKUs
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="font-bold text-indigo-700 block mb-1">
                  Tag: synthetic_operational
                </span>
                <p className="text-slate-600">
                  Simulated 60-day operational telemetry, promised vs actual delivery timestamps, GPS stores, and rider dispatches.
                </p>
                <span className="mt-2 text-[11px] font-semibold text-slate-800 block">
                  Records: {summary.data_sources.synthetic_operational.toLocaleString()} orders
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="font-bold text-amber-700 block mb-1">
                  Tag: csv_upload_ingestion
                </span>
                <p className="text-slate-600">
                  Batches uploaded via CSV pipeline, validated, cleansed, and appended to PostgreSQL storage.
                </p>
                <span className="mt-2 text-[11px] font-semibold text-slate-800 block">
                  Records: {summary.data_sources.csv_uploaded} user ingested
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
