# Provider demo event contract

Provider, Operator and Officer are implemented as connected demo workspaces. All Provider data lives in the existing SharedState session. This is a single-person, cross-role demo, not production authentication or multi-user synchronization. Existing bootstrap/initialize enforce route role, reset on a new document, and load booking_id / equipment_id into Provider editor selections. Logout retains records. The equipment route parameter identifies a vehicle asset, not a catalogue type.

## Routes

`/provider` and `/provider/requests`: incoming requests and approval/allocation queue. `/provider/assign/[booking_id]`: owned request review, acceptance/rejection, approved allocation or read-only deployment details. `/provider/schedule`: date-filtered bookings with resolved vehicles/operators. `/provider/fleet`: searchable vehicles/operators and operator editor. `/provider/equipment/new`, `/provider/equipment/[equipment_id]/edit`: asset editor. `/provider/profile`: identity, earnings statements, editable labeled demo account/compliance/support notes and logout.

## Exact new public events on SharedState

- `open_provider_booking(booking_id: str)` — ownership guard; selects booking, clears transient messages, redirects to `/provider/assign/{booking_id}`. Pending approval is review-only.
- `accept_provider_request(form_data: dict[str, Any])` — current owned pending_provider booking; keys are catalogue equipment IDs, values whole accepted quantities. Each must be 0 through requested quantity; at least one positive. Preserves requested_lines/requested_total, stores all accepted lines (including zero), computes accepted totals using original quoted rates, records audit, transitions to pending_approval and redirects to allocation detail. No approval bypass.
- `reject_provider_request(form_data: dict[str, Any])` — owned pending_provider only; `reason` 5–500 characters and `confirm` required. Rejects with visible reason and audit.
- `confirm_provider_assignment(form_data: dict[str, Any])` — owned approved booking only. For each unit returned by provider_allocation_units, keys `vehicle_{unit.key}` and `operator_{unit.key}` contain shared resource IDs. Revalidates equipment compatibility, availability, no duplicates and overlapping same-day shift conflicts before any record changes. Assigns accepted units, updates fleet/operators/audit, selects booking date and redirects to `/provider/schedule`.
- `set_provider_date(value: str)` — valid ISO schedule date.
- `search_provider_fleet(value: str)` — bounded search; UI debounce 500ms.
- `filter_provider_fleet(value: str)` — All/available/assigned/maintenance/unavailable.
- `set_provider_tab(value: str)` — Vehicles/Operators; closes editor panel.
- `open_provider_vehicle(vehicle_id: str)` — empty ID selects new asset and redirects `/provider/equipment/new`; owned asset selects editor and redirects `/provider/equipment/{vehicle_id}/edit`.
- `save_provider_vehicle(form_data: dict[str, Any])` — equipment_id, category, model, registration, rate, overtime, depot, status. Equipment belongs to Provider and category matches; model/depot required, registration canonicalized and globally unique; rates finite/nonnegative. Cannot fabricate assigned status. Reserved assets allow future rates only, not identity/type/depot/availability changes. Base rate updates the matching Provider catalogue type and its fleet units for new Contractor calculations; existing quote/agreed booking totals never change. Audits and redirects `/provider/fleet`.
- `open_provider_operator(operator_id: str)` — owned operator or empty for new; opens inline editor.
- `save_provider_operator(form_data: dict[str, Any])` — name, phone, license, status. Contact 10–12 digits, licence 6–30 letters/digits/hyphens and unique, valid availability. Reserved identity/licence/status locked, contact editable. Audits and closes editor.
- `open_provider_panel(panel: str)` — empty/bank/compliance/support/earnings.
- `save_provider_demo(form_data: dict[str, Any])` — value 5–250 characters; only current bank/compliance/support panel; audited sample edits. No real banking details, document verification, support transmission or payment integration.

Every new mutation enforces role Provider AND identity provider-1; record editors additionally enforce ownership. Booking actions validate lifecycle state. The original BMC-8845 arrived operator-1 fixture remains unchanged. A new BMC-8852 approved-but-unassigned fixture enables allocation without inventing an Officer approval button. Approved is recognized by Contractor labels, badges, live explanation and cancellation guard.

Partial acceptance is explicitly shown in Contractor detail/live and Provider detail: original, accepted and unfulfilled quantities and monetary estimates. Unfulfilled units are not billed/deployed; requested_lines/requested_total are used by Officer verification and reporting. Completed earnings sum agreed completed booking totals; completed unit shifts sum quantities. All completed earnings remain sample pending clearance because no bank settlement is modeled. Overtime is stored for fleet reference, not silently billed.

## Three navigation handler tests

`tests/test_provider.py` uses async unittest cases with injected `test_utils.run_event`. Never call decorated handlers directly. Test harness provides run_event and drains returned events; redirect assertions can inspect its captured client events.

1. `open_provider_booking` → detail redirect, then `accept_provider_request` → same detail: assert original 2 units retained, 1 accepted, total halved, pending_approval and assignment attempt blocked.
2. `open_provider_vehicle` → editor, then `save_provider_vehicle` → fleet: assert catalogue rate updated, all previous booking totals unchanged and non-Provider mutation ignored.
3. `open_provider_booking` for approved fixture, then `confirm_provider_assignment` → schedule: assert correct shared pair/status/date/audit, original arrived fixture unchanged, logout preserves deployment.

These tests are added, not executed by the editing tools. Browser coverage should check mobile/wide layouts, bottom navigation clearance, direct-route guards, empty results, form errors, duplicate/overlap rejection, reload reset, and switching back to Contractor to see acceptance/rate changes.
