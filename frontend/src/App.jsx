import React, { useState } from 'react';
import LoginPage from './domains/auth/LoginPage';
import AppShell from './layouts/AppShell';

// Contractor Screens
import ContractorHome from './domains/contractor/ContractorHome';
import ContractorCatalogue from './domains/contractor/ContractorCatalogue';
import ContractorBookingWizard from './domains/contractor/ContractorBookingWizard';
import ContractorBookingsList from './domains/contractor/ContractorBookingsList';
import ContractorLiveBooking from './domains/contractor/ContractorLiveBooking';
import ContractorProfile from './domains/contractor/ContractorProfile';

// Provider Screens
import ProviderRequests from './domains/provider/ProviderRequests';
import ProviderAssign from './domains/provider/ProviderAssign';
import ProviderSchedule from './domains/provider/ProviderSchedule';
import ProviderFleet from './domains/provider/ProviderFleet';
import ProviderEquipmentEdit from './domains/provider/ProviderEquipmentEdit';
import ProviderProfile from './domains/provider/ProviderProfile';

// Operator Screens
import OperatorToday from './domains/operator/OperatorToday';
import OperatorStartCode from './domains/operator/OperatorStartCode';
import OperatorLiveShift from './domains/operator/OperatorLiveShift';
import OperatorHistory from './domains/operator/OperatorHistory';
import OperatorProfile from './domains/operator/OperatorProfile';

// Officer Screens
import OfficerDashboard from './domains/officer/OfficerDashboard';
import OfficerRequests from './domains/officer/OfficerRequests';
import OfficerVerification from './domains/officer/OfficerVerification';
import OfficerDirectory from './domains/officer/OfficerDirectory';
import OfficerMore from './domains/officer/OfficerMore';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [domain, setDomain] = useState('contractor');
  
  // Navigation tabs per domain
  const [contractorTab, setContractorTab] = useState('home');
  const [providerTab, setProviderTab] = useState('requests');
  const [operatorTab, setOperatorTab] = useState('today');
  const [officerTab, setOfficerTab] = useState('dashboard');

  // Shared payload states
  const [selectedBookingId, setSelectedBookingId] = useState('BMC-8845');
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [officerFilter, setOfficerFilter] = useState('All');
  const [refreshKey, setRefreshKey] = useState(0);

  const triggerRefresh = () => {
    setRefreshKey((k) => k + 1);
  };

  const handleLogin = (chosenDomain) => {
    setDomain(chosenDomain);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  const getActiveTab = () => {
    switch (domain) {
      case 'contractor':
        return contractorTab === 'booking_wizard' ? 'equipment' : (contractorTab === 'live_booking' ? 'bookings' : contractorTab);
      case 'provider':
        return providerTab === 'assign' || providerTab === 'equipment_edit' ? 'requests' : providerTab;
      case 'operator':
        return operatorTab === 'start_code' || operatorTab === 'live_shift' ? 'today' : operatorTab;
      case 'officer':
        return officerTab === 'verification' ? 'requests' : officerTab;
      default:
        return 'home';
    }
  };

  const handleTabChange = (tabId) => {
    switch (domain) {
      case 'contractor':
        setContractorTab(tabId);
        break;
      case 'provider':
        setProviderTab(tabId);
        break;
      case 'operator':
        setOperatorTab(tabId);
        break;
      case 'officer':
        setOfficerTab(tabId);
        break;
    }
  };

  // If not logged in, render the exact Equip Me Workspace Chooser Login Page
  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <AppShell
      currentDomain={domain}
      activeTab={getActiveTab()}
      onSelectTab={handleTabChange}
      onLogout={handleLogout}
    >
      {/* CONTRACTOR DOMAIN */}
      {domain === 'contractor' && (
        <>
          {contractorTab === 'home' && (
            <ContractorHome
              key={refreshKey}
              onNavigate={(screen) => setContractorTab(screen)}
              onSelectBooking={(id) => {
                setSelectedBookingId(id);
                setContractorTab('live_booking');
              }}
            />
          )}

          {contractorTab === 'equipment' && (
            <ContractorCatalogue
              key={refreshKey}
              onSelectEquipment={(eq) => setSelectedEquipment(eq)}
              onProceedToBooking={() => setContractorTab('booking_wizard')}
            />
          )}

          {contractorTab === 'booking_wizard' && (
            <ContractorBookingWizard
              initialEquipment={selectedEquipment}
              onBack={() => setContractorTab('equipment')}
              onBookingSuccess={(newId) => {
                setSelectedBookingId(newId);
                triggerRefresh();
                setContractorTab('live_booking');
              }}
            />
          )}

          {contractorTab === 'bookings' && (
            <ContractorBookingsList
              key={refreshKey}
              onSelectBooking={(id) => {
                setSelectedBookingId(id);
                setContractorTab('live_booking');
              }}
              onNavigate={(screen) => setContractorTab(screen)}
            />
          )}

          {contractorTab === 'live_booking' && (
            <ContractorLiveBooking
              bookingId={selectedBookingId}
              onBack={() => setContractorTab('bookings')}
              onRefresh={triggerRefresh}
            />
          )}

          {contractorTab === 'profile' && (
            <ContractorProfile
              key={refreshKey}
              onLogout={handleLogout}
            />
          )}
        </>
      )}

      {/* PROVIDER DOMAIN */}
      {domain === 'provider' && (
        <>
          {providerTab === 'requests' && (
            <ProviderRequests
              key={refreshKey}
              onSelectBookingToAssign={(id) => {
                setSelectedBookingId(id);
                setProviderTab('assign');
              }}
            />
          )}

          {providerTab === 'assign' && (
            <ProviderAssign
              bookingId={selectedBookingId}
              onBack={() => setProviderTab('requests')}
              onComplete={() => {
                triggerRefresh();
                setProviderTab('schedule');
              }}
            />
          )}

          {providerTab === 'schedule' && <ProviderSchedule key={refreshKey} />}

          {providerTab === 'fleet' && (
            <ProviderFleet
              key={refreshKey}
              onNavigateToAddEdit={(veh) => {
                setSelectedEquipment(veh || null);
                setProviderTab('equipment_edit');
              }}
            />
          )}

          {providerTab === 'equipment_edit' && (
            <ProviderEquipmentEdit
              initialData={selectedEquipment}
              onBack={() => setProviderTab('fleet')}
              onSaved={() => {
                triggerRefresh();
                setProviderTab('fleet');
              }}
            />
          )}

          {providerTab === 'profile' && (
            <ProviderProfile
              key={refreshKey}
              onLogout={handleLogout}
            />
          )}
        </>
      )}

      {/* OPERATOR DOMAIN */}
      {domain === 'operator' && (
        <>
          {operatorTab === 'today' && (
            <OperatorToday
              key={refreshKey}
              onNavigateToStartCode={(id) => {
                setSelectedBookingId(id);
                setOperatorTab('start_code');
              }}
              onNavigateToLiveShift={(id) => {
                setSelectedBookingId(id);
                setOperatorTab('live_shift');
              }}
            />
          )}

          {operatorTab === 'start_code' && (
            <OperatorStartCode
              bookingId={selectedBookingId}
              onBack={() => setOperatorTab('today')}
              onVerified={() => {
                triggerRefresh();
                setOperatorTab('live_shift');
              }}
            />
          )}

          {operatorTab === 'live_shift' && (
            <OperatorLiveShift
              bookingId={selectedBookingId}
              onShiftComplete={() => {
                triggerRefresh();
                setOperatorTab('history');
              }}
            />
          )}

          {operatorTab === 'history' && <OperatorHistory key={refreshKey} />}

          {operatorTab === 'profile' && (
            <OperatorProfile
              key={refreshKey}
              onLogout={handleLogout}
            />
          )}
        </>
      )}

      {/* OFFICER DOMAIN */}
      {domain === 'officer' && (
        <>
          {officerTab === 'dashboard' && (
            <OfficerDashboard
              key={refreshKey}
              onNavigateToVerification={(id) => {
                setSelectedBookingId(id);
                setOfficerTab('verification');
              }}
              onNavigateToRequests={(filter) => {
                setOfficerFilter(filter);
                setOfficerTab('requests');
              }}
            />
          )}

          {officerTab === 'requests' && (
            <OfficerRequests
              key={refreshKey}
              initialFilter={officerFilter}
              onNavigateToVerification={(id) => {
                setSelectedBookingId(id);
                setOfficerTab('verification');
              }}
              onRefresh={triggerRefresh}
            />
          )}

          {officerTab === 'verification' && (
            <OfficerVerification
              bookingId={selectedBookingId}
              onBack={() => setOfficerTab('requests')}
              onActionComplete={() => {
                triggerRefresh();
                setOfficerTab('dashboard');
              }}
            />
          )}

          {officerTab === 'providers' && <OfficerDirectory key={refreshKey} />}

          {officerTab === 'more' && (
            <OfficerMore
              key={refreshKey}
              onLogout={handleLogout}
            />
          )}
        </>
      )}
    </AppShell>
  );
}
