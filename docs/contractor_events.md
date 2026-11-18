# Contractor demo: route and event contract

The unified demo entry connects the completed Contractor, Provider, Operator and Officer workspaces. There is no production authentication, GPS, payment collection or remote service integration. Original reference image URLs are used with accessible placeholder fallback.

## Routes

- `/` and `/login`: unified role/identity selection.
- `/contractor`: recent bookings and Order Equipment.
- `/contractor/equipment`: catalogue search, category filters and multi-selection.
- `/contractor/booking/step-1`: equipment quantities, date and shift.
- `/contractor/booking/step-2`: address, ward, manual coordinates and work order.
- `/contractor/booking/step-3`: review, edit links, safety confirmation and submit.
- `/contractor/bookings`: filtered booking list.
- `/contractor/bookings/[booking_id]`: owned booking details, cancellation, disputes, audit history and draft continuation.
- `/contractor/bookings/[booking_id]/live`: status, assignments, start and end handoffs.
- `/contractor/profile`: company identity, active/completed counters and logout.
- `/provider`, `/operator`, `/officer`: connected workspaces; their event contracts are documented separately.

All page loads invoke `SharedState.bootstrap`, followed by the callback `initialize(document_token)`. The token is a window-only document identifier, not a cookie or persistent store. New documents reset the demo from deep-copied fixtures and clear login. Client-side navigation retains data. Logout clears role and identity only, retaining data and draft selection for switching roles. Browser tabs/documents are intentionally independent: this is a single-person cross-role demo, not multi-user synchronization.

## Exact public events

All below are on `SharedState` in the shared state module. Form payload parameters accept the framework's `dict[str, Any]`; stored state is fully typed.

### Entry and guards

- `bootstrap()` — returns the window document-token script with `initialize` callback.
- `initialize(token: str)` — reset on new document, route-role guard, select detail ID, wizard prerequisite guards.
- `select_role(role: str)` — only Contractor, Provider, Operator, Officer; only while logged out.
- `login()` — bind the selected role's fixed demo identity and redirect to its workspace.
- `logout()` — clear role/identity and redirect to login; preserve demo records.

### Catalogue and draft

- `search(query: str)` — search machinery name and description; 500ms UI debounce.
- `choose_category(category: str)` — All, Earthmoving, Haulage, Compaction & RMC, Cranes.
- `clear_filters()` — reset search/category.
- `toggle_equipment(equipment_id: str)` — add quantity 1 or remove; invalidate wizard approvals.
- `change_quantity(equipment_id: str, change: int)` — change −1/+1; clamp 1–10; invalidate wizard approvals.
- `choose_shift(shift: str)` — Shift A · 08:00–16:00 (8h), Shift B · 16:00–00:00 (8h), Full day · 08:00–20:00 (12h).
- `proceed_booking()` — reject empty selection, redirect to step 1.
- `save_schedule(form_data)` — keys `date`, `shift`; valid non-past date within 365 days, nonempty selection and valid shift.
- `save_site(form_data)` — keys `address`, `ward`, `latitude`, `longitude`, `work_order`; complete address, work reference and valid coordinate ranges. No browser geolocation.
- `submit_booking(form_data)` — key `safety`; revalidate entire draft; create pending_provider booking with exact rate × quantity × hours totals. Consumes selection and prerequisites, preventing repeat submission. Resumed drafts retain their ID.
- `resume_draft(booking_id: str)` — only an owned draft; populate all fields and redirect to step 1.

### Bookings and handoffs

- `filter_bookings(value: str)` — All, Active, Completed, Drafts, Closed.
- `open_action(action: str)` — cancel/report, subject to ownership and status.
- `close_action()` — close action panel and clear error.
- `cancel_booking(form_data)` — keys `reason`, `confirm`; only draft, pending_provider, pending_approval, assigned, in_transit. Requires reason and checkbox, marks cancelled, releases assigned vehicle/operator and records audit. Working bookings must use issue reporting instead.
- `report_issue(form_data)` — keys `category`, `description`; Breakdown, Delay, Safety, Billing, Other; description at least 10 characters. Creates an open dispute and audit entry; deliberately preserves operational status. Rejects drafts/cancelled/rejected bookings.
- `confirm_start(form_data)` — key `arrival_confirmed`; arrived → working, records start timestamp and audit. The Contractor explicitly confirms arrival and safe access. This is a labeled demo authorization, not operator PIN authentication.
- `request_end()` — working → awaiting_end, audit record; exposes end handoff code.
- `confirm_end(form_data)` — key `end_confirmed`; awaiting_end → completed after Contractor confirms inspection and code handoff; records end timestamp/audit and releases resources. No payment is recorded.

Every Contractor mutation checks the selected Contractor demo identity. Record-specific handlers additionally enforce contractor ownership and allowed lifecycle status. Non-Contractor route access redirects to the selected role destination, or login if logged out. Wizard edit links retain saved fields; modifying equipment/shift invalidates prerequisites.

## Connected fixtures

The catalogue contains the six reference items with hourly rates: Heavy Excavator 1850; JCB 3DX Backhoe 1250; 16-Ton Tipper 1450; Soil Compactor 1150; Transit Mixer 1700; Hydra Crane 2100. Each line stores equipment_id, name, quantity, rate, hours and amount. Booking totals are the sum of line amounts, with no unexplained taxes or fees.

Fixed entry identities: contractor-1 (Patel Infrastructure / Rajesh Patel), provider-1 (Desai Earthmovers / Amit Desai), operator-1 (Ramesh Solanki), officer-1 (Anita Joshi). The operator-1 fleet record is assigned to arrived booking BMC-8845. A second contractor and provider are also seeded. Vehicle/operator IDs in assignments are resolvable in their fixture lists; each assigned unit has one vehicle/operator pair.

Status examples: BMC-8840 draft; 8841 pending_provider; 8842 pending_approval; 8843 assigned; 8844 in_transit; 8845 arrived; 8846 working; 8847 awaiting_end; 8848 completed; 8849 rejected; 8850 cancelled; 8851 problem. Dispute-1 references BMC-8851. Codes and lifecycle entries are sample evidence.

All four roles use the same SharedState session records with role and entity guards. No separate authoritative fixture copies, persistence or production authentication are introduced. Multi-user synchronization, if separately requested, requires linked rx.SharedState rather than these private session fixtures.

## Tests

`tests/test_contractor.py` contains unittest coverage for fixture totals/foreign keys, role guards, quantity bounds, shift totals, schedule/coordinate validation, safety and duplicate submit, resumed draft IDs, start/end transitions, cancellation restrictions, disputes and logout retention. Run via `python -m unittest discover -s tests`. These tests were added but not executed in this editing environment. Browser checks should additionally cover 360px width, image failure fallback, route guards, full reload reset, sticky footer clearance, back/edit field retention and domain destinations.
