# Officer workflow — approved checklist item 4

## Scope and routes

Officer demo login selects `officer-1`, Anita Joshi, BMC H/West. This is a single-person cross-role sample-data demo, not production authentication, synchronized multi-user state, GPS, telemetry, messaging or payout processing. All authoritative bookings, quoted lines, identities, fleet, operators, disputes and audits remain on the existing SharedState. New browser documents reset deep-copied fixtures; same-document navigation and role switching retain records. Logout clears Officer booking/entity/dispute selection and action panels, not evidence or records.

All five routes invoke `bootstrap()` → `initialize(token)` with the existing role routing guard:

- `/officer`: date/ward-scoped counts, earliest scheduled approval queue, actual exceptions, active deployment cards and recent audit.
- `/officer/requests`: search ID/work order/site/parties, date/ward filters and All/Awaiting provider/Awaiting approval/Approved/Active/Completed/Closed/Issues filters. Issues includes stopped problem bookings or open linked disputes.
- `/officer/bookings/[booking_id]`: verification, requested versus accepted lines and quote snapshots, resolved allocation, disputes and booking audit. Missing IDs show a helpful empty view without actions. Viewing never adds evidence.
- `/officer/directory`: Providers/Contractors, searchable real identities, derived counts, labeled sample telephone/email links and inline own bookings/fleet/operators. Provider-2 and contractor-2 have no invented bookings or assets.
- `/officer/more`: Reports/Disputes/Audit tabs and logout. CSV exports precisely the current report search/date/ward/status scope, with UTF-8 BOM, proper CSV quoting and spreadsheet-formula escaping. Completed earnings and accepted planned totals are separate estimates; neither represents a payout.

Officer screens share Noto Sans, 16px mobile gutters, thin-bordered white cards on #F5F5F5, charcoal ink, amber primary controls, full-width responsive max-w-5xl shell and four-tab safe-area bottom navigation. No charts or packages were added. Tables scroll inside their containers, not across the whole page.

## Exact public events on SharedState

Every Officer event/selector checks role Officer AND identity officer-1 with a real Officer identity. Record events additionally resolve real IDs and lifecycle eligibility. Form parameters use Reflex's `dict[str, Any]`; stored variables and computed values are fully typed.

### Selection, filters and panels

- `open_officer_booking(booking_id: str)` — validates booking ID, selects it, clears action/messages and redirects to its Officer detail route. Invalid IDs retain prior selection and return an error.
- `filter_officer_bookings(form_data)` — keys `date` (valid ISO or blank), `ward` (All or an actual booking ward); validates atomically. These shared date/ward selectors scope dashboard, requests, reports and disputes.
- `search_officer_bookings(value: str)` — bounded to 120 characters; UI debounce 500ms; searches ID, work order, address and resolved Contractor/Provider names/companies.
- `set_officer_status(value: str)` — All, Awaiting provider, Awaiting approval, Approved, Active, Completed, Closed, Issues; affects Requests and Reports, not dashboard counts.
- `clear_officer_filters()` — restores All status/ward and empty date/search.
- `set_officer_panel(panel: str)` — empty/approve/reject/reassign/note; checks booking and action lifecycle before opening; clearing does not alter records.
- `set_officer_directory_tab(value: str)` — Providers/Contractors; clears inline selection.
- `search_officer_directory(value: str)` — bounded firm/ID/name/contact search.
- `open_officer_entity(entity_id: str)` — validates identity in selected directory tab; blank closes detail.
- `set_officer_more_tab(value: str)` — Reports/Disputes/Audit; clears dispute selection and transient messages.
- `filter_officer_disputes(form_data)` — keys `status` Open/Resolved/All and `category` All/Breakdown/Delay/Safety/Billing/Other; validates before applying.
- `open_officer_dispute(dispute_id: str)` — validates real case and linked booking; blank closes inline resolution.
- `search_officer_audit(value: str)` — bounded search over booking/action/note/actor ID and resolved actor name.
- `filter_officer_audit(form_data)` — keys `date` valid ISO or blank and `action` All or existing action; no evidence mutation.

### Review and lifecycle

- `approve_officer_booking(form_data)` — keys `site_verified`, `work_order_verified`, `provider_verified`, `safety_verified`, `partial_ack`, `note`. Only pending_approval with Provider acceptance, no allocation/start/end, at least one accepted unit, matching requested/accepted equipment sets without duplicates, whole bounded quantities, accepted <= requested, original rates/hours, finite exact quote totals, real party/catalogue IDs and Provider ownership. Valid current/future date within 365 days, shift/hours, site address, ward, work order and Contractor safety readiness required. All four verification checkboxes and note 5–1000 characters required; partial acceptance additionally requires explicit partial_ack. Records approved plus officer-authored audit. Does NOT assign resources or start work; quotes/requests/Provider are unchanged. Duplicate approval is blocked.
- `add_officer_note(form_data)` — key `note`, 5–1000 characters. Appends officer_review evidence for current real booking, without changing lifecycle. Used for Record review / Ask for info; no message is transmitted.
- `reject_officer_booking(form_data)` — keys `reason` 5–500 characters, `confirm`. Pending-approval or approved only, with no start/end timestamps. Records rejected/reason/audit and uses shared resource synchronization so another nonterminal booking's reservation is never released. Arrived/working/end-handoff/completed work is blocked.
- `reassign_officer_booking(form_data)` — `reason` 5–500, `confirm`, then `vehicle_{unit.key}` and `operator_{unit.key}` for EACH accepted unit. `officer_units` keys are equipment_id plus zero-based index (e.g. eq-4_0). Assigned/in_transit/unstarted problem only; no started or ended timestamp. Entire replacement is validated before mutation: same booked Provider, matching equipment/category, real available vehicle/operator (or current assigned pair), unique vehicle/operator per unit, no overlapping nonterminal booking reservation using `_resource_conflict`. Existing pairs may be kept. Assignments change atomically, status becomes assigned, shared `_sync_booking_resources` refreshes both old and new resources and `_resource_reserved` protects other reservations. A changed allocation or reset from transit/problem generates a different start PIN. End PIN, dates, requested quantities, accepted rates and totals remain intact. Arrived/started/working/awaiting_end/completed cannot revert. Audit records old/new pairs and reason. Provider-2 is not fabricated as a replacement fleet.
- `resolve_officer_dispute(form_data)` — keys `note` 10–1000 characters and `confirm`; only selected real open case with existing booking. Stores resolved/resolution and appends dispute_resolved audit with case ID. Preserves ALL booking phases/timestamps/allocations. A stopped legacy problem booking never silently resumes; review/reassignment is separate. Original reporter is resolved from matching issue_reported audit when present, otherwise contractor_id. Resolved cases remain searchable and read-only; no reopening action is offered.
- `export_officer_report()` — guarded backend CSV generation and `rx.download(data=..., filename=...)`. Uses filtered current records, with requested/accepted quantities and estimates, parties, date/ward/status, work order/site. No filesystem, bank or network operation.
- `logout()` — existing event also clears Officer transient selections/panel, retains sample mutations and redirects to login.

Audit records are append-only through public UI events; there is no editing/deleting evidence. Production immutable storage is not claimed.

## Qualifying tests to run

`tests/test_officer.py` uses injected `test_utils.run_event`; it never directly invokes decorated events. Each independent scenario constructs SharedState(_reflex_internal_init=True), assigns role/identity afterward and DEEPCOPYs sample_fixtures plus catalogue/identities. Constructor kwargs for data/role are intentionally avoided. Tests were added, not executed by these editing tools. With the injected harness available, run `python -m unittest discover -s tests -p test_officer.py` and the existing Contractor/Provider/Operator suites.

1. Review navigation: login Officer → Requests → BMC-8842 → Review verification. Missing checkbox/wrong note/partial acknowledgement must show error without mutations. Approve valid partial request; audit actor is Anita/officer-1 and quotes remain unchanged. Switch role in the same document to Provider, allocate that approved booking; Contractor sees acceptance and assignment. Direct wrong-domain routes redirect to the current role; invalid Officer booking ID shows empty details.
2. Replacement and errors: open BMC-8843 assigned or BMC-8851 stopped problem. Open reassignment, try wrong equipment/Provider, duplicate resources, overlapping reservations, missing confirmation: no partial mutation. Valid complete replacement updates both domains, releases only unreserved old pairs and regenerates start PIN when necessary. Keeping an existing nonconflicting pair works. BMC-8845 arrived and BMC-8846 working must have disabled rejection/reassignment and backend attempts must be blocked.
3. Directory → More flow at 390×844 and desktop: inspect provider-2/contractor-2 empty own records, search/clear filters, Reports → export CSV and compare filtered rows/totals, Disputes → short/unconfirmed resolution error → valid resolution, verify stopped booking stays problem and active working timestamp is unchanged. Audit search shows actor/action/case evidence and booking link. Use keyboard to reach all controls, check four-tab dock and no horizontal page overflow/browser errors. Logout retains records; full reload clears login and restores fixtures/new Officer fields. Navigate all existing domain screens to confirm regression-free layouts and handoffs.
