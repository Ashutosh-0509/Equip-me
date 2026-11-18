import React, { useEffect, useState } from 'react';
import { Truck, Calendar, Clock, ChevronRight } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';

export default function ContractorBookingsList({ onSelectBooking, onNavigate }) {
  const [bookings, setBookings] = useState([]);
  const [activeTab, setActiveTab] = useState('All');
  const [loading, setLoading] = useState(true);

  const tabs = ['All', 'Active', 'Completed', 'Issues'];

  useEffect(() => {
    loadBookings();
  }, [activeTab]);

  const loadBookings = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorBookings(activeTab);
      setBookings(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Bar with Filter Tabs */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle space-y-2.5">
        <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
          Contractor Bookings
        </h2>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {tabs.map((tab) => {
            const active = activeTab === tab;
            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                  active
                    ? 'bg-[#1C1C1E] text-white'
                    : 'bg-[#F5F5F7] text-text-secondary hover:bg-gray-200'
                }`}
              >
                {tab}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bookings List */}
      <div className="p-4 space-y-3">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading bookings...</div>
        ) : bookings.length === 0 ? (
          <div className="py-12 text-center text-xs text-text-muted">No bookings found in this view.</div>
        ) : (
          bookings.map((b) => (
            <div
              key={b.id}
              onClick={() => {
                onSelectBooking(b.id);
                onNavigate('live_booking');
              }}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3 cursor-pointer hover:border-gray-300 shadow-2xs transition-all"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-text-primary">{b.id}</span>
                    <span className="text-[10px] text-text-muted">· {b.ward}</span>
                  </div>
                  <h3 className="text-xs font-bold text-text-primary mt-1">
                    {b.lines?.[0]?.quantity || 1}x {b.lines?.[0]?.name || 'Machinery'}
                  </h3>
                </div>
                <StatusBadge status={b.status} label={b.status_label} />
              </div>

              <p className="text-[11px] text-text-secondary line-clamp-1">{b.address}</p>

              <div className="pt-2.5 border-t border-border-subtle/70 flex items-center justify-between text-xs text-text-secondary">
                <div className="flex items-center gap-3">
                  <span className="flex items-center gap-1">
                    <Calendar size={13} className="text-text-muted" />
                    <span>{b.date}</span>
                  </span>
                  <span className="font-bold text-text-primary">
                    ₹{Number(b.total || 0).toLocaleString('en-IN')}
                  </span>
                </div>

                <div className="flex items-center gap-0.5 text-xs font-bold text-[#7E5700]">
                  <span>Details</span>
                  <ChevronRight size={14} />
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
