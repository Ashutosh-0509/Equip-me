import React, { useEffect, useState } from 'react';
import { User, ShieldCheck, FileCheck, Phone, Mail, Building2, LogOut } from 'lucide-react';
import { api } from '../../services/api';

export default function ContractorProfile({ onLogout }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await api.getContractorProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20 p-4 space-y-4 bg-white">
      <h2 className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wider">Contractor Profile</h2>

      {/* Main Profile Card (Reference Image 4 Screen 2) */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-5 text-center space-y-3 shadow-2xs">
        <div className="w-16 h-16 rounded-full bg-[#FFFBF0] text-[#7E5700] border-2 border-[#FFB400]/40 flex items-center justify-center mx-auto text-xl font-bold">
          SI
        </div>

        <div>
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#FFFBF0] text-[#7E5700] border border-[#FFB400]/30">
            Registered Civil Contractor
          </span>
          <h3 className="text-base font-bold text-[#1C1C1E] mt-1">
            {profile?.company || 'Sharma Infra & Co.'}
          </h3>
          <p className="text-xs text-[#6B6B6B] mt-0.5">
            {profile?.contact_person || 'Rajesh Sharma'} · {profile?.phone || '+91 98201 44512'}
          </p>
        </div>

        {/* 2 Big Counters (Active Tasks / Completed) */}
        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#E5E5EA]">
          <div className="bg-[#F5F5F5] p-3 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-bold text-[#6B6B6B] uppercase tracking-wider block">
              Active Tasks
            </span>
            <span className="text-2xl font-black text-[#1C1C1E] mt-1 block">
              {String(profile?.active_tasks ?? 1).padStart(2, '0')}
            </span>
          </div>

          <div className="bg-[#F5F5F5] p-3 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-bold text-[#6B6B6B] uppercase tracking-wider block">
              Completed
            </span>
            <span className="text-2xl font-black text-[#1C1C1E] mt-1 block">
              {String(profile?.completed_tasks ?? 48).padStart(2, '0')}
            </span>
          </div>
        </div>
      </div>

      {/* Municipal Registration Details */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-3 text-xs">
        <span className="text-[11px] font-bold text-[#6B6B6B] uppercase tracking-wider block">
          Municipal Registration & Compliance
        </span>

        <div className="space-y-2">
          <div className="flex items-center justify-between py-1.5 border-b border-[#E5E5EA]">
            <span className="text-[#6B6B6B]">Registration ID:</span>
            <span className="font-semibold text-[#1C1C1E] font-mono">
              {profile?.registration_no || 'BMC/CIVIL/2019/312'}
            </span>
          </div>

          <div className="flex items-center justify-between py-1.5 border-b border-[#E5E5EA]">
            <span className="text-[#6B6B6B]">Assigned Ward:</span>
            <span className="font-semibold text-[#1C1C1E]">Ward H/West (Santacruz)</span>
          </div>

          <div className="flex items-center justify-between py-1.5">
            <span className="text-[#6B6B6B]">Safety & Compliance:</span>
            <span className="font-bold text-[#1E9E5A] flex items-center gap-1">
              <ShieldCheck size={14} />
              <span>100% Verified</span>
            </span>
          </div>
        </div>
      </div>

      {/* Log Out from Device Button (Reference Image 4 Screen 2) */}
      <div className="pt-2">
        <button
          onClick={onLogout}
          className="w-full h-12 bg-white hover:bg-red-50 border border-red-200 text-[#D93025] rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-colors"
        >
          <LogOut size={14} />
          <span>Log Out from Device</span>
        </button>
      </div>

      <div className="text-center pt-1">
        <span className="text-[11px] text-[#6B6B6B]">
          Brihanmumbai Municipal Corporation · Civil Machinery Pool System
        </span>
      </div>
    </div>
  );
}
