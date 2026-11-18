import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { MapPin, LocateFixed, Layers, Navigation, Compass, AlertCircle } from 'lucide-react';

// Milan Subway, Santacruz (West), Mumbai coordinates
const DEFAULT_CENTER = [19.0830, 72.8370];
const BANDRA_DEPOT = [19.0596, 72.8295];

export default function SiteLocationMap({
  initialLat = 19.0830,
  initialLng = 72.8370,
  onLocationChange,
  mode = 'picker', // 'picker' | 'route' | 'depot'
  pinLabel = 'Drop Point',
  coverageRadius = 3500, // in meters for depot mode
  height = 'h-[250px]',
  interactive = true,
  caption = '',
}) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markerRef = useRef(null);

  const [coords, setCoords] = useState({ lat: initialLat, lng: initialLng });
  const [addressLabel, setAddressLabel] = useState(
    mode === 'depot' ? 'Bandra Municipal Yard, S.V. Rd' : 'SV Rd, Santacruz (W)'
  );
  const [isLocating, setIsLocating] = useState(false);
  const [mapStyle, setMapStyle] = useState('voyager'); // 'voyager' | 'satellite'

  // Custom Site Yellow Drop Pin HTML Icon
  const createCustomIcon = (label = pinLabel, color = '#FFB400', isVehicle = false) => {
    return L.divIcon({
      className: 'custom-map-icon',
      html: `
        <div style="position: relative; display: flex; flex-direction: column; align-items: center; transform: translate(-50%, -100%); pointer-events: auto;">
          <div style="position: absolute; width: 42px; height: 42px; border-radius: 9999px; background-color: rgba(255, 180, 0, 0.35); top: 10px;" class="map-pulse-ring"></div>
          <div style="background-color: #1C1C1E; color: ${color}; padding: 2px 7px; border-radius: 4px; font-size: 9px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; box-shadow: 0 2px 6px rgba(0,0,0,0.25); white-space: nowrap; margin-bottom: 2px; border: 1px solid rgba(255,180,0,0.4);">
            ${label}
          </div>
          <div style="width: 32px; height: 32px; border-radius: 9999px; background-color: ${color}; border: 2.5px solid #1C1C1E; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.25); color: #1C1C1E;">
            ${
              isVehicle
                ? `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>`
                : `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg>`
            }
          </div>
          <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #1C1C1E; margin-top: -1px;"></div>
          <div style="width: 10px; height: 3px; border-radius: 9999px; background-color: rgba(28, 28, 30, 0.35); filter: blur(1px); margin-top: 2px;"></div>
        </div>
      `,
      iconSize: [40, 50],
      iconAnchor: [20, 50],
    });
  };

  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Clean up if instance already exists
    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    const startLat = mode === 'depot' ? BANDRA_DEPOT[0] : coords.lat;
    const startLng = mode === 'depot' ? BANDRA_DEPOT[1] : coords.lng;

    // Initialize Leaflet Map
    const map = L.map(mapContainerRef.current, {
      center: [startLat, startLng],
      zoom: mode === 'route' ? 13 : mode === 'depot' ? 14 : 15,
      zoomControl: false,
      attributionControl: false,
      dragging: interactive,
      touchZoom: interactive,
      scrollWheelZoom: interactive,
      doubleClickZoom: interactive,
    });

    mapInstanceRef.current = map;

    // CartoDB Voyager Tile Layer (clean, minimal, industrial palette with zero API keys required)
    const tileUrl =
      mapStyle === 'satellite'
        ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

    L.tileLayer(tileUrl, {
      maxZoom: 19,
      subdomains: 'abcd',
    }).addTo(map);

    // MODE 1: PICKER (Draggable Pin)
    if (mode === 'picker') {
      const marker = L.marker([coords.lat, coords.lng], {
        icon: createCustomIcon(pinLabel),
        draggable: interactive,
      }).addTo(map);

      markerRef.current = marker;

      if (interactive) {
        marker.on('dragend', () => {
          const position = marker.getLatLng();
          updateLocation(position.lat, position.lng);
        });

        map.on('click', (e) => {
          const { lat, lng } = e.latlng;
          marker.setLatLng([lat, lng]);
          updateLocation(lat, lng);
        });
      }
    }

    // MODE 2: DEPOT & COVERAGE (Circle radius + Depot marker)
    if (mode === 'depot') {
      // Municipal Coverage Radius Circle
      L.circle(BANDRA_DEPOT, {
        color: '#FFB400',
        weight: 2,
        opacity: 0.9,
        fillColor: '#FFB400',
        fillOpacity: 0.12,
        dashArray: '4, 6',
      }).addTo(map);

      // Depot marker
      const depotMarker = L.marker(BANDRA_DEPOT, {
        icon: createCustomIcon('Bandra Municipal Depot', '#FFB400'),
        draggable: false,
      }).addTo(map);
      markerRef.current = depotMarker;
    }

    // MODE 3: LIVE ROUTE & TELEMATICS (Transit Polyline + Origin + Destination + Live Machine)
    if (mode === 'route') {
      const origin = BANDRA_DEPOT;
      const destination = [19.0830, 72.8370];
      const liveMachinePos = [19.0745, 72.8340]; // midway along SV Road corridor

      // Route waypoints along SV Road
      const routeWaypoints = [
        origin,
        [19.0630, 72.8310],
        [19.0680, 72.8325],
        [19.0725, 72.8335],
        liveMachinePos,
        [19.0780, 72.8355],
        destination,
      ];

      // Route line
      L.polyline(routeWaypoints, {
        color: '#1C1C1E',
        weight: 6,
        opacity: 0.25,
      }).addTo(map);

      L.polyline(routeWaypoints, {
        color: '#FFB400',
        weight: 4,
        opacity: 0.95,
      }).addTo(map);

      // Origin Marker
      L.marker(origin, {
        icon: createCustomIcon('Depot Base', '#FFFFFF'),
      }).addTo(map);

      // Destination Marker
      L.marker(destination, {
        icon: createCustomIcon('Site Gate 3', '#16A34A'),
      }).addTo(map);

      // Live In-Transit Machine
      const machineMarker = L.marker(liveMachinePos, {
        icon: createCustomIcon('JCB 3DX · 18 km/h', '#FFB400', true),
      }).addTo(map);
      markerRef.current = machineMarker;

      // Fit map bounds comfortably
      map.fitBounds(L.latLngBounds([origin, destination]), { padding: [35, 35] });
    }

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [mapStyle, mode]);

  const updateLocation = async (lat, lng) => {
    const formattedLat = parseFloat(lat.toFixed(6));
    const formattedLng = parseFloat(lng.toFixed(6));
    setCoords({ lat: formattedLat, lng: formattedLng });

    // Reverse geocode via free OpenStreetMap Nominatim API with graceful fallback
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${formattedLat}&lon=${formattedLng}&zoom=18&addressdetails=1`,
        { headers: { 'Accept-Language': 'en' } }
      );
      if (res.ok) {
        const data = await res.json();
        const road = data.address?.road || data.address?.suburb || 'SV Road';
        const suburb = data.address?.suburb || data.address?.neighbourhood || 'Santacruz West';
        const label = `${road}, ${suburb}`;
        setAddressLabel(label);

        if (onLocationChange) {
          onLocationChange({
            lat: formattedLat.toString(),
            lng: formattedLng.toString(),
            address: data.display_name || `${road}, ${suburb}, Mumbai 400054`,
          });
        }
        return;
      }
    } catch (e) {
      // offline fallback
    }

    setAddressLabel(`Lat: ${formattedLat}, Lng: ${formattedLng}`);
    if (onLocationChange) {
      onLocationChange({
        lat: formattedLat.toString(),
        lng: formattedLng.toString(),
        address: `Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Ward H/West, Mumbai 400054`,
      });
    }
  };

  const handleZoomIn = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.zoomIn();
    }
  };

  const handleZoomOut = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.zoomOut();
    }
  };

  const handleUseMyLocation = () => {
    setIsLocating(true);
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude;
          const lng = pos.coords.longitude;
          if (mapInstanceRef.current && markerRef.current) {
            mapInstanceRef.current.flyTo([lat, lng], 16, { duration: 1.2 });
            markerRef.current.setLatLng([lat, lng]);
            updateLocation(lat, lng);
          }
          setIsLocating(false);
        },
        () => {
          if (mapInstanceRef.current && markerRef.current) {
            mapInstanceRef.current.flyTo(DEFAULT_CENTER, 16, { duration: 1.0 });
            markerRef.current.setLatLng(DEFAULT_CENTER);
            updateLocation(DEFAULT_CENTER[0], DEFAULT_CENTER[1]);
          }
          setIsLocating(false);
        },
        { timeout: 4000 }
      );
    } else {
      if (mapInstanceRef.current && markerRef.current) {
        mapInstanceRef.current.flyTo(DEFAULT_CENTER, 16, { duration: 1.0 });
        markerRef.current.setLatLng(DEFAULT_CENTER);
        updateLocation(DEFAULT_CENTER[0], DEFAULT_CENTER[1]);
      }
      setIsLocating(false);
    }
  };

  return (
    <div className={`relative w-full ${height} bg-[#E9E8E7] overflow-hidden rounded-2xl border border-[#E5E5EA] shadow-xs`}>
      {/* Leaflet DOM container */}
      <div ref={mapContainerRef} className="w-full h-full z-0 cursor-crosshair" />

      {/* Top-Left Location / Mode Badge */}
      <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-md px-2.5 py-1.5 rounded-lg border border-[#E5E5EA] shadow-xs flex items-center space-x-1.5 z-10 pointer-events-none">
        {mode === 'route' ? (
          <Navigation size={13} className="text-[#FFB400]" />
        ) : (
          <MapPin size={13} className="text-[#1C1C1E]" />
        )}
        <span className="text-[11px] font-semibold text-[#1C1C1E] leading-none max-w-[150px] truncate">
          {mode === 'route' ? 'Live Telematics Corridor' : addressLabel}
        </span>
        <span className="text-[9px] font-bold text-[#1E9E5A] bg-[#1E9E5A]/10 px-1 py-0.5 rounded leading-none">
          {mode === 'route' ? 'GPS Active' : '±2m'}
        </span>
      </div>

      {/* Top-Right Custom Minimal Controls */}
      <div className="absolute top-3 right-3 flex flex-col space-y-1.5 z-10">
        <button
          type="button"
          onClick={() => setMapStyle((s) => (s === 'voyager' ? 'satellite' : 'voyager'))}
          title="Toggle Satellite / Street View"
          className="w-7 h-7 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-md border border-[#E5E5EA] shadow-xs flex items-center justify-center hover:bg-[#F5F5F7] active:scale-95 transition-all"
        >
          <Layers size={13} />
        </button>

        {interactive && (
          <>
            <button
              type="button"
              onClick={handleZoomIn}
              aria-label="Zoom in"
              className="w-7 h-7 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-md border border-[#E5E5EA] shadow-xs flex items-center justify-center hover:bg-[#F5F5F7] active:scale-95 text-[15px] font-bold leading-none transition-all"
            >
              +
            </button>

            <button
              type="button"
              onClick={handleZoomOut}
              aria-label="Zoom out"
              className="w-7 h-7 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-md border border-[#E5E5EA] shadow-xs flex items-center justify-center hover:bg-[#F5F5F7] active:scale-95 text-[15px] font-bold leading-none transition-all"
            >
              −
            </button>
          </>
        )}
      </div>

      {/* Bottom Coordinates & Recentering Bar */}
      <div className="absolute bottom-2.5 left-3 right-3 flex items-center justify-between z-10 pointer-events-none">
        <div className="bg-white/90 backdrop-blur-xs px-2 py-1 rounded-md border border-[#E5E5EA] text-[9px] font-mono text-[#6B6B6B]">
          {caption || (mode === 'route' ? 'SV Road Transit · Santacruz Sector' : `${coords.lat.toFixed(4)}° N, ${coords.lng.toFixed(4)}° E`)}
        </div>

        {mode === 'picker' && interactive && (
          <button
            type="button"
            onClick={handleUseMyLocation}
            className="pointer-events-auto h-8 px-2.5 bg-white/95 backdrop-blur-md text-[#1C1C1E] rounded-lg shadow-sm border border-[#E5E5EA] flex items-center space-x-1.5 active:scale-95 text-[11px] font-semibold hover:bg-[#F5F5F7] transition-all"
          >
            <LocateFixed size={13} className={isLocating ? 'animate-spin text-[#FFB400]' : 'text-[#1C1C1E]'} />
            <span>{isLocating ? 'Locating...' : 'Use my location'}</span>
          </button>
        )}
      </div>
    </div>
  );
}
