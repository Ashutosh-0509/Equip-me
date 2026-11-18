import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, Calendar, Clock, MapPin, ShieldCheck, Check, Truck } from 'lucide-react';
import { api } from '../../services/api';
import SiteLocationMap from '../../components/SiteLocationMap';

export default function ContractorBookingWizard({
  initialEquipment,
  onBack,
  onBookingSuccess,
}) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // Form State
  const [equipment, setEquipment] = useState(
    initialEquipment || {
      id: 'eq-2',
      name: 'JCB 3DX Heavy Loader',
      description: 'Loader + Backhoe · 1.2 m³ bucket',
      rate: 1450,
      quantity: 2,
    }
  );

  const [date, setDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    return d.toISOString().split('T')[0];
  });

  const [shift, setShift] = useState('Shift A · 08:00–16:00');
  const [hours, setHours] = useState(8);
  const [address, setAddress] = useState(
    'Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Ward H/West, Mumbai 400054'
  );
  const [ward, setWard] = useState('H/West');
  const [latitude, setLatitude] = useState('19.0830');
  const [longitude, setLongitude] = useState('72.8370');
  const [workOrder, setWorkOrder] = useState('WO-2024-8842 · Storm Water Drain Widening & Desilting');
  const [safetyConfirmed, setSafetyConfirmed] = useState(true);

  const handleShiftChange = (s, h) => {
    setShift(s);
    setHours(h);
  };

  const subtotal = (equipment.rate || 1450) * (equipment.quantity || 1) * hours;
  const tax = Math.round(subtotal * 0.18);
  const total = subtotal + tax;

  const handleSubmit = async () => {
    if (!safetyConfirmed) {
      alert('Please confirm adherence to BMC safety protocols.');
      return;
    }

    try {
      setLoading(true);
      const res = await api.createContractorBooking({
        equipment_id: equipment.id,
        quantity: equipment.quantity || 1,
        date: date,
        shift: shift,
        hours: hours,
        address: address,
        ward: ward,
        latitude: latitude,
        longitude: longitude,
        work_order: workOrder,
        safety_confirmed: safetyConfirmed,
      });

      onBookingSuccess(res.id);
    } catch (err) {
      alert('Failed to submit booking: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-24 bg-white">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-white px-4 h-14 flex items-center justify-between border-b border-[#E5E5EA]">
        <button
          onClick={() => {
            if (step > 1) setStep(step - 1);
            else onBack();
          }}
          className="w-8 h-8 -ml-1 rounded-full flex items-center justify-center text-[#1C1C1E] hover:bg-[#F5F5F7] border border-[#E5E5EA] transition-all"
        >
          <ArrowLeft size={16} />
        </button>
        <h1 className="text-sm font-bold text-[#1C1C1E]">New Booking</h1>
        <div className="w-8" />
      </header>

      {/* Progress Bar (Exact Stitch reference) */}
      <section className="px-4 py-2.5 bg-white border-b border-[#E5E5EA]">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs font-semibold text-[#1C1C1E]">
            {step === 1 ? 'Step 1: Equipment & Schedule' : step === 2 ? 'Step 2: Site Location' : 'Step 3: Review & Confirm'}
          </span>
          <span className="text-[11px] font-medium text-[#6B6B6B]">Step {step} of 3</span>
        </div>
        <div className="grid grid-cols-3 gap-1.5 h-1 w-full">
          <div className="h-full rounded-full bg-[#FFB400]"></div>
          <div className={`h-full rounded-full ${step >= 2 ? 'bg-[#FFB400]' : 'bg-[#E5E5EA]'}`}></div>
          <div className={`h-full rounded-full ${step >= 3 ? 'bg-[#FFB400]' : 'bg-[#E5E5EA]'}`}></div>
        </div>
      </section>

      <div className="p-4 space-y-4 flex-1">
        {/* STEP 1: EQUIPMENT & SCHEDULE */}
        {step === 1 && (
          <div className="space-y-4">
            {/* Selected Equipment Card */}
            <div className="bg-[#F5F5F5] rounded-2xl border border-[#E5E5EA] p-3.5 space-y-3">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-white border border-[#E5E5EA] flex items-center justify-center text-[#1C1C1E] shrink-0">
                    <Truck size={22} className="text-[#7E5700]" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-[#1C1C1E]">{equipment.name}</h3>
                    <p className="text-[11px] text-[#6B6B6B] mt-0.5">{equipment.description}</p>
                    <div className="text-xs font-bold text-[#7E5700] mt-1">
                      ₹{Number(equipment.rate).toLocaleString('en-IN')}{' '}
                      <span className="text-[10px] text-[#6B6B6B] font-normal">/ hr</span>
                    </div>
                  </div>
                </div>

                {/* Stepper */}
                <div className="flex items-center gap-1.5 bg-white border border-[#E5E5EA] rounded-xl p-1">
                  <button
                    onClick={() =>
                      setEquipment((prev) => ({
                        ...prev,
                        quantity: Math.max(1, (prev.quantity || 1) - 1),
                      }))
                    }
                    className="w-7 h-7 flex items-center justify-center font-bold text-[#6B6B6B] hover:text-[#1C1C1E]"
                  >
                    -
                  </button>
                  <span className="w-5 text-center text-xs font-bold text-[#1C1C1E]">
                    {equipment.quantity || 1}
                  </span>
                  <button
                    onClick={() =>
                      setEquipment((prev) => ({
                        ...prev,
                        quantity: Math.min(10, (prev.quantity || 1) + 1),
                      }))
                    }
                    className="w-7 h-7 flex items-center justify-center font-bold text-[#6B6B6B] hover:text-[#1C1C1E]"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            {/* Date Selection */}
            <div className="bg-white rounded-2xl border border-[#E5E5EA] p-3.5 space-y-2">
              <label className="text-xs font-bold text-[#1C1C1E] flex items-center gap-1.5">
                <Calendar size={14} className="text-[#7E5700]" />
                <span>Start Date</span>
              </label>
              <input
                type="date"
                value={date}
                min={new Date().toISOString().split('T')[0]}
                onChange={(e) => setDate(e.target.value)}
                className="w-full bg-[#F5F5F5] border border-[#E5E5EA] rounded-xl px-3.5 py-2.5 text-xs text-[#1C1C1E] font-medium focus:outline-none focus:ring-1 focus:ring-[#FFB400]"
              />
            </div>

            {/* Shift Timing */}
            <div className="bg-white rounded-2xl border border-[#E5E5EA] p-3.5 space-y-2.5">
              <label className="text-xs font-bold text-[#1C1C1E] flex items-center gap-1.5">
                <Clock size={14} className="text-[#7E5700]" />
                <span>Shift Timing</span>
              </label>

              <div className="space-y-2">
                {[
                  { id: 'Shift A · 08:00–16:00', label: 'Shift A (08:00 AM – 04:00 PM)', h: 8 },
                  { id: 'Shift B · 16:00–00:00', label: 'Shift B (04:00 PM – 12:00 AM)', h: 8 },
                  { id: 'Full day · 08:00–20:00', label: 'Full Day (08:00 AM – 08:00 PM)', h: 12 },
                ].map((s) => (
                  <div
                    key={s.id}
                    onClick={() => handleShiftChange(s.id, s.h)}
                    className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition-all ${
                      shift === s.id
                        ? 'border-[#FFB400] bg-[#FFFBF0]'
                        : 'border-[#E5E5EA] bg-white hover:bg-[#F5F5F5]'
                    }`}
                  >
                    <div>
                      <div className="text-xs font-bold text-[#1C1C1E]">{s.label}</div>
                      <div className="text-[10px] text-[#6B6B6B] mt-0.5">{s.h} operational hours</div>
                    </div>
                    <div
                      className={`w-4 h-4 rounded-full border flex items-center justify-center ${
                        shift === s.id
                          ? 'border-[#FFB400] bg-[#FFB400]'
                          : 'border-[#E5E5EA] bg-white'
                      }`}
                    >
                      {shift === s.id && <div className="w-1.5 h-1.5 rounded-full bg-[#1C1C1E]" />}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Subtotal Preview */}
            <div className="bg-[#F5F5F5] rounded-2xl border border-[#E5E5EA] p-3.5 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-[#6B6B6B] block">Estimated Subtotal</span>
                <span className="text-sm font-bold text-[#1C1C1E]">
                  ₹{subtotal.toLocaleString('en-IN')}
                </span>
              </div>
              <button
                onClick={() => setStep(2)}
                className="h-12 px-5 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center gap-1.5 shadow-sm transition-all"
              >
                <span>Choose Site Location</span>
                <ArrowRight size={15} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: SITE LOCATION (Google Maps API & Stitch Design) */}
        {step === 2 && (
          <div className="space-y-4">
            {/* Google Maps API Component */}
            <SiteLocationMap
              address={address}
              initialLat={parseFloat(latitude) || 19.0830}
              initialLng={parseFloat(longitude) || 72.8370}
              height="h-[280px]"
              caption={address}
              onLocationChange={({ lat, lng, address: newAddr }) => {
                setAddress(newAddr);
                setLatitude(lat);
                setLongitude(lng);
              }}
            />

            {/* Site Address Container with live update to Google Map */}
            <div className="bg-white p-3.5 rounded-xl border border-[#E5E5EA] shadow-xs space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[13px] font-bold text-[#1C1C1E] flex items-center gap-1.5">
                  <MapPin size={14} className="text-[#FFB400]" />
                  <span>Site Address (Updated on Google Maps)</span>
                </span>
                <span className="text-[10px] font-mono text-[#6B6B6B]">Ward H/West</span>
              </div>
              <textarea
                rows={2}
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Enter site deployment address..."
                className="w-full text-[13px] font-medium text-[#1C1C1E] leading-relaxed bg-[#F5F5F5] border border-[#E5E5EA] rounded-xl p-2.5 focus:outline-none focus:ring-1 focus:ring-[#FFB400]"
              />

              {/* Quick Municipal Address Suggestions */}
              <div className="pt-1">
                <span className="text-[10px] font-bold text-[#6B6B6B] block mb-1">Quick Select Municipal Sites:</span>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    'Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai 400054',
                    'Bandra Municipal Yard, S.V. Road, Bandra West, Mumbai 400050',
                    'Dharavi Link Road Desilting Works, Sector 5, Mumbai 400017',
                    'Kurla West Municipal Heavy Machinery Depot, Mumbai 400070',
                  ].map((loc, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setAddress(loc)}
                      className={`text-[10px] font-medium px-2 py-1 rounded-lg border transition-all ${
                        address === loc
                          ? 'bg-[#1C1C1E] text-[#FFB400] border-[#1C1C1E]'
                          : 'bg-[#F5F5F5] text-[#1C1C1E] border-[#E5E5EA] hover:bg-gray-200'
                      }`}
                    >
                      {loc.split(',')[0]}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Work Order / Project Reference Container */}
            <div className="space-y-1.5">
              <label className="text-[13px] font-bold text-[#1C1C1E] px-0.5">
                Work Order / Project
              </label>
              <div className="bg-white border border-[#E5E5EA] hover:border-[#1C1C1E]/40 rounded-xl p-3 shadow-xs transition-all">
                <div className="flex items-center space-x-2.5">
                  <div className="w-8 h-8 rounded-lg bg-[#F5F5F5] border border-[#E5E5EA] text-[#1C1C1E] flex items-center justify-center shrink-0">
                    <ShieldCheck size={16} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center space-x-1.5">
                      <span className="text-[11px] font-mono font-semibold text-[#1C1C1E]">
                        WO-2024-8842
                      </span>
                    </div>
                    <h3 className="text-[13px] font-bold text-[#1C1C1E] leading-tight truncate mt-0.5">
                      Storm Water Drain Widening & Desilting
                    </h3>
                    <p className="text-[11px] text-[#6B6B6B] mt-0.5">
                      Ward H/West · Valid till Dec 31, 2026
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Action button */}
            <button
              onClick={() => setStep(3)}
              className="w-full h-14 bg-[#FFB400] text-[#1C1C1E] border-2 border-[#1C1C1E] rounded-xl font-bold text-[16px] flex items-center justify-center space-x-2 shadow-md active:scale-[0.98] transition-all hover:brightness-95"
            >
              <span>Review & Confirm</span>
              <ArrowRight size={18} />
            </button>
          </div>
        )}

        {/* STEP 3: REVIEW & CONFIRM (Exact Stitch Reference) */}
        {step === 3 && (
          <div className="space-y-4">
            <div className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-3.5 shadow-2xs">
              <div className="flex items-center justify-between pb-3 border-b border-[#E5E5EA]">
                <span className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wide">
                  Order Summary
                </span>
                <button
                  onClick={() => setStep(1)}
                  className="text-[11px] font-bold text-[#7E5700] hover:underline"
                >
                  Edit
                </button>
              </div>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="font-bold text-[#1C1C1E]">
                      {equipment.quantity || 1}x {equipment.name}
                    </span>
                    <span className="text-[#6B6B6B] block text-[11px]">
                      ₹{equipment.rate}/hr × {hours} hrs × {equipment.quantity || 1} units
                    </span>
                  </div>
                  <span className="font-bold text-[#1C1C1E]">₹{subtotal.toLocaleString('en-IN')}</span>
                </div>

                <div className="pt-2 border-t border-[#E5E5EA]/60 space-y-1.5 text-[11px]">
                  <div className="flex items-center justify-between text-[#6B6B6B]">
                    <span>Date & Shift:</span>
                    <span className="font-medium text-[#1C1C1E]">
                      {date} · {shift.split('·')[0]}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[#6B6B6B]">
                    <span>Deployment Site:</span>
                    <span className="font-medium text-[#1C1C1E] truncate max-w-[200px]">
                      {address.split(',')[0]}, {ward}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[#6B6B6B]">
                    <span>BMC Project:</span>
                    <span className="font-medium text-[#1C1C1E] truncate max-w-[200px]">
                      {workOrder.split('·')[0]}
                    </span>
                  </div>
                </div>

                <div className="pt-2.5 border-t border-[#E5E5EA] flex items-center justify-between text-sm">
                  <span className="font-bold text-[#1C1C1E]">Estimated Total Cost</span>
                  <span className="font-bold text-[#1C1C1E] text-base">
                    ₹{total.toLocaleString('en-IN')}
                  </span>
                </div>
                <p className="text-[10px] text-[#6B6B6B]">
                  Total charges computed based on verified machine operational hours.
                </p>
              </div>
            </div>

            {/* Safety Declaration Checkbox */}
            <div className="bg-[#FFFBF0] rounded-xl border border-[#FFB400]/40 p-3 flex items-start gap-2.5">
              <input
                type="checkbox"
                id="safety-check"
                checked={safetyConfirmed}
                onChange={(e) => setSafetyConfirmed(e.target.checked)}
                className="mt-0.5 w-4 h-4 rounded text-[#FFB400] focus:ring-[#FFB400]"
              />
              <label htmlFor="safety-check" className="text-[11px] text-[#6B6B6B] leading-snug cursor-pointer">
                I confirm that machinery deployment adheres to BMC Safety protocols, site access is clear, and work is authorized under municipal contract.
              </label>
            </div>

            {/* Action button */}
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-base rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all disabled:opacity-50"
            >
              <span>{loading ? 'Submitting Requisition...' : 'Book Now · Pay After Work'}</span>
              <ArrowRight size={18} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
