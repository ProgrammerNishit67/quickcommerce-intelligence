const BASE_URL = import.meta.env.VITE_API_URL || 
  (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000/api'
    : '/api');

export async function fetchAPI<T>(endpoint: string, params: Record<string, string | undefined> = {}): Promise<T> {
  const isAbsolute = BASE_URL.startsWith('http://') || BASE_URL.startsWith('https://');
  const fullBase = isAbsolute ? BASE_URL : `${window.location.origin}${BASE_URL}`;
  const url = new URL(`${fullBase}${endpoint}`);
  Object.entries(params).forEach(([key, val]) => {
    if (val && val !== 'all') {
      url.searchParams.append(key, val);
    }
  });

  const res = await fetch(url.toString(), {
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API Error ${res.status}: ${errorText || res.statusText}`);
  }

  return res.json();
}

export async function uploadCSV(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${BASE_URL}/data-management/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Upload Error: ${err}`);
  }

  return res.json();
}

export function getExportUrl(reportType: string, format: 'csv' | 'excel', storeId?: string): string {
  const url = new URL(`${BASE_URL}/reports/export`);
  url.searchParams.append('report_type', reportType);
  url.searchParams.append('format', format);
  if (storeId && storeId !== 'all') {
    url.searchParams.append('store_id', storeId);
  }
  return url.toString();
}

export function getSampleCsvUrl(): string {
  return `${BASE_URL}/data-management/sample-download`;
}
