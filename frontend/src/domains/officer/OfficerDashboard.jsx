import React, { useEffect, useState } from 'react';
import { ShieldAlert, Check, Clock, AlertTriangle, ArrowRight, ChevronRight, Zap } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';

export default function OfficerDashboard({ onNavigateToVerification, onNavigateToRequests }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [approvingId, setApprovingId] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getOfficerDashboard();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickApprove = async (bookingId, e) => {
    if (e) e.stopPropagation();
    try {
      setApprovingId(bookingId);
      await api.approveOfficerBooking(bookingId, '1-Tap Municipal Approval confirmed by Executive Engineer.');
      alert(`Booking ${bookingId} approved successfully!`);
      await loadDashboard();
    } catch (err) {
      alert('Approval failed: ' + err.message);
    } finally {
      setApprovingId(null);
    }
  };

  const pulse = data?.pulse || { waiting_approval: 4, not_matched: 2, active_today: 18, problems_open: 1 };
  const urgent = data?.urgent_queue || [];

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header (Reference Image 1 Screen 3) */}
      <div className="bg-surface px-4 py-3 border-b border-border-subtle space-y-1.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-[#1C1C1E] text-[#FFB400] flex items-center justify-center font-black text-xs">
              MC
            </div>
            <div>
              <span className="text-xs font-black text-text-primary uppercase tracking-tight block">
                Control Room · Ward G/N
              </span>
              <p className="text-[10px] text-text-muted">Brihanmumbai Municipal Corporation</p>
            </div>
          </div>

          <span className="text-[10px] font-bold text-text-secondary bg-[#F5F5F7] px-2 py-0.5 rounded-full border border-border-subtle">
            Er. Amit Deshmukh
          </span>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Urgent Notification Banner */}
        <div className="bg-[#FFF7E6] border border-[#FFB400]/40 rounded-xl px-3.5 py-2.5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#E67E22] animate-ping" />
            <span className="text-xs font-bold text-[#7E5700]">
              {pulse.waiting_approval + pulse.problems_open} tasks require immediate municipal intervention
            </span>
          </div>
          <button
            onClick={() => onNavigateToRequests('needs_approval')}
            className="text-[11px] font-bold text-[#7E5700] hover:underline"
          >
            View All
          </button>
        </div>

        {/* Operational Pulse 4-Grid (Reference Image 1 Screen 3) */}
        <div>
          <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider block mb-2">
            Operational Pulse
          </span>
          <div className="grid grid-cols-2 gap-3">
            {/* Waiting Approval */}
            <div
              onClick={() => onNavigateToRequests('needs_approval')}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="text-text-secondary font-medium">Waiting Approval</span>
                <span className="w-2 h-2 rounded-full bg-[#E67E22]" />
              </div>
              <span className="text-2xl font-black text-text-primary mt-1 block">
                {pulse.waiting_approval}
              </span>
            </div>

            {/* Not Matched */}
            <div
              onClick={() => onNavigateToRequests('not_matched')}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="text-text-secondary font-medium">Not Matched</span>
                <span className="w-2 h-2 rounded-full bg-gray-400" />
              </div>
              <span className="text-2xl font-black text-text-primary mt-1 block">
                {pulse.not_matched}
              </span>
            </div>

            {/* Active Today */}
            <div
              onClick={() => onNavigateToRequests('active')}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="text-text-secondary font-medium">Active Today</span>
                <span className="w-2 h-2 rounded-full bg-status-green" />
              </div>
              <span className="text-2xl font-black text-text-primary mt-1 block">
                {pulse.active_today}
              </span>
              <span className="text-[9px] text-text-muted">14 jobs in progress</span>
            </div>

            {/* Problems Open */}
            <div
              onClick={() => onNavigateToRequests('issues')}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="text-text-secondary font-medium">Problems Open</span>
                <span className="w-2 h-2 rounded-full bg-status-error" />
              </div>
              <span className="text-2xl font-black text-status-error mt-1 block">
                {pulse.problems_open}
              </span>
              <span className="text-[9px] text-status-error">Breakdown reported</span>
            </div>
          </div>
        </div>

        {/* "Needs You Now" Urgent Approval Queue (Reference Image 1 Screen 3) */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <span className="text-xs font-bold text-text-primary uppercase tracking-wide">
                Needs You Now
              </span>
              <span className="bg-[#D93025] text-white text-[10px] font-bold px-1.5 py-0.2 rounded-full">
                {urgent.length || 2} Urgent
              </span>
            </div>
            <button
              onClick={() => onNavigateToRequests('needs_approval')}
              className="text-[11px] font-semibold text-text-secondary hover:text-text-primary"
            >
              Triage All →
            </button>
          </div>

          {urgent.slice(0, 3).map((item) => (
            <div
              key={item.id}
              className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3 shadow-2xs"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-[#E67E22] bg-[#FEF3C7] px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <Clock size={11} />
                  <span>Approval Timeout: 14m Left</span>
                </span>
                <span className="text-xs font-bold text-text-primary">
                  ₹{Number(item.total || 23200).toLocaleString('en-IN')}
                </span>
              </div>

              <div>
                <h4 className="text-xs font-bold text-text-primary">
                  {item.work_order?.split('·')[1] || 'Storm Water Drain Widening'}
                </h4>
                <p className="text-[11px] text-text-secondary mt-0.5">
                  {item.lines?.[0]?.quantity || 2}x {item.lines?.[0]?.name || 'JCB 3DX Backhoe'} · {item.contractor_company}
                </p>
                <p className="text-[10px] text-text-muted mt-0.5">
                  Scheduled: Tomorrow 08:00 AM · Ward {item.ward}
                </p>
              </div>

              {/* 2-Button Action Bar: Review Details vs Approve (1-Tap) */}
              <div className="pt-2 border-t border-border-subtle/80 flex items-center gap-2">
                <button
                  onClick={() => onNavigateToVerification(item.id)}
                  className="flex-1 h-10 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-xl text-xs font-bold text-text-primary transition-colors"
                >
                  Review Details
                </button>

                <button
                  onClick={(e) => handleQuickApprove(item.id, e)}
                  disabled={approvingId === item.id}
                  className="flex-1 h-10 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1 shadow-sm transition-all"
                >
                  <Zap size={14} />
                  <span>{approvingId === item.id ? 'Approving...' : 'Approve (1-Tap)'}</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
