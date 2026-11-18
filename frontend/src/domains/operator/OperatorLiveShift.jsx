import React, { useEffect, useState } from 'react';
import { Clock, Phone, AlertCircle, CheckCircle2, ArrowRight, ShieldAlert } from 'lucide-react';
import { api } from '../../services/api';
import Modal from '../../components/Modal';

export default function OperatorLiveShift({ bookingId, onShiftComplete }) {
  const [booking, setBooking] = useState(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(14105); // Default to ~03:55:05 from reference
  const [showEndModal, setShowEndModal] = useState(false);
  const [endCode, setEndCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadBooking();
    // Live ticking timer
    const interval = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [bookingId]);

  const loadBooking = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorBooking(bookingId || 'BMC-8846');
      setBooking(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatElapsed = (sec) => {
    const hrs = String(Math.floor(sec / 3600)).padStart(2, '0');
    const mins = String(Math.floor((sec % 3600) / 60)).padStart(2, '0');
    const s = String(sec % 60).padStart(2, '0');
    return `${hrs}:${mins}:${s}`;
  };

  const handleRequestEnd = async () => {
    if (!booking) return;
    try {
      setActionLoading(true);
      await api.requestOperatorEnd(booking.id);
      setShowEndModal(true);
    } catch (err) {
      alert('Error requesting end code: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleVerifyEnd = async () => {
    if (!endCode || endCode.length !== 4) {
      alert('Please enter the 4-digit handover code.');
      return;
    }
    try {
      setActionLoading(true);
      await api.verifyOperatorEnd(booking.id, endCode);
      alert('Shift complete! Machine safely locked and hours verified.');
      setShowEndModal(false);
      onShiftComplete();
    } catch (err) {
      alert('Failed to complete shift: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const assignedUnit = booking?.assignments?.[0] || {};
  const progressPercent = Math.min(100, Math.round((elapsedSeconds / 28800) * 100)) || 46;

  return (
    <div className="flex flex-col min-h-full pb-20 bg-[#F8F9FA]">
      {/* Top Header */}
      <div className="bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#16A34A] animate-ping" />
          <span className="text-xs font-bold text-text-primary">BMC Operator</span>
        </div>
        <span className="text-xs font-mono font-bold text-text-secondary">
          {booking?.id || '#BMC-8842-JCB'}
        </span>
      </div>

      <div className="p-4 space-y-4">
        {/* Operational Status Green Banner (Reference Image 2 Screen 3) */}
        <div className="bg-[#16A34A] text-white rounded-xl px-4 py-2.5 flex items-center justify-between shadow-xs">
          <span className="text-xs font-black uppercase tracking-wider">
            WORK IN PROGRESS · MACHINE OPERATIONAL
          </span>
          <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
        </div>

        {/* Live Running Digital Clock Card */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-5 text-center space-y-3 shadow-2xs">
          <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider flex items-center justify-center gap-1.5">
            <Clock size={14} className="text-[#E67E22]" />
            <span>Elapsed Work Time</span>
          </span>

          {/* Running Clock readout */}
          <div className="font-mono text-4xl sm:text-5xl font-black text-text-primary tracking-wider py-1">
            {formatElapsed(elapsedSeconds)}
          </div>

          {/* Target Progress Bar */}
          <div className="space-y-1.5 pt-2 border-t border-border-subtle/80">
            <div className="flex items-center justify-between text-xs">
              <span className="text-text-secondary font-medium">Shift Target Progress</span>
              <span className="font-bold text-[#7E5700]">{progressPercent}%</span>
            </div>
            <div className="w-full bg-[#F5F5F7] h-2.5 rounded-full overflow-hidden border border-border-subtle/60">
              <div
                className="bg-[#FFB400] h-full rounded-full transition-all duration-500"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Machine & Site Metadata */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3 text-xs shadow-2xs">
          {/* Equipment */}
          <div>
            <span className="text-[10px] font-bold text-text-muted uppercase block">Assigned Equipment</span>
            <div className="flex items-center justify-between mt-1">
              <span className="font-bold text-text-primary text-sm">
                {booking?.lines?.[0]?.name || 'JCB 3DX EcoExpert'}
              </span>
              <span className="font-mono font-bold bg-[#F5F5F7] px-2 py-0.5 rounded border border-border-subtle text-text-primary">
                {assignedUnit.vehicle_reg || 'MH-02-EQ-4491'}
              </span>
            </div>
          </div>

          {/* Site */}
          <div className="pt-2 border-t border-border-subtle/70">
            <span className="text-[10px] font-bold text-text-muted uppercase block">Assigned Work Site</span>
            <p className="font-medium text-text-primary mt-1 line-clamp-2">
              {booking?.address || 'Santacruz SV Road Storm Water Drain, Gate 3'}
            </p>
          </div>

          {/* Supervisor Card */}
          <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between">
            <div>
              <span className="text-[10px] font-bold text-status-green flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-status-green" />
                <span>Supervisor On Duty</span>
              </span>
              <span className="font-bold text-text-primary block mt-0.5">Rajesh V. Sharma</span>
              <span className="text-[10px] text-text-muted">Ward K/W - Zone 2 · Shift Lead</span>
            </div>

            <a
              href="tel:+919820144521"
              className="px-3 py-1.5 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-xl text-xs font-bold text-text-primary flex items-center gap-1.5"
            >
              <Phone size={13} className="text-[#7E5700]" />
              <span>Call</span>
            </a>
          </div>
        </div>

        {/* Warning Note */}
        <div className="bg-[#FFF7E6] border border-[#FFB400]/40 rounded-xl p-3 flex items-start gap-2 text-[11px] text-[#7E5700]">
          <AlertCircle size={15} className="shrink-0 mt-0.5" />
          <span>
            Ensure fuel log is updated and hydraulic pressure verified before requesting handover code.
          </span>
        </div>

        {/* Primary Action Button */}
        <button
          onClick={handleRequestEnd}
          disabled={actionLoading}
          className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-extrabold text-sm rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all tracking-wide disabled:opacity-50"
        >
          <span>Shift Complete · Request End Code</span>
          <ArrowRight size={18} />
        </button>
      </div>

      {/* End Code Modal */}
      <Modal
        isOpen={showEndModal}
        onClose={() => setShowEndModal(false)}
        title="Enter Shift Handover Code"
      >
        <div className="space-y-4">
          <p className="text-xs text-text-secondary">
            Obtain the 4-digit End Handover PIN from the contractor site supervisor to officially log out of shift:
          </p>

          <input
            type="text"
            maxLength={4}
            placeholder="e.g. 6250"
            value={endCode}
            onChange={(e) => setEndCode(e.target.value)}
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-3 text-center text-2xl font-black font-mono tracking-widest focus:ring-1 focus:ring-primary"
          />

          <div className="text-[11px] text-text-muted text-center">
            Demo End Code for this booking: <strong>{booking?.end_pin || '6250'}</strong>
          </div>

          <button
            onClick={handleVerifyEnd}
            disabled={actionLoading}
            className="w-full h-12 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center transition-all disabled:opacity-50"
          >
            <span>Verify & Complete Machine Handover</span>
          </button>
        </div>
      </Modal>
    </div>
  );
}
