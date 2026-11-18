# Operator workflow (approved checklist item 3)

This is a local, single-tab demo using the existing SharedState records. Operator login resolves operator-1, Ramesh Solanki, from the same operators list used by Provider. Provider is Desai Earthmovers. No production authentication, GPS, machine telemetry, messaging, payment, support transmission or external service is connected. Officer review, allocation replacement and dispute resolution use the same session records.

## Routes and selectors

Every route runs SharedState.bootstrap → initialize. `/operator` and `/operator/today` show the operationally prioritized assignment; working and end handoff take precedence over arrival, transit and assigned work. BMC-8845 starts as arrived for operator-1. `/operator/start` and `/operator/shift` resolve the current operational booking. Explicit routes are `/operator/bookings/[booking_id]/start`, `/operator/bookings/[booking_id]/shift` and read-only `/operator/bookings/[booking_id]`. `/operator/history` filters owned assignments by date/status. `/operator/profile` uses the actual operator record.

All Operator events and selectors require role Operator, identity operator-1, and an existing operator record. Booking events additionally require an assignment with that operator_id. Operator views blank both PINs and filter assignments/units to the logged-in operator. Shared lifecycle status remains book-level for multiunit bookings; no per-unit restart or private identity-edit actions are exposed. Unapproved or unassigned work cannot start. History details have no mutation controls.

## Exact events

- `open_operator_booking(booking_id, view)` — guarded navigation; view is start, shift or detail. Clears entered code and messages.
- `operator_transit()` — assigned → in_transit, only on the scheduled date; records audit without GPS.
- `operator_arrive()` — in_transit → arrived; audits and opens start-code screen.
- `operator_key(key)` — append one digit, clear, or backspace; at most four digits; only arrived/awaiting_end.
- `verify_operator_start(form_data)` — reads code from optional form `code` or keypad state; exactly four numeric digits must equal the authoritative start_pin. Requires arrived, no prior start timestamp, and safety_confirmed. Records working, UTC started_at, resource reservations and audit; navigates to live shift. Duplicate working submission does not restart.
- `operator_request_end()` — working → awaiting_end; audits inspection/code request. Does not release resources or stop timestamp-based elapsed display.
- `verify_operator_end(form_data)` — code must equal end_pin and `inspection` must confirm contractor inspection/equipment secured. Requires awaiting_end and a start timestamp. Records completed, ended_at and audit; releases resources only if no other nonterminal booking reserves them. Already-completed submissions are no-ops. Wrong PINs never mutate bookings.
- `set_operator_panel(panel)` — empty, report or support; reporting additionally requires an eligible owned operational phase.
- `operator_report_issue(form_data)` — category Breakdown/Delay/Safety/Other and description 10–1000 characters. Creates an open shared dispute using the booking's contractor_id and an operator-authored audit. Preserves the current operational phase, timestamps and reservations: reports never automatically restart, complete or silently release unsafe equipment. The user is instructed to stop unsafe work and contact supervision directly.
- `filter_operator_history(value)` — All, Active, Completed, Closed.
- `set_operator_date(value)` — valid ISO date or empty.
- `clear_operator_filters()` — clears date and restores All.
- `save_operator_phone(form_data)` — edits only own contact; 10–12 digits with optional phone punctuation. Does not alter licence/availability or transmit anything.
- `logout()` — clears identity, entered codes and panels, retaining bookings/resources/disputes/contact changes for role switching. A new document token resets all new Operator fields and shared fixtures. Client navigation preserves operational data.

Contractor `confirm_start` and `confirm_end` remain explicitly labelled demo shortcuts. They use the same statuses, timestamps and resource synchronization as the Operator pathway. Site safety/arrival and end inspection checkboxes remain meaningful; status/timestamp guards prevent duplicate starts or completions. Contractor `request_end` reaches the same awaiting_end phase. Provider counts use assigned resources during working; completed bookings immediately contribute to existing demo earnings.

The custom elapsed-clock client component derives its display from started_at and Date.now(), then from ended_at once completed. Its interval and mutation observer are removed on component unmount/disconnection; there is no server polling. Elapsed includes time awaiting end inspection, and is not a billing or telemetry measure.

## Qualifying navigation checks to perform

1. At 390×844, choose Operator at login; verify Ramesh Solanki, Desai Earthmovers and BMC-8845. Enter start screen, use keypad/backspace/clear and submit a wrong PIN: visible error, still arrived. Switch via Profile logout to Contractor in the same tab, obtain the start PIN from BMC-8845 Live Booking without using the demo shortcut; return to Operator, verify it and confirm live elapsed advances over two seconds. Switch to History/Profile and back; timer must resume from the timestamp, not zero. Check no horizontal overflow or browser errors.
2. From live shift, record a valid Safety issue; switch Contractor and verify the shared dispute and unchanged working status. Return Operator, request end, try wrong end code and missing inspection: no completion. Obtain Contractor end PIN, complete after inspection, and verify frozen duration and audit in read-only History detail. Switch Provider and verify completed schedule and earnings plus released resources. Repeat submission: no extra completion audit or timestamp change.
3. In a fixture with multiple owned assignments, confirm operational phase wins over newest date; future assigned work cannot transit. Open another operator's explicit booking URL: no assignment/secret/actions. Navigate Today → History → detail → Profile → logout; phone edit persists on role switch, while full reload resets contact and Operator filters/code/panel. Officer opens its completed dashboard and sees the shared lifecycle and disputes.

`tests/test_operator.py` supplies three run_event scenarios covering lifecycle navigation/idempotency, ownership/approval/multiunit guards, and issue/profile/logout/code controls. Standalone state construction MUST use `SharedState(_reflex_internal_init=True)` followed by role/identity assignment; constructor keywords are ignored by the framework. Tests are added, not executed by this editing pass.
