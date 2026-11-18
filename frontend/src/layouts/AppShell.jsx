import React from 'react';
import BottomNav from '../components/BottomNav';
import { ArrowLeftRight } from 'lucide-react';

export default function AppShell({
  currentDomain,
  activeTab,
  onSelectTab,
  onLogout,
  children,
}) {
  const getDomainTitle = () => {
    switch (currentDomain) {
      case 'contractor':
        return 'BMC HEAVYLOGIX';
      case 'provider':
        return 'BMC FLEET OPS';
      case 'operator':
        return 'BMC OPERATOR';
      case 'officer':
        return 'BMC OFFICER CONSOLE';
      default:
        return 'BMC HEAVYLOGIX';
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F5F7] flex flex-col font-sans selection:bg-[#FFB400] selection:text-[#1C1C1E]">
      {/* Clean Minimal Mobile-first Application Container */}
      <div className="w-full max-w-[430px] mx-auto min-h-screen bg-white flex flex-col relative shadow-md border-x border-[#E5E7EB]">
        {/* Subtle, Minimalist App Bar */}
        <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-4 py-2.5 border-b border-[#E5E7EB] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-[#1C1C1E] text-[#FFB400] flex items-center justify-center font-bold text-[10px] tracking-wider shadow-2xs">
              HL
            </div>
            <span className="text-xs font-bold tracking-tight text-[#1C1C1E]">
              {getDomainTitle()}
            </span>
          </div>

          <button
            onClick={onLogout}
            title="Switch Workspace"
            className="px-2.5 py-1 rounded-lg text-[11px] font-semibold text-[#6B7280] hover:text-[#1C1C1E] hover:bg-[#F5F5F7] border border-[#E5E7EB] flex items-center gap-1.5 transition-all active:scale-95"
          >
            <ArrowLeftRight size={12} />
            <span>Switch Role</span>
          </button>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 flex flex-col pb-16">
          {children}
        </main>

        {/* Persistent Bottom Navigation */}
        <BottomNav
          domain={currentDomain}
          activeTab={activeTab}
          onSelectTab={onSelectTab}
        />
      </div>
    </div>
  );
}
