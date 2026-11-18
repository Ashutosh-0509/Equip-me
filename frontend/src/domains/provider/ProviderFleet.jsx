import React, { useEffect, useState } from 'react';
import { Truck, User, Plus, Edit2, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../../services/api';

export default function ProviderFleet({ onNavigateToAddEdit }) {
  const [activeTab, setActiveTab] = useState('vehicles');
  const [fleet, setFleet] = useState({ vehicles: [], operators: [], counts: {} });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFleet();
  }, []);

  const loadFleet = async () => {
    try {
      setLoading(true);
      const data = await api.getProviderFleet();
      setFleet(data || { vehicles: [], operators: [], counts: {} });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const counts = fleet.counts || {};

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle space-y-2.5">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
            Fleet & Operators
          </h2>
          <button
            onClick={() => onNavigateToAddEdit()}
            className="px-3 py-1.5 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] rounded-xl text-xs font-bold flex items-center gap-1 shadow-2xs transition-all"
          >
            <Plus size={14} />
            <span>Add Machine</span>
          </button>
        </div>

        {/* Vehicles / Operators Tabs */}
        <div className="flex items-center bg-[#F5F5F7] p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('vehicles')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'vehicles' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Vehicles ({fleet.vehicles.length || 8})
          </button>
          <button
            onClick={() => setActiveTab('operators')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'operators' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Operators ({fleet.operators.length || 6})
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Availability Counters (Reference Image 3 Screen 2) */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-surface rounded-2xl border border-border-subtle p-3 flex items-center gap-3 shadow-2xs">
            <div className="w-9 h-9 rounded-xl bg-[#DCFCE7] text-[#16A34A] flex items-center justify-center font-bold">
              <CheckCircle2 size={18} />
            </div>
            <div>
              <span className="text-sm font-bold text-text-primary block">
                {counts.free_vehicles ?? 5} Available
              </span>
              <span className="text-[10px] text-text-muted">Free for dispatch</span>
            </div>
          </div>

          <div className="bg-surface rounded-2xl border border-border-subtle p-3 flex items-center gap-3 shadow-2xs">
            <div className="w-9 h-9 rounded-xl bg-[#FEF3C7] text-[#B45309] flex items-center justify-center font-bold">
              <Truck size={18} />
            </div>
            <div>
              <span className="text-sm font-bold text-text-primary">
                {counts.booked_vehicles ?? 2} On Shift
              </span>
              <span className="text-[10px] text-text-muted">Active job sites</span>
            </div>
          </div>
        </div>

        {/* Units Feed */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold text-text-primary uppercase tracking-wide">
            {activeTab === 'vehicles' ? 'Active Machinery Units' : 'Certified Machine Operators'}
          </h3>

          {loading ? (
            <div className="py-12 text-center text-xs text-text-muted">Loading fleet assets...</div>
          ) : activeTab === 'vehicles' ? (
            fleet.vehicles.map((v) => (
              <div
                key={v.id}
                className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3 shadow-2xs"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl bg-surface-subtle border border-border-subtle flex items-center justify-center text-text-secondary shrink-0">
                      <Truck size={22} className="text-[#7E5700]" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-text-primary">{v.model}</h4>
                      <p className="text-[11px] font-mono text-text-secondary mt-0.5">{v.registration}</p>
                    </div>
                  </div>

                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      v.status === 'available'
                        ? 'bg-[#DCFCE7] text-[#16A34A]'
                        : 'bg-[#FEF3C7] text-[#B45309]'
                    }`}
                  >
                    {v.status === 'available' ? 'Available' : 'Booked'}
                  </span>
                </div>

                <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-xs">
                  <div>
                    <span className="font-bold text-text-primary">₹{Number(v.rate).toLocaleString('en-IN')}</span>
                    <span className="text-text-muted text-[10px]"> / hr</span>
                  </div>

                  <button
                    onClick={() => onNavigateToAddEdit(v)}
                    className="text-xs font-bold text-[#7E5700] hover:underline flex items-center gap-1"
                  >
                    <Edit2 size={12} />
                    <span>Edit Rates</span>
                  </button>
                </div>
              </div>
            ))
          ) : (
            fleet.operators.map((o) => (
              <div
                key={o.id}
                className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5 shadow-2xs"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-surface-subtle flex items-center justify-center text-text-primary font-bold text-xs">
                      {o.name[0]}
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-text-primary">{o.name}</h4>
                      <p className="text-[11px] text-text-secondary mt-0.5">{o.license}</p>
                    </div>
                  </div>

                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      o.status === 'available'
                        ? 'bg-[#DCFCE7] text-[#16A34A]'
                        : 'bg-[#FEF3C7] text-[#B45309]'
                    }`}
                  >
                    {o.status === 'available' ? 'Available' : 'On Shift'}
                  </span>
                </div>

                <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-xs text-text-secondary">
                  <span>Contact: {o.phone}</span>
                  <span className="text-[10px] font-bold text-status-green">BMC Verified</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
