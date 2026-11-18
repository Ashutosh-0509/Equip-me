import React from 'react';
import {
  Home,
  LayoutGrid,
  Calendar,
  User,
  Inbox,
  Truck,
  Clock,
  LayoutDashboard,
  ClipboardList,
  Building2,
  MoreHorizontal,
  CalendarCheck,
  FileText
} from 'lucide-react';

export default function BottomNav({ domain, activeTab, onSelectTab }) {
  const getTabs = () => {
    switch (domain) {
      case 'contractor':
        return [
          { id: 'home', label: 'Home', icon: Home },
          { id: 'equipment', label: 'Equipment', icon: LayoutGrid },
          { id: 'bookings', label: 'Bookings', icon: FileText },
          { id: 'profile', label: 'Profile', icon: User },
        ];
      case 'provider':
        return [
          { id: 'requests', label: 'Requests', icon: Inbox },
          { id: 'schedule', label: 'Schedule', icon: Calendar },
          { id: 'fleet', label: 'Fleet', icon: Truck },
          { id: 'profile', label: 'Profile', icon: User },
        ];
      case 'operator':
        return [
          { id: 'today', label: 'Today', icon: CalendarCheck },
          { id: 'history', label: 'History', icon: Clock },
          { id: 'profile', label: 'Profile', icon: User },
        ];
      case 'officer':
        return [
          { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
          { id: 'requests', label: 'Requests', icon: ClipboardList },
          { id: 'providers', label: 'Providers', icon: Building2 },
          { id: 'more', label: 'More', icon: MoreHorizontal },
        ];
      default:
        return [];
    }
  };

  const tabs = getTabs();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-t border-border-subtle py-2">
      <div className="max-w-md mx-auto flex items-center justify-around px-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`flex flex-col items-center justify-center flex-1 py-1 transition-all ${
                isActive ? 'text-[#1C1C1E]' : 'text-text-muted hover:text-text-secondary'
              }`}
            >
              <div className="relative">
                <Icon size={20} strokeWidth={isActive ? 2.4 : 1.8} />
                {isActive && (
                  <span className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-[#FFB400] rounded-full"></span>
                )}
              </div>
              <span className={`text-[11px] mt-1 ${isActive ? 'font-bold' : 'font-medium'}`}>
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
