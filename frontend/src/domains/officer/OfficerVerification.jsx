import React, { useEffect, useState } from 'react';
import { ArrowLeft, Check, CheckSquare, Square, X, AlertTriangle, ShieldCheck, ArrowRight, Zap } from 'lucide-react';
import { api } from '../../services/api';
import Modal from '../../components/Modal';

export default function OfficerVerification({ bookingId, onBack, onActionComplete }) {
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  // Verification Checklist State
  const [siteVerified, setSiteVerified] = useState(true);
  const [woVerified, setWoVerified] = useState(true);
  const [providerVerified, setProviderVerified] = useState(true);
  const [safetyVerified, setSafetyVerified] = useState(true);

  // Modal States
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [showInfoModal, setShowInfoModal] = useState(false);
  const [infoNote, setInfoNote] = useState('');

  useEffect(() => {
    loadBooking();
  }, [bookingId]);

  const loadBooking = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorBooking(bookingId || 'BMC-8842');
      setBooking(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!booking) return;
    try {
      setActionLoading(true);
      await api.approveOfficerBooking(
        booking.id,
        'Municipal requisition verified & approved. Financial lock activated.'
      );
      alert(`Booking ${booking.id} verified and approved successfully!`);
      onActionComplete();
    } catch (err) {
      alert('Approval failed: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async () => {
    if (!booking) return;
    if (!rejectReason || rejectReason.length < 5) {
      alert('Please provide a reason for requisition rejection.');
      return;
    }
    try {
      setActionLoading(true);
      await api.rejectOfficerBooking(booking.id, rejectReason);
      setShowRejectModal(false);
      alert('Requisition rejected.');
      onActionComplete();
    } catch (err) {
      alert('Rejection failed: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading || !booking) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-xs text-text-muted">
        Loading booking verification details...
      </div>
    );
  }

  const isApproved = booking.status === 'approved';

  return (
    <div className="flex flex-col min-h-full pb-24 bg-[#F8F9FA]">
      {/* Top Header (Reference Image 1 Screen 5) */}
      <div className="sticky top-0 z-20 bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <button onClick={onBack} className="p-1 -ml-1 text-text-secondary hover:text-text-primary rounded-lg">
          <ArrowLeft size={18} />
        </button>
        <div className="text-center">
          <h2 className="text-xs font-bold text-text-primary">{booking.id}</h2>
          <span className="text-[10px] text-text-muted">Ward {booking.ward} · Sub-Division</span>
        </div>
        <div className="w-6" />
      </div>

      <div className="p-4 space-y-4">
        {/* Verification Summary Card (Reference Image 1 Screen 5) */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3.5 shadow-2xs">
          <div className="flex items-center gap-2 pb-2.5 border-b border-border-subtle/80">
            <ShieldCheck size={18} className="text-[#16A34A]" />
            <h3 className="text-xs font-bold text-text-primary uppercase tracking-wide">
              Verification Summary
            </h3>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">
                Registered Contractor
              </span>
              <span className="font-bold text-text-primary mt-0.5 block">
                {booking.contractor_company || 'Sharma Infra & Co.'}
              </span>
            </div>

            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">
                Assigned Provider
              </span>
              <span className="font-bold text-text-primary mt-0.5 block">
                {booking.provider_company || 'Mahalaxmi Fleet'}
              </span>
            </div>
          </div>

          <div className="pt-2 border-t border-border-subtle/60 text-xs space-y-2">
            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">Equipment</span>
              <span className="font-bold text-text-primary">
                {booking.lines?.[0]?.quantity || 2}x {booking.lines?.[0]?.name || 'JCB 3DX Backhoe'}
              </span>
            </div>

            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">Site Location</span>
              <span className="text-text-secondary font-medium line-clamp-2">
                {booking.address}
              </span>
            </div>

            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">Deployment Slot</span>
              <span className="text-text-secondary font-medium">
                {booking.date} · {booking.shift?.split('·')[0]}
              </span>
            </div>
          </div>

          {/* Financial Lock Box */}
          <div className="bg-[#FFF7E6] p-3 rounded-xl border border-[#FFB400]/40 flex items-center justify-between">
            <div>
              <span className="text-[10px] font-bold text-[#7E5700] uppercase tracking-wider block">
                Financial Lock
              </span>
              <span className="text-xs text-text-muted">Total escrow budget commitment</span>
            </div>
            <span className="text-lg font-black text-text-primary">
              ₹{Number(booking.total || 23200).toLocaleString('en-IN')}
            </span>
          </div>
        </div>

        {/* Verification Checklist */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-2.5 shadow-2xs">
          <span className="text-xs font-bold text-text-primary uppercase tracking-wide block mb-1">
            Requisition Protocol Checks
          </span>

          {[
            { id: 'site', label: 'Site and road width access verified', val: siteVerified, set: setSiteVerified },
            { id: 'wo', label: 'Municipal Work Order budget allocated', val: woVerified, set: setWoVerified },
            { id: 'prov', label: 'Provider fleet fitness certificates verified', val: providerVerified, set: setProviderVerified },
            { id: 'saf', label: 'Safety protocols and PPE checklist confirmed', val: safetyVerified, set: setSafetyVerified },
          ].map((item) => (
            <div
              key={item.id}
              onClick={() => item.set(!item.val)}
              className="flex items-center gap-2.5 p-2 rounded-lg hover:bg-surface-subtle cursor-pointer text-xs"
            >
              {item.val ? (
                <CheckSquare size={16} className="text-[#16A34A]" />
              ) : (
                <Square size={16} className="text-text-muted" />
              )}
              <span className={item.val ? 'font-medium text-text-primary' : 'text-text-secondary'}>
                {item.label}
              </span>
            </div>
          ))}
        </div>

        {/* Primary Action Button (Reference Image 1 Screen 5) */}
        {!isApproved ? (
          <div className="space-y-2.5 pt-2">
            <button
              onClick={handleApprove}
              disabled={actionLoading}
              className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-black text-sm rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all tracking-wide disabled:opacity-50"
            >
              <Zap size={18} />
              <span>{actionLoading ? 'Approving Requisition...' : 'Approve Requisition (1-Tap)'}</span>
              <ArrowRight size={18} />
            </button>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setShowInfoModal(true)}
                className="h-10 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-xl text-xs font-bold text-text-primary transition-colors"
              >
                Ask for Info
              </button>
              <button
                onClick={() => setShowRejectModal(true)}
                className="h-10 bg-surface-subtle hover:bg-red-50 text-red-700 border border-border-subtle rounded-xl text-xs font-bold transition-colors"
              >
                Reject / Remarks
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-[#DCFCE7] border border-[#BBF7D0] p-4 rounded-2xl text-center space-y-1">
            <span className="text-xs font-bold text-[#16A34A] block">Requisition Approved & Locked</span>
            <p className="text-[11px] text-[#166534]">
              Clearance recorded in audit log. Provider has been instructed to assign vehicle & operator.
            </p>
          </div>
        )}
      </div>

      {/* Reject Modal */}
      <Modal
        isOpen={showRejectModal}
        onClose={() => setShowRejectModal(false)}
        title="Reject Requisition"
      >
        <div className="space-y-3">
          <p className="text-xs text-text-secondary">
            Provide the municipal officer remarks for rejecting this requisition:
          </p>
          <textarea
            rows={3}
            value={rejectReason}
            onChange={(e) => setRejectReason(e.target.value)}
            placeholder="e.g. Work order budget exhausted or road cutting permission pending."
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
          />
          <button
            onClick={handleReject}
            disabled={actionLoading}
            className="w-full h-11 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl flex items-center justify-center transition-all"
          >
            <span>Confirm Rejection</span>
          </button>
        </div>
      </Modal>

      {/* Ask for Info Modal */}
      <Modal
        isOpen={showInfoModal}
        onClose={() => setShowInfoModal(false)}
        title="Record Note / Ask for Info"
      >
        <div className="space-y-3">
          <p className="text-xs text-text-secondary">
            Append an executive officer review note into the audit trail for this booking:
          </p>
          <textarea
            rows={3}
            value={infoNote}
            onChange={(e) => setInfoNote(e.target.value)}
            placeholder="Enter clarification note..."
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
          />
          <button
            onClick={() => {
              alert('Review note recorded in municipal audit trail.');
              setShowInfoModal(false);
              setInfoNote('');
            }}
            className="w-full h-11 bg-[#1C1C1E] text-white font-bold text-xs rounded-xl flex items-center justify-center"
          >
            <span>Record Review Note</span>
          </button>
        </div>
      </Modal>
    </div>
  );
}
