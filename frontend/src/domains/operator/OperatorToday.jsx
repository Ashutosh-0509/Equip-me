import React, { useEffect, useState } from 'react';
import { ArrowRight, Phone, Navigation, Clock, MapPin, User, ChevronRight, CheckCircle2, Map } from 'lucide-react';
import { api } from '../../services/api';
import SiteLocationMap from '../../components/SiteLocationMap';

export default function OperatorToday({ onNavigateToStartCode, onNavigateToLiveShift }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [showMap, setShowMap] = useState(false);

  useEffect(() => {
    loadToday();
  }, []);

  const loadToday = async () => {
    try {
      setLoading(true);
      const res = await api.getOperatorToday();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async () => {
    if (!data?.current_assignment) return;
    const b = data.current_assignment;

    try {
      setActionLoading(true);
      if (b.status === 'assigned') {
        await api.startOperatorTransit(b.id);
        await loadToday();
      } else if (b.status === 'in_transit') {
        await api.markOperatorArrived(b.id);
        onNavigateToStartCode(b.id);
      } else if (b.status === 'arrived') {
        onNavigateToStartCode(b.id);
      } else if (b.status === 'working' || b.status === 'awaiting_end') {
        onNavigateToLiveShift(b.id);
      }
    } catch (err) {
      alert('Action error: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const operator = data?.operator || {};
  const current = data?.current_assignment;
  const nextShift = data?.next_shift || {};

  const getActionButtonText = () => {
    if (!current) return 'No Active Assignment';
    switch (current.status) {
      case 'assigned':
        return 'START TRANSIT & NAVIGATE';
      case 'in_transit':
        return 'MARK ARRIVED AT SITE';
      case 'arrived':
        return 'ENTER START CODE & VERIFY';
      case 'working':
        return 'VIEW LIVE SHIFT CLOCK';
      case 'awaiting_end':
        return 'COMPLETE END HANDOFF';
      default:
        return 'VIEW SHIFT DETAILS';
    }
  };

  return (
    <div className="flex flex-col min-h-full pb-20">
      {/* Top Header (Reference Image 2 Screen 1) */}
      <div className="bg-surface px-4 py-3 border-b border-border-subtle space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-[#FFB400] text-[#1C1C1E] flex items-center justify-center font-bold text-xs">
              ⚡
            </div>
            <div>
              <span className="text-xs font-black text-text-primary uppercase tracking-tight block">
                BMC Operator <span className="bg-[#FFF7E6] text-[#7E5700] px-1.5 py-0.5 rounded text-[10px]">CIVIL</span>
              </span>
              <p className="text-[10px] text-text-muted">Municipal Corp of Greater Mumbai</p>
            </div>
          </div>

          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#DCFCE7] text-[#16A34A]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#16A34A] animate-pulse"></span>
            <span>On Duty</span>
          </span>
        </div>

        {/* Operator Identity */}
        <div className="pt-2 border-t border-border-subtle/60 flex items-center justify-between text-xs">
          <span className="text-text-secondary">
            Operator: <strong className="text-text-primary">{operator.name || 'Ramesh Solanki'}</strong>
          </span>
          <span className="text-text-muted text-[10px]">Lic: {operator.license || 'MH-OP-1005'}</span>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Main Duty Card */}
        {current ? (
          <div className="bg-surface rounded-2xl border border-border-subtle p-4 space-y-3.5 shadow-2xs">
            {/* Shift Timing */}
            <div className="flex items-center justify-between text-xs pb-2.5 border-b border-border-subtle/80">
              <div className="flex items-center gap-1.5 font-bold text-text-primary">
                <Clock size={14} className="text-[#7E5700]" />
                <span>Today · {current.shift?.split('·')[0] || '08:00 AM - 04:00 PM'}</span>
              </div>
              <span className="text-[10px] font-bold text-text-muted uppercase">Shift 1 (8 hrs)</span>
            </div>

            {/* Site Address Card */}
            <div className="bg-[#FFF7E6] p-3 rounded-xl border border-[#FFB400]/40 space-y-2">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-start gap-2.5">
                  <MapPin size={16} className="text-[#7E5700] shrink-0 mt-0.5" />
                  <div>
                    <span className="text-xs font-bold text-text-primary block">
                      {current.address}
                    </span>
                    <span className="text-[10px] text-[#7E5700] font-semibold mt-0.5 block">
                      Ward {current.ward} · Sub-Division Site 3
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => setShowMap(!showMap)}
                  className="px-2 py-1 bg-white hover:bg-gray-100 border border-[#FFB400]/50 rounded-lg text-[10px] font-bold text-[#7E5700] shrink-0 flex items-center gap-1 shadow-2xs transition-all"
                >
                  <Map size={11} />
                  <span>{showMap ? 'Hide Map' : 'View Map'}</span>
                </button>
              </div>

              {(showMap || current.status === 'in_transit') && (
                <div className="pt-1.5 border-t border-[#FFB400]/30">
                  <SiteLocationMap
                    address={current.address || 'SV Road, Near Milan Subway Junction, Santacruz (W), Mumbai'}
                    mode="route"
                    height="h-[180px]"
                    caption={`Route to: ${current.address || 'Santacruz Gate 3'}`}
                  />
                </div>
              )}
            </div>

            {/* Assigned Contractor & Supervisor */}
            <div className="bg-surface-subtle p-3 rounded-xl border border-border-subtle/70 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider block">
                  Assigned Contractor
                </span>
                <h4 className="text-xs font-bold text-text-primary mt-0.5">
                  {current.contractor_company || 'Patel Infrastructure Ltd'}
                </h4>
                <p className="text-[11px] text-text-secondary">Supervisor: Rajesh Sharma</p>
              </div>

              <a
                href="tel:+919820144512"
                className="px-3 py-1.5 bg-white hover:bg-gray-100 border border-border-subtle rounded-xl text-xs font-bold text-text-primary flex items-center gap-1.5 shadow-2xs"
              >
                <Phone size={13} className="text-[#7E5700]" />
                <span>Call Site Mgr</span>
              </a>
            </div>

            {/* Primary Action Button */}
            <button
              onClick={handleAction}
              disabled={actionLoading}
              className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] active:scale-[0.99] text-[#1C1C1E] font-extrabold text-sm rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all tracking-wide disabled:opacity-50"
            >
              <span>{actionLoading ? 'Processing...' : getActionButtonText()}</span>
              <ArrowRight size={18} />
            </button>
          </div>
        ) : (
          <div className="bg-surface rounded-2xl border border-border-subtle p-8 text-center text-xs text-text-muted">
            No active assignment found for today.
          </div>
        )}

        {/* Next Roster Shift Card (Reference Image 2 Screen 1) */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3.5 space-y-2.5 shadow-2xs">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-text-primary uppercase tracking-wide">Next Roster Shift</span>
            <span className="text-[11px] font-semibold text-text-secondary">View All →</span>
          </div>

          <div className="bg-surface-subtle p-3 rounded-xl border border-border-subtle/70 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold bg-[#1C1C1E] text-white px-2 py-0.5 rounded-full">
                  TOMORROW
                </span>
                <span className="text-xs font-bold text-text-primary">{nextShift.time}</span>
              </div>
              <h5 className="text-xs font-semibold text-text-primary mt-1">{nextShift.equipment}</h5>
              <p className="text-[10px] text-text-muted mt-0.5">{nextShift.site}</p>
            </div>
            <ChevronRight size={16} className="text-text-muted" />
          </div>
        </div>
      </div>
    </div>
  );
}
