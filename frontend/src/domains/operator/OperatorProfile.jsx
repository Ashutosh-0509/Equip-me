import React, { useEffect, useState } from 'react';
import { User, ShieldCheck, Award, Phone, Truck, LogOut } from 'lucide-react';
import { api } from '../../services/api';

export default function OperatorProfile({ onLogout }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await api.getOperatorProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20 p-4 space-y-4 bg-white">
      <h2 className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wider">Operator Profile</h2>

      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-5 text-center space-y-3 shadow-2xs">
        <div className="w-16 h-16 rounded-full bg-[#FFFBF0] text-[#7E5700] border-2 border-[#FFB400]/40 flex items-center justify-center mx-auto text-xl font-black">
          RP
        </div>

        <div>
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#DCFCE7] text-[#16A34A]">
            BMC Certified Heavy Machinery Operator
          </span>
          <h3 className="text-base font-bold text-[#1C1C1E] mt-1">
            {profile?.name || 'Ramesh Solanki'}
          </h3>
          <p className="text-xs text-[#6B6B6B] mt-0.5">
            Fleet: {profile?.provider || 'Mahalaxmi Earthmovers & Fleet'}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#E5E5EA] text-xs">
          <div className="bg-[#F5F5F5] p-2.5 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-semibold text-[#6B6B6B] block">Safety Rating</span>
            <span className="text-lg font-bold text-[#1C1C1E] mt-0.5 block">★ 4.9 / 5.0</span>
          </div>

          <div className="bg-[#F5F5F5] p-2.5 rounded-xl border border-[#E5E5EA]">
            <span className="text-[10px] font-semibold text-[#6B6B6B] block">Total Shifts Logged</span>
            <span className="text-lg font-bold text-[#1C1C1E] mt-0.5 block">48 Shifts</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-3.5 space-y-2.5 text-xs">
        <span className="text-[11px] font-bold text-[#6B6B6B] uppercase tracking-wider block">
          Credentials & Licences
        </span>

        <div className="divide-y divide-[#E5E5EA]">
          <div className="py-2 flex items-center justify-between">
            <span className="text-[#6B6B6B]">Commercial Heavy Badge:</span>
            <span className="font-mono font-bold text-[#1C1C1E]">MH-OP-1005</span>
          </div>
          <div className="py-2 flex items-center justify-between">
            <span className="text-[#6B6B6B]">Registered Mobile:</span>
            <span className="font-semibold text-[#1C1C1E]">{profile?.phone || '+91 98201 44554'}</span>
          </div>
          <div className="py-2 flex items-center justify-between">
            <span className="text-[#6B6B6B]">Medical & Fitness Certificate:</span>
            <span className="font-bold text-[#1E9E5A] flex items-center gap-1">
              <ShieldCheck size={14} />
              <span>Valid till Dec 2026</span>
            </span>
          </div>
        </div>
      </div>

      {/* Log Out from Device Button */}
      <div className="pt-2">
        <button
          onClick={onLogout}
          className="w-full h-12 bg-white hover:bg-red-50 border border-red-200 text-[#D93025] rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-colors"
        >
          <LogOut size={14} />
          <span>Log Out from Device</span>
        </button>
      </div>
    </div>
  );
}
