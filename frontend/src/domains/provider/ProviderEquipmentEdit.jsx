import React, { useState } from 'react';
import { ArrowLeft, Save, Truck, Check, MapPin } from 'lucide-react';
import { api } from '../../services/api';
import SiteLocationMap from '../../components/SiteLocationMap';

export default function ProviderEquipmentEdit({ initialData, onBack, onSaved }) {
  const isEditing = !!initialData?.id;
  const [tab, setTab] = useState(isEditing ? 'edit' : 'add');
  const [loading, setLoading] = useState(false);

  const [category, setCategory] = useState(initialData?.category || 'Earthmoving');
  const [model, setModel] = useState(initialData?.model || 'JCB 3DX EcoXpert 4WD');
  const [registration, setRegistration] = useState(initialData?.registration || 'MH-02-EQ-4491');
  const [rate, setRate] = useState(initialData?.rate || 1450);
  const [overtime, setOvertime] = useState(initialData?.overtime || 220);
  const [depot, setDepot] = useState(initialData?.depot || 'Depot Bandra West, S.V. Road');

  const categories = ['Earthmoving', 'Haulage', 'Compaction & RMC', 'Cranes'];

  const handleSave = async () => {
    if (!model || !registration) {
      alert('Please fill out model and registration number.');
      return;
    }

    try {
      setLoading(true);
      await api.saveProviderEquipment({
        id: isEditing ? initialData.id : undefined,
        equipment_id: initialData?.equipment_id || 'eq-2',
        model,
        category,
        registration,
        rate: Number(rate),
        overtime: Number(overtime),
        depot,
      });

      alert('Equipment profile updated successfully!');
      onSaved();
    } catch (err) {
      alert('Failed to save equipment: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-24 bg-[#F8F9FA]">
      {/* Header */}
      <div className="sticky top-0 z-20 bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <button onClick={onBack} className="p-1 -ml-1 text-text-secondary hover:text-text-primary rounded-lg">
          <ArrowLeft size={18} />
        </button>
        <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
          {isEditing ? 'Edit Equipment' : 'Add New Machine'}
        </h2>
        <div className="w-6" />
      </div>

      <div className="p-4 space-y-4">
        {/* Toggle Mode */}
        <div className="flex items-center bg-[#F5F5F7] p-1 rounded-xl">
          <button
            onClick={() => setTab('add')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              tab === 'add' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Add New Machine
          </button>
          <button
            onClick={() => setTab('edit')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-bold transition-all ${
              tab === 'edit' ? 'bg-white text-text-primary shadow-xs' : 'text-text-secondary'
            }`}
          >
            Edit Existing
          </button>
        </div>

        {/* Category Selection */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2">
          <label className="text-xs font-bold text-text-primary block">1. Category Selection</label>
          <div className="grid grid-cols-2 gap-2">
            {categories.map((c) => (
              <button
                key={c}
                type="button"
                onClick={() => setCategory(c)}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold text-left transition-all ${
                  category === c
                    ? 'border-[#FFB400] bg-[#FFF7E6] text-[#7E5700] font-bold'
                    : 'border-border-subtle bg-surface text-text-secondary'
                }`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        {/* Identification Form */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3">
          <label className="text-xs font-bold text-text-primary block">2. Machinery Identification</label>

          <div>
            <label className="text-[11px] font-semibold text-text-secondary block mb-1">
              Make & Full Model Name
            </label>
            <input
              type="text"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-medium focus:ring-1 focus:ring-primary"
            />
          </div>

          <div>
            <label className="text-[11px] font-semibold text-text-secondary block mb-1">
              Vehicle Registration No.
            </label>
            <input
              type="text"
              value={registration}
              onChange={(e) => setRegistration(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-mono focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>

        {/* Commercial Rates & Shift Billing */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3">
          <label className="text-xs font-bold text-text-primary block">
            3. Commercial Rates & Shift Billing
          </label>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-semibold text-text-secondary block mb-1">
                Base Hourly Rate (₹)
              </label>
              <input
                type="number"
                value={rate}
                onChange={(e) => setRate(e.target.value)}
                className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-bold focus:ring-1 focus:ring-primary"
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-text-secondary block mb-1">
                Overtime Rate (₹/hr)
              </label>
              <input
                type="number"
                value={overtime}
                onChange={(e) => setOvertime(e.target.value)}
                className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-bold focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
        </div>

        {/* Base Depot */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-text-primary block">4. Base Depot & Coverage</label>
            <span className="text-[10px] text-text-muted font-mono">Bandra Yard West</span>
          </div>

          <div className="relative">
            <input
              type="text"
              value={depot}
              onChange={(e) => setDepot(e.target.value)}
              className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 pr-20 text-xs text-text-primary font-medium focus:ring-1 focus:ring-primary"
            />
            <button
              type="button"
              className="absolute right-1.5 top-1.5 bottom-1.5 px-2 bg-white hover:bg-gray-100 border border-border-subtle rounded-lg text-[10px] font-bold text-text-primary flex items-center gap-1 shadow-2xs"
            >
              <MapPin size={11} className="text-[#FFB400]" />
              <span>Map Pin</span>
            </button>
          </div>

          {/* Attractive Depot Coverage Map */}
          <div className="pt-1">
            <SiteLocationMap
              address={depot || 'Bandra Municipal Yard, S.V. Road, Bandra West, Mumbai'}
              mode="depot"
              height="h-[180px]"
              caption={`Depot: ${depot || 'Bandra Municipal Yard'}`}
            />
          </div>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          disabled={loading}
          className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-base rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
        >
          <Save size={18} />
          <span>{loading ? 'Saving Changes...' : 'Save Equipment Changes'}</span>
        </button>
      </div>
    </div>
  );
}
