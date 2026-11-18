import React, { useEffect, useState } from 'react';
import { Calendar, Clock, MapPin, Truck, User, ChevronRight } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';

export default function ProviderSchedule() {
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);

  useEffect(() => {
    loadSchedule();
  }, [selectedDate]);

  const loadSchedule = async () => {
    try {
      setLoading(true);
      const data = await api.getProviderSchedule();
      setSchedule(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle flex items-center justify-between">
        <div>
          <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
            Fleet Schedule
          </h2>
          <span className="text-[11px] text-text-secondary">Today's active shifts & deployments</span>
        </div>

        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="bg-[#F5F5F7] border border-border-subtle rounded-xl px-2.5 py-1 text-xs text-text-primary font-medium"
        />
      </div>

      <div className="p-4 space-y-3">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading schedule timeline...</div>
        ) : schedule.length === 0 ? (
          <div className="py-12 text-center text-xs text-text-muted">No deployments found for this day.</div>
        ) : (
          schedule.map((item) => {
            const assignment = item.assignments?.[0] || {};
            return (
              <div
                key={item.id}
                className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-3 shadow-2xs"
              >
                {/* Time slot header */}
                <div className="flex items-center justify-between pb-2 border-b border-border-subtle/80 text-xs">
                  <div className="flex items-center gap-1.5 font-bold text-text-primary">
                    <Clock size={13} className="text-[#7E5700]" />
                    <span>{item.shift?.split('·')[0] || '08:00 AM - 04:00 PM'}</span>
                    <span className="text-[10px] text-text-muted font-normal">({item.hours} hrs)</span>
                  </div>
                  <StatusBadge status={item.status} label={item.status_label} />
                </div>

                {/* Equipment & Reg */}
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-surface-subtle border border-border-subtle flex items-center justify-center text-text-secondary shrink-0">
                    <Truck size={20} className="text-[#7E5700]" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-text-primary">
                      {item.lines?.[0]?.name || 'JCB 3DX Heavy Loader'}
                    </h3>
                    <p className="text-[11px] text-text-secondary mt-0.5">
                      Reg: {assignment.vehicle_reg || 'MH-02-CB-4801'}
                    </p>
                  </div>
                </div>

                {/* Site & Operator */}
                <div className="bg-surface-subtle p-2.5 rounded-xl border border-border-subtle/70 space-y-1.5 text-xs">
                  <div className="flex items-start gap-1.5 text-text-secondary text-[11px]">
                    <MapPin size={13} className="text-text-muted shrink-0 mt-0.5" />
                    <span className="truncate">{item.address}</span>
                  </div>
                  <div className="flex items-center justify-between pt-1 border-t border-border-subtle/50 text-[11px]">
                    <span className="text-text-muted">Operator:</span>
                    <span className="font-semibold text-text-primary">
                      {assignment.operator_name || 'Ramesh Solanki'}
                    </span>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
