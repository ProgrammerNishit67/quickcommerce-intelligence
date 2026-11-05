import React, { useState, useEffect } from 'react';
import { FilterProvider } from './context/FilterContext';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { FilterBar } from './components/layout/FilterBar';

import { OverviewPage } from './pages/OverviewPage';
import { DeliveryPage } from './pages/DeliveryPage';
import { InventoryPage } from './pages/InventoryPage';
import { RevenuePage } from './pages/RevenuePage';
import { OrderQualityPage } from './pages/OrderQualityPage';
import { StorePerformancePage } from './pages/StorePerformancePage';
import { OperationalAlertsPage } from './pages/OperationalAlertsPage';
import { BusinessInsightsPage } from './pages/BusinessInsightsPage';
import { DataManagementPage } from './pages/DataManagementPage';
import { ReportsPage } from './pages/ReportsPage';
import { fetchAPI } from './api/client';
import { OperationalAlert } from './types';

export const AppContent: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [alertCount, setAlertCount] = useState<number>(0);

  useEffect(() => {
    fetchAPI<OperationalAlert[]>('/alerts')
      .then(res => {
        const criticalOrWarning = res.filter(a => a.severity === 'CRITICAL' || a.severity === 'WARNING');
        setAlertCount(criticalOrWarning.length);
      })
      .catch(() => {});
  }, []);

  const pageTitles: Record<string, { title: string; subtitle: string }> = {
    overview: {
      title: 'Executive Operations Overview',
      subtitle: 'Real-time telemetry across all quick-commerce micro-fulfillment dark stores'
    },
    delivery: {
      title: 'Delivery Operations & SLA Monitoring',
      subtitle: 'Tracking 15-minute fulfillment SLA adherence, peak congestion & fleet performance'
    },
    inventory: {
      title: 'Inventory Intelligence & Replenishment',
      subtitle: 'Stockout risk detection, safety-stock monitoring & automated order reorder queue'
    },
    revenue: {
      title: 'Revenue Analytics & Contribution Economics',
      subtitle: 'Gross merchandise value, net receipts, promotional discount burn & basket margins'
    },
    'order-quality': {
      title: 'Order Quality, Defects & Refund Audit',
      subtitle: 'Root causes for order cancellations, missing items & customer refund reconciliation'
    },
    'store-performance': {
      title: 'Dark Store Benchmarking & Efficiency Scorecard',
      subtitle: 'Composite ranking evaluating throughput, SLA compliance, low cancellation & in-stock health'
    },
    alerts: {
      title: 'Operational Anomaly & Threshold Alerts',
      subtitle: 'Rule-based detection for immediate operational interventions and fleet rebalancing'
    },
    insights: {
      title: 'Root Cause Business Insights & Playbooks',
      subtitle: 'Algorithmically generated diagnostic narratives with supporting database metrics and actionable next steps'
    },
    'data-management': {
      title: 'Data Management & Ingestion Pipeline',
      subtitle: 'CSV upload, schema validation, missing-value imputation, deduplication & relational PostgreSQL lineage'
    },
    reports: {
      title: 'Executive Reporting & Data Export Center',
      subtitle: '1-click Excel (.xlsx) and CSV exports for SLA, operations, inventory and revenue accounting'
    }
  };

  const renderActivePage = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewPage />;
      case 'delivery':
        return <DeliveryPage />;
      case 'inventory':
        return <InventoryPage />;
      case 'revenue':
        return <RevenuePage />;
      case 'order-quality':
        return <OrderQualityPage />;
      case 'store-performance':
        return <StorePerformancePage />;
      case 'alerts':
        return <OperationalAlertsPage />;
      case 'insights':
        return <BusinessInsightsPage />;
      case 'data-management':
        return <DataManagementPage />;
      case 'reports':
        return <ReportsPage />;
      default:
        return <OverviewPage />;
    }
  };

  const currentMeta = pageTitles[activeTab] || pageTitles.overview;

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} alertCount={alertCount} />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header title={currentMeta.title} subtitle={currentMeta.subtitle} />
        <FilterBar />

        {/* Scrollable Page Body */}
        <main className="flex-1 overflow-y-auto">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <FilterProvider>
      <AppContent />
    </FilterProvider>
  );
}
