import React, { useEffect, useState } from 'react';
import { ShieldAlert, Download, AlertTriangle, CheckCircle2, ChevronRight, FileText, User, LogOut } from 'lucide-react';
import { api } from '../../services/api';
import Modal from '../../components/Modal';

export default function OfficerMore({ onLogout }) {
  const [disputes, setDisputes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDispute, setSelectedDispute] = useState(null);
  const [resolutionNote, setResolutionNote] = useState('Penalty waived per BMC mechanical inspection certificate #4812.');
  const [resolving, setResolving] = useState(false);

  useEffect(() => {
    loadDisputes();
  }, []);

  const loadDisputes = async () => {
    try {
      setLoading(true);
      const data = await api.getOfficerDisputes();
      setDisputes(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!selectedDispute) return;
    try {
      setResolving(true);
      await api.resolveOfficerDispute(selectedDispute.id, resolutionNote);
      alert(`Dispute ${selectedDispute.id} resolved and recorded in municipal audit!`);
      setSelectedDispute(null);
      await loadDisputes();
    } catch (err) {
      alert('Failed to resolve dispute: ' + err.message);
    } finally {
      setResolving(false);
    }
  };

  const handleExportCSV = () => {
    window.open(api.getOfficerExportUrl(), '_blank');
  };

  const openCases = disputes.filter((d) => d.status === 'open');

  return (
    <div className="flex flex-col min-h-full pb-20 p-4 space-y-4 bg-white">
      {/* Top Banner (Reference Image 1 Screen 1) */}
      <div className="bg-[#FFB400] text-[#1C1C1E] px-4 py-2 rounded-xl flex items-center justify-between shadow-xs">
        <span className="text-[11px] font-black uppercase tracking-wider">
          BMC OFFICER CONSOLE · LIVE TELEMATICS
        </span>
        <span className="w-2 h-2 rounded-full bg-[#1C1C1E] animate-pulse" />
      </div>

      {/* Engineer Identity Card */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-1 shadow-2xs">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-[#FFFBF0] text-[#7E5700] flex items-center justify-center font-bold text-xs border border-[#FFB400]/30">
            AD
          </div>
          <div>
            <h3 className="text-xs font-bold text-[#1C1C1E] flex items-center gap-1.5">
              <span>Er. Amit Deshmukh</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#1E9E5A]" />
            </h3>
            <p className="text-[11px] text-[#6B6B6B]">Ward Executive Engineer (Machinery Pool)</p>
          </div>
        </div>
      </div>

      {/* Problems & Disputes Section (Reference Image 1 Screen 1) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-[#1C1C1E] uppercase tracking-wide">
            Problems & Disputes
          </h3>
          <span className="bg-[#D93025] text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
            {openCases.length} Open Cases
          </span>
        </div>

        {/* Dispute Cards */}
        {disputes.map((d) => {
          const isOpen = d.status === 'open';
          return (
            <div
              key={d.id}
              className="bg-white rounded-2xl border border-[#E5E5EA] p-4 space-y-3 shadow-2xs"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-bold text-[#D93025] bg-[#FEE2E2] px-2 py-0.5 rounded">
                  {d.id.toUpperCase()}
                </span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    isOpen ? 'bg-[#FEF3C7] text-[#B45309]' : 'bg-[#DCFCE7] text-[#1E9E5A]'
                  }`}
                >
                  {isOpen ? 'Pending Investigation' : 'Resolved'}
                </span>
              </div>

              <div>
                <h4 className="text-xs font-bold text-[#1C1C1E]">{d.category}</h4>
                <p className="text-[11px] text-[#6B6B6B] mt-1 leading-snug">
                  {d.description}
                </p>
                {d.resolution && (
                  <p className="text-[10px] text-[#1E9E5A] mt-1 font-semibold">
                    Resolution: {d.resolution}
                  </p>
                )}
              </div>

              {isOpen && (
                <div className="pt-2 border-t border-[#E5E5EA]">
                  <button
                    onClick={() => setSelectedDispute(d)}
                    className="w-full h-10 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 shadow-2xs transition-all"
                  >
                    <span>Open & Resolve Case</span>
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Municipal Support & Tickets (Reference Image 1 Screen 1) */}
      <div className="bg-white rounded-2xl border border-[#E5E5EA] p-3.5 space-y-2 text-xs">
        <span className="text-[11px] font-bold text-[#6B6B6B] uppercase tracking-wider block">
          Municipal Support & Escalations
        </span>

        <div className="bg-[#F5F5F5] p-3 rounded-xl border border-[#E5E5EA] flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-[#1C1C1E] block">
              Contractor Rate Dispute Inquiries
            </span>
            <span className="text-[10px] text-[#6B6B6B]">2 pending escalations · Dharavi Sector 5</span>
          </div>
          <ChevronRight size={16} className="text-[#6B6B6B]" />
        </div>
      </div>

      {/* Export Report CSV Button */}
      <div className="pt-1">
        <button
          onClick={handleExportCSV}
          className="w-full h-12 bg-white hover:bg-[#F5F5F5] border border-[#E5E5EA] rounded-xl text-xs font-bold text-[#1C1C1E] flex items-center justify-center gap-2 shadow-2xs transition-colors"
        >
          <Download size={15} className="text-[#7E5700]" />
          <span>Export All Ward Requisitions Report (CSV)</span>
        </button>
      </div>

      {/* Log Out from Officer Console Button (Reference Image 1 Screen 1) */}
      <div className="pt-1">
        <button
          onClick={onLogout}
          className="w-full h-12 bg-white hover:bg-red-50 border border-red-200 text-[#D93025] rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-colors"
        >
          <LogOut size={14} />
          <span>Log Out from Officer Console</span>
        </button>
      </div>

      {/* Resolve Dispute Modal */}
      <Modal
        isOpen={!!selectedDispute}
        onClose={() => setSelectedDispute(null)}
        title="Resolve Municipal Dispute Case"
      >
        {selectedDispute && (
          <div className="space-y-3">
            <div className="bg-[#F5F5F5] p-3 rounded-xl border border-[#E5E5EA] text-xs">
              <span className="font-bold text-[#1C1C1E]">{selectedDispute.category}</span>
              <p className="text-[#6B6B6B] mt-1">{selectedDispute.description}</p>
            </div>

            <div>
              <label className="text-xs font-bold text-[#1C1C1E] block mb-1">
                Official Resolution Decision / Ruling
              </label>
              <textarea
                rows={3}
                value={resolutionNote}
                onChange={(e) => setResolutionNote(e.target.value)}
                className="w-full bg-[#F5F5F5] border border-[#E5E5EA] rounded-xl p-2.5 text-xs text-[#1C1C1E]"
              />
            </div>

            <button
              onClick={handleResolve}
              disabled={resolving}
              className="w-full h-11 bg-[#1C1C1E] hover:bg-black text-white font-bold text-xs rounded-xl flex items-center justify-center transition-all disabled:opacity-50"
            >
              <span>{resolving ? 'Recording...' : 'Close & Record Final Resolution'}</span>
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}
