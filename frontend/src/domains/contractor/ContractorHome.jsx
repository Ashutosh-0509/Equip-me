import React, { useEffect, useState } from 'react';
import { ChevronRight, ArrowRight, Truck, Clock, ShieldCheck, Plus, PhoneCall } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';

export default function ContractorHome({ onNavigate, onSelectBooking }) {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorBookings();
      setBookings(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const activeDeployment = bookings.find((b) =>
    ['arrived', 'working', 'in_transit'].includes(b.status)
  ) || bookings[0];

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Integrated Contractor Identity Strip */}
      <div className="bg-surface px-4 py-3 border-b border-border-subtle flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-status-green"></span>
            <span className="text-xs font-bold text-text-primary">Patel Infrastructure Pvt. Ltd.</span>
          </div>
          <p className="text-[11px] text-text-secondary mt-0.5">BMC Municipal Class 1 Contractor · Ward H/W</p>
        </div>
        <div className="text-right">
          <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider block">Active Tasks</span>
          <span className="text-sm font-bold text-text-primary">
            {bookings.filter((b) => ['assigned', 'in_transit', 'arrived', 'working'].includes(b.status)).length || 1}
          </span>
        </div>
      </div>

      <div className="px-4 py-4 space-y-4">
        {/* Active Deployment Card if any */}
        {activeDeployment && (
          <div className="bg-surface rounded-2xl border border-primary/40 shadow-xs overflow-hidden relative">
            <div className="bg-[#FFF7E6] px-3.5 py-2 border-b border-primary/20 flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-status-warning animate-pulse"></span>
                <span className="text-[11px] font-bold text-[#7E5700] uppercase tracking-wide">
                  Active Deployment
                </span>
              </div>
              <span className="text-[11px] font-bold text-text-primary">{activeDeployment.id}</span>
            </div>

            <div className="p-3.5 space-y-2.5">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-bold text-text-primary">
                    {activeDeployment.lines?.[0]?.name || 'JCB 3DX Heavy Loader'}
                  </h3>
                  <p className="text-xs text-text-secondary mt-0.5 line-clamp-1">
                    {activeDeployment.address}
                  </p>
                </div>
                <StatusBadge status={activeDeployment.status} label={activeDeployment.status_label} />
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-border-subtle/70 text-xs text-text-secondary">
                <div className="flex items-center gap-1">
                  <Clock size={13} className="text-text-muted" />
                  <span>{activeDeployment.shift?.split('·')[0] || 'Shift A'}</span>
                </div>
                <button
                  onClick={() => {
                    onSelectBooking(activeDeployment.id);
                    onNavigate('live_booking');
                  }}
                  className="font-bold text-[#7E5700] hover:underline flex items-center gap-0.5 text-xs"
                >
                  <span>Track Live Shift</span>
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions Row */}
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => onNavigate('equipment')}
            className="bg-surface hover:bg-surface-subtle p-3 rounded-xl border border-border-subtle flex flex-col items-start gap-1 transition-all text-left shadow-2xs"
          >
            <div className="w-8 h-8 rounded-lg bg-[#FFF7E6] text-[#7E5700] flex items-center justify-center font-bold">
              <Plus size={18} />
            </div>
            <span className="text-xs font-bold text-text-primary mt-1">Book Machinery</span>
            <span className="text-[10px] text-text-secondary">Browse verified fleet catalogue</span>
          </button>

          <button
            onClick={() => onNavigate('bookings')}
            className="bg-surface hover:bg-surface-subtle p-3 rounded-xl border border-border-subtle flex flex-col items-start gap-1 transition-all text-left shadow-2xs"
          >
            <div className="w-8 h-8 rounded-lg bg-surface-subtle text-text-primary flex items-center justify-center font-bold">
              <Truck size={18} />
            </div>
            <span className="text-xs font-bold text-text-primary mt-1">My Bookings</span>
            <span className="text-[10px] text-text-secondary">View active shifts and PINs</span>
          </button>
        </div>

        {/* Recent Bookings Section (Matching Reference Image 4) */}
        <section className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold text-text-primary uppercase tracking-wide">
              Recent Bookings
            </h2>
            <button
              onClick={() => onNavigate('bookings')}
              className="text-[11px] font-semibold text-text-secondary hover:text-text-primary flex items-center gap-0.5"
            >
              <span>View All</span>
              <ChevronRight size={14} />
            </button>
          </div>

          <div className="divide-y divide-border-subtle/70">
            {bookings.slice(0, 4).map((b) => (
              <div
                key={b.id}
                onClick={() => {
                  onSelectBooking(b.id);
                  onNavigate('live_booking');
                }}
                className="py-2.5 first:pt-0 last:pb-0 flex items-center justify-between gap-3 cursor-pointer hover:bg-surface-subtle/50 rounded-lg px-1 transition-colors"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="w-8 h-8 rounded-lg bg-surface-subtle border border-border-subtle flex items-center justify-center text-text-secondary shrink-0">
                    <Truck size={16} />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="text-xs font-bold text-text-primary truncate">
                        {b.lines?.[0]?.quantity || 1}x {b.lines?.[0]?.name || 'Equipment'}
                      </span>
                    </div>
                    <p className="text-[11px] text-text-secondary truncate mt-0.5">
                      {b.ward} · {b.date}
                    </p>
                  </div>
                </div>

                <div className="text-right shrink-0">
                  <div className="text-xs font-bold text-text-primary">
                    ₹{Number(b.total || 0).toLocaleString('en-IN')}
                  </div>
                  <div className="mt-0.5">
                    <StatusBadge status={b.status} label={b.status_label} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Primary Action Button (Fixed to bottom above Nav) */}
        <div className="pt-2">
          <button
            onClick={() => onNavigate('equipment')}
            className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] active:scale-[0.99] text-[#1C1C1E] font-bold text-base rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
          >
            <span>Order Equipment</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
