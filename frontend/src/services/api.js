const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      let errorMsg = `HTTP Error ${res.status}`;
      try {
        const errJson = await res.json();
        errorMsg = errJson.detail || errorMsg;
      } catch (e) {
        // fallback
      }
      throw new Error(errorMsg);
    }
    return await res.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // Contractor
  getContractorCatalogue: (category, search) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    return request(`/contractor/catalogue?${params.toString()}`);
  },
  getContractorBookings: (status) => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    return request(`/contractor/bookings?${params.toString()}`);
  },
  getContractorBooking: (id) => request(`/contractor/bookings/${id}`),
  createContractorBooking: (data) =>
    request('/contractor/bookings', { method: 'POST', body: JSON.stringify(data) }),
  cancelContractorBooking: (id, reason) =>
    request(`/contractor/bookings/${id}/cancel`, {
      method: 'POST',
      body: JSON.stringify({ reason, confirm: true }),
    }),
  reportContractorDispute: (id, category, description) =>
    request(`/contractor/bookings/${id}/dispute`, {
      method: 'POST',
      body: JSON.stringify({ category, description }),
    }),
  getContractorProfile: () => request('/contractor/profile'),

  // Provider
  getProviderRequests: () => request('/provider/requests'),
  acceptProviderRequest: (id, quantities) =>
    request(`/provider/requests/${id}/accept`, {
      method: 'POST',
      body: JSON.stringify({ quantities }),
    }),
  rejectProviderRequest: (id, reason) =>
    request(`/provider/requests/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason, confirm: true }),
    }),
  assignProviderUnits: (id, assignments) =>
    request(`/provider/assign/${id}`, {
      method: 'POST',
      body: JSON.stringify({ assignments }),
    }),
  getProviderSchedule: (date) => {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    return request(`/provider/schedule?${params.toString()}`);
  },
  getProviderFleet: () => request('/provider/fleet'),
  saveProviderEquipment: (data) =>
    request('/provider/equipment', { method: 'POST', body: JSON.stringify(data) }),
  getProviderProfile: () => request('/provider/profile'),

  // Operator
  getOperatorToday: () => request('/operator/today'),
  startOperatorTransit: (id) =>
    request(`/operator/transit/${id}`, { method: 'POST' }),
  markOperatorArrived: (id) =>
    request(`/operator/arrive/${id}`, { method: 'POST' }),
  verifyOperatorStart: (id, code) =>
    request(`/operator/verify_start/${id}`, {
      method: 'POST',
      body: JSON.stringify({ code, safety_confirmed: true }),
    }),
  requestOperatorEnd: (id) =>
    request(`/operator/request_end/${id}`, { method: 'POST' }),
  verifyOperatorEnd: (id, code) =>
    request(`/operator/verify_end/${id}`, {
      method: 'POST',
      body: JSON.stringify({ code, inspection_confirmed: true }),
    }),
  reportOperatorIssue: (bookingId, category, description) =>
    request('/operator/report_issue', {
      method: 'POST',
      body: JSON.stringify({ booking_id: bookingId, category, description }),
    }),
  getOperatorHistory: () => request('/operator/history'),
  getOperatorProfile: () => request('/operator/profile'),

  // Officer
  getOfficerDashboard: () => request('/officer/dashboard'),
  getOfficerRequests: (search, status, ward) => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    if (ward) params.append('ward', ward);
    return request(`/officer/requests?${params.toString()}`);
  },
  approveOfficerBooking: (id, note) =>
    request(`/officer/bookings/${id}/approve`, {
      method: 'POST',
      body: JSON.stringify({ note, site_verified: true, work_order_verified: true, provider_verified: true, safety_verified: true }),
    }),
  rejectOfficerBooking: (id, reason) =>
    request(`/officer/bookings/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason, confirm: true }),
    }),
  reassignOfficerBooking: (id, reason, assignments) =>
    request(`/officer/bookings/${id}/reassign`, {
      method: 'POST',
      body: JSON.stringify({ reason, confirm: true, assignments }),
    }),
  getOfficerDirectory: (tab, search) => {
    const params = new URLSearchParams();
    if (tab) params.append('tab', tab);
    if (search) params.append('search', search);
    return request(`/officer/directory?${params.toString()}`);
  },
  getOfficerDisputes: () => request('/officer/disputes'),
  resolveOfficerDispute: (id, note) =>
    request(`/officer/disputes/${id}/resolve`, {
      method: 'POST',
      body: JSON.stringify({ note, confirm: true }),
    }),
  getOfficerExportUrl: () => `${API_BASE}/officer/export`,

  // Shared
  resetDemoData: () => request('/shared/reset', { method: 'POST' }),
  getSharedOverview: () => request('/shared/overview'),
};
