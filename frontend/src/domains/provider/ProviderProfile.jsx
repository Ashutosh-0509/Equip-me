import React, { useEffect, useState } from 'react';
import { Building2, DollarSign, FileCheck, PhoneCall, ShieldCheck, ChevronRight, LogOut } from 'lucide-react';
import { api } from '../../services/api';

export default function ProviderProfile({ onLogout }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await api.getProviderProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20 p-4 space-y-4 bg-white">
      {/* Title */}
      <h2 className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wider">
        Provider Profile & Earnings
      </h2>

      {/* Profile Card */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-2.5 shadow-2xs">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-[#FFFBF0] text-[#7E5700] border border-[#FFB400]/40 flex items-center justify-center font-bold text-base">
            MF
          </div>
          <div>
            <h3 className="text-xs font-bold text-[#1C1C1E]">
              {profile?.name || 'Mahalaxmi Earthmovers & Fleet'}
            </h3>
            <p className="text-[11px] text-[#6B6B6B] mt-0.5">
              Authorized Heavy Machinery Supplier · {profile?.depot || 'Depot Bandra West'}
            </p>
          </div>
        </div>

        <div className="pt-2 border-t border-[#E5E5EA] text-xs text-[#6B6B6B] flex items-center justify-between">
          <span>{profile?.phone || '+91 98201 44553'}</span>
          <span className="text-[10px] font-mono text-[#6B6B6B]">GST: {profile?.gstin || '27AAECM4819M1ZV'}</span>
        </div>
      </div>

      {/* Revenue & Payouts Card (Reference Image 3 Screen 5) */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-3.5 shadow-2xs">
        <div className="flex items-center justify-between pb-2 border-b border-[#E5E5EA]">
          <span className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wide">
            Revenue & Payouts (October)
          </span>
          <span className="text-[10px] font-bold text-[#1E9E5A] bg-[#DCFCE7] px-2 py-0.5 rounded-full">
            Active Cycle
          </span>
        </div>

        <div>
          <span className="text-[11px] text-[#6B6B6B] block">Total Settled This Month</span>
          <span className="text-2xl font-black text-[#1C1C1E] mt-0.5 block">
            ₹{Number(profile?.total_settled || 342800).toLocaleString('en-IN')}
          </span>
          <button className="text-[11px] font-bold text-[#7E5700] hover:underline mt-1 block">
            View Detailed Earnings & GST Statements →
          </button>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#E5E5EA]">
          <div className="bg-[#F5F5F5] p-2.5 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-semibold text-[#6B6B6B] block">Pending Clearance</span>
            <span className="text-sm font-bold text-[#1C1C1E] mt-0.5 block">
              ₹{Number(profile?.pending_clearance || 46500).toLocaleString('en-IN')}
            </span>
            <span className="text-[9px] text-[#6B6B6B]">Next settlement: In 2d</span>
          </div>

          <div className="bg-[#F5F5F5] p-2.5 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-semibold text-[#6B6B6B] block">Completed Shifts</span>
            <span className="text-sm font-bold text-[#1C1C1E] mt-0.5 block">
              {profile?.completed_shifts || 34} shifts
            </span>
            <span className="text-[9px] text-[#6B6B6B]">100% verified</span>
          </div>
        </div>
      </div>

      {/* Account, Compliance & Support List */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-3.5 space-y-2 text-xs">
        <span className="text-[11px] font-bold text-[#6B6B6B] uppercase tracking-wider block mb-1">
          Account, Compliance & Support
        </span>

        <div className="divide-y divide-[#E5E5EA]">
          <div className="py-2.5 flex items-center justify-between cursor-pointer hover:bg-[#F5F5F5] px-1 rounded-lg">
            <div className="flex items-center gap-2.5">
              <Building2 size={16} className="text-[#6B6B6B]" />
              <div>
                <span className="font-bold text-[#1C1C1E] block">Bank Account & Settlement</span>
                <span className="text-[10px] text-[#1E9E5A] font-semibold">Verified · HDFC Bank</span>
              </div>
            </div>
            <ChevronRight size={14} className="text-[#6B6B6B]" />
          </div>

          <div className="py-2.5 flex items-center justify-between cursor-pointer hover:bg-[#F5F5F5] px-1 rounded-lg">
            <div className="flex items-center gap-2.5">
              <FileCheck size={16} className="text-[#6B6B6B]" />
              <div>
                <span className="font-bold text-[#1C1C1E] block">Fleet Compliance Papers</span>
                <span className="text-[10px] text-[#6B6B6B]">PUC, Fitness & Commercial Permits</span>
              </div>
            </div>
            <ChevronRight size={14} className="text-[#6B6B6B]" />
          </div>

          <div className="py-2.5 flex items-center justify-between cursor-pointer hover:bg-[#F5F5F5] px-1 rounded-lg">
            <div className="flex items-center gap-2.5">
              <PhoneCall size={16} className="text-[#6B6B6B]" />
              <div>
                <span className="font-bold text-[#1C1C1E] block">Support & Ward Helpline</span>
                <span className="text-[10px] text-[#6B6B6B]">Dedicated Municipal Fleet Dispatch</span>
              </div>
            </div>
            <ChevronRight size={14} className="text-[#6B6B6B]" />
          </div>
        </div>
      </div>

      {/* Log Out from Provider Console Button (Reference Image 3 Screen 5) */}
      <div className="pt-2">
        <button
          onClick={onLogout}
          className="w-full h-12 bg-white hover:bg-red-50 border border-red-200 text-[#D93025] rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-colors"
        >
          <LogOut size={14} />
          <span>Log Out from Provider Console</span>
        </button>
      </div>
    </div>
  );
}
