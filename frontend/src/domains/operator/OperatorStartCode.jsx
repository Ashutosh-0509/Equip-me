import React, { useState } from 'react';
import { ArrowLeft, Lock, Delete, Phone, ArrowRight, ShieldCheck } from 'lucide-react';
import { api } from '../../services/api';

export default function OperatorStartCode({ bookingId, onBack, onVerified }) {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleKeyPress = (char) => {
    setError('');
    if (char === 'CLR') {
      setCode('');
    } else if (char === 'DEL') {
      setCode((prev) => prev.slice(0, -1));
    } else {
      if (code.length < 4) {
        setCode((prev) => prev + char);
      }
    }
  };

  const handleVerify = async () => {
    if (code.length !== 4) {
      setError('Please enter all 4 digits of the start code.');
      return;
    }

    try {
      setLoading(true);
      await api.verifyOperatorStart(bookingId || 'BMC-8845', code);
      alert('Start code verified! Machine shift commenced.');
      onVerified();
    } catch (err) {
      setError(err.message || 'Invalid PIN code. Please obtain the correct code from Site Contractor.');
    } finally {
      setLoading(false);
    }
  };

  const digits = code.padEnd(4, ' ').split('');

  return (
    <div className="flex flex-col min-h-full pb-20 bg-[#F8F9FA]">
      {/* Step Yellow Top Banner (Reference Image 2 Screen 2) */}
      <div className="bg-[#FFB400] text-[#1C1C1E] px-4 py-3 flex items-center justify-between shadow-xs">
        <button onClick={onBack} className="p-1 -ml-1 text-[#1C1C1E] hover:opacity-80 rounded-lg">
          <ArrowLeft size={18} />
        </button>
        <div className="flex items-center gap-1.5 font-black text-xs uppercase tracking-wide">
          <span>Step 3: Arrived at Site</span>
        </div>
        <Lock size={15} />
      </div>

      <div className="p-4 space-y-4 max-w-sm mx-auto w-full">
        {/* Code Input Display */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-5 text-center space-y-3 shadow-2xs">
          <span className="text-[11px] font-bold text-text-muted uppercase tracking-wider block">
            Enter Start Code
          </span>

          {/* 4 Digit Boxes */}
          <div className="flex items-center justify-center gap-2.5">
            {digits.map((d, i) => (
              <div
                key={i}
                className={`w-14 h-16 rounded-xl border-2 flex items-center justify-center text-3xl font-black transition-all ${
                  d !== ' '
                    ? 'border-[#FFB400] bg-[#FFF7E6] text-text-primary shadow-xs'
                    : i === code.length
                    ? 'border-[#FFB400] bg-white ring-2 ring-[#FFB400]/30'
                    : 'border-border-subtle bg-surface-subtle text-text-muted'
                }`}
              >
                {d !== ' ' ? d : ''}
              </div>
            ))}
          </div>

          {error && <p className="text-xs font-bold text-status-error">{error}</p>}

          <p className="text-[11px] text-text-secondary">
            Request the 4-digit municipal code from the on-site contractor.
          </p>
        </div>

        {/* Functional Numeric Keypad (Reference Image 2 Screen 2) */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3 shadow-2xs">
          <div className="grid grid-cols-3 gap-2">
            {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((n) => (
              <button
                key={n}
                onClick={() => handleKeyPress(n)}
                className="h-13 bg-surface-subtle hover:bg-gray-200 active:bg-[#FFB400]/20 rounded-xl text-xl font-bold text-text-primary flex items-center justify-center border border-border-subtle/60 transition-colors"
              >
                {n}
              </button>
            ))}

            <button
              onClick={() => handleKeyPress('CLR')}
              className="h-13 bg-surface-subtle hover:bg-gray-200 text-xs font-bold text-text-secondary rounded-xl flex items-center justify-center border border-border-subtle/60 uppercase"
            >
              CLR
            </button>

            <button
              onClick={() => handleKeyPress('0')}
              className="h-13 bg-surface-subtle hover:bg-gray-200 active:bg-[#FFB400]/20 rounded-xl text-xl font-bold text-text-primary flex items-center justify-center border border-border-subtle/60"
            >
              0
            </button>

            <button
              onClick={() => handleKeyPress('DEL')}
              className="h-13 bg-surface-subtle hover:bg-gray-200 text-text-secondary rounded-xl flex items-center justify-center border border-border-subtle/60"
            >
              <Delete size={20} />
            </button>
          </div>
        </div>

        {/* Contractor In-Charge Contact Card */}
        <div className="bg-surface rounded-2xl border border-border-subtle p-3 flex items-center justify-between shadow-2xs">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-[#FFF7E6] text-[#7E5700] flex items-center justify-center text-xs font-bold">
              RS
            </div>
            <div>
              <span className="text-[10px] font-semibold text-text-muted uppercase block">
                Contractor In-Charge
              </span>
              <span className="text-xs font-bold text-text-primary">Rajesh Sharma</span>
            </div>
          </div>

          <a
            href="tel:+919820144512"
            className="px-3.5 py-1.5 bg-surface-subtle hover:bg-gray-200 border border-border-subtle rounded-xl text-xs font-bold text-text-primary flex items-center gap-1.5 shadow-2xs"
          >
            <Phone size={13} className="text-[#7E5700]" />
            <span>Call</span>
          </a>
        </div>

        {/* Primary Action Button */}
        <button
          onClick={handleVerify}
          disabled={loading || code.length !== 4}
          className="w-full h-14 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-extrabold text-sm rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all tracking-wide disabled:opacity-50"
        >
          <span>{loading ? 'Verifying Code...' : 'Verify & Start Machine'}</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
