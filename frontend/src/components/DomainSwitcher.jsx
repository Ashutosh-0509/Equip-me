import React from 'react';
import { RotateCcw, HardHat, Truck, UserCheck, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';

export default function DomainSwitcher({ currentDomain, onSelectDomain, onRefreshData }) {
  const domains = [
    { id: 'contractor', label: 'Contractor', icon: HardHat, role: 'Patel / Sharma Infra' },
    { id: 'provider', label: 'Provider', icon: Truck, role: 'Mahalaxmi Fleet' },
    { id: 'operator', label: 'Operator', icon: UserCheck, role: 'Ramesh Solanki' },
    { id: 'officer', label: 'Officer', icon: ShieldAlert, role: 'Control Room G/N' },
  ];

  const handleReset = async () => {
    if (window.confirm('Reset all demo data back to default fixtures?')) {
      try {
        await api.resetDemoData();
        if (onRefreshData) onRefreshData();
      } catch (err) {
        alert('Failed to reset data: ' + err.message);
      }
    }
  };

  return (
    <div className="w-full bg-[#1C1C1E] text-white border-b border-gray-800 px-3 py-2 shrink-0">
      <div className="max-w-md mx-auto flex items-center justify-between gap-2">
        {/* Domain Tabs */}
        <div className="flex items-center gap-1 bg-[#2C2C2E] p-1 rounded-xl flex-1 overflow-x-auto">
          {domains.map((d) => {
            const Icon = d.icon;
            const active = currentDomain === d.id;
            return (
              <button
                key={d.id}
                onClick={() => onSelectDomain(d.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap flex-1 justify-center ${
                  active
                    ? 'bg-[#FFB400] text-[#1C1C1E] shadow-sm font-bold'
                    : 'text-gray-300 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon size={14} className={active ? 'text-[#1C1C1E]' : 'text-gray-400'} />
                <span>{d.label}</span>
              </button>
            );
          })}
        </div>

        {/* Reset Demo button */}
        <button
          onClick={handleReset}
          title="Reset Demo Data"
          className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors flex items-center gap-1 text-[11px]"
        >
          <RotateCcw size={14} />
          <span className="hidden sm:inline">Reset</span>
        </button>
      </div>
    </div>
  );
}
