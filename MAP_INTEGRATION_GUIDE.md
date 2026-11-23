# Google Maps Integration Guide (Zero-API-Key Embed)

This guide explains how to integrate the exact same interactive Google Maps component used in **Equip-Me** into any other application (React, Next.js, Vue, or Vanilla HTML/JS).

---

## 1. How It Works (No API Key Required)

This implementation uses **Google Maps' Native Embed URL structure**.
- **No Google Cloud Account or Billing required**
- **No API Quota or Expiration limits**
- Supports dynamic addresses, pin locations, zoom levels, street view, and satellite imagery.

### Core Embed URL Template

```text
https://maps.google.com/maps?q={QUERY}&t={TYPE}&z={ZOOM}&ie=UTF8&iwloc=&output=embed
```

| Parameter | Description | Options / Examples |
|---|---|---|
| `q` | Search query, address, or GPS coordinates | `q=Milan+Subway,+Santacruz+West,+Mumbai` or `q=19.0830,72.8370` |
| `t` | Map view type | `t=m` (Roadmap / Street view)<br>`t=k` (Satellite view) |
| `z` | Zoom level | `z=11` (City view) to `z=19` (Building/Street level) |
| `ie` | Character encoding | `ie=UTF8` |
| `iwloc` | Info window popup | Leave empty (`&iwloc=`) to suppress default bubble |
| `output` | Embed mode | `output=embed` (Required for iframe embedding) |

### Direct External Navigation URL (Opens Google Maps App / Website)

```text
https://www.google.com/maps/search/?api=1&query={QUERY}
```

---

## 2. React / Vite / Next.js Component (`SiteLocationMap.jsx`)

### Prerequisites & Dependencies

Install Lucide icons (or replace with your own icons):
```bash
npm install lucide-react
```

### Complete Component Code

Save this file as `SiteLocationMap.jsx` in your project's components folder:

```jsx
import React, { useState, useEffect } from 'react';
import { Layers, ExternalLink } from 'lucide-react';

export default function SiteLocationMap({
  address = 'Milan Subway, Santacruz (West), Mumbai, Maharashtra',
  initialLat = 19.0830,
  initialLng = 72.8370,
  height = 'h-[270px]',
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
      return currentAddress.trim();
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

  return (
    <div className={`relative w-full ${height} bg-[#F0F0F2] overflow-hidden rounded-2xl border border-[#E5E5EA] shadow-sm flex flex-col`}>
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
              {currentAddress ? currentAddress.split(',')[0] : 'Site Location'}
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
```

### Usage in Any Page

```jsx
import SiteLocationMap from './components/SiteLocationMap';

function MyPage() {
  return (
    <div className="p-4 max-w-lg mx-auto">
      <h2 className="text-lg font-bold mb-3">Project Site Map</h2>
      <SiteLocationMap 
        address="Connaught Place, New Delhi, India"
        height="h-[320px]"
        caption="Main Site Office"
      />
    </div>
  );
}
```

---

## 3. Plain HTML / CSS / Vanilla JavaScript Version

If your other application is built with plain HTML, PHP, Django, Laravel, or standard JavaScript:

```html
<div style="position: relative; width: 100%; height: 300px; border-radius: 16px; overflow: hidden; border: 1px solid #E5E5EA;">
  <iframe
    title="Google Maps Location View"
    src="https://maps.google.com/maps?q=Milan+Subway,+Santacruz+West,+Mumbai&t=m&z=15&ie=UTF8&iwloc=&output=embed"
    width="100%"
    height="100%"
    style="border: 0;"
    loading="lazy"
    allowfullscreen
    referrerpolicy="no-referrer-when-downgrade">
  </iframe>
</div>
```
