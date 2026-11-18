import React, { useEffect, useState } from 'react';
import { Search, Filter, Truck, AlertTriangle, Zap, CheckCircle2, ChevronRight, Navigation, Radio } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';
import Modal from '../../components/Modal';
import SiteLocationMap from '../../components/SiteLocationMap';

export default function OfficerRequests({ initialFilter, onNavigateToVerification, onRefresh }) {
  const [requests, setRequests] = useState([]);
  const [activeTab, setActiveTab] = useState(initialFilter || 'All');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  // Reassign Modal State
  const [reassignModalBooking, setReassignModalBooking] = useState(null);
  const [reassignReason, setReassignReason] = useState('Replacement due to mechanical oil pressure failure on site.');
  const [availableFleet, setAvailableFleet] = useState({ vehicles: [], operators: [] });
  const [selectedVehId, setSelectedVehId] = useState('');
  const [selectedOpId, setSelectedOpId] = useState('');
  const [reassignLoading, setReassignLoading] = useState(false);

  // Live Telematics Map Modal State
  const [telematicsModalBooking, setTelematicsModalBooking] = useState(null);

  const tabs = [
    { id: 'All', label: 'All (25)' },
    { id: 'needs_approval', label: 'Needs Approval (4)' },
    { id: 'not_matched', label: 'Not Matched (2)' },
    { id: 'active', label: 'Active Today' },
    { id: 'issues', label: 'Issues & Disputes' },
  ];

  useEffect(() => {
    loadRequests();
  }, [activeTab, searchQuery]);

  const loadRequests = async () => {
    try {
      setLoading(true);
      const data = await api.getOfficerRequests(searchQuery, activeTab);
      setRequests(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenReassign = async (b, e) => {
    e.stopPropagation();
    try {
      const f = await api.getProviderFleet();
      setAvailableFleet(f);
      setSelectedVehId(f.vehicles[0]?.id || '');
      setSelectedOpId(f.operators[0]?.id || '');
      setReassignModalBooking(b);
    } catch (err) {
      alert('Failed to load available fleet: ' + err.message);
    }
  };

  const handleConfirmReassign = async () => {
    if (!reassignModalBooking) return;
    try {
      setReassignLoading(true);
      await api.reassignOfficerBooking(reassignModalBooking.id, reassignReason, [
        {
          unit_key: 'unit-1',
          equipment_id: reassignModalBooking.lines?.[0]?.equipment_id || 'eq-2',
          vehicle_id: selectedVehId,
          operator_id: selectedOpId,
        },
      ]);
      alert(`Booking ${reassignModalBooking.id} successfully reassigned to new machine & operator!`);
      setReassignModalBooking(null);
      await loadRequests();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert('Reassignment failed: ' + err.message);
    } finally {
      setReassignLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header & Search Bar (Reference Image 1 Screen 4) */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle space-y-2.5">
        <div>
          <span className="text-[10px] font-bold text-text-muted uppercase">Control Room · Ward G/N</span>
          <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
            All Ward Bookings & Triage
          </h2>
        </div>

        {/* Search */}
        <div className="relative">
          <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            type="text"
            placeholder="Search contractor, #order or vehicle..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl pl-9 pr-4 py-2 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        {/* Filter Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {tabs.map((t) => {
            const active = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                  active
                    ? 'bg-[#1C1C1E] text-white'
                    : 'bg-[#F5F5F7] text-text-secondary hover:bg-gray-200'
                }`}
              >
                {t.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-4 space-y-3.5">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading ward bookings triage...</div>
        ) : requests.length === 0 ? (
          <div className="py-12 text-center text-xs text-text-muted">No bookings match the selected criteria.</div>
        ) : (
          requests.map((b) => {
            const isPendingApproval = b.status === 'pending_approval';
            const isWorking = b.status === 'working';
            const isProblem = b.status === 'problem';
            const assignment = b.assignments?.[0] || {};

            return (
              <div
                key={b.id}
                onClick={() => onNavigateToVerification(b.id)}
                className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-text-primary">{b.id}</span>
                      <span className="text-[10px] text-text-muted">· Ward {b.ward}</span>
                    </div>
                    <h4 className="text-xs font-bold text-text-primary mt-1">
                      {b.contractor_company || 'Contractor'}
                    </h4>
                    <p className="text-[11px] text-text-secondary">
                      {b.lines?.[0]?.quantity || 1}x {b.lines?.[0]?.name || 'Machinery'}
                    </p>
                  </div>

                  <div className="text-right">
                    <StatusBadge status={b.status} label={b.status_label} />
                    <span className="text-xs font-bold text-text-primary block mt-1">
                      ₹{Number(b.total || 0).toLocaleString('en-IN')}
                    </span>
                  </div>
                </div>

                <p className="text-[11px] text-text-secondary line-clamp-1">{b.address}</p>

                {/* Specific Card Layouts Matching Reference Image 1 Screen 4 */}
                {isPendingApproval && (
                  <div className="pt-2 border-t border-border-subtle/80">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onNavigateToVerification(b.id);
                      }}
                      className="w-full h-11 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 shadow-sm transition-all"
                    >
                      <Zap size={14} />
                      <span>Review & Approve (1-Tap)</span>
                    </button>
                  </div>
                )}

                {isWorking && (
                  <div className="pt-2 border-t border-border-subtle/80 space-y-2">
                    <div className="bg-surface-subtle p-2.5 rounded-xl border border-border-subtle/60 text-[11px] space-y-1">
                      <div className="flex items-center justify-between text-text-secondary">
                        <span>Operator: {assignment.operator_name || 'Mahesh Shinde'}</span>
                        <span className="text-status-green font-semibold">Verified GPS</span>
                      </div>
                      <div className="text-[10px] text-text-muted">Shift 46% complete · Working normal</div>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setTelematicsModalBooking(b);
                      }}
                      className="w-full h-10 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-xl text-xs font-bold text-text-primary flex items-center justify-center gap-1.5 transition-colors"
                    >
                      <Navigation size={13} className="text-[#FFB400]" />
                      <span>View Telematics & Route</span>
                      <ChevronRight size={14} />
                    </button>
                  </div>
                )}

                {isProblem && (
                  <div className="pt-2 border-t border-border-subtle/80 space-y-2">
                    <div className="bg-[#FEE2E2] border border-[#FECACA] rounded-xl p-2.5 text-xs text-[#D93025] space-y-0.5">
                      <div className="font-bold flex items-center gap-1">
                        <AlertTriangle size={13} />
                        <span>Dispute / Breakdown Reported</span>
                      </div>
                      <p className="text-[11px] text-red-900 leading-tight">
                        {b.reason || 'Machine stalled due to oil pressure alarm at 10:15 AM - Traffic obstruction at Pillar #42.'}
                      </p>
                    </div>

                    <button
                      onClick={(e) => handleOpenReassign(b, e)}
                      className="w-full h-11 bg-[#1C1C1E] hover:bg-black text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
                    >
                      <span>Reassign Fleet Immediately</span>
                      <ChevronRight size={14} />
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Immediate Reassignment Modal */}
      <Modal
        isOpen={!!reassignModalBooking}
        onClose={() => setReassignModalBooking(null)}
        title="Immediate Municipal Fleet Reassignment"
      >
        {reassignModalBooking && (
          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Resolve incident on booking <strong>{reassignModalBooking.id}</strong> by allocating standby machinery & crew:
            </p>

            <div>
              <label className="text-xs font-bold text-text-primary block mb-1">Select Standby Machinery</label>
              <select
                value={selectedVehId}
                onChange={(e) => setSelectedVehId(e.target.value)}
                className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-medium"
              >
                {availableFleet.vehicles.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.registration} ({v.model}) · Depot Bandra West
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-bold text-text-primary block mb-1">Select Certified Standby Operator</label>
              <select
                value={selectedOpId}
                onChange={(e) => setSelectedOpId(e.target.value)}
                className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-medium"
              >
                {availableFleet.operators.map((o) => (
                  <option key={o.id} value={o.id}>
                    {o.name} ({o.license}) · Available
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-bold text-text-primary block mb-1">Reassignment Justification</label>
              <textarea
                rows={2}
                value={reassignReason}
                onChange={(e) => setReassignReason(e.target.value)}
                className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
              />
            </div>

            <button
              onClick={handleConfirmReassign}
              disabled={reassignLoading}
              className="w-full h-11 bg-[#1C1C1E] hover:bg-black text-white font-bold text-xs rounded-xl flex items-center justify-center transition-all disabled:opacity-50"
            >
              <span>{reassignLoading ? 'Dispatching...' : 'Dispatch Standby Machinery'}</span>
            </button>
          </div>
        )}
      </Modal>

      {/* Live Telematics & GPS Route Modal */}
      <Modal
        isOpen={!!telematicsModalBooking}
        onClose={() => setTelematicsModalBooking(null)}
        title="Live Telematics & GPS Route"
      >
        {telematicsModalBooking && (
          <div className="space-y-3.5">
            <div className="bg-[#FFF7E6] border border-[#FFB400]/40 rounded-xl p-3 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#7E5700] block">
                  Active Requisition
                </span>
                <h4 className="text-xs font-bold text-text-primary">
                  {telematicsModalBooking.id} · {telematicsModalBooking.equipment_type || 'Tata Prima 16T Tipper'}
                </h4>
                <p className="text-[11px] text-text-secondary mt-0.5">
                  Operator: {telematicsModalBooking.assignment?.operator_name || 'Mahesh Shinde'}
                </p>
              </div>
              <span className="px-2 py-1 rounded-full text-[10px] font-bold bg-[#DCFCE7] text-[#16A34A] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-[#16A34A] animate-pulse"></span>
                <span>GPS Lock</span>
              </span>
            </div>

            {/* Interactive Route Map */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-text-primary block">
                Live Transit Corridor & Geofence (Milan Subway / SV Road)
              </label>
              <SiteLocationMap
                address={telematicsModalBooking.address || 'Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai'}
                mode="route"
                height="h-[210px]"
                caption={telematicsModalBooking.address || 'Transit Corridor: Bandra Depot → Santacruz Gate 3'}
              />
            </div>

            {/* Telematics Metrics Grid */}
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="bg-surface-subtle p-2.5 rounded-xl border border-border-subtle">
                <span className="text-[9px] font-bold uppercase text-text-muted block">Speed</span>
                <span className="text-xs font-extrabold text-text-primary mt-0.5 block">18 km/h</span>
                <span className="text-[9px] text-[#16A34A] font-semibold">Active Work</span>
              </div>
              <div className="bg-surface-subtle p-2.5 rounded-xl border border-border-subtle">
                <span className="text-[9px] font-bold uppercase text-text-muted block">Engine Hours</span>
                <span className="text-xs font-extrabold text-text-primary mt-0.5 block">3.9 / 8.0 h</span>
                <span className="text-[9px] text-text-muted font-semibold">48% elapsed</span>
              </div>
              <div className="bg-surface-subtle p-2.5 rounded-xl border border-border-subtle">
                <span className="text-[9px] font-bold uppercase text-text-muted block">Fuel Level</span>
                <span className="text-xs font-extrabold text-text-primary mt-0.5 block">76%</span>
                <span className="text-[9px] text-[#16A34A] font-semibold">Optimal</span>
              </div>
            </div>

            <div className="pt-1 flex gap-2">
              <button
                type="button"
                onClick={() => {
                  const bId = telematicsModalBooking.id;
                  setTelematicsModalBooking(null);
                  onNavigateToVerification(bId);
                }}
                className="flex-1 h-11 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 shadow-sm transition-all"
              >
                <span>Open Verification Details</span>
                <ChevronRight size={14} />
              </button>
              <button
                type="button"
                onClick={() => setTelematicsModalBooking(null)}
                className="px-4 h-11 bg-surface hover:bg-gray-100 border border-border-subtle text-text-primary font-bold text-xs rounded-xl transition-all"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
