import React, { useEffect, useState } from 'react';
import { Search, Plus, Minus, ArrowRight, Check } from 'lucide-react';
import { api } from '../../services/api';

export default function ContractorCatalogue({ onSelectEquipment, onProceedToBooking }) {
  const [catalogue, setCatalogue] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);

  const categories = ['All', 'Earthmoving', 'Haulage', 'Compaction & RMC', 'Cranes'];

  useEffect(() => {
    loadCatalogue();
  }, [selectedCategory, searchQuery]);

  const loadCatalogue = async () => {
    try {
      setLoading(true);
      const data = await api.getContractorCatalogue(
        selectedCategory === 'All' ? null : selectedCategory,
        searchQuery
      );
      setCatalogue(data || []);
      if (data && data.length > 0 && !selectedItem) {
        setSelectedItem(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (item) => {
    if (selectedItem?.id === item.id) {
      setSelectedItem(null);
    } else {
      setSelectedItem(item);
      setQuantity(1);
    }
  };

  const handleProceed = () => {
    if (!selectedItem) {
      alert('Please select an equipment from the catalogue first.');
      return;
    }
    onSelectEquipment({ ...selectedItem, quantity });
    onProceedToBooking();
  };

  return (
    <div className="flex flex-col min-h-full pb-28">
      {/* Search and Filters */}
      <div className="sticky top-0 z-20 bg-surface/95 backdrop-blur-md px-4 pt-3 pb-2 border-b border-border-subtle space-y-2.5">
        {/* Search Bar */}
        <div className="relative">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            type="text"
            placeholder="Search machinery, tonnage (e.g. 20T, JCB)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#F5F5F7] border border-border-subtle rounded-xl pl-9 pr-4 py-2.5 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
          />
        </div>

        {/* Category Chips Horizontal Scroll */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {categories.map((cat) => {
            const active = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                  active
                    ? 'bg-[#1C1C1E] text-white'
                    : 'bg-[#F5F5F7] text-text-secondary hover:bg-gray-200'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Equipment List / Grid */}
      <div className="px-4 py-3 space-y-3">
        {loading ? (
          <div className="py-12 text-center text-xs text-text-muted">Loading equipment catalogue...</div>
        ) : catalogue.length === 0 ? (
          <div className="py-12 text-center text-xs text-text-muted">No machinery found matching your filter.</div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {catalogue.map((eq) => {
              const isSelected = selectedItem?.id === eq.id;
              return (
                <div
                  key={eq.id}
                  onClick={() => handleSelect(eq)}
                  className={`bg-surface rounded-2xl border transition-all overflow-hidden flex flex-col cursor-pointer ${
                    isSelected
                      ? 'border-[#FFB400] ring-2 ring-[#FFB400]/20 shadow-md'
                      : 'border-border-subtle hover:border-gray-300 shadow-2xs'
                  }`}
                >
                  {/* Clean Isolated Machinery Image */}
                  <div className="relative aspect-4/3 bg-[#F8F9FA] overflow-hidden flex items-center justify-center p-2.5">
                    <img
                      src={eq.image}
                      alt={eq.name}
                      onError={(e) => {
                        e.target.src = '/placeholder.svg';
                      }}
                      className="w-full h-full object-contain"
                    />
                    {isSelected && (
                      <div className="absolute top-2 right-2 w-6 h-6 rounded-full bg-[#FFB400] text-[#1C1C1E] flex items-center justify-center shadow-xs">
                        <Check size={14} strokeWidth={3} />
                      </div>
                    )}
                  </div>

                  {/* Info */}
                  <div className="p-3 flex-1 flex flex-col justify-between space-y-2">
                    <div>
                      <h4 className="text-xs font-bold text-text-primary line-clamp-1">{eq.name}</h4>
                      <p className="text-[11px] text-text-secondary mt-0.5 line-clamp-1">{eq.description}</p>
                    </div>

                    <div className="pt-2 border-t border-border-subtle/70 flex items-center justify-between">
                      <div>
                        <span className="text-xs font-bold text-text-primary">
                          ₹{Number(eq.rate).toLocaleString('en-IN')}
                        </span>
                        <span className="text-[10px] text-text-muted">/hr</span>
                      </div>

                      {isSelected ? (
                        <div
                          className="flex items-center gap-1 bg-[#FFF7E6] border border-[#FFB400]/40 rounded-lg px-1.5 py-0.5"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <button
                            onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                            className="text-[#7E5700] hover:text-[#1C1C1E]"
                          >
                            <Minus size={12} />
                          </button>
                          <span className="text-xs font-bold text-[#1C1C1E] px-1">{quantity}</span>
                          <button
                            onClick={() => setQuantity((q) => Math.min(10, q + 1))}
                            className="text-[#7E5700] hover:text-[#1C1C1E]"
                          >
                            <Plus size={12} />
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleSelect(eq);
                          }}
                          className="px-2.5 py-1 bg-surface-subtle hover:bg-[#FFF7E6] text-text-primary hover:text-[#7E5700] border border-border-subtle rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
                        >
                          <Plus size={12} />
                          <span>Add</span>
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Selected Equipment Bottom Card (Exact match to Reference media_1795008872941_37704d0a.jpg) */}
      {selectedItem && (
        <div className="sticky bottom-16 bg-white border-t border-[#E5E5EA] p-3.5 shadow-lg space-y-3 z-30">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-[#1C1C1E]">{selectedItem.name}</h3>
              <p className="text-[11px] text-[#6B6B6B] mt-0.5">{selectedItem.description}</p>
              <div className="text-xs font-bold text-[#1C1C1E] mt-1">
                ₹{Number(selectedItem.rate).toLocaleString('en-IN')}{' '}
                <span className="text-[10px] text-[#6B6B6B] font-normal">/ hr</span>
              </div>
            </div>

            {/* Stepper with amber highlight */}
            <div className="flex items-center gap-2 bg-[#FFF7E6] border border-[#FFB400]/40 rounded-xl px-2 py-1">
              <button
                type="button"
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                className="w-7 h-7 flex items-center justify-center font-extrabold text-[#7E5700] hover:text-[#1C1C1E] active:scale-95"
              >
                −
              </button>
              <span className="text-sm font-extrabold text-[#1C1C1E] px-1">{quantity}</span>
              <button
                type="button"
                onClick={() => setQuantity((q) => Math.min(10, q + 1))}
                className="w-7 h-7 flex items-center justify-center font-extrabold text-[#7E5700] hover:text-[#1C1C1E] active:scale-95"
              >
                +
              </button>
            </div>
          </div>

          <button
            type="button"
            onClick={handleProceed}
            className="w-full h-12 bg-[#FFB400] hover:bg-[#E5A000] text-[#1C1C1E] font-bold text-sm rounded-xl flex items-center justify-center gap-2 shadow-sm active:scale-98 transition-all"
          >
            <span>Proceed to Booking Step 1</span>
            <ArrowRight size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
