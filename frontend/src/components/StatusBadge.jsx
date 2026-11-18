import React from 'react';

export default function StatusBadge({ status, label }) {
  const s = (status || '').toLowerCase();
  
  let colorClasses = 'bg-gray-100 text-gray-700 border-gray-200';
  let dotColor = 'bg-gray-400';
  let displayLabel = label || status;

  if (s === 'working' || s === 'completed' || s.includes('normal') || s === 'active') {
    colorClasses = 'bg-[#DCFCE7] text-[#16A34A] border-[#BBF7D0]';
    dotColor = 'bg-[#16A34A]';
  } else if (s === 'pending_approval' || s.includes('approval') || s === 'awaiting_end') {
    colorClasses = 'bg-[#FEF3C7] text-[#B45309] border-[#FDE68A]';
    dotColor = 'bg-[#D97706]';
  } else if (s === 'pending_provider' || s.includes('provider')) {
    colorClasses = 'bg-amber-50 text-amber-900 border-amber-200';
    dotColor = 'bg-amber-500';
  } else if (s === 'in_transit' || s === 'arrived' || s === 'assigned') {
    colorClasses = 'bg-blue-50 text-blue-700 border-blue-200';
    dotColor = 'bg-blue-500';
  } else if (s === 'problem' || s === 'rejected' || s === 'cancelled' || s.includes('breakdown')) {
    colorClasses = 'bg-[#FEE2E2] text-[#D93025] border-[#FECACA]';
    dotColor = 'bg-[#D93025]';
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide border ${colorClasses}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`}></span>
      <span className="capitalize">{displayLabel}</span>
    </span>
  );
}
