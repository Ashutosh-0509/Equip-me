// Client-side in-memory & localStorage fallback database for Equip-Me
// Ensures 100% functionality even when deployed on static frontend hosts (like Vercel frontend-only)

const STORAGE_KEY = 'equip_me_db_v2';

const INITIAL_CATALOGUE = [
  {
    id: 'eq-1',
    name: 'Heavy Excavator',
    category: 'Earthmoving',
    description: '20T · Heavy digging & trenches',
    rate: 1850,
    provider_id: 'provider-1',
    image: '/assets/machinery/excavator.jpg',
  },
  {
    id: 'eq-2',
    name: 'JCB 3DX Backhoe',
    category: 'Earthmoving',
    description: 'Loader + Backhoe multi-use',
    rate: 1450,
    provider_id: 'provider-1',
    image: '/assets/machinery/backhoe.jpg',
  },
  {
    id: 'eq-3',
    name: '16-Ton Tipper',
    category: 'Haulage',
    description: 'Muck & debris haulage',
    rate: 1100,
    provider_id: 'provider-1',
    image: '/assets/machinery/tipper.jpg',
  },
  {
    id: 'eq-4',
    name: 'Soil Compactor',
    category: 'Compaction & RMC',
    description: '11T Vibratory roller',
    rate: 1150,
    provider_id: 'provider-1',
    image: '/assets/machinery/compactor.jpg',
  },
  {
    id: 'eq-5',
    name: 'Transit Mixer',
    category: 'Compaction & RMC',
    description: '6 cu.m RMC Batching',
    rate: 1250,
    provider_id: 'provider-1',
    image: '/assets/machinery/mixer.jpg',
  },
  {
    id: 'eq-6',
    name: 'Hydra Crane',
    category: 'Cranes',
    description: '14T Girder & Precast Lift',
    rate: 2150,
    provider_id: 'provider-1',
    image: '/assets/machinery/crane.jpg',
  },
];

const INITIAL_VEHICLES = [
  { id: 'veh-1', registration: 'MH-02-EQ-3812', model: 'JCB 3DX Plus 4WD', category: 'Earthmoving', status: 'available', rate: 1450, overtime: 220, depot: 'Depot Bandra West' },
  { id: 'veh-2', registration: 'MH-02-EQ-4691', model: 'JCB 3DX EcoXpert', category: 'Earthmoving', status: 'available', rate: 1450, overtime: 220, depot: 'Depot Bandra West' },
  { id: 'veh-3', registration: 'MH-02-AX-1802', model: 'Tata Hitachi EX200', category: 'Earthmoving', status: 'available', rate: 1850, overtime: 280, depot: 'Depot Bandra West' },
  { id: 'veh-4', registration: 'MH-04-DE-2008', model: 'Tata Prima 16T Tipper', category: 'Haulage', status: 'available', rate: 1100, overtime: 180, depot: 'Depot Kurla West' },
];

const INITIAL_OPERATORS = [
  { id: 'op-1', name: 'Ramesh Solanki', phone: '+91 98201 44554', status: 'available', rating: 4.9, license: 'MH-OP-2001' },
  { id: 'op-2', name: 'Sunil Jadhav', phone: '+91 98201 44521', status: 'available', rating: 4.8, license: 'MH-OP-2002' },
  { id: 'op-3', name: 'Ramesh Pawar', phone: '+91 98201 44522', status: 'available', rating: 4.7, license: 'MH-OP-2003' },
  { id: 'op-4', name: 'Dinesh Gaikwad', phone: '+91 98201 44523', status: 'available', rating: 4.8, license: 'MH-OP-2004' },
];

function getTomorrow() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split('T')[0];
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function createDefaultBookings() {
  const tomorrow = getTomorrow();
  const today = getToday();

  return [
    {
      id: 'BMC-8842',
      contractor_id: 'contractor-1',
      contractor_name: 'Sharma Infra & Co.',
      contractor_company: 'Sharma Infra & Co.',
      provider_id: 'provider-1',
      provider_name: 'Mahalaxmi Fleet',
      provider_company: 'Mahalaxmi Earthmovers & Fleet',
      status: 'arrived',
      status_label: 'Arrived at Site',
      date: today,
      shift: 'Shift A · 08:00–16:00',
      hours: 8,
      address: 'Plot 42, SV Road near Milan Subway, Santacruz West, Ward H/West, Mumbai 400054',
      ward: 'Ward H/West',
      latitude: '19.0830',
      longitude: '72.8370',
      work_order: 'WO-2024-8842 · Storm Water Drain Widening',
      items: [
        {
          equipment_id: 'eq-2',
          name: 'JCB 3DX Backhoe',
          quantity: 2,
          rate: 1450,
          hours: 8,
          amount: 23200,
        },
      ],
      subtotal: 23200,
      tax: 4176,
      total: 27376,
      financial_lock: 23200,
      start_pin: '8429',
      end_pin: '6250',
      created_at: `${today}T07:15:00+05:30`,
      assignments: [
        {
          equipment_id: 'eq-2',
          vehicle_id: 'veh-1',
          vehicle_model: 'JCB 3DX Plus 4WD',
          vehicle_reg: 'MH-02-EQ-3812',
          operator_id: 'op-1',
          operator_name: 'Ramesh Solanki',
          operator_phone: '+91 98201 44554',
        },
        {
          equipment_id: 'eq-2',
          vehicle_id: 'veh-2',
          vehicle_model: 'JCB 3DX EcoXpert',
          vehicle_reg: 'MH-02-EQ-4691',
          operator_id: 'op-2',
          operator_name: 'Sunil Jadhav',
          operator_phone: '+91 98201 44521',
        },
      ],
    },
    {
      id: 'BMC-8843',
      contractor_id: 'contractor-1',
      contractor_name: 'Patel Infrastructure',
      contractor_company: 'Patel Infrastructure Pvt. Ltd.',
      provider_id: 'provider-1',
      provider_name: 'Mahalaxmi Fleet',
      provider_company: 'Mahalaxmi Earthmovers & Fleet',
      status: 'working',
      status_label: 'Work in Progress',
      date: today,
      shift: 'Shift A · 08:00–16:00',
      hours: 8,
      address: 'SV Road, Near Milan Subway Junction, Santacruz (W)',
      ward: 'Ward H/West',
      latitude: '19.0830',
      longitude: '72.8370',
      work_order: 'WO-2024-8843 · Culvert Excavation',
      items: [
        {
          equipment_id: 'eq-1',
          name: 'Heavy Excavator',
          quantity: 1,
          rate: 1850,
          hours: 8,
          amount: 14800,
        },
      ],
      subtotal: 14800,
      tax: 2664,
      total: 17464,
      financial_lock: 14800,
      start_pin: '5821',
      end_pin: '7190',
      created_at: `${today}T06:30:00+05:30`,
      assignments: [
        {
          equipment_id: 'eq-1',
          vehicle_id: 'veh-3',
          vehicle_model: 'Tata Hitachi EX200',
          vehicle_reg: 'MH-02-AX-1802',
          operator_id: 'op-3',
          operator_name: 'Ramesh Pawar',
          operator_phone: '+91 98201 44522',
        },
      ],
    },
    {
      id: 'BMC-8844',
      contractor_id: 'contractor-1',
      contractor_name: 'Sharma Infra & Co.',
      contractor_company: 'Sharma Infra & Co.',
      provider_id: 'provider-1',
      provider_name: 'Mahalaxmi Fleet',
      provider_company: 'Mahalaxmi Earthmovers & Fleet',
      status: 'pending_provider',
      status_label: 'Awaiting Provider',
      date: tomorrow,
      shift: 'Shift A · 08:00–16:00',
      hours: 8,
      address: 'Santacruz SV Road Storm Water Drain (Gate 3)',
      ward: 'Ward H/West',
      latitude: '19.0830',
      longitude: '72.8370',
      work_order: 'WO-2024-8844 · Muck & Debris Clearing',
      items: [
        {
          equipment_id: 'eq-3',
          name: '16-Ton Tipper',
          quantity: 1,
          rate: 1100,
          hours: 8,
          amount: 8800,
        },
      ],
      subtotal: 8800,
      tax: 1584,
      total: 10384,
      financial_lock: 8800,
      start_pin: '4391',
      end_pin: '8820',
      created_at: `${today}T10:00:00+05:30`,
      assignments: [],
    },
    {
      id: 'BMC-8845',
      contractor_id: 'contractor-2',
      contractor_name: 'Mehta Constructions',
      contractor_company: 'Mehta Constructions Ltd.',
      provider_id: 'provider-1',
      provider_name: 'Mahalaxmi Fleet',
      provider_company: 'Mahalaxmi Earthmovers & Fleet',
      status: 'pending_approval',
      status_label: 'Awaiting Approval',
      date: tomorrow,
      shift: 'Shift A · 08:00–16:00',
      hours: 8,
      address: 'Plot 18, Link Road, Kurla West',
      ward: 'Ward L',
      latitude: '19.0650',
      longitude: '72.8790',
      work_order: 'WO-2024-8845 · Asphalt Compaction',
      items: [
        {
          equipment_id: 'eq-4',
          name: 'Soil Compactor',
          quantity: 1,
          rate: 1150,
          hours: 8,
          amount: 9200,
        },
      ],
      subtotal: 9200,
      tax: 1656,
      total: 10856,
      financial_lock: 9200,
      start_pin: '7729',
      end_pin: '3310',
      created_at: `${today}T11:20:00+05:30`,
      assignments: [],
    },
    {
      id: 'BMC-8846',
      contractor_id: 'contractor-1',
      contractor_name: 'BMC Direct Ward Ops',
      contractor_company: 'Brihanmumbai Municipal Corporation',
      provider_id: 'provider-1',
      provider_name: 'Mahalaxmi Fleet',
      provider_company: 'Mahalaxmi Earthmovers & Fleet',
      status: 'problem',
      status_label: 'Dispute / Breakdown',
      date: today,
      shift: 'Shift A · 08:00–16:00',
      hours: 8,
      address: 'Pillar #42, Milan Subway Junction',
      ward: 'Ward H/West',
      latitude: '19.0830',
      longitude: '72.8370',
      work_order: 'WO-2024-8846 · Emergency Traffic Obstruction Clearance',
      items: [
        {
          equipment_id: 'eq-2',
          name: 'JCB 3DX Backhoe',
          quantity: 1,
          rate: 1450,
          hours: 8,
          amount: 11600,
        },
      ],
      subtotal: 11600,
      tax: 2088,
      total: 13688,
      financial_lock: 11600,
      start_pin: '9102',
      end_pin: '4450',
      created_at: `${today}T08:00:00+05:30`,
      assignments: [
        {
          equipment_id: 'eq-2',
          vehicle_id: 'veh-1',
          vehicle_model: 'JCB 3DX Plus 4WD',
          vehicle_reg: 'MH-02-EQ-3812',
          operator_id: 'op-1',
          operator_name: 'Ramesh Solanki',
          operator_phone: '+91 98201 44554',
        },
      ],
    },
  ];
}

const INITIAL_DISPUTES = [
  {
    id: 'dispute-1',
    booking_id: 'BMC-8846',
    contractor_id: 'contractor-1',
    category: 'Breakdown & Downtime Penalty Dispute',
    description: 'Dispute between Sharma Infra and Sion Civil Yard regarding hydraulic hose failure on CAT 320D. Contested penalty: ₹48,500.',
    status: 'open',
    resolution: '',
    created_at: `${getToday()}T09:20:00+05:30`,
  },
  {
    id: 'dispute-2',
    booking_id: 'BMC-8842',
    contractor_id: 'contractor-1',
    category: 'Overtime Hours Discrepancy',
    description: 'Operator logged 9.5 hrs vs 8.0 hrs claimed on Dharavi Pipeline culvert reinforcement. GPS ignition records compiled.',
    status: 'open',
    resolution: '',
    created_at: `${getToday()}T11:15:00+05:30`,
  },
];

class LocalBackendDatabase {
  constructor() {
    this.init();
  }

  init() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        this.catalogue = parsed.catalogue || INITIAL_CATALOGUE;
        this.bookings = parsed.bookings || createDefaultBookings();
        this.vehicles = parsed.vehicles || INITIAL_VEHICLES;
        this.operators = parsed.operators || INITIAL_OPERATORS;
        this.disputes = parsed.disputes || INITIAL_DISPUTES;
        return;
      }
    } catch (e) {
      // LocalStorage not available or parse failed
    }

    this.reset();
  }

  save() {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          catalogue: this.catalogue,
          bookings: this.bookings,
          vehicles: this.vehicles,
          operators: this.operators,
          disputes: this.disputes,
        })
      );
    } catch (e) {
      // Ignore
    }
  }

  reset() {
    this.catalogue = [...INITIAL_CATALOGUE];
    this.bookings = createDefaultBookings();
    this.vehicles = [...INITIAL_VEHICLES];
    this.operators = [...INITIAL_OPERATORS];
    this.disputes = [...INITIAL_DISPUTES];
    this.save();
  }

  // --- Router Dispatcher ---
  handle(endpoint, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    const [pathOnly, queryString] = endpoint.split('?');
    const params = new URLSearchParams(queryString || '');
    const body = options.body ? JSON.parse(options.body) : {};

    // 1. Shared
    if (pathOnly === '/shared/health' || pathOnly === '/health') {
      return { status: 'healthy', mode: 'client-offline-state', version: '1.0.0' };
    }
    if (pathOnly === '/shared/reset') {
      this.reset();
      return { status: 'success', message: 'Demo data successfully reset' };
    }
    if (pathOnly === '/shared/overview') {
      return {
        total_bookings: this.bookings.length,
        pending_provider: this.bookings.filter((b) => b.status === 'pending_provider').length,
        pending_approval: this.bookings.filter((b) => b.status === 'pending_approval').length,
        approved: this.bookings.filter((b) => b.status === 'approved').length,
        active: this.bookings.filter((b) => ['assigned', 'in_transit', 'arrived', 'working'].includes(b.status)).length,
        completed: this.bookings.filter((b) => b.status === 'completed').length,
        problems: this.bookings.filter((b) => b.status === 'problem').length,
      };
    }

    // 2. Contractor
    if (pathOnly === '/contractor/catalogue') {
      const cat = params.get('category');
      const search = (params.get('search') || '').toLowerCase();
      let res = this.catalogue;
      if (cat && cat !== 'All') {
        res = res.filter((item) => item.category === cat);
      }
      if (search) {
        res = res.filter(
          (item) =>
            item.name.toLowerCase().includes(search) ||
            item.description.toLowerCase().includes(search)
        );
      }
      return res;
    }

    if (pathOnly === '/contractor/bookings') {
      if (method === 'POST') {
        const id = `BMC-${Math.floor(1000 + Math.random() * 9000)}`;
        const eq = this.catalogue.find((c) => c.id === body.equipment_id) || this.catalogue[0];
        const hours = body.hours || 8;
        const qty = body.quantity || 1;
        const subtotal = eq.rate * qty * hours;
        const tax = Math.round(subtotal * 0.18);
        const total = subtotal + tax;

        const newBooking = {
          id,
          contractor_id: 'contractor-1',
          contractor_name: 'Sharma Infra & Co.',
          contractor_company: 'Sharma Infra & Co.',
          provider_id: 'provider-1',
          provider_name: 'Mahalaxmi Fleet',
          provider_company: 'Mahalaxmi Earthmovers & Fleet',
          status: 'pending_provider',
          status_label: 'Awaiting Provider',
          date: body.date || getTomorrow(),
          shift: body.shift || 'Shift A · 08:00–16:00',
          hours,
          address: body.address || 'Plot 42, SV Road, Santacruz West, Mumbai',
          ward: body.ward || 'Ward H/West',
          latitude: body.latitude || '19.0830',
          longitude: body.longitude || '72.8370',
          work_order: body.work_order || 'WO-2024-8842 · Storm Water Drain Widening',
          items: [{ equipment_id: eq.id, name: eq.name, quantity: qty, rate: eq.rate, hours, amount: subtotal }],
          subtotal,
          tax,
          total,
          financial_lock: subtotal,
          start_pin: `${Math.floor(1000 + Math.random() * 9000)}`,
          end_pin: `${Math.floor(1000 + Math.random() * 9000)}`,
          created_at: new Date().toISOString(),
          assignments: [],
        };
        this.bookings.unshift(newBooking);
        this.save();
        return newBooking;
      }

      const status = params.get('status');
      if (status && status !== 'all') {
        return this.bookings.filter((b) => b.status === status);
      }
      return this.bookings;
    }

    const bookingIdMatch = pathOnly.match(/^\/contractor\/bookings\/([^/]+)$/);
    if (bookingIdMatch) {
      const b = this.bookings.find((item) => item.id === bookingIdMatch[1]);
      if (b) return b;
      return this.bookings[0];
    }

    if (pathOnly.startsWith('/contractor/bookings/') && pathOnly.endsWith('/cancel')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'cancelled';
        b.status_label = 'Cancelled';
        this.save();
        return b;
      }
      return { status: 'cancelled' };
    }

    if (pathOnly.startsWith('/contractor/bookings/') && pathOnly.endsWith('/dispute')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'problem';
        b.status_label = 'Dispute / Breakdown';
        this.disputes.unshift({
          id: `dispute-${Date.now()}`,
          booking_id: bId,
          contractor_id: 'contractor-1',
          category: body.category || 'Breakdown',
          description: body.description || 'Reported breakdown',
          status: 'open',
          created_at: new Date().toISOString(),
        });
        this.save();
        return b;
      }
      return { status: 'problem' };
    }

    if (pathOnly === '/contractor/profile') {
      return {
        company: 'Sharma Infra & Co.',
        contact_person: 'Rajesh Sharma',
        phone: '+91 98201 44512',
        email: 'contact@sharmainfra.test',
        registration_no: 'BMC/CIVIL/2019/312',
        active_tasks: this.bookings.filter((b) => ['assigned', 'in_transit', 'arrived', 'working'].includes(b.status)).length,
        completed_tasks: 48,
        ward: 'Ward H/West',
        compliance: '100%',
      };
    }

    // 3. Provider
    if (pathOnly === '/provider/requests') {
      return this.bookings.filter((b) => ['pending_provider', 'approved'].includes(b.status));
    }

    if (pathOnly.startsWith('/provider/requests/') && pathOnly.endsWith('/accept')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'pending_approval';
        b.status_label = 'Awaiting Approval';
        this.save();
        return b;
      }
      return { status: 'pending_approval' };
    }

    if (pathOnly.startsWith('/provider/requests/') && pathOnly.endsWith('/reject')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'rejected';
        b.status_label = 'Rejected';
        this.save();
        return b;
      }
      return { status: 'rejected' };
    }

    if (pathOnly.startsWith('/provider/assign/')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'assigned';
        b.status_label = 'Assigned';
        b.assignments = body.assignments || [
          {
            equipment_id: b.items[0]?.equipment_id,
            vehicle_id: 'veh-1',
            vehicle_model: 'JCB 3DX Plus 4WD',
            vehicle_reg: 'MH-02-EQ-3812',
            operator_id: 'op-1',
            operator_name: 'Ramesh Solanki',
            operator_phone: '+91 98201 44554',
          },
        ];
        this.save();
        return b;
      }
      return { status: 'assigned' };
    }

    if (pathOnly === '/provider/schedule') {
      return this.bookings.filter((b) => ['assigned', 'in_transit', 'arrived', 'working', 'completed'].includes(b.status));
    }

    if (pathOnly === '/provider/fleet') {
      return {
        vehicles: this.vehicles,
        operators: this.operators,
        depots: ['Depot Bandra West', 'Depot Kurla West', 'Depot Andheri East'],
      };
    }

    if (pathOnly === '/provider/profile') {
      return {
        company: 'Mahalaxmi Earthmovers & Fleet',
        contact_person: 'Amit Desai',
        phone: '+91 98201 44553',
        email: 'dispatch@mahalaxmifleet.test',
        depot: 'Depot Bandra West, S.V. Road',
        total_payout: '₹3,42,800',
        pending_clearance: '₹46,500',
        completed_shifts: 34,
        vehicles_count: 5,
        operators_count: 4,
      };
    }

    // 4. Operator
    if (pathOnly === '/operator/today') {
      const active = this.bookings.find((b) => ['assigned', 'in_transit', 'arrived', 'working', 'awaiting_end'].includes(b.status));
      return {
        operator: { name: 'Ramesh Pawar', phone: '+91 98201 44522', status: 'On Duty' },
        current_shift: active || this.bookings[0],
        next_shift: {
          time: 'Tomorrow · 08:30 AM',
          equipment: 'Tata Hitachi EX200',
          site: 'Dharavi Link Road Desilting Works · Sector 5',
        },
      };
    }

    if (pathOnly.startsWith('/operator/transit/')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'in_transit';
        b.status_label = 'In Transit';
        this.save();
        return b;
      }
      return { status: 'in_transit' };
    }

    if (pathOnly.startsWith('/operator/arrive/')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'arrived';
        b.status_label = 'Arrived at Site';
        this.save();
        return b;
      }
      return { status: 'arrived' };
    }

    if (pathOnly.startsWith('/operator/verify_start/')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'working';
        b.status_label = 'Work in Progress';
        this.save();
        return b;
      }
      return { status: 'working' };
    }

    if (pathOnly.startsWith('/operator/request_end/') || pathOnly.startsWith('/operator/verify_end/')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'completed';
        b.status_label = 'Completed';
        this.save();
        return b;
      }
      return { status: 'completed' };
    }

    if (pathOnly === '/operator/history') {
      return this.bookings.filter((b) => b.status === 'completed');
    }

    if (pathOnly === '/operator/profile') {
      return {
        name: 'Ramesh Pawar',
        role: 'Heavy Machinery Lead Operator',
        phone: '+91 98201 44522',
        license: 'MH-OP-2002',
        rating: 4.9,
        total_hours: '1,420 hrs',
        verified: true,
      };
    }

    // 5. Officer
    if (pathOnly === '/officer/dashboard') {
      return {
        officer: { name: 'Er. Amit Deshmukh', role: 'Ward Executive Engineer (Machinery Pool)', ward: 'Ward G/N' },
        metrics: {
          waiting_approval: this.bookings.filter((b) => b.status === 'pending_approval').length,
          not_matched: this.bookings.filter((b) => b.status === 'pending_provider').length,
          active_today: this.bookings.filter((b) => ['assigned', 'in_transit', 'arrived', 'working'].includes(b.status)).length,
          problems_open: this.disputes.filter((d) => d.status === 'open').length,
        },
        needs_you_now: this.bookings.filter((b) => b.status === 'pending_approval').slice(0, 3),
      };
    }

    if (pathOnly === '/officer/requests') {
      const status = params.get('status');
      if (status && status !== 'All') {
        return this.bookings.filter((b) => b.status === status);
      }
      return this.bookings;
    }

    if (pathOnly.startsWith('/officer/bookings/') && pathOnly.endsWith('/approve')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'approved';
        b.status_label = 'Approved · Ready for Allocation';
        this.save();
        return b;
      }
      return { status: 'approved' };
    }

    if (pathOnly.startsWith('/officer/bookings/') && pathOnly.endsWith('/reject')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'rejected';
        b.status_label = 'Rejected';
        this.save();
        return b;
      }
      return { status: 'rejected' };
    }

    if (pathOnly.startsWith('/officer/bookings/') && pathOnly.endsWith('/reassign')) {
      const bId = pathOnly.split('/')[3];
      const b = this.bookings.find((item) => item.id === bId);
      if (b) {
        b.status = 'assigned';
        b.status_label = 'Reassigned Fleet';
        this.save();
        return b;
      }
      return { status: 'assigned' };
    }

    if (pathOnly === '/officer/disputes') {
      return this.disputes;
    }

    if (pathOnly.startsWith('/officer/disputes/') && pathOnly.endsWith('/resolve')) {
      const dId = pathOnly.split('/')[3];
      const d = this.disputes.find((item) => item.id === dId);
      if (d) {
        d.status = 'resolved';
        d.resolution = body.note || 'Resolved by Ward Executive Engineer';
        this.save();
        return d;
      }
      return { status: 'resolved' };
    }

    if (pathOnly === '/officer/directory') {
      return {
        providers: [
          { name: 'Mahalaxmi Earthmovers & Fleet', depot: 'Kurla West Depot', grade: 'Grade A · 4.8', fleet_size: 12, phone: '+91 98201 44553' },
          { name: 'Bandra Infra Heavy Machineries', depot: 'Bandra East Depot', grade: 'Grade B · 4.2', fleet_size: 8, phone: '+91 98201 44557' },
        ],
        contractors: [
          { name: 'Sharma Infra & Co.', reg: 'BMC/CIVIL/2019/312', active: 2, phone: '+91 98201 44556' },
          { name: 'Patel Infrastructure Pvt. Ltd.', reg: 'BMC/CIVIL/2021/804', active: 1, phone: '+91 98201 44552' },
        ],
      };
    }

    // Default fallback
    return { status: 'ok' };
  }
}

export const localBackend = new LocalBackendDatabase();
