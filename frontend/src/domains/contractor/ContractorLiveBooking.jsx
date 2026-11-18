import React, { useEffect, useState } from 'react';
import { ArrowLeft, Phone, Truck, User, MapPin, AlertTriangle, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';
import Modal from '../../components/Modal';

export default function ContractorLiveBooking({ bookingId, onBack, onRefresh }) {
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDisputeModal, setShowDisputeModal] = useState(false);
  const [disputeCategory, setDisputeCategory] = useState('Breakdown');
  const [disputeDesc, setDisputeDesc] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadBooking();
  }, [bookingId]);

  const loadBooking = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorBooking(bookingId || 'BMC-8845');
      setBooking(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartShift = async () => {
    if (!booking) return;
    try {
      setActionLoading(true);
      // Operator start verification with the pin
      await api.verifyOperatorStart(booking.id, booking.start_pin || '8429');
      await loadBooking();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert('Error starting shift: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleEndShift = async () => {
    if (!booking) return;
    try {
      setActionLoading(true);
      await api.verifyOperatorEnd(booking.id, booking.end_pin || '6250');
      await loadBooking();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert('Error ending shift: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReportDispute = async () => {
    if (!disputeDesc || disputeDesc.length < 5) {
      alert('Please enter a description for the dispute.');
      return;
    }
    try {
      setActionLoading(true);
      await api.reportContractorDispute(booking.id, disputeCategory, disputeDesc);
      setShowDisputeModal(false);
      setDisputeDesc('');
      await loadBooking();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert('Failed to report issue: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading || !booking) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-xs text-text-muted">
        Loading live booking telemetry...
      </div>
    );
  }

  const assignedUnit = booking.assignments?.[0] || {};
  const isArrived = booking.status === 'arrived';
  const isWorking = booking.status === 'working';
  const isAwaitingEnd = booking.status === 'awaiting_end';
  const isCompleted = booking.status === 'completed';

  // PIN characters
  const pinDigits = (booking.start_pin || '8429').slice(0, 4).split('');

  return (
    <div className="flex flex-col min-h-full pb-24 bg-[#F8F9FA]">
      {/* Header */}
      <div className="sticky top-0 z-20 bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <button onClick={onBack} className="p-1 -ml-1 text-text-secondary hover:text-text-primary rounded-lg">
          <ArrowLeft size={18} />
        </button>
        <div className="text-center">
          <h2 className="text-xs font-bold text-text-primary">{booking.id}</h2>
          <span className="text-[10px] text-text-muted">Ward {booking.ward} · Sub-Division</span>
        </div>
        <StatusBadge status={booking.status} label={booking.status_label} />
      </div>

      <div className="p-4 space-y-4">
        {/* Status Notification Banner */}
        {isArrived && (
          <div className="bg-[#DCFCE7] border border-[#BBF7D0] rounded-xl px-3.5 py-2.5 flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#16A34A] animate-ping shrink-0" />
            <div>
              <div className="text-xs font-bold text-[#16A34A]">Operator Arrived at Site</div>
              <p className="text-[11px] text-[#166534]">
                Hand over the start verification code below to begin the municipal shift.
              </p>
            </div>
          </div>
        )}

        {isWorking && (
          <div className="bg-[#DCFCE7] border border-[#BBF7D0] rounded-xl px-3.5 py-2.5 flex items-center gap-2.5">
            <CheckCircle2 size={18} className="text-[#16A34A] shrink-0" />
            <div>
              <div className="text-xs font-bold text-[#16A34A]">Work in Progress · Machine Operational</div>
              <p className="text-[11px] text-[#166534]">
                Machine is live on site. Telematics and shift clock active.
              </p>
            </div>
          </div>
        )}

        {/* Prominent Verification Arrival PIN Card (Reference Image 4 Screen 7) */}
        {!isCompleted && (
          <div className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3.5 shadow-2xs">
            <div className="text-center space-y-1">
              <span className="text-xs font-bold text-text-primary uppercase tracking-wide">
                {isWorking ? 'End Handover Code' : 'Verify Arrival PIN'}
              </span>
              <p className="text-[11px] text-text-secondary">
                {isWorking
                  ? 'Provide this code at end of shift to complete verification'
                  : `Share this 4-digit code with operator ${assignedUnit.operator_name || 'Ramesh Solanki'} to begin shift`}
              </p>
            </div>

            {/* 4 Digit Boxes */}
            <div className="flex items-center justify-center gap-2.5 py-1">
              {(isWorking ? (booking.end_pin || '6250').slice(0, 4).split('') : pinDigits).map(
                (digit, idx) => (
                  <div
                    key={idx}
                    className="w-12 h-14 rounded-xl bg-[#F5F5F7] border-2 border-border-subtle flex items-center justify-center text-2xl font-bold text-[#1C1C1E] tracking-wider shadow-inner"
                  >
                    {digit}
                  </div>
                )
              )}
            </div>

            {/* Action buttons */}
            {isArrived && (
              <button
                onClick={handleStartShift}
                disabled={actionLoading}
                className="w-full h-12 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                <span>Confirm & Start Work</span>
              </button>
            )}

            {(isWorking || isAwaitingEnd) && (
              <button
                onClick={handleEndShift}
                disabled={actionLoading}
                className="w-full h-12 bg-[#1C1C1E] hover:bg-black text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                <span>Confirm Inspection & Complete Shift</span>
              </button>
            )}
          </div>
        )}

        {/* Assigned Operator & Vehicle Card */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3">
          <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider block">
            Assigned Machine & Crew
          </span>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-surface-subtle border border-border-subtle flex items-center justify-center text-text-secondary">
                <Truck size={20} className="text-[#7E5700]" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-text-primary">
                  {booking.lines?.[0]?.name || 'JCB 3DX Heavy Loader'}
                </h4>
                <p className="text-[11px] text-text-secondary mt-0.5">
                  Reg: {assignedUnit.vehicle_reg || 'MH-02-EQ-4491'}
                </p>
              </div>
            </div>

            <span className="text-xs font-bold text-text-primary">
              ₹{Number(booking.lines?.[0]?.rate || 1450).toLocaleString('en-IN')}/hr
            </span>
          </div>

          <div className="pt-2.5 border-t border-border-subtle/70 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-surface-subtle flex items-center justify-center text-text-primary text-xs font-bold">
                {assignedUnit.operator_name?.[0] || 'R'}
              </div>
              <div>
                <span className="text-xs font-bold text-text-primary block">
                  {assignedUnit.operator_name || 'Ramesh Solanki'}
                </span>
                <span className="text-[10px] text-text-muted">Municipal Certified Operator</span>
              </div>
            </div>

            <a
              href={`tel:${assignedUnit.operator_phone || '+919820144554'}`}
              className="px-3 py-1.5 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-lg text-xs font-bold text-text-primary flex items-center gap-1.5 transition-colors"
            >
              <Phone size={13} />
              <span>Call</span>
            </a>
          </div>
        </div>

        {/* Site Details Card */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5 text-xs">
          <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider block">
            Deployment Site
          </span>
          <div className="flex items-start gap-2 text-text-secondary">
            <MapPin size={15} className="text-text-muted shrink-0 mt-0.5" />
            <span>{booking.address}</span>
          </div>
          <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-[11px]">
            <span className="text-text-muted">Work Order:</span>
            <span className="font-semibold text-text-primary">{booking.work_order}</span>
          </div>
          <div className="flex items-center justify-between text-[11px]">
            <span className="text-text-muted">Fleet Provider:</span>
            <span className="font-semibold text-text-primary">{booking.provider_company}</span>
          </div>
        </div>

        {/* Dispute / Issue Trigger */}
        <div className="pt-2 flex justify-center">
          <button
            onClick={() => setShowDisputeModal(true)}
            className="text-xs font-bold text-[#D93025] hover:underline flex items-center gap-1.5"
          >
            <AlertTriangle size={14} />
            <span>Report Breakdown / Raise Dispute</span>
          </button>
        </div>
      </div>

      {/* Dispute Modal */}
      <Modal
        isOpen={showDisputeModal}
        onClose={() => setShowDisputeModal(false)}
        title="Report Breakdown or Dispute"
      >
        <div className="space-y-3">
          <div>
            <label className="text-xs font-bold text-text-primary block mb-1">Issue Category</label>
            <select
              value={disputeCategory}
              onChange={(e) => setDisputeCategory(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
            >
              <option value="Breakdown">Mechanical Breakdown / Leak</option>
              <option value="Delay">Operator Delay / No Show</option>
              <option value="Safety">Jobsite Safety Concern</option>
              <option value="Billing">Rate / Overtime Dispute</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-bold text-text-primary block mb-1">Description</label>
            <textarea
              rows={3}
              placeholder="Describe machine issue or reason for escalation..."
              value={disputeDesc}
              onChange={(e) => setDisputeDesc(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
            />
          </div>

          <button
            onClick={handleReportDispute}
            disabled={actionLoading}
            className="w-full h-11 bg-[#D93025] hover:bg-red-700 text-white font-bold text-xs rounded-xl flex items-center justify-center transition-all disabled:opacity-50"
          >
            <span>Submit Issue to Municipal Control Room</span>
          </button>
        </div>
      </Modal>
    </div>
  );
}
