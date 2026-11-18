import React, { useEffect, useState } from 'react';
import { Clock, Calendar, CheckCircle2, Truck } from 'lucide-react';
import { api } from '../../services/api';
import StatusBadge from '../../components/StatusBadge';

export default function OperatorHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await api.getOperatorHistory();
      setHistory(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle">
        <h2 className="text-xs font-bold text-text-primary uppercase tracking-wider">
          Operator Shift History
        </h2>
        <span className="text-[11px] text-text-secondary">Verified municipal machine logbooks</span>
      </div>

      <div className="p-4 space-y-3">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading shift logbook...</div>
        ) : history.length === 0 ? (
          <div className="py-12 text-center text-xs text-text-muted">No past shifts logged yet.</div>
        ) : (
          history.map((item) => (
            <div
              key={item.id}
              className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5 shadow-2xs"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-text-primary">{item.id}</span>
                <StatusBadge status={item.status} label={item.status_label} />
              </div>

              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-surface-subtle border border-border-subtle flex items-center justify-center text-text-secondary">
                  <Truck size={16} />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-text-primary">
                    {item.lines?.[0]?.name || 'Excavator / Backhoe'}
                  </h4>
                  <p className="text-[10px] text-text-muted">Ward {item.ward}</p>
                </div>
              </div>

              <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between text-[11px] text-text-secondary">
                <span className="flex items-center gap-1">
                  <Calendar size={12} className="text-text-muted" />
                  <span>{item.date}</span>
                </span>
                <span className="flex items-center gap-1 font-semibold text-text-primary">
                  <Clock size={12} className="text-[#7E5700]" />
                  <span>{item.hours} hrs completed</span>
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
