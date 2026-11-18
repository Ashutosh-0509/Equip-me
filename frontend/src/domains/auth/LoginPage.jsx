import React, { useState } from 'react';
import { HardHat, Truck, Construction, ClipboardCheck, ArrowRight, Building2, Check, ShieldCheck } from 'lucide-react';

export default function LoginPage({ onLogin }) {
  const [selectedRole, setSelectedRole] = useState('Contractor');

  const roles = [
    {
      id: 'Contractor',
      domain: 'contractor',
      title: 'Contractor',
      icon: HardHat,
      desc: 'Manage projects, equipment requests and site activities.',
      identity: {
        name: 'Rajesh Patel',
        company: 'Patel Infrastructure Pvt. Ltd.',
        featureTitle: 'Equipment requests & site bookings',
        featureDesc: 'Create requests, track status and manage site activities.',
      },
    },
    {
      id: 'Provider',
      domain: 'provider',
      title: 'Provider',
      icon: Truck,
      desc: 'Deliver equipment and manage services.',
      identity: {
        name: 'Amit Desai',
        company: 'Mahalaxmi Earthmovers & Fleet',
        featureTitle: 'Incoming demands & fleet dispatch',
        featureDesc: 'Accept requisitions, allocate vehicles and track payouts.',
      },
    },
    {
      id: 'Operator',
      domain: 'operator',
      title: 'Operator',
      icon: Construction,
      desc: 'Oversee operations and site performance.',
      identity: {
        name: 'Ramesh Solanki',
        company: 'Certified Heavy Machine Operator',
        featureTitle: 'Daily shift execution & telematics',
        featureDesc: 'Transit navigation, start code verification & shift execution.',
      },
    },
    {
      id: 'Officer',
      domain: 'officer',
      title: 'Officer',
      icon: ClipboardCheck,
      desc: 'Monitor compliance and approvals.',
      identity: {
        name: 'Er. Amit Deshmukh',
        company: 'BMC · Ward G/North Control Room',
        featureTitle: 'Municipal triage & compliance',
        featureDesc: '1-Tap approvals, live telematics, disputes and audit trails.',
      },
    },
  ];

  const activeRoleData = roles.find((r) => r.id === selectedRole) || roles[0];

  const handleEnterWorkspace = () => {
    onLogin(activeRoleData.domain);
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] flex flex-col justify-center items-center p-4 selection:bg-[#FFB400] selection:text-[#1C1C1E]">
      <div className="w-full max-w-[460px] bg-white rounded-3xl border border-[#E5E7EB] p-6 sm:p-8 shadow-sm flex flex-col space-y-6">
        {/* Brand Header */}
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            {/* Hexagon Shield Check Logo */}
            <div className="w-8 h-8 rounded-xl bg-[#1C1C1E] flex items-center justify-center text-[#FFB400]">
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z"/>
                <path d="m9 12 2 2 4-4"/>
              </svg>
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-[#1C1C1E]">Equip Me</h1>
          </div>
          <p className="text-xs text-[#6B7280] flex items-center gap-1.5 font-medium pl-0.5">
            <span>Demo access</span>
            <span className="w-1 h-1 rounded-full bg-[#FFB400]" />
            <span>Sample data</span>
          </p>
        </div>

        {/* Section Header */}
        <div className="space-y-1">
          <h2 className="text-lg font-bold text-[#1C1C1E]">Choose your workspace</h2>
          <p className="text-xs text-[#6B7280]">
            Select the role that best fits what you want to do today.
          </p>
        </div>

        {/* 2x2 Grid of Role Cards (Exact match to Reference Image) */}
        <div className="grid grid-cols-2 gap-3">
          {roles.map((r) => {
            const Icon = r.icon;
            const isSelected = selectedRole === r.id;

            return (
              <div
                key={r.id}
                onClick={() => setSelectedRole(r.id)}
                className={`p-3.5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between min-h-[110px] ${
                  isSelected
                    ? 'border-[#FFB400] bg-[#FFFBF0] shadow-xs'
                    : 'border-[#E5E7EB] bg-white hover:border-gray-300'
                }`}
              >
                {/* Top row: Icon & Radio/Check circle */}
                <div className="flex items-center justify-between">
                  <div className="text-[#1C1C1E]">
                    <Icon size={22} strokeWidth={2} />
                  </div>

                  {isSelected ? (
                    <div className="w-5 h-5 rounded-full bg-[#FFB400] text-[#1C1C1E] flex items-center justify-center shadow-2xs">
                      <Check size={12} strokeWidth={3} />
                    </div>
                  ) : (
                    <div className="w-5 h-5 rounded-full border border-gray-300" />
                  )}
                </div>

                {/* Bottom info */}
                <div className="mt-2 space-y-0.5">
                  <h3 className="text-xs font-bold text-[#1C1C1E]">{r.title}</h3>
                  <p className="text-[10px] text-[#6B7280] leading-tight line-clamp-2">
                    {r.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Role Preview Box (Exact match to Reference Image) */}
        <div className="bg-[#FFFBF0] rounded-2xl border border-[#FDE68A] p-4 space-y-3">
          <div>
            <span className="text-[11px] font-bold text-[#D97706] uppercase tracking-wide block">
              {activeRoleData.title}
            </span>
            <h3 className="text-base font-extrabold text-[#1C1C1E] mt-0.5">
              {activeRoleData.identity.name}
            </h3>
            <p className="text-xs text-[#6B7280] mt-0.5">
              {activeRoleData.identity.company}
            </p>
          </div>

          <div className="pt-2.5 border-t border-[#FDE68A]/70 flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-[#FEF3C7] text-[#92400E] flex items-center justify-center shrink-0">
              <Building2 size={16} />
            </div>
            <div>
              <h4 className="text-xs font-bold text-[#1C1C1E]">
                {activeRoleData.identity.featureTitle}
              </h4>
              <p className="text-[11px] text-[#6B7280] leading-tight">
                {activeRoleData.identity.featureDesc}
              </p>
            </div>
          </div>
        </div>

        {/* Big Yellow Action Button (Exact match to Reference Image) */}
        <button
          onClick={handleEnterWorkspace}
          className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] active:scale-[0.99] text-[#1C1C1E] font-bold text-sm sm:text-base rounded-2xl flex items-center justify-center gap-2 shadow-sm transition-all"
        >
          <span>Enter {activeRoleData.title} workspace</span>
          <ArrowRight size={18} />
        </button>

        {/* Bottom Notice (Exact match to Reference Image) */}
        <div className="bg-[#FFFDF7] rounded-xl border border-[#FDE68A]/60 p-3 flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-full bg-[#FEF3C7] text-[#D97706] flex items-center justify-center shrink-0">
            <ShieldCheck size={14} />
          </div>
          <p className="text-[11px] text-[#6B7280] leading-tight">
            No password required. Data resets when you reload; switching roles keeps this session’s changes.
          </p>
        </div>
      </div>
    </div>
  );
}
