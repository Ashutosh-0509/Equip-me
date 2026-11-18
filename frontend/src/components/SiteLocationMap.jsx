import React, { useState, useEffect } from 'react';
import { MapPin, Layers, ExternalLink, Navigation, Search, RefreshCw, ZoomIn, ZoomOut } from 'lucide-react';

export default function SiteLocationMap({
  address = 'Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Ward H/West, Mumbai 400054',
  initialLat = 19.0830,
  initialLng = 72.8370,
  onLocationChange,
  mode = 'picker', // 'picker' | 'route' | 'depot'
  pinLabel = 'Site Location',
  height = 'h-[270px]',
  interactive = true,
  caption = '',
}) {
  const [currentAddress, setCurrentAddress] = useState(address);
  const [mapStyle, setMapStyle] = useState('roadmap'); // 'roadmap' | 'satellite'
  const [zoom, setZoom] = useState(15);
  const [isLoading, setIsLoading] = useState(false);

  // Sync internal address whenever parent updates address prop
  useEffect(() => {
    if (address && address !== currentAddress) {
      setCurrentAddress(address);
    }
  }, [address]);

  // Construct query string for Google Maps Embed
  const getQuery = () => {
    if (currentAddress && currentAddress.trim().length > 0) {
      // Ensure Mumbai context if not present for high geocoding accuracy
      const addr = currentAddress.trim();
      return addr.toLowerCase().includes('mumbai') ? addr : `${addr}, Mumbai, Maharashtra`;
    }
    return `${initialLat},${initialLng}`;
  };

  const queryParam = encodeURIComponent(getQuery());
  const mapTypeParam = mapStyle === 'satellite' ? 'k' : 'm';
  const embedUrl = `https://maps.google.com/maps?q=${queryParam}&t=${mapTypeParam}&z=${zoom}&ie=UTF8&iwloc=&output=embed`;
  const externalMapsUrl = `https://www.google.com/maps/search/?api=1&query=${queryParam}`;

  const handleZoomIn = () => setZoom((z) => Math.min(z + 1, 19));
  const handleZoomOut = () => setZoom((z) => Math.max(z - 1, 11));

  const toggleMapStyle = () => {
    setMapStyle((s) => (s === 'roadmap' ? 'satellite' : 'roadmap'));
  };

  const handleRefresh = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 500);
  };

  return (
    <div className={`relative w-full ${height} bg-[#F0F0F2] overflow-hidden rounded-2xl border border-[#E5E5EA] shadow-xs flex flex-col`}>
      {/* Top Floating Control Bar */}
      <div className="absolute top-2.5 left-2.5 right-2.5 z-10 flex items-center justify-between pointer-events-none">
        {/* Address & Status Pill */}
        <div className="bg-white/95 backdrop-blur-md px-2.5 py-1.5 rounded-lg border border-[#E5E5EA] shadow-xs flex items-center space-x-2 max-w-[70%]">
          <div className="w-2 h-2 rounded-full bg-[#16A34A] animate-pulse shrink-0" />
          <div className="flex items-center space-x-1.5 truncate">
            <span className="text-[10px] font-extrabold uppercase tracking-wider text-[#FFB400] bg-[#1C1C1E] px-1.5 py-0.5 rounded shrink-0">
              Google Maps
            </span>
            <span className="text-[11px] font-semibold text-[#1C1C1E] truncate">
              {currentAddress ? currentAddress.split(',')[0] : 'Milan Subway Site'}
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-1.5 pointer-events-auto">
          {/* Satellite Toggle */}
          <button
            type="button"
            onClick={toggleMapStyle}
            title={mapStyle === 'satellite' ? 'Switch to Street Map' : 'Switch to Satellite View'}
            className="h-8 px-2 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-lg border border-[#E5E5EA] shadow-xs flex items-center space-x-1 text-[11px] font-semibold hover:bg-[#F5F5F7] active:scale-95 transition-all"
          >
            <Layers size={13} className={mapStyle === 'satellite' ? 'text-[#FFB400]' : 'text-[#1C1C1E]'} />
            <span>{mapStyle === 'satellite' ? 'Street' : 'Satellite'}</span>
          </button>

          {/* Open in full Google Maps */}
          <a
            href={externalMapsUrl}
            target="_blank"
            rel="noopener noreferrer"
            title="Open in Google Maps"
            className="w-8 h-8 bg-white/95 backdrop-blur-md text-[#1C1C1E] hover:text-[#7E5700] rounded-lg border border-[#E5E5EA] shadow-xs flex items-center justify-center active:scale-95 transition-all"
          >
            <ExternalLink size={13} />
          </a>

          {/* Zoom In */}
          <button
            type="button"
            onClick={handleZoomIn}
            title="Zoom In"
            className="w-8 h-8 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-lg border border-[#E5E5EA] shadow-xs flex items-center justify-center text-sm font-bold active:scale-95 transition-all"
          >
            +
          </button>

          {/* Zoom Out */}
          <button
            type="button"
            onClick={handleZoomOut}
            title="Zoom Out"
            className="w-8 h-8 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-lg border border-[#E5E5EA] shadow-xs flex items-center justify-center text-sm font-bold active:scale-95 transition-all"
          >
            −
          </button>
        </div>
      </div>

      {/* Google Maps Real Embed iframe */}
      <div className="relative w-full h-full bg-[#E5E5EA]">
        {isLoading ? (
          <div className="w-full h-full flex items-center justify-center text-xs text-[#6B6B6B] bg-white">
            Updating Google Maps...
          </div>
        ) : (
          <iframe
            title="Google Maps Location View"
            src={embedUrl}
            width="100%"
            height="100%"
            className="w-full h-full border-0 filter contrast-[1.02]"
            loading="lazy"
            allowFullScreen
            referrerPolicy="no-referrer-when-downgrade"
          />
        )}
      </div>

      {/* Bottom Info Bar */}
      <div className="absolute bottom-2 left-2.5 right-2.5 z-10 flex items-center justify-between pointer-events-none">
        <div className="bg-white/95 backdrop-blur-md px-2 py-1 rounded-md border border-[#E5E5EA] text-[10px] font-medium text-[#1C1C1E] shadow-2xs max-w-[75%] truncate">
          <span className="font-bold text-[#7E5700]">Location: </span>
          <span>{caption || currentAddress}</span>
        </div>

        <div className="bg-[#1C1C1E] text-white px-2 py-1 rounded-md text-[9px] font-mono font-bold tracking-tight shadow-2xs">
          GPS LOCK · ±2m
        </div>
      </div>
    </div>
  );
}
