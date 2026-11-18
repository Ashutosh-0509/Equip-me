import React, { useEffect, useState } from 'react';
import { Search, Building2, Truck, Phone, Plus, ShieldCheck, AlertCircle } from 'lucide-react';
import { api } from '../../services/api';
import Modal from '../../components/Modal';

export default function OfficerDirectory() {
  const [activeTab, setActiveTab] = useState('providers');
  const [searchQuery, setSearchQuery] = useState('');
  const [data, setData] = useState({ stats: {}, providers: [], contractors: [] });
  const [filterChip, setFilterChip] = useState('All');
  const [loading, setLoading] = useState(true);

  // New Vendor Modal
  const [showVendorModal, setShowVendorModal] = useState(false);
  const [vendorName, setVendorName] = useState('');
  const [vendorDepot, setVendorDepot] = useState('Bandra Municipal Yard');
  const [vendorPhone, setVendorPhone] = useState('+91 98201 00000');

  useEffect(() => {
    loadDirectory();
  }, [activeTab, searchQuery]);

  const loadDirectory = async () => {
    try {
      setLoading(true);
      const res = await api.getOfficerDirectory(activeTab, searchQuery);
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterVendor = () => {
    if (!vendorName) {
      alert('Please enter vendor firm name.');
      return;
    }
    alert(`Vendor "${vendorName}" registered and added to Municipal Machinery Pool.`);
    setShowVendorModal(false);
    setVendorName('');
  };

  const stats = data.stats || { registered_providers: 42, civil_contractors: 18, compliance_rate: '98.4%' };
  const providers = data.providers || [];
  const contractors = data.contractors || [];

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header & Metrics (Reference Image 1 Screen 2) */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle space-y-2.5">
        <div>
          <span className="text-[10px] font-bold text-text-muted uppercase">Control Room · Ward G/N</span>
          <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
            Municipal Directory
          </h2>
        </div>

        {/* 3 Metric Pills */}
        <div className="grid grid-cols-3 gap-2 py-1">
          <div className="bg-surface-subtle p-2 rounded-xl text-center border border-border-subtle/80">
            <span className="text-base font-black text-text-primary block">
              {stats.registered_providers}
            </span>
            <span className="text-[9px] font-semibold text-text-secondary leading-tight block">
              Registered Providers
            </span>
          </div>

          <div className="bg-surface-subtle p-2 rounded-xl text-center border border-border-subtle/80">
            <span className="text-base font-black text-text-primary block">
              {stats.civil_contractors}
            </span>
            <span className="text-[9px] font-semibold text-text-secondary leading-tight block">
              Civil Contractors
            </span>
          </div>

          <div className="bg-surface-subtle p-2 rounded-xl text-center border border-border-subtle/80">
            <span className="text-base font-black text-status-green block">
              {stats.compliance_rate}
            </span>
            <span className="text-[9px] font-semibold text-text-secondary leading-tight block">
              Compliance Rate
            </span>
          </div>
        </div>

        {/* Tabs: Providers vs Contractors */}
        <div className="flex items-center bg-[#F5F5F7] p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('providers')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'providers' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Providers ({stats.registered_providers})
          </button>
          <button
            onClick={() => setActiveTab('contractors')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'contractors' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Contractors ({stats.civil_contractors})
          </button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            type="text"
            placeholder="Search by firm, vendor ID, or machinery..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl pl-9 pr-3 py-1.5 text-xs text-text-primary placeholder:text-text-muted focus:ring-1 focus:ring-primary"
          />
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {['All (42)', 'Grade A (28)', 'Papers Expired (2)'].map((chip) => {
            const active = filterChip === chip;
            return (
              <button
                key={chip}
                onClick={() => setFilterChip(chip)}
                className={`px-3 py-1 rounded-full text-[11px] font-semibold whitespace-nowrap transition-all ${
                  active ? 'bg-[#1C1C1E] text-white' : 'bg-[#F5F5F7] text-text-secondary hover:bg-gray-200'
                }`}
              >
                {chip}
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-4 space-y-3">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading municipal directory...</div>
        ) : activeTab === 'providers' ? (
          providers.map((p) => (
            <div
              key={p.id}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3 shadow-2xs"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-xs font-bold text-text-primary">{p.name}</h4>
                  <p className="text-[11px] text-text-secondary mt-0.5">{p.depot}</p>
                </div>
                <span className="text-[10px] font-bold bg-[#DCFCE7] text-[#16A34A] px-2 py-0.5 rounded-full">
                  {p.grade}
                </span>
              </div>

              <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-xs">
                <span className="font-semibold text-text-secondary text-[11px]">
                  Fleet Capacity: <strong>{p.fleet_count} Heavy Units</strong>
                </span>

                <div className="flex items-center gap-2">
                  <a
                    href={`tel:${p.phone}`}
                    className="px-3 py-1.5 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center gap-1 shadow-2xs"
                  >
                    <Phone size={12} />
                    <span>Call (Masked)</span>
                  </a>
                </div>
              </div>
            </div>
          ))
        ) : (
          contractors.map((c) => (
            <div
              key={c.id}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5 shadow-2xs"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-xs font-bold text-text-primary">{c.name}</h4>
                  <p className="text-[11px] text-text-secondary mt-0.5">{c.contact_person}</p>
                </div>
                <span className="text-[10px] font-bold bg-[#FFF7E6] text-[#7E5700] px-2 py-0.5 rounded-full">
                  {c.grade}
                </span>
              </div>

              <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-xs text-text-secondary">
                <span className="text-[11px]">Reg: {c.registration_no}</span>
                <span className="text-[11px] font-bold text-status-green">Compliance 100%</span>
              </div>
            </div>
          ))
        )}

        {/* Register New Vendor Button */}
        <div className="pt-2">
          <button
            onClick={() => setShowVendorModal(true)}
            className="w-full h-12 bg-surface hover:bg-surface-subtle border-2 border-dashed border-[#FFB400] rounded-xl text-xs font-bold text-[#7E5700] flex items-center justify-center gap-2 transition-colors"
          >
            <Plus size={16} />
            <span>Register New Machinery Vendor</span>
          </button>
        </div>
      </div>

      {/* Register Vendor Modal */}
      <Modal
        isOpen={showVendorModal}
        onClose={() => setShowVendorModal(false)}
        title="Register New Machinery Vendor"
      >
        <div className="space-y-3">
          <div>
            <label className="text-xs font-bold text-text-primary block mb-1">Firm / Vendor Name</label>
            <input
              type="text"
              placeholder="e.g. Apex Earthworks & Cranes"
              value={vendorName}
              onChange={(e) => setVendorName(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-text-primary block mb-1">Base Depot Address</label>
            <input
              type="text"
              value={vendorDepot}
              onChange={(e) => setVendorDepot(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-text-primary block mb-1">Dispatch Contact Number</label>
            <input
              type="text"
              value={vendorPhone}
              onChange={(e) => setVendorPhone(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary"
            />
          </div>

          <button
            onClick={handleRegisterVendor}
            className="w-full h-11 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center shadow-sm"
          >
            <span>Register & Issue Pool Access</span>
          </button>
        </div>
      </Modal>
    </div>
  );
}
