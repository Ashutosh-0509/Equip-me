import React, { useEffect, useState } from 'react';
import { ArrowLeft, Check, Truck, User, ArrowRight } from 'lucide-react';
import { api } from '../../services/api';

export default function ProviderAssign({ bookingId, onBack, onComplete }) {
  const [booking, setBooking] = useState(null);
  const [fleet, setFleet] = useState({ vehicles: [], operators: [] });
  const [allocations, setAllocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadData();
  }, [bookingId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [bData, fData] = await Promise.all([
        api.getContractorBooking(bookingId || 'BMC-8852'),
        api.getProviderFleet(),
      ]);

      setBooking(bData);
      setFleet(fData);

      // Determine required units from booking lines
      const totalUnits = bData.lines?.reduce((acc, l) => acc + (l.quantity || 1), 0) || 1;
      const initialAlloc = [];

      for (let i = 0; i < totalUnits; i++) {
        const existingAssignment = bData.assignments?.[i];
        if (existingAssignment) {
          initialAlloc.push({
            unit_key: `unit-${i + 1}`,
            equipment_id: existingAssignment.equipment_id,
            vehicle_id: existingAssignment.vehicle_id,
            operator_id: existingAssignment.operator_id,
            is_locked: true,
          });
        } else {
          // prefill with available options
          const availVeh = fData.vehicles.find((v) => v.status === 'available') || fData.vehicles[0];
          const availOp = fData.operators.find((o) => o.status === 'available') || fData.operators[0];
          initialAlloc.push({
            unit_key: `unit-${i + 1}`,
            equipment_id: bData.lines?.[0]?.equipment_id || 'eq-2',
            vehicle_id: availVeh?.id || 'vehicle-101',
            operator_id: availOp?.id || 'operator-101',
            is_locked: false,
          });
        }
      }
      setAllocations(initialAlloc);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAllocation = (index, field, value) => {
    setAllocations((prev) => {
      const copy = [...prev];
      copy[index] = { ...copy[index], [field]: value };
      return copy;
    });
  };

  const handleConfirm = async () => {
    if (!booking) return;
    try {
      setSubmitting(true);
      await api.assignProviderUnits(booking.id, allocations);
      alert('Vehicle and operator assignment confirmed successfully!');
      onComplete();
    } catch (err) {
      alert('Failed to confirm assignment: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading || !booking) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-xs text-text-muted">
        Loading fleet assignment workbench...
      </div>
    );
  }

  const completedCount = allocations.filter((a) => a.vehicle_id && a.operator_id).length;

  return (
    <div className="flex flex-col min-h-full pb-24 bg-[#F8F9FA]">
      {/* Top Header */}
      <div className="sticky top-0 z-20 bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <button onClick={onBack} className="p-1 -ml-1 text-text-secondary hover:text-text-primary rounded-lg">
          <ArrowLeft size={18} />
        </button>
        <div className="text-center">
          <h2 className="text-xs font-bold text-text-primary">Assign Vehicle & Operator</h2>
          <span className="text-[10px] text-text-muted">{booking.id}</span>
        </div>
        <div className="w-6" />
      </div>

      <div className="p-4 space-y-4">
        {/* Booking Context Banner */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-1.5">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-text-primary">
              {booking.lines?.[0]?.name || 'JCB 3DX Heavy Loader'}
            </h3>
            <span className="text-xs font-bold text-[#7E5700]">
              ₹{Number(booking.lines?.[0]?.rate || 1450).toLocaleString('en-IN')}/hr
            </span>
          </div>
          <p className="text-[11px] text-text-secondary">
            Ward {booking.ward} · {booking.date} · {booking.shift?.split('·')[0]}
          </p>
          <p className="text-[10px] text-text-muted truncate">Site: {booking.address}</p>
        </div>

        {/* Required Allocations Progress Bar */}
        <div className="flex items-center justify-between text-xs">
          <span className="font-bold text-text-primary uppercase tracking-wide">Required Allocations</span>
          <span className="font-bold text-[#7E5700] bg-[#FFF7E6] px-2 py-0.5 rounded-full text-[11px]">
            {completedCount} of {allocations.length} Complete
          </span>
        </div>

        {/* Allocation Units List */}
        <div className="space-y-3">
          {allocations.map((alloc, idx) => {
            const isAssigned = alloc.is_locked;
            return (
              <div
                key={alloc.unit_key}
                className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3.5 shadow-2xs"
              >
                <div className="flex items-center justify-between pb-2 border-b border-border-subtle/80">
                  <span className="text-xs font-bold text-text-primary">
                    Unit {idx + 1} of {allocations.length} · {booking.lines?.[0]?.name || 'Machinery'}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      isAssigned
                        ? 'bg-[#DCFCE7] text-[#16A34A]'
                        : 'bg-[#FEF3C7] text-[#B45309]'
                    }`}
                  >
                    {isAssigned ? 'Assigned' : 'Pending Selection'}
                  </span>
                </div>

                {/* Vehicle Selection */}
                <div>
                  <label className="text-xs font-bold text-text-secondary flex items-center gap-1.5 mb-1">
                    <Truck size={13} />
                    <span>Select Machinery</span>
                  </label>
                  <select
                    disabled={isAssigned}
                    value={alloc.vehicle_id}
                    onChange={(e) => handleUpdateAllocation(idx, 'vehicle_id', e.target.value)}
                    className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-medium focus:ring-1 focus:ring-primary disabled:opacity-80"
                  >
                    {fleet.vehicles.map((v) => (
                      <option key={v.id} value={v.id}>
                        {v.registration} ({v.model}) · {v.status === 'available' ? 'Available' : 'Assigned'}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Operator Selection */}
                <div>
                  <label className="text-xs font-bold text-text-secondary flex items-center gap-1.5 mb-1">
                    <User size={13} />
                    <span>Select Certified Operator</span>
                  </label>
                  <select
                    disabled={isAssigned}
                    value={alloc.operator_id}
                    onChange={(e) => handleUpdateAllocation(idx, 'operator_id', e.target.value)}
                    className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl p-2.5 text-xs text-text-primary font-medium focus:ring-1 focus:ring-primary disabled:opacity-80"
                  >
                    {fleet.operators.map((o) => (
                      <option key={o.id} value={o.id}>
                        {o.name} ({o.phone}) · {o.status === 'available' ? 'Available' : 'Assigned'}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            );
          })}
        </div>

        {/* Primary Action Button */}
        <button
          onClick={handleConfirm}
          disabled={submitting}
          className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-base rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all disabled:opacity-50"
        >
          <span>{submitting ? 'Confirming...' : 'Confirm Assignment'}</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
