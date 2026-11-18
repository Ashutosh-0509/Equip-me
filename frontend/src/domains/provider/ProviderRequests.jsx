import React, { useEffect, useState } from 'react';
import { Truck, Clock, MapPin, Check, X, AlertCircle } from 'lucide-react';
import { api } from '../../services/api';
import Modal from '../../components/Modal';

export default function ProviderRequests({ onSelectBookingToAssign }) {
  const [requests, setRequests] = useState([]);
  const [online, setOnline] = useState(true);
  const [loading, setLoading] = useState(true);

  // Accept Modal State
  const [selectedReq, setSelectedReq] = useState(null);
  const [acceptQuantities, setAcceptQuantities] = useState({});
  const [rejectModalReq, setRejectModalReq] = useState(null);
  const [rejectReason, setRejectReason] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    try {
      setLoading(true);
      const data = await api.getProviderRequests();
      setRequests(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenAcceptModal = (req) => {
    setSelectedReq(req);
    const initialQty = {};
    req.lines?.forEach((l) => {
      initialQty[l.equipment_id] = l.quantity;
    });
    setAcceptQuantities(initialQty);
  };

  const handleConfirmAccept = async () => {
    if (!selectedReq) return;
    try {
      setActionLoading(true);
      await api.acceptProviderRequest(selectedReq.id, acceptQuantities);
      setSelectedReq(null);
      await loadRequests();
      // Navigate to assign
      onSelectBookingToAssign(selectedReq.id);
    } catch (err) {
      alert('Failed to accept request: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleConfirmReject = async () => {
    if (!rejectModalReq) return;
    if (!rejectReason || rejectReason.length < 5) {
      alert('Please enter a rejection reason.');
      return;
    }
    try {
      setActionLoading(true);
      await api.rejectProviderRequest(rejectModalReq.id, rejectReason);
      setRejectModalReq(null);
      setRejectReason('');
      await loadRequests();
    } catch (err) {
      alert('Failed to reject request: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Bar with Online Switch (Reference Image 3 Screen 3) */}
      <div className="bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <div>
          <span className="text-xs font-bold text-text-primary block">BMC Fleet Ops</span>
          <p className="text-[11px] text-text-secondary">Mahalaxmi Earthmovers & Fleet</p>
        </div>

        {/* Online Toggle */}
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-semibold text-text-secondary">
            {online ? 'Online · Accepting' : 'Offline'}
          </span>
          <button
            onClick={() => setOnline(!online)}
            className={`w-11 h-6 rounded-full p-1 transition-colors ${
              online ? 'bg-status-green' : 'bg-gray-300'
            }`}
          >
            <div
              className={`w-4 h-4 rounded-full bg-white transition-transform ${
                online ? 'translate-x-5' : 'translate-x-0'
              }`}
            />
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* KPI Counter Row */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 text-center shadow-2xs">
            <span className="text-2xl font-black text-[#7E5700] block">
              {requests.filter((r) => r.status === 'pending_provider').length || 3}
            </span>
            <span className="text-[11px] font-bold text-text-secondary mt-0.5 block">
              New Requests
            </span>
          </div>

          <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 text-center shadow-2xs">
            <span className="text-2xl font-black text-text-primary block">
              {requests.filter((r) => r.status === 'approved').length || 2}
            </span>
            <span className="text-[11px] font-bold text-text-secondary mt-0.5 block">
              Awaiting Allocation
            </span>
          </div>
        </div>

        {/* Incoming Requests Feed */}
        <div className="space-y-3">
          <h2 className="text-xs font-bold text-text-primary uppercase tracking-wide">
            Incoming Demands
          </h2>

          {loading ? (
            <div className="py-12 text-center text-xs text-text-muted">Loading incoming requests...</div>
          ) : requests.length === 0 ? (
            <div className="py-12 text-center text-xs text-text-muted">No pending requests right now.</div>
          ) : (
            requests.map((req, idx) => {
              const expiresMins = 42 + idx * 45;
              const isApproved = req.status === 'approved';

              return (
                <div
                  key={req.id}
                  className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3 shadow-2xs"
                >
                  {/* Card Header with Expiry */}
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-[#E67E22] bg-[#FEF3C7] px-2.5 py-0.5 rounded-full flex items-center gap-1">
                      <Clock size={11} />
                      <span>{isApproved ? 'Approved by Officer' : `Expires in ${expiresMins}m`}</span>
                    </span>
                    <span className="text-[11px] font-semibold text-text-muted">
                      Ward {req.ward}
                    </span>
                  </div>

                  {/* Machinery Title */}
                  <div>
                    <h3 className="text-xs font-bold text-text-primary">
                      {req.lines?.[0]?.quantity || 1}x {req.lines?.[0]?.name || 'Backhoe Loader'}
                    </h3>
                    <p className="text-[11px] text-text-secondary mt-0.5">
                      {req.date} · {req.shift?.split('·')[0]}
                    </p>
                    <p className="text-[10px] text-text-muted mt-0.5">
                      Contractor: {req.contractor_company}
                    </p>
                  </div>

                  {/* Actions Row */}
                  <div className="pt-2 border-t border-border-subtle/80 flex items-center gap-2">
                    {isApproved ? (
                      <button
                        onClick={() => onSelectBookingToAssign(req.id)}
                        className="w-full h-10 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 shadow-sm transition-all"
                      >
                        <Truck size={14} />
                        <span>Assign Vehicle & Crew Now</span>
                      </button>
                    ) : (
                      <>
                        <button
                          onClick={() => setRejectModalReq(req)}
                          className="flex-1 h-10 bg-surface-subtle hover:bg-red-50 text-text-secondary hover:text-red-700 border border-border-subtle rounded-xl text-xs font-bold transition-colors"
                        >
                          Reject
                        </button>
                        <button
                          onClick={() => handleOpenAcceptModal(req)}
                          className="flex-2 h-10 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1 shadow-sm transition-all"
                        >
                          <span>Accept Request</span>
                        </button>
                      </>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Accept Quantity Modal */}
      <Modal
        isOpen={!!selectedReq}
        onClose={() => setSelectedReq(null)}
        title="Accept Demand & Confirm Availability"
      >
        {selectedReq && (
          <div className="space-y-4">
            <p className="text-xs text-text-secondary">
              Review and specify how many units your fleet can fulfill for booking{' '}
              <strong className="text-text-primary">{selectedReq.id}</strong>:
            </p>

            <div className="space-y-2.5">
              {selectedReq.lines?.map((line) => (
                <div
                  key={line.equipment_id}
                  className="bg-surface-subtle p-3 rounded-xl border border-border-subtle flex items-center justify-between"
                >
                  <div>
                    <div className="text-xs font-bold text-text-primary">{line.name}</div>
                    <div className="text-[10px] text-text-muted">
                      Requested: {line.quantity} units · ₹{line.rate}/hr
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() =>
                        setAcceptQuantities((prev) => ({
                          ...prev,
                          [line.equipment_id]: Math.max(0, (prev[line.equipment_id] || 0) - 1),
                        }))
                      }
                      className="w-7 h-7 bg-white rounded-lg border border-border-subtle font-bold text-xs"
                    >
                      -
                    </button>
                    <span className="w-5 text-center text-xs font-bold text-text-primary">
                      {acceptQuantities[line.equipment_id] ?? line.quantity}
                    </span>
                    <button
                      onClick={() =>
                        setAcceptQuantities((prev) => ({
                          ...prev,
                          [line.equipment_id]: Math.min(
                            line.quantity,
                            (prev[line.equipment_id] || 0) + 1
                          ),
                        }))
                      }
                      className="w-7 h-7 bg-white rounded-lg border border-border-subtle font-bold text-xs"
                    >
                      +
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleConfirmAccept}
              disabled={actionLoading}
              className="w-full h-11 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center transition-all disabled:opacity-50"
            >
              <span>Confirm Acceptance → Send for Officer Clearance</span>
            </button>
          </div>
        )}
      </Modal>

      {/* Reject Modal */}
      <Modal
        isOpen={!!rejectModalReq}
        onClose={() => setRejectModalReq(null)}
        title="Decline Booking Request"
      >
        <div className="space-y-3">
          <p className="text-xs text-text-secondary">
            Please provide a valid reason for declining to dispatch machinery:
          </p>
          <textarea
            rows={3}
            placeholder="e.g. All hydraulic excavators currently deployed on Western Express Highway works."
            value={rejectReason}
            onChange={(e) => setRejectReason(e.target.value)}
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
          />
          <button
            onClick={handleConfirmReject}
            disabled={actionLoading}
            className="w-full h-11 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl flex items-center justify-center transition-all"
          >
            <span>Confirm Rejection</span>
          </button>
        </div>
      </Modal>
    </div>
  );
}
