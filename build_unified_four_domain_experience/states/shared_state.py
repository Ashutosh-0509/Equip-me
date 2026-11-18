import reflex as rx

from copy import deepcopy
from datetime import date, datetime, timezone
from secrets import randbelow
import math
import re
import csv
import io
from typing import Any
from uuid import uuid4

from build_unified_four_domain_experience.states.demo_data import (
    Audit,
    Assignment,
    Booking,
    CATALOGUE,
    CONTRACTORS,
    Dispute,
    EMPTY_BOOKING,
    Equipment,
    IDENTITIES,
    Identity,
    Line,
    Operator,
    PROVIDERS,
    SHIFTS,
    STATUS_LABELS,
    Vehicle,
    sample_fixtures,
)

SEED_BOOKINGS, SEED_VEHICLES, SEED_OPERATORS, SEED_AUDITS, SEED_DISPUTES = (
    sample_fixtures()
)
TERMINAL = {"completed", "cancelled", "rejected"}
CANCELLABLE = {
    "draft",
    "pending_provider",
    "pending_approval",
    "approved",
    "assigned",
    "in_transit",
}
DESTINATIONS = {
    "Contractor": "/contractor",
    "Provider": "/provider",
    "Operator": "/operator",
    "Officer": "/officer",
}


class SharedState(rx.State):
    document_token: str = ""
    role: str = ""
    identity_id: str = ""
    selected_role: str = "Contractor"
    catalogue: list[Equipment] = deepcopy(CATALOGUE)
    identities: list[Identity] = deepcopy(IDENTITIES)
    contractors: list[Identity] = deepcopy(CONTRACTORS)
    providers: list[Identity] = deepcopy(PROVIDERS)
    bookings: list[Booking] = deepcopy(SEED_BOOKINGS)
    vehicles: list[Vehicle] = deepcopy(SEED_VEHICLES)
    operators: list[Operator] = deepcopy(SEED_OPERATORS)
    audit: list[Audit] = deepcopy(SEED_AUDITS)
    disputes: list[Dispute] = deepcopy(SEED_DISPUTES)
    selected: dict[str, int] = {"eq-1": 1}
    query: str = ""
    category: str = "All"
    booking_filter: str = "All"
    draft_date: str = (date.today()).isoformat()
    draft_shift: str = "Shift A · 08:00–16:00"
    draft_address: str = "Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai 400054"
    draft_ward: str = "H/West"
    draft_latitude: str = "19.0830"
    draft_longitude: str = "72.8370"
    draft_work_order: str = (
        "WO-2026-8842 · Storm Water Drain Widening & Desilting"
    )
    draft_source_id: str = ""
    schedule_saved: bool = False
    site_saved: bool = False
    error: str = ""
    feedback: str = ""
    action_panel: str = ""
    active_booking_id: str = ""
    operator_booking_id: str = ""
    operator_code: str = ""
    operator_filter: str = "All"
    operator_date: str = ""
    operator_panel: str = ""
    officer_booking_id: str = ""
    officer_query: str = ""
    officer_date: str = ""
    officer_ward: str = "All"
    officer_status: str = "All"
    officer_directory_tab: str = "Providers"
    officer_directory_query: str = ""
    officer_entity_id: str = ""
    officer_more_tab: str = "Reports"
    officer_dispute_filter: str = "Open"
    officer_dispute_category: str = "All"
    officer_dispute_id: str = ""
    officer_audit_query: str = ""
    officer_audit_date: str = ""
    officer_audit_action: str = "All"
    officer_panel: str = ""
    provider_booking_id: str = ""
    provider_vehicle_id: str = ""
    provider_operator_id: str = ""
    provider_tab: str = "Vehicles"
    provider_query: str = ""
    provider_filter: str = "All"
    provider_date: str = date.today().isoformat()
    provider_panel: str = ""
    provider_demo: dict[str, str] = {
        "bank": "Demo bank · account ending 0042",
        "compliance": "Sample documents only; not verified by BMC",
        "support": "dispatch@example.test",
    }

    @rx.var
    def login_identity(self) -> Identity:
        return next(
            (i for i in self.identities if i["role"] == self.selected_role),
            deepcopy(IDENTITIES[0]),
        )

    @rx.var
    def contractor_identity(self) -> Identity:
        return next(
            (i for i in self.contractors if i["id"] == self.identity_id),
            deepcopy(CONTRACTORS[0]),
        )

    @rx.var
    def today(self) -> str:
        return date.today().isoformat()

    @rx.var
    def filtered_equipment(self) -> list[Equipment]:
        query = self.query.strip().lower()
        return [
            e
            for e in self.catalogue
            if (self.category == "All" or e["category"] == self.category)
            and query in f"{e['name']} {e['description']}".lower()
        ]

    @rx.var
    def draft_hours(self) -> int:
        return SHIFTS.get(self.draft_shift, 0)

    @rx.var
    def draft_lines(self) -> list[Line]:
        return [
            {
                "equipment_id": e["id"],
                "name": e["name"],
                "quantity": self.selected[e["id"]],
                "rate": e["rate"],
                "hours": self.draft_hours,
                "amount": e["rate"] * self.selected[e["id"]] * self.draft_hours,
            }
            for e in self.catalogue
            if self.selected.get(e["id"], 0) > 0
        ]

    @rx.var
    def draft_total(self) -> float:
        return sum(line["amount"] for line in self.draft_lines)

    @rx.var
    def selected_count(self) -> int:
        return sum(self.selected.values())

    @rx.var
    def hourly_total(self) -> float:
        return sum(
            e["rate"] * self.selected.get(e["id"], 0) for e in self.catalogue
        )

    @rx.var
    def contractor_bookings(self) -> list[Booking]:
        return [
            b for b in self.bookings if b["contractor_id"] == self.identity_id
        ]

    @rx.var
    def recent_bookings(self) -> list[Booking]:
        return sorted(
            self.contractor_bookings,
            key=lambda b: (b["date"], b["id"]),
            reverse=True,
        )[:4]

    @rx.var
    def active_count(self) -> int:
        return sum(
            b["status"] not in TERMINAL and b["status"] != "draft"
            for b in self.contractor_bookings
        )

    @rx.var
    def completed_count(self) -> int:
        return sum(b["status"] == "completed" for b in self.contractor_bookings)

    @rx.var
    def filtered_bookings(self) -> list[Booking]:
        return sorted(
            [
                b
                for b in self.contractor_bookings
                if self.booking_filter == "All"
                or (
                    self.booking_filter == "Active"
                    and b["status"] not in TERMINAL
                    and b["status"] != "draft"
                )
                or (
                    self.booking_filter == "Completed"
                    and b["status"] == "completed"
                )
                or (self.booking_filter == "Drafts" and b["status"] == "draft")
                or (
                    self.booking_filter == "Closed"
                    and b["status"] in {"cancelled", "rejected"}
                )
            ],
            key=lambda b: (b["date"], b["id"]),
            reverse=True,
        )

    @rx.var
    def current_booking(self) -> Booking:
        return deepcopy(
            next(
                (
                    b
                    for b in self.bookings
                    if b["id"] == self.active_booking_id
                    and b["contractor_id"] == self.identity_id
                ),
                EMPTY_BOOKING,
            )
        )

    @rx.var
    def status_label(self) -> str:
        return STATUS_LABELS.get(
            self.current_booking["status"], "Booking status"
        )

    @rx.var
    def can_cancel(self) -> bool:
        return (
            bool(self.current_booking["id"])
            and self.current_booking["status"] in CANCELLABLE
        )

    @rx.var
    def can_report(self) -> bool:
        return bool(self.current_booking["id"]) and self.current_booking[
            "status"
        ] not in {"draft", "rejected", "cancelled"}

    @rx.var
    def assigned_people(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for assignment in self.current_booking["assignments"]:
            vehicle = next(
                (
                    v
                    for v in self.vehicles
                    if v["id"] == assignment["vehicle_id"]
                ),
                None,
            )
            operator = next(
                (
                    o
                    for o in self.operators
                    if o["id"] == assignment["operator_id"]
                ),
                None,
            )
            equipment = next(
                (
                    e
                    for e in self.catalogue
                    if e["id"] == assignment["equipment_id"]
                ),
                None,
            )
            result.append(
                {
                    "vehicle": vehicle["registration"]
                    if vehicle
                    else "Assignment pending",
                    "operator": operator["name"]
                    if operator
                    else "Operator pending",
                    "equipment": equipment["name"]
                    if equipment
                    else "Equipment",
                    "id": assignment["vehicle_id"],
                }
            )
        return result

    @rx.var
    def booking_audit(self) -> list[Audit]:
        return [
            a
            for a in self.audit
            if a["booking_id"] == self.current_booking["id"]
        ]

    @rx.var
    def booking_disputes(self) -> list[Dispute]:
        return [
            d
            for d in self.disputes
            if d["booking_id"] == self.current_booking["id"]
        ]

    def _allowed(self) -> bool:
        return self.role == "Contractor" and self.identity_id == "contractor-1"

    def _owned(self, booking_id: str) -> Booking | None:
        if not self._allowed():
            return None
        return next(
            (
                b
                for b in self.bookings
                if b["id"] == booking_id
                and b["contractor_id"] == self.identity_id
            ),
            None,
        )

    def _audit(self, booking_id: str, action: str, note: str = ""):
        self.audit.append(
            {
                "id": f"audit-{uuid4().hex[:12]}",
                "booking_id": booking_id,
                "actor_id": self.identity_id,
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "note": note,
            }
        )

    def _schedule_error(self) -> str:
        if not self.selected or not self.draft_lines:
            return "Select at least one equipment item."
        if any(q < 1 or q > 10 for q in self.selected.values()):
            return "Each equipment quantity must be between 1 and 10."
        try:
            scheduled = date.fromisoformat(self.draft_date)
        except ValueError:
            return "Choose a valid booking date."
        if scheduled < date.today():
            return "Booking date cannot be in the past."
        if (scheduled - date.today()).days > 365:
            return "Choose a date within the next 12 months."
        if self.draft_shift not in SHIFTS:
            return "Choose a valid shift."
        return ""

    def _site_error(self) -> str:
        if len(self.draft_address.strip()) < 12:
            return "Enter a complete site address (at least 12 characters)."
        if not self.draft_ward.strip() or len(self.draft_ward) > 40:
            return "Enter a valid BMC ward."
        if len(self.draft_work_order.strip()) < 5:
            return "Enter the work-order or project reference."
        try:
            latitude, longitude = (
                float(self.draft_latitude),
                float(self.draft_longitude),
            )
        except ValueError:
            return "Enter numeric latitude and longitude."
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            return "Latitude must be −90 to 90; longitude must be −180 to 180."
        return ""

    @rx.event
    def bootstrap(self):
        return rx.call_script(
            "window.__heavyLogixDocument ||= crypto.randomUUID(); window.__heavyLogixDocument",
            callback=SharedState.initialize,
        )

    @rx.event
    def initialize(self, token: str):
        if token != self.document_token:
            self.document_token = token
            self.role = ""
            self.identity_id = ""
            self.selected_role = "Contractor"
            self.catalogue = deepcopy(CATALOGUE)
            self.identities = deepcopy(IDENTITIES)
            self.contractors = deepcopy(CONTRACTORS)
            self.providers = deepcopy(PROVIDERS)
            (
                self.bookings,
                self.vehicles,
                self.operators,
                self.audit,
                self.disputes,
            ) = deepcopy(
                (
                    SEED_BOOKINGS,
                    SEED_VEHICLES,
                    SEED_OPERATORS,
                    SEED_AUDITS,
                    SEED_DISPUTES,
                )
            )
            self.selected = {"eq-1": 1}
            self.draft_date = date.today().isoformat()
            self.draft_shift = "Shift A · 08:00–16:00"
            self.draft_address = "Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai 400054"
            self.draft_ward = "H/West"
            self.draft_latitude = "19.0830"
            self.draft_longitude = "72.8370"
            self.draft_work_order = (
                "WO-2026-8842 · Storm Water Drain Widening & Desilting"
            )
            self.active_booking_id = ""
            self.draft_source_id = ""
            self.schedule_saved = False
            self.site_saved = False
            self.query = ""
            self.category = "All"
            self.booking_filter = "All"
            self.operator_booking_id = ""
            self.operator_code = ""
            self.operator_filter = "All"
            self.operator_date = ""
            self.operator_panel = ""
            self.officer_booking_id = ""
            self.officer_query = ""
            self.officer_date = ""
            self.officer_ward = "All"
            self.officer_status = "All"
            self.officer_directory_tab = "Providers"
            self.officer_directory_query = ""
            self.officer_entity_id = ""
            self.officer_more_tab = "Reports"
            self.officer_dispute_filter = "Open"
            self.officer_dispute_category = "All"
            self.officer_dispute_id = ""
            self.officer_audit_query = ""
            self.officer_audit_date = ""
            self.officer_audit_action = "All"
            self.officer_panel = ""
            self.provider_booking_id = ""
            self.provider_vehicle_id = ""
            self.provider_operator_id = ""
            self.provider_tab = "Vehicles"
            self.provider_query = ""
            self.provider_filter = "All"
            self.provider_date = date.today().isoformat()
            self.provider_panel = ""
            self.provider_demo = {
                "bank": "Demo bank · account ending 0042",
                "compliance": "Sample documents only; not verified by BMC",
                "support": "dispatch@example.test",
            }
        self.error = ""
        self.feedback = ""
        self.action_panel = ""
        path = self.router.url.path.rstrip("/") or "/"
        if path in ("/", "/login"):
            if self.role:
                return rx.redirect(DESTINATIONS[self.role])
            return
        if not self.role:
            return rx.redirect("/login")
        expected = path.split("/")[1].capitalize()
        if expected != self.role:
            return rx.redirect(DESTINATIONS[self.role])
        if expected == "Operator":
            if not self._operator_allowed():
                return rx.redirect("/login")
            self.operator_code = ""
            self.operator_panel = ""
            requested = str(self.router.page.params.get("booking_id", ""))
            self.operator_booking_id = (
                requested or self.operator_today_booking["id"]
            )
            booking = self._operator_owned(self.operator_booking_id)
            if requested and not booking:
                self.operator_booking_id = ""
                self.error = "This assignment is not available to you."
            if (
                path.endswith("/start")
                and booking
                and booking["status"] != "arrived"
            ):
                return rx.redirect(f"/operator/bookings/{booking['id']}/shift")
        if expected == "Officer":
            if not self._officer_allowed():
                return rx.redirect("/login")
            requested = str(self.router.page.params.get("booking_id", ""))
            self.officer_booking_id = requested
            self.officer_panel = ""
            if requested and not self._officer_booking(requested):
                self.officer_booking_id = ""
                self.error = (
                    "Booking not found. Choose a booking from Requests."
                )
        if expected == "Provider":
            if not self._provider_allowed():
                return rx.redirect("/login")
            self.provider_booking_id = str(
                self.router.page.params.get("booking_id", "")
            )
            self.provider_vehicle_id = str(
                self.router.page.params.get("equipment_id", "")
            )
            self.provider_panel = ""
        if expected == "Contractor":
            self.active_booking_id = str(
                self.router.page.params.get("booking_id", "")
            )
            if path.endswith("/step-2") and not self.schedule_saved:
                return rx.redirect("/contractor/booking/step-1")
            if path.endswith("/step-3") and (
                not self.schedule_saved or not self.site_saved
            ):
                return rx.redirect("/contractor/booking/step-1")

    @rx.event
    def select_role(self, role: str):
        if role in DESTINATIONS and not self.role:
            self.selected_role = role
            self.error = ""

    @rx.event
    def login(self):
        if self.role or self.selected_role not in DESTINATIONS:
            return
        self.role = self.selected_role
        self.identity_id = self.login_identity["id"]
        return rx.redirect(DESTINATIONS[self.role])

    @rx.event
    def logout(self):
        self.role = ""
        self.identity_id = ""
        self.active_booking_id = ""
        self.operator_booking_id = ""
        self.operator_code = ""
        self.operator_panel = ""
        self.officer_booking_id = ""
        self.officer_entity_id = ""
        self.officer_dispute_id = ""
        self.officer_panel = ""
        self.error = ""
        self.feedback = ""
        self.action_panel = ""
        return rx.redirect("/login")

    @rx.event
    def search(self, query: str):
        if self._allowed():
            self.query = query[:120]

    @rx.event
    def choose_category(self, category: str):
        if self._allowed() and category in {
            "All",
            "Earthmoving",
            "Haulage",
            "Compaction & RMC",
            "Cranes",
        }:
            self.category = category

    @rx.event
    def clear_filters(self):
        if self._allowed():
            self.query = ""
            self.category = "All"

    @rx.event
    def toggle_equipment(self, equipment_id: str):
        if not self._allowed() or equipment_id not in {
            e["id"] for e in self.catalogue
        }:
            return
        if equipment_id in self.selected:
            del self.selected[equipment_id]
        else:
            self.selected[equipment_id] = 1
        self.schedule_saved = False
        self.site_saved = False
        self.error = ""

    @rx.event
    def change_quantity(self, equipment_id: str, change: int):
        if (
            not self._allowed()
            or equipment_id not in self.selected
            or change not in (-1, 1)
        ):
            return
        self.selected[equipment_id] = min(
            10, max(1, self.selected[equipment_id] + change)
        )
        self.schedule_saved = False
        self.site_saved = False

    @rx.event
    def proceed_booking(self):
        if not self._allowed():
            return rx.redirect("/login")
        if not self.selected:
            self.error = "Select equipment before continuing."
            return
        return rx.redirect("/contractor/booking/step-1")

    @rx.event
    def choose_shift(self, shift: str):
        if self._allowed() and shift in SHIFTS:
            self.draft_shift = shift
            self.schedule_saved = False
            self.site_saved = False

    @rx.event
    def save_schedule(self, form_data: dict[str, Any]):
        if not self._allowed():
            return rx.redirect("/login")
        self.draft_date = str(form_data.get("date", ""))
        self.draft_shift = str(form_data.get("shift", ""))
        self.error = self._schedule_error()
        self.schedule_saved = not bool(self.error)
        self.site_saved = False
        if not self.error:
            return rx.redirect("/contractor/booking/step-2")

    @rx.event
    def save_site(self, form_data: dict[str, Any]):
        if not self._allowed():
            return rx.redirect("/login")
        if not self.schedule_saved or self._schedule_error():
            return rx.redirect("/contractor/booking/step-1")
        self.draft_address = str(form_data.get("address", "")).strip()[:500]
        self.draft_ward = str(form_data.get("ward", "")).strip()[:40]
        self.draft_latitude = str(form_data.get("latitude", "")).strip()[:30]
        self.draft_longitude = str(form_data.get("longitude", "")).strip()[:30]
        self.draft_work_order = str(form_data.get("work_order", "")).strip()[
            :250
        ]
        self.error = self._site_error()
        self.site_saved = not bool(self.error)
        if not self.error:
            return rx.redirect("/contractor/booking/step-3")

    @rx.event
    def submit_booking(self, form_data: dict[str, Any]):
        if not self._allowed():
            return rx.redirect("/login")
        self.error = self._schedule_error() or self._site_error()
        if self.error:
            return
        if not self.schedule_saved or not self.site_saved:
            self.error = "Save equipment, schedule and site before confirming."
            return
        if not form_data.get("safety"):
            self.error = (
                "Confirm site access and safety readiness before booking."
            )
            return
        source = self._owned(self.draft_source_id)
        if source and source["status"] != "draft":
            self.error = "This draft has already been submitted."
            return
        booking_id = self.draft_source_id or f"BMC-{uuid4().hex[:8].upper()}"
        booking: Booking = {
            "id": booking_id,
            "contractor_id": self.identity_id,
            "provider_id": "provider-1",
            "status": "pending_provider",
            "date": self.draft_date,
            "shift": self.draft_shift,
            "hours": self.draft_hours,
            "address": self.draft_address,
            "ward": self.draft_ward,
            "latitude": self.draft_latitude,
            "longitude": self.draft_longitude,
            "work_order": self.draft_work_order,
            "lines": deepcopy(self.draft_lines),
            "requested_lines": deepcopy(self.draft_lines),
            "requested_total": self.draft_total,
            "provider_reviewed": False,
            "total": self.draft_total,
            "assignments": [],
            "start_pin": str(1000 + randbelow(9000)),
            "end_pin": str(1000 + randbelow(9000)),
            "started_at": "",
            "ended_at": "",
            "reason": "",
            "safety_confirmed": True,
        }
        if source:
            self.bookings = [
                booking if b["id"] == booking_id else b for b in self.bookings
            ]
        else:
            self.bookings.append(booking)
        self._audit(
            booking_id,
            "pending_provider",
            "Contractor submitted booking; site safety confirmed.",
        )
        self.selected = {}
        self.draft_source_id = ""
        self.schedule_saved = False
        self.site_saved = False
        return rx.redirect(f"/contractor/bookings/{booking_id}")

    @rx.event
    def filter_bookings(self, value: str):
        if self._allowed() and value in {
            "All",
            "Active",
            "Completed",
            "Drafts",
            "Closed",
        }:
            self.booking_filter = value

    @rx.event
    def resume_draft(self, booking_id: str):
        booking = self._owned(booking_id)
        if not booking or booking["status"] != "draft":
            return
        self.selected = {
            line["equipment_id"]: line["quantity"] for line in booking["lines"]
        }
        self.draft_date = max(booking["date"], date.today().isoformat())
        self.draft_shift = booking["shift"]
        self.draft_address = booking["address"]
        self.draft_ward = booking["ward"]
        self.draft_latitude = booking["latitude"]
        self.draft_longitude = booking["longitude"]
        self.draft_work_order = booking["work_order"]
        self.draft_source_id = booking_id
        self.schedule_saved = False
        self.site_saved = False
        return rx.redirect("/contractor/booking/step-1")

    @rx.event
    def open_action(self, action: str):
        if not self._owned(self.active_booking_id):
            return
        if (action == "cancel" and self.can_cancel) or (
            action == "report" and self.can_report
        ):
            self.action_panel = action
            self.error = ""
            self.feedback = ""

    @rx.event
    def close_action(self):
        if self._allowed():
            self.action_panel = ""
            self.error = ""

    @rx.event
    def cancel_booking(self, form_data: dict[str, Any]):
        if not self._allowed():
            return rx.redirect("/login")
        booking = self._owned(self.active_booking_id)
        if not booking or booking["status"] not in CANCELLABLE:
            self.error = "This booking can no longer be cancelled. Report an issue instead."
            return
        reason = str(form_data.get("reason", "")).strip()[:500]
        if len(reason) < 5 or not form_data.get("confirm"):
            self.error = "Enter a reason and confirm cancellation."
            return
        booking["status"] = "cancelled"
        booking["reason"] = reason
        for assignment in booking["assignments"]:
            for vehicle in self.vehicles:
                if vehicle["id"] == assignment["vehicle_id"]:
                    vehicle["status"] = "available"
            for operator in self.operators:
                if operator["id"] == assignment["operator_id"]:
                    operator["status"] = "available"
        self.bookings = deepcopy(self.bookings)
        self._audit(booking["id"], "cancelled", reason)
        self.action_panel = ""
        self.feedback = "Booking cancelled."

    @rx.event
    def report_issue(self, form_data: dict[str, Any]):
        booking = self._owned(self.active_booking_id)
        if not booking or booking["status"] in {
            "draft",
            "rejected",
            "cancelled",
        }:
            return
        description = str(form_data.get("description", "")).strip()[:1000]
        category = str(form_data.get("category", ""))
        if len(description) < 10 or category not in {
            "Breakdown",
            "Delay",
            "Safety",
            "Billing",
            "Other",
        }:
            self.error = "Choose an issue type and describe the issue (at least 10 characters)."
            return
        dispute_id = f"dispute-{uuid4().hex[:10]}"
        self.disputes.append(
            {
                "id": dispute_id,
                "booking_id": booking["id"],
                "contractor_id": self.identity_id,
                "category": category,
                "description": description,
                "status": "open",
                "resolution": "",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._audit(
            booking["id"], "issue_reported", f"{category}: {description}"
        )
        self.action_panel = ""
        self.feedback = "Issue recorded for officer review."
        self.error = ""

    @rx.event
    def confirm_start(self, form_data: dict[str, Any]):
        booking = self._owned(self.active_booking_id)
        if not booking or booking["status"] != "arrived":
            return
        if (
            booking["started_at"]
            or not booking["assignments"]
            or not booking["safety_confirmed"]
        ):
            self.error = (
                "An assigned operator and confirmed site safety are required."
            )
            return
        if not form_data.get("arrival_confirmed"):
            self.error = "Confirm equipment arrival and site safety first."
            return
        booking["status"] = "working"
        booking["started_at"] = datetime.now(timezone.utc).isoformat()
        self._sync_booking_resources(booking)
        self.bookings = deepcopy(self.bookings)
        self._audit(
            booking["id"],
            "working",
            "Contractor confirmed arrival and authorized start in demo.",
        )
        self.error = ""
        self.feedback = "Start authorized. Work is in progress."

    @rx.event
    def confirm_end(self, form_data: dict[str, Any]):
        booking = self._owned(self.active_booking_id)
        if not booking or booking["status"] != "awaiting_end":
            return
        if booking["ended_at"] or not booking["started_at"]:
            return
        if not form_data.get("end_confirmed"):
            self.error = "Confirm inspection and end-code handoff first."
            return
        booking["status"] = "completed"
        booking["ended_at"] = datetime.now(timezone.utc).isoformat()
        self._sync_booking_resources(booking)
        self.bookings = deepcopy(self.bookings)
        self._audit(
            booking["id"],
            "completed",
            "Contractor confirmed inspection and end-code handoff in demo.",
        )
        self.error = ""
        self.feedback = "End handoff recorded. Booking completed."

    def _sync_booking_resources(self, booking: Booking):
        for assignment in booking["assignments"]:
            for records, key in (
                (self.vehicles, "vehicle_id"),
                (self.operators, "operator_id"),
            ):
                for resource in records:
                    if resource["id"] == assignment[key]:
                        resource["status"] = (
                            "assigned"
                            if self._resource_reserved(key, resource["id"])
                            else "available"
                        )
        self.vehicles = deepcopy(self.vehicles)
        self.operators = deepcopy(self.operators)

    def _operator_allowed(self) -> bool:
        return (
            self.role == "Operator"
            and self.identity_id == "operator-1"
            and any(o["id"] == self.identity_id for o in self.operators)
        )

    def _operator_owned(self, booking_id: str) -> Booking | None:
        if not self._operator_allowed():
            return None
        return next(
            (
                b
                for b in self.bookings
                if b["id"] == booking_id
                and any(
                    a["operator_id"] == self.identity_id
                    for a in b["assignments"]
                )
            ),
            None,
        )

    def _operator_view(self, booking: Booking) -> Booking:
        result = deepcopy(booking)
        result["start_pin"] = ""
        result["end_pin"] = ""
        result["assignments"] = [
            a
            for a in result["assignments"]
            if a["operator_id"] == self.identity_id
        ]
        equipment_ids = {a["equipment_id"] for a in result["assignments"]}
        result["lines"] = [
            l for l in result["lines"] if l["equipment_id"] in equipment_ids
        ]
        result["requested_lines"] = []
        return result

    @rx.var
    def operator_record(self) -> Operator:
        empty: Operator = {
            "id": "",
            "provider_id": "",
            "name": "",
            "phone": "",
            "license": "",
            "status": "",
        }
        return deepcopy(
            next(
                (
                    o
                    for o in self.operators
                    if self._operator_allowed() and o["id"] == self.identity_id
                ),
                empty,
            )
        )

    @rx.var
    def operator_company(self) -> str:
        return next(
            (
                p["company"]
                for p in self.providers
                if p["id"] == self.operator_record["provider_id"]
            ),
            "",
        )

    @rx.var
    def operator_bookings(self) -> list[Booking]:
        if not self._operator_allowed():
            return []
        return [
            self._operator_view(b)
            for b in self.bookings
            if any(
                a["operator_id"] == self.identity_id for a in b["assignments"]
            )
        ]

    @rx.var
    def operator_today_booking(self) -> Booking:
        priorities = {
            "working": 0,
            "awaiting_end": 1,
            "arrived": 2,
            "in_transit": 3,
            "problem": 4,
            "assigned": 5,
        }
        eligible = [
            b
            for b in self.operator_bookings
            if b["status"] in priorities
            and (
                b["date"] <= self.today
                or b["status"]
                in {"working", "awaiting_end", "arrived", "in_transit"}
            )
        ]
        return deepcopy(
            min(
                eligible,
                key=lambda b: (
                    priorities[b["status"]],
                    b["date"],
                    b["shift"],
                    b["id"],
                ),
                default=EMPTY_BOOKING,
            )
        )

    @rx.var
    def operator_current(self) -> Booking:
        booking = self._operator_owned(self.operator_booking_id)
        return (
            self._operator_view(booking) if booking else deepcopy(EMPTY_BOOKING)
        )

    @rx.var
    def operator_upcoming(self) -> list[Booking]:
        return sorted(
            [
                b
                for b in self.operator_bookings
                if b["status"] == "assigned"
                and b["id"] != self.operator_today_booking["id"]
            ],
            key=lambda b: (b["date"], b["shift"]),
        )

    @rx.var
    def operator_history(self) -> list[Booking]:
        return sorted(
            [
                b
                for b in self.operator_bookings
                if (not self.operator_date or b["date"] == self.operator_date)
                and (
                    self.operator_filter == "All"
                    or (
                        self.operator_filter == "Active"
                        and b["status"] not in TERMINAL
                    )
                    or (
                        self.operator_filter == "Completed"
                        and b["status"] == "completed"
                    )
                    or (
                        self.operator_filter == "Closed"
                        and b["status"] in {"cancelled", "rejected"}
                    )
                )
            ],
            key=lambda b: (b["date"], b["id"]),
            reverse=True,
        )

    @rx.var
    def operator_duty(self) -> str:
        return (
            "On duty · Assignment active"
            if self.operator_today_booking["id"]
            else "No active duty"
        )

    @rx.var
    def operator_supervisor(self) -> dict[str, str]:
        return next(
            (
                {
                    "name": c["name"],
                    "company": c["company"],
                    "phone": c["phone"],
                }
                for c in self.contractors
                if self.operator_current["id"]
                and c["id"] == self.operator_current["contractor_id"]
            ),
            {"name": "Not available", "company": "", "phone": ""},
        )

    @rx.var
    def operator_units(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for a in self.operator_current["assignments"]:
            vehicle = next(
                (v for v in self.vehicles if v["id"] == a["vehicle_id"]), None
            )
            line = next(
                (
                    l
                    for l in self.operator_current["lines"]
                    if l["equipment_id"] == a["equipment_id"]
                ),
                None,
            )
            result.append(
                {
                    "id": a["vehicle_id"],
                    "vehicle": vehicle["model"]
                    if vehicle
                    else "Vehicle unavailable",
                    "registration": vehicle["registration"] if vehicle else "",
                    "equipment": line["name"] if line else a["equipment_id"],
                    "rate": f"₹{line['rate']:,.2f} / hour"
                    if line
                    else "Rate unavailable",
                }
            )
        return result

    @rx.var
    def operator_audit(self) -> list[Audit]:
        return [
            a
            for a in self.audit
            if self.operator_current["id"]
            and a["booking_id"] == self.operator_current["id"]
        ]

    @rx.var
    def operator_can_report(self) -> bool:
        return bool(self.operator_current["id"]) and self.operator_current[
            "status"
        ] in {
            "assigned",
            "in_transit",
            "arrived",
            "working",
            "awaiting_end",
            "problem",
        }

    @rx.var
    def operator_issues(self) -> list[Dispute]:
        return [
            d
            for d in self.disputes
            if self.operator_current["id"]
            and d["booking_id"] == self.operator_current["id"]
        ]

    @rx.var
    def operator_code_display(self) -> str:
        return (
            self.operator_code.ljust(4, "–")
            if self._operator_allowed()
            else "––––"
        )

    @rx.var
    def operator_duration(self) -> str:
        b = self.operator_current
        if not b["started_at"] or not b["ended_at"]:
            return "Duration available after completion"
        try:
            seconds = max(
                0,
                int(
                    (
                        datetime.fromisoformat(b["ended_at"])
                        - datetime.fromisoformat(b["started_at"])
                    ).total_seconds()
                ),
            )
        except ValueError:
            return "Duration unavailable"
        return (
            f"{seconds // 3600:02d}:{seconds // 60 % 60:02d}:{seconds % 60:02d}"
        )

    @rx.event
    def open_operator_booking(self, booking_id: str, view: str):
        if not self._operator_owned(booking_id) or view not in {
            "start",
            "shift",
            "detail",
        }:
            return
        self.operator_booking_id = booking_id
        self.operator_code = ""
        self.error = ""
        self.feedback = ""
        suffix = "" if view == "detail" else f"/{view}"
        return rx.redirect(f"/operator/bookings/{booking_id}{suffix}")

    @rx.event
    def operator_transit(self):
        b = self._operator_owned(self.operator_booking_id)
        if (
            not b
            or b["status"] != "assigned"
            or b["date"] != self.today
            or b["started_at"]
        ):
            self.error = (
                "Only today's approved, assigned work can begin transit."
            )
            return
        b["status"] = "in_transit"
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"], "in_transit", "Operator started transit; no GPS tracking."
        )
        self.error = ""
        self.feedback = (
            "Transit recorded. Mark arrival when you reach the site."
        )

    @rx.event
    def operator_arrive(self):
        b = self._operator_owned(self.operator_booking_id)
        if not b or b["status"] != "in_transit" or b["started_at"]:
            return
        b["status"] = "arrived"
        self.bookings = deepcopy(self.bookings)
        self._audit(b["id"], "arrived", "Operator recorded site arrival.")
        self.operator_code = ""
        self.error = ""
        return rx.redirect(f"/operator/bookings/{b['id']}/start")

    @rx.event
    def operator_key(self, key: str):
        b = self._operator_owned(self.operator_booking_id)
        if not b or b["status"] not in {"arrived", "awaiting_end"}:
            return
        if key == "clear":
            self.operator_code = ""
        elif key == "backspace":
            self.operator_code = self.operator_code[:-1]
        elif (
            key in "0123456789"
            and len(key) == 1
            and len(self.operator_code) < 4
        ):
            self.operator_code = f"{self.operator_code}{key}"
        self.error = ""

    @rx.event
    def verify_operator_code(self, form_data: dict[str, Any]):
        if self.operator_current["status"] == "arrived":
            yield SharedState.verify_operator_start(form_data)
        else:
            yield SharedState.verify_operator_end(form_data)

    @rx.event
    def verify_operator_start(self, form_data: dict[str, Any]):
        b = self._operator_owned(self.operator_booking_id)
        if not b:
            return
        if b["status"] == "working" and b["started_at"]:
            return rx.redirect(f"/operator/bookings/{b['id']}/shift")
        if b["status"] != "arrived" or b["started_at"]:
            self.error = "This assignment is not ready to start."
            return
        code = str(form_data.get("code", self.operator_code)).strip()
        if not re.fullmatch(r"[0-9]{4}", code) or code != b["start_pin"]:
            self.error = "Incorrect start code. Ask the contractor for the four-digit code."
            return
        if not b["safety_confirmed"]:
            self.error = "Contractor site safety confirmation is required before starting."
            return
        b["status"] = "working"
        b["started_at"] = datetime.now(timezone.utc).isoformat()
        self._sync_booking_resources(b)
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"],
            "working",
            "Operator verified start code and confirmed authorized site readiness.",
        )
        self.operator_code = ""
        self.error = ""
        return rx.redirect(f"/operator/bookings/{b['id']}/shift")

    @rx.event
    def operator_request_end(self):
        b = self._operator_owned(self.operator_booking_id)
        if not b or b["status"] != "working" or not b["started_at"]:
            return
        b["status"] = "awaiting_end"
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"],
            "awaiting_end",
            "Operator requested contractor inspection and end-code handoff.",
        )
        self.operator_code = ""
        self.error = ""
        self.feedback = "Secure the equipment. Ask the contractor to inspect the work and share the end code."

    @rx.event
    def verify_operator_end(self, form_data: dict[str, Any]):
        b = self._operator_owned(self.operator_booking_id)
        if not b or b["status"] == "completed":
            return
        if (
            b["status"] != "awaiting_end"
            or not b["started_at"]
            or b["ended_at"]
        ):
            self.error = "Request the end handoff before completing this shift."
            return
        code = str(form_data.get("code", self.operator_code)).strip()
        if not re.fullmatch(r"[0-9]{4}", code) or code != b["end_pin"]:
            self.error = "Incorrect end code. Obtain the four-digit handoff code from the contractor."
            return
        if not form_data.get("inspection"):
            self.error = "Confirm contractor inspection and that the equipment is secured."
            return
        b["status"] = "completed"
        b["ended_at"] = datetime.now(timezone.utc).isoformat()
        self._sync_booking_resources(b)
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"],
            "completed",
            "Operator verified end code after contractor inspection; resources released where no other booking reserves them.",
        )
        self.operator_code = ""
        self.error = ""
        self.feedback = (
            "Shift completed. Handoff recorded; no payment was sent."
        )

    @rx.event
    def operator_report_issue(self, form_data: dict[str, Any]):
        b = self._operator_owned(self.operator_booking_id)
        if not b or b["status"] not in {
            "assigned",
            "in_transit",
            "arrived",
            "working",
            "awaiting_end",
            "problem",
        }:
            return
        description = str(form_data.get("description", "")).strip()
        category = str(form_data.get("category", ""))
        if not 10 <= len(description) <= 1000 or category not in {
            "Breakdown",
            "Delay",
            "Safety",
            "Other",
        }:
            self.error = "Choose an issue type and enter a description of 10–1000 characters."
            return
        self.disputes.append(
            {
                "id": f"dispute-{uuid4().hex[:10]}",
                "booking_id": b["id"],
                "contractor_id": b["contractor_id"],
                "category": category,
                "description": description,
                "status": "open",
                "resolution": "",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._audit(
            b["id"],
            "issue_reported",
            f"Operator report · {category}: {description}",
        )
        self.operator_panel = ""
        self.error = ""
        self.feedback = "Issue recorded locally for review. Stop unsafe work and contact site supervision; no message was transmitted. Lifecycle and resource reservations are unchanged."

    @rx.event
    def set_operator_panel(self, panel: str):
        if not self._operator_allowed() or panel not in {
            "",
            "support",
            "report",
        }:
            return
        if panel == "report" and not self.operator_can_report:
            return
        self.operator_panel = panel
        self.error = ""

    @rx.event
    def filter_operator_history(self, value: str):
        if self._operator_allowed() and value in {
            "All",
            "Active",
            "Completed",
            "Closed",
        }:
            self.operator_filter = value

    @rx.event
    def set_operator_date(self, value: str):
        if not self._operator_allowed():
            return
        try:
            if value:
                date.fromisoformat(value)
        except ValueError:
            self.error = "Choose a valid date."
            return
        self.operator_date = value
        self.error = ""

    @rx.event
    def clear_operator_filters(self):
        if self._operator_allowed():
            self.operator_filter = "All"
            self.operator_date = ""

    @rx.event
    def save_operator_phone(self, form_data: dict[str, Any]):
        if not self._operator_allowed():
            return
        phone = str(form_data.get("phone", "")).strip()
        if (
            not re.fullmatch(r"[+0-9 ()-]{10,24}", phone)
            or not 10 <= len(re.sub(r"\D", "", phone)) <= 12
        ):
            self.error = "Enter a valid 10–12 digit contact number."
            return
        for o in self.operators:
            if o["id"] == self.identity_id:
                o["phone"] = phone
        self.operators = deepcopy(self.operators)
        self._audit(
            "", "operator_contact_updated", "Operator updated own demo contact."
        )
        self.error = ""
        self.feedback = "Contact saved for this demo session; no verification or message sent."

    def _provider_allowed(self) -> bool:
        return self.role == "Provider" and self.identity_id == "provider-1"

    def _provider_owned(self, booking_id: str) -> Booking | None:
        if not self._provider_allowed():
            return None
        return next(
            (
                b
                for b in self.bookings
                if b["id"] == booking_id
                and b["provider_id"] == self.identity_id
            ),
            None,
        )

    @rx.var
    def provider_identity(self) -> Identity:
        return next(
            (p for p in self.providers if p["id"] == self.identity_id),
            deepcopy(PROVIDERS[0]),
        )

    @rx.var
    def provider_bookings(self) -> list[Booking]:
        return (
            [b for b in self.bookings if b["provider_id"] == self.identity_id]
            if self._provider_allowed()
            else []
        )

    @rx.var
    def provider_requests(self) -> list[Booking]:
        return sorted(
            [
                b
                for b in self.provider_bookings
                if b["status"] == "pending_provider"
            ],
            key=lambda b: (b["date"], b["id"]),
        )

    @rx.var
    def provider_review_queue(self) -> list[Booking]:
        return [
            b
            for b in self.provider_bookings
            if b["status"] in {"pending_approval", "approved"}
        ]

    @rx.var
    def provider_schedule(self) -> list[Booking]:
        return sorted(
            [
                b
                for b in self.provider_bookings
                if b["date"] == self.provider_date
                and b["status"]
                not in {"draft", "pending_provider", "rejected", "cancelled"}
            ],
            key=lambda b: (b["shift"], b["id"]),
        )

    @rx.var
    def provider_today_jobs(self) -> int:
        return sum(
            b["date"] == date.today().isoformat()
            and bool(b["assignments"])
            and b["status"] not in TERMINAL
            for b in self.provider_bookings
        )

    @rx.var
    def provider_current(self) -> Booking:
        return deepcopy(
            self._provider_owned(self.provider_booking_id) or EMPTY_BOOKING
        )

    @rx.var
    def provider_equipment(self) -> list[Equipment]:
        return (
            [e for e in self.catalogue if e["provider_id"] == self.identity_id]
            if self._provider_allowed()
            else []
        )

    @rx.var
    def provider_vehicles(self) -> list[Vehicle]:
        return (
            [v for v in self.vehicles if v["provider_id"] == self.identity_id]
            if self._provider_allowed()
            else []
        )

    @rx.var
    def provider_operators(self) -> list[Operator]:
        return (
            [o for o in self.operators if o["provider_id"] == self.identity_id]
            if self._provider_allowed()
            else []
        )

    @rx.var
    def provider_filtered_vehicles(self) -> list[Vehicle]:
        return [
            v
            for v in self.provider_vehicles
            if self.provider_query.lower()
            in f"{v['registration']} {v['model']} {v['category']}".lower()
            and (
                self.provider_filter == "All"
                or self.provider_filter == v["status"]
            )
        ]

    @rx.var
    def provider_filtered_operators(self) -> list[Operator]:
        return [
            o
            for o in self.provider_operators
            if self.provider_query.lower()
            in f"{o['name']} {o['license']} {o['phone']}".lower()
            and (
                self.provider_filter == "All"
                or self.provider_filter == o["status"]
            )
        ]

    @rx.var
    def provider_counts(self) -> dict[str, int]:
        records = (
            self.provider_vehicles
            if self.provider_tab == "Vehicles"
            else self.provider_operators
        )
        return {
            "total": len(records),
            "available": sum(r["status"] == "available" for r in records),
            "assigned": sum(r["status"] == "assigned" for r in records),
            "unavailable": sum(
                r["status"] in {"maintenance", "unavailable"} for r in records
            ),
        }

    @rx.var
    def provider_vehicle_form(self) -> dict[str, str]:
        vehicle = next(
            (
                v
                for v in self.provider_vehicles
                if v["id"] == self.provider_vehicle_id
            ),
            None,
        )
        if vehicle:
            return {
                k: str(vehicle[k])
                for k in (
                    "equipment_id",
                    "model",
                    "registration",
                    "category",
                    "rate",
                    "overtime",
                    "depot",
                    "status",
                )
            }
        return {
            "equipment_id": "eq-1",
            "model": "",
            "registration": "",
            "category": "Earthmoving",
            "rate": "1850.0",
            "overtime": "1850.0",
            "depot": "",
            "status": "available",
        }

    @rx.var
    def provider_operator_form(self) -> dict[str, str]:
        operator = next(
            (
                o
                for o in self.provider_operators
                if o["id"] == self.provider_operator_id
            ),
            None,
        )
        return {
            k: str(operator[k])
            if operator
            else "available"
            if k == "status"
            else ""
            for k in ("name", "phone", "license", "status")
        }

    def _resource_conflict(
        self, booking: Booking, key: str, resource_id: str
    ) -> bool:
        periods = {
            "Shift A · 08:00–16:00": (8, 16),
            "Shift B · 16:00–00:00": (16, 24),
            "Full day · 08:00–20:00": (8, 20),
        }
        start, end = periods.get(booking["shift"], (0, 24))
        for other in self.bookings:
            if (
                other["id"] == booking["id"]
                or other["date"] != booking["date"]
                or other["status"] in TERMINAL
            ):
                continue
            a, b = periods.get(other["shift"], (0, 24))
            if (
                start < b
                and a < end
                and any(x[key] == resource_id for x in other["assignments"])
            ):
                return True
        return False

    @rx.var
    def provider_allocation_units(self) -> list[dict[str, str]]:
        return [
            {
                "key": f"{line['equipment_id']}_{i}",
                "equipment_id": line["equipment_id"],
                "name": f"{line['name']} · Unit {i + 1} of {line['quantity']}",
            }
            for line in self.provider_current["lines"]
            for i in range(line["quantity"])
        ]

    @rx.var
    def provider_available_vehicles(self) -> list[Vehicle]:
        return [
            v
            for v in self.provider_vehicles
            if v["status"] == "available"
            and not self._resource_conflict(
                self.provider_current, "vehicle_id", v["id"]
            )
        ]

    @rx.var
    def provider_available_operators(self) -> list[Operator]:
        return [
            o
            for o in self.provider_operators
            if o["status"] == "available"
            and not self._resource_conflict(
                self.provider_current, "operator_id", o["id"]
            )
        ]

    @rx.var
    def provider_assignment_details(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for a in self.provider_current["assignments"]:
            v = next(
                (v for v in self.vehicles if v["id"] == a["vehicle_id"]), None
            )
            o = next(
                (o for o in self.operators if o["id"] == a["operator_id"]), None
            )
            result.append(
                {
                    "id": a["vehicle_id"],
                    "vehicle": v["registration"] if v else "Vehicle missing",
                    "operator": o["name"] if o else "Operator missing",
                    "phone": o["phone"] if o else "",
                    "equipment": a["equipment_id"],
                }
            )
        return result

    @rx.var
    def provider_history(self) -> list[Audit]:
        return [
            a
            for a in self.audit
            if a["booking_id"] == self.provider_current["id"]
        ]

    @rx.var
    def provider_completed(self) -> list[Booking]:
        return [b for b in self.provider_bookings if b["status"] == "completed"]

    @rx.var
    def provider_earnings(self) -> float:
        return sum(b["total"] for b in self.provider_completed)

    @rx.var
    def provider_completed_shifts(self) -> int:
        return sum(
            sum(l["quantity"] for l in b["lines"])
            for b in self.provider_completed
        )

    @rx.event
    def open_provider_booking(self, booking_id: str):
        if not self._provider_owned(booking_id):
            return
        self.provider_booking_id = booking_id
        self.provider_panel = ""
        self.error = ""
        self.feedback = ""
        return rx.redirect(f"/provider/assign/{booking_id}")

    @rx.event
    def accept_provider_request(self, form_data: dict[str, Any]):
        booking = self._provider_owned(self.provider_booking_id)
        if not booking or booking["status"] != "pending_provider":
            return
        lines: list[Line] = []
        try:
            for original in booking["requested_lines"]:
                quantity = int(str(form_data.get(original["equipment_id"], "")))
                if quantity < 0 or quantity > original["quantity"]:
                    raise ValueError
                line = deepcopy(original)
                line["quantity"] = quantity
                line["amount"] = quantity * line["rate"] * line["hours"]
                lines.append(line)
            if not any(l["quantity"] > 0 for l in lines):
                raise ValueError
        except (ValueError, TypeError):
            self.error = "Accept whole quantities from 0 to requested, with at least one unit accepted."
            return
        booking["lines"] = lines
        booking["total"] = sum(l["amount"] for l in lines)
        booking["provider_reviewed"] = True
        booking["status"] = "pending_approval"
        self.bookings = deepcopy(self.bookings)
        self._audit(
            booking["id"],
            "pending_approval",
            f"Provider accepted {sum(l['quantity'] for l in lines)} units; original request retained. Accepted total ₹{booking['total']:.2f}; requested ₹{booking['requested_total']:.2f}.",
        )
        self.error = ""
        self.feedback = "Acceptance recorded. Awaiting Officer approval; deployment is blocked."
        return rx.redirect(f"/provider/assign/{booking['id']}")

    @rx.event
    def reject_provider_request(self, form_data: dict[str, Any]):
        booking = self._provider_owned(self.provider_booking_id)
        if not booking or booking["status"] != "pending_provider":
            return
        reason = str(form_data.get("reason", "")).strip()
        if not 5 <= len(reason) <= 500 or not form_data.get("confirm"):
            self.error = (
                "Enter a reason (5–500 characters) and confirm rejection."
            )
            return
        booking["status"] = "rejected"
        booking["reason"] = reason
        self.bookings = deepcopy(self.bookings)
        self._audit(booking["id"], "rejected", reason)
        self.error = ""
        self.feedback = "Request rejected; Contractor can see the reason."

    @rx.event
    def confirm_provider_assignment(self, form_data: dict[str, Any]):
        booking = self._provider_owned(self.provider_booking_id)
        if not booking:
            return
        if booking["status"] != "approved":
            self.error = "Officer approval is required before allocation."
            return
        assignments: list[Assignment] = []
        vehicle_ids: set[str] = set()
        operator_ids: set[str] = set()
        for unit in self.provider_allocation_units:
            vehicle_id = str(form_data.get(f"vehicle_{unit['key']}", ""))
            operator_id = str(form_data.get(f"operator_{unit['key']}", ""))
            vehicle = next(
                (
                    v
                    for v in self.provider_available_vehicles
                    if v["id"] == vehicle_id
                    and v["equipment_id"] == unit["equipment_id"]
                ),
                None,
            )
            operator = next(
                (
                    o
                    for o in self.provider_available_operators
                    if o["id"] == operator_id
                ),
                None,
            )
            if (
                not vehicle
                or not operator
                or vehicle_id in vehicle_ids
                or operator_id in operator_ids
            ):
                self.error = "Choose one compatible available vehicle and operator per unit. Duplicates and overlapping shifts are not allowed."
                return
            vehicle_ids.add(vehicle_id)
            operator_ids.add(operator_id)
            assignments.append(
                {
                    "equipment_id": unit["equipment_id"],
                    "vehicle_id": vehicle_id,
                    "operator_id": operator_id,
                }
            )
        if not assignments:
            self.error = "No accepted units to allocate."
            return
        booking["assignments"] = assignments
        booking["status"] = "assigned"
        for v in self.vehicles:
            if v["id"] in vehicle_ids:
                v["status"] = "assigned"
        for o in self.operators:
            if o["id"] in operator_ids:
                o["status"] = "assigned"
        self.bookings = deepcopy(self.bookings)
        self.vehicles = deepcopy(self.vehicles)
        self.operators = deepcopy(self.operators)
        self._audit(
            booking["id"],
            "assigned",
            "; ".join(
                f"{a['equipment_id']}: {a['vehicle_id']} / {a['operator_id']}"
                for a in assignments
            ),
        )
        self.error = ""
        self.feedback = "All accepted units assigned."
        self.provider_date = booking["date"]
        return rx.redirect("/provider/schedule")

    @rx.event
    def set_provider_date(self, value: str):
        if not self._provider_allowed():
            return
        try:
            date.fromisoformat(value)
        except ValueError:
            self.error = "Select a valid schedule date."
            return
        self.provider_date = value
        self.error = ""

    @rx.event
    def search_provider_fleet(self, value: str):
        if self._provider_allowed():
            self.provider_query = value[:120]

    @rx.event
    def filter_provider_fleet(self, value: str):
        if self._provider_allowed() and value in {
            "All",
            "available",
            "assigned",
            "maintenance",
            "unavailable",
        }:
            self.provider_filter = value

    @rx.event
    def set_provider_tab(self, value: str):
        if self._provider_allowed() and value in {"Vehicles", "Operators"}:
            self.provider_tab = value
            self.provider_panel = ""
            self.error = ""

    @rx.event
    def open_provider_vehicle(self, vehicle_id: str):
        if not self._provider_allowed():
            return
        if vehicle_id and not any(
            v["id"] == vehicle_id for v in self.provider_vehicles
        ):
            return
        self.provider_vehicle_id = vehicle_id
        self.error = ""
        return rx.redirect(
            f"/provider/equipment/{vehicle_id}/edit"
            if vehicle_id
            else "/provider/equipment/new"
        )

    def _resource_reserved(self, key: str, resource_id: str) -> bool:
        return any(
            b["status"] not in TERMINAL
            and any(a[key] == resource_id for a in b["assignments"])
            for b in self.bookings
        )

    @rx.event
    def save_provider_vehicle(self, form_data: dict[str, Any]):
        if not self._provider_allowed():
            return
        old = next(
            (
                v
                for v in self.provider_vehicles
                if v["id"] == self.provider_vehicle_id
            ),
            None,
        )
        if self.provider_vehicle_id and not old:
            self.error = "Vehicle not found in your fleet."
            return
        equipment = next(
            (
                e
                for e in self.provider_equipment
                if e["id"] == str(form_data.get("equipment_id", ""))
            ),
            None,
        )
        model = str(form_data.get("model", "")).strip()
        depot = str(form_data.get("depot", "")).strip()
        registration = re.sub(
            r"[^A-Z0-9]", "", str(form_data.get("registration", "")).upper()
        )
        category = str(form_data.get("category", ""))
        status = str(form_data.get("status", ""))
        try:
            rate = float(form_data.get("rate", ""))
            overtime = float(form_data.get("overtime", ""))
            if not all(math.isfinite(n) and n >= 0 for n in (rate, overtime)):
                raise ValueError
        except (ValueError, TypeError, OverflowError):
            self.error = "Rates must be finite, nonnegative numbers."
            return
        if (
            not equipment
            or category != equipment["category"]
            or not 2 <= len(model) <= 120
            or not 5 <= len(depot) <= 250
            or not re.fullmatch(
                r"[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}", registration
            )
            or status not in {"available", "maintenance", "assigned"}
        ):
            self.error = "Choose matching category/equipment, model, depot and valid registration (e.g. MH02AB4200)."
            return
        if any(
            v["id"] != self.provider_vehicle_id
            and re.sub(r"[^A-Z0-9]", "", v["registration"].upper())
            == registration
            for v in self.vehicles
        ):
            self.error = "Registration already exists."
            return
        reserved = bool(old) and self._resource_reserved(
            "vehicle_id", old["id"]
        )
        if reserved and (
            equipment["id"] != old["equipment_id"]
            or model != old["model"]
            or depot != old["depot"]
            or registration
            != re.sub(r"[^A-Z0-9]", "", old["registration"].upper())
            or status != old["status"]
        ):
            self.error = "Assigned fleet can only have future commercial rates edited; assignment details are locked."
            return
        if status == "assigned" and not reserved:
            self.error = "Only booking allocation can mark a vehicle assigned."
            return
        vehicle: Vehicle = {
            "id": old["id"] if old else f"vehicle-{uuid4().hex[:10]}",
            "provider_id": self.identity_id,
            "equipment_id": equipment["id"],
            "model": model,
            "category": category,
            "registration": old["registration"] if reserved else registration,
            "rate": rate,
            "overtime": overtime,
            "depot": depot,
            "status": status,
        }
        self.vehicles = (
            [vehicle if v["id"] == vehicle["id"] else v for v in self.vehicles]
            if old
            else [*self.vehicles, vehicle]
        )
        for e in self.catalogue:
            if (
                e["id"] == equipment["id"]
                and e["provider_id"] == self.identity_id
            ):
                e["rate"] = rate
        for v in self.vehicles:
            if (
                v["provider_id"] == self.identity_id
                and v["equipment_id"] == equipment["id"]
            ):
                v["rate"] = rate
        self.catalogue = deepcopy(self.catalogue)
        self.vehicles = deepcopy(self.vehicles)
        self._audit(
            "",
            "fleet_saved",
            f"{vehicle['id']} · {registration}; category rate ₹{rate:.2f} for new requests only.",
        )
        self.error = ""
        self.feedback = "Fleet saved. Catalogue base rate updated for new bookings; agreed totals unchanged."
        return rx.redirect("/provider/fleet")

    @rx.event
    def open_provider_operator(self, operator_id: str):
        if not self._provider_allowed() or (
            operator_id
            and not any(o["id"] == operator_id for o in self.provider_operators)
        ):
            return
        self.provider_operator_id = operator_id
        self.provider_panel = "operator"
        self.error = ""

    @rx.event
    def save_provider_operator(self, form_data: dict[str, Any]):
        if not self._provider_allowed():
            return
        old = next(
            (
                o
                for o in self.provider_operators
                if o["id"] == self.provider_operator_id
            ),
            None,
        )
        if self.provider_operator_id and not old:
            return
        name = str(form_data.get("name", "")).strip()
        phone = str(form_data.get("phone", "")).strip()
        license_number = str(form_data.get("license", "")).strip().upper()
        status = str(form_data.get("status", ""))
        digits = re.sub(r"\D", "", phone)
        if (
            not 2 <= len(name) <= 100
            or not 10 <= len(digits) <= 12
            or not re.fullmatch(r"[A-Z0-9-]{6,30}", license_number)
            or status not in {"available", "unavailable", "assigned"}
        ):
            self.error = "Enter name, 10–12 digit contact, licence (6–30 letters/digits/hyphens) and availability."
            return
        if any(
            o["id"] != self.provider_operator_id
            and o["license"] == license_number
            for o in self.operators
        ):
            self.error = "Licence already exists."
            return
        reserved = bool(old) and self._resource_reserved(
            "operator_id", old["id"]
        )
        if reserved and (
            name != old["name"]
            or license_number != old["license"]
            or status != old["status"]
        ):
            self.error = "Assigned operator identity/licence/availability are locked; contact may be updated."
            return
        if status == "assigned" and not reserved:
            self.error = (
                "Only booking allocation can mark an operator assigned."
            )
            return
        operator: Operator = {
            "id": old["id"] if old else f"operator-{uuid4().hex[:10]}",
            "provider_id": self.identity_id,
            "name": name,
            "phone": phone,
            "license": license_number,
            "status": status,
        }
        self.operators = (
            [
                operator if o["id"] == operator["id"] else o
                for o in self.operators
            ]
            if old
            else [*self.operators, operator]
        )
        self._audit("", "operator_saved", operator["id"])
        self.provider_panel = ""
        self.error = ""
        self.feedback = "Operator saved."

    @rx.event
    def open_provider_panel(self, panel: str):
        if self._provider_allowed() and panel in {
            "",
            "bank",
            "compliance",
            "support",
            "earnings",
        }:
            self.provider_panel = panel
            self.error = ""

    @rx.event
    def save_provider_demo(self, form_data: dict[str, Any]):
        if not self._provider_allowed() or self.provider_panel not in {
            "bank",
            "compliance",
            "support",
        }:
            return
        value = str(form_data.get("value", "")).strip()
        if not 5 <= len(value) <= 250:
            self.error = "Enter a demo value (5–250 characters); do not enter real banking details."
            return
        self.provider_demo[self.provider_panel] = value
        self._audit("", "demo_profile_saved", self.provider_panel)
        self.feedback = (
            "Demo detail saved; no verification, message or payout was sent."
        )
        self.error = ""

    def _officer_allowed(self) -> bool:
        return (
            self.role == "Officer"
            and self.identity_id == "officer-1"
            and any(
                i["id"] == "officer-1" and i["role"] == "Officer"
                for i in self.identities
            )
        )

    def _officer_booking(self, booking_id: str) -> Booking | None:
        if not self._officer_allowed():
            return None
        return next((b for b in self.bookings if b["id"] == booking_id), None)

    def _officer_name(self, entity_id: str) -> str:
        return next(
            (
                r["name"]
                for r in [
                    *self.identities,
                    *self.providers,
                    *self.contractors,
                    *self.operators,
                ]
                if r["id"] == entity_id
            ),
            entity_id or "Not recorded",
        )

    def _officer_parties(self, b: Booking) -> str:
        return " · ".join(
            next(
                (
                    f"{p['company']} / {p['name']}"
                    for p in records
                    if p["id"] == b[key]
                ),
                f"Unknown {key}: {b[key]}",
            )
            for records, key in (
                (self.contractors, "contractor_id"),
                (self.providers, "provider_id"),
            )
        )

    def _officer_status_matches(self, b: Booking) -> bool:
        groups = {
            "Awaiting provider": {"pending_provider"},
            "Awaiting approval": {"pending_approval"},
            "Approved": {"approved"},
            "Active": {
                "assigned",
                "in_transit",
                "arrived",
                "working",
                "awaiting_end",
            },
            "Completed": {"completed"},
            "Closed": {"cancelled", "rejected"},
        }
        if self.officer_status == "Issues":
            return b["status"] == "problem" or any(
                d["booking_id"] == b["id"] and d["status"] == "open"
                for d in self.disputes
            )
        return self.officer_status == "All" or b["status"] in groups.get(
            self.officer_status, set()
        )

    @rx.var
    def officer_current(self) -> Booking:
        result = deepcopy(
            self._officer_booking(self.officer_booking_id) or EMPTY_BOOKING
        )
        result["start_pin"] = ""
        result["end_pin"] = ""
        return result

    @rx.var
    def officer_assignment_details(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for a in self.officer_current["assignments"]:
            vehicle = next(
                (v for v in self.vehicles if v["id"] == a["vehicle_id"]), None
            )
            operator = next(
                (o for o in self.operators if o["id"] == a["operator_id"]), None
            )
            line = next(
                (
                    l
                    for l in self.officer_current["lines"]
                    if l["equipment_id"] == a["equipment_id"]
                ),
                None,
            )
            result.append(
                {
                    "equipment": line["name"] if line else a["equipment_id"],
                    "vehicle": f"{vehicle['registration']} · {vehicle['model']} · {vehicle['id']}"
                    if vehicle
                    else f"Missing vehicle: {a['vehicle_id']}",
                    "operator": f"{operator['name']} · {operator['license']} · {operator['id']}"
                    if operator
                    else f"Missing operator: {a['operator_id']}",
                    "phone": operator["phone"] if operator else "",
                }
            )
        return result

    @rx.var
    def officer_parties(self) -> str:
        return (
            self._officer_parties(self.officer_current)
            if self.officer_current["id"]
            else ""
        )

    @rx.var
    def officer_wards(self) -> list[str]:
        return (
            ["All", *sorted({b["ward"] for b in self.bookings if b["ward"]})]
            if self._officer_allowed()
            else ["All"]
        )

    @rx.var
    def officer_scope(self) -> list[Booking]:
        if not self._officer_allowed():
            return []
        return sorted(
            [
                b
                for b in self.bookings
                if (not self.officer_date or b["date"] == self.officer_date)
                and (
                    self.officer_ward == "All" or b["ward"] == self.officer_ward
                )
            ],
            key=lambda b: (b["date"], b["id"]),
        )

    @rx.var
    def officer_requests(self) -> list[Booking]:
        q = self.officer_query.strip().lower()
        return [
            b
            for b in self.officer_scope
            if self._officer_status_matches(b)
            and q
            in f"{b['id']} {b['work_order']} {b['address']} {self._officer_parties(b)}".lower()
        ]

    @rx.var
    def officer_queue(self) -> list[Booking]:
        return [
            b for b in self.officer_scope if b["status"] == "pending_approval"
        ]

    @rx.var
    def officer_deployments(self) -> list[Booking]:
        return [
            b
            for b in self.officer_scope
            if b["status"]
            in {"assigned", "in_transit", "arrived", "working", "awaiting_end"}
        ]

    @rx.var
    def officer_exceptions(self) -> list[Booking]:
        return [
            b
            for b in self.officer_scope
            if b["status"] in {"problem", "pending_provider", "approved"}
            or any(
                d["status"] == "open" and d["booking_id"] == b["id"]
                for d in self.disputes
            )
        ]

    @rx.var
    def officer_metrics(self) -> dict[str, int]:
        ids = {b["id"] for b in self.officer_scope}
        return {
            "pending": len(self.officer_queue),
            "active": len(self.officer_deployments),
            "disputes": sum(
                d["status"] == "open" and d["booking_id"] in ids
                for d in self.disputes
            )
            if self._officer_allowed()
            else 0,
            "completed": sum(
                b["status"] == "completed" for b in self.officer_scope
            ),
        }

    @rx.var
    def officer_report_totals(self) -> dict[str, float]:
        return {
            "completed": sum(
                b["total"]
                for b in self.officer_requests
                if b["status"] == "completed"
            ),
            "planned": sum(
                b["total"]
                for b in self.officer_requests
                if b["provider_reviewed"]
                and b["status"] not in TERMINAL
                and b["status"] != "draft"
            ),
        }

    @rx.var
    def officer_cards(self) -> dict[str, dict[str, str]]:
        if not self._officer_allowed():
            return {}
        return {
            b["id"]: {
                "parties": self._officer_parties(b),
                "units": f"Requested {sum(l['quantity'] for l in b['requested_lines'])} · Accepted {sum(l['quantity'] for l in b['lines']) if b['provider_reviewed'] else 'awaiting provider'}",
                "assignment": "; ".join(
                    f"{next((v['registration'] for v in self.vehicles if v['id'] == a['vehicle_id']), a['vehicle_id'])} / {self._officer_name(a['operator_id'])}"
                    for a in b["assignments"]
                )
                or "No allocation recorded",
            }
            for b in self.bookings
        }

    def _officer_quote_error(self, b: Booking) -> str:
        if (
            not b["provider_reviewed"]
            or not b["requested_lines"]
            or not b["lines"]
        ):
            return "Provider acceptance is required."
        originals = {l["equipment_id"]: l for l in b["requested_lines"]}
        if (
            len(originals) != len(b["requested_lines"])
            or len({l["equipment_id"] for l in b["lines"]}) != len(b["lines"])
            or set(originals) != {l["equipment_id"] for l in b["lines"]}
        ):
            return "Requested and accepted equipment records must match without duplicates."
        for l in b["requested_lines"]:
            if (
                type(l["quantity"]) is not int
                or not 1 <= l["quantity"] <= 10
                or not math.isfinite(l["rate"])
                or l["rate"] < 0
                or l["hours"] != SHIFTS.get(b["shift"], 0)
                or l["hours"] <= 0
                or not math.isfinite(l["amount"])
                or not math.isclose(
                    l["amount"],
                    l["quantity"] * l["rate"] * l["hours"],
                    abs_tol=0.01,
                )
                or not any(
                    e["id"] == l["equipment_id"]
                    and e["provider_id"] == b["provider_id"]
                    for e in self.catalogue
                )
            ):
                return "Invalid requested quantities, equipment ownership or quoted rates/schedule."
        for l in b["lines"]:
            original = originals[l["equipment_id"]]
            if (
                type(l["quantity"]) is not int
                or not 0 <= l["quantity"] <= original["quantity"]
                or l["rate"] != original["rate"]
                or l["hours"] != original["hours"]
                or not math.isfinite(l["amount"])
                or not math.isclose(
                    l["amount"],
                    l["quantity"] * l["rate"] * l["hours"],
                    abs_tol=0.01,
                )
            ):
                return "Accepted units must not exceed requested units; quoted rates and amounts must be intact."
        if not any(l["quantity"] > 0 for l in b["lines"]):
            return "At least one accepted unit is required."
        if (
            not math.isfinite(b["total"])
            or not math.isfinite(b["requested_total"])
            or not math.isclose(
                b["total"], sum(l["amount"] for l in b["lines"]), abs_tol=0.01
            )
            or not math.isclose(
                b["requested_total"],
                sum(l["amount"] for l in b["requested_lines"]),
                abs_tol=0.01,
            )
        ):
            return "The finite quoted totals must equal their line amounts."
        return ""

    def _officer_approval_error(self, b: Booking) -> str:
        if (
            b["status"] != "pending_approval"
            or b["started_at"]
            or b["ended_at"]
            or b["assignments"]
        ):
            return "Only unstarted, unallocated bookings awaiting approval can be approved."
        error = self._officer_quote_error(b)
        if error:
            return error
        try:
            scheduled = date.fromisoformat(b["date"])
        except ValueError:
            return "A valid booking date is required."
        if (
            scheduled < date.today()
            or (scheduled - date.today()).days > 365
            or b["shift"] not in SHIFTS
            or b["hours"] != SHIFTS[b["shift"]]
        ):
            return "Verify a current/future date within 365 days and matching shift hours."
        if (
            not 5 <= len(b["work_order"].strip()) <= 250
            or not 12 <= len(b["address"].strip()) <= 500
            or not 1 <= len(b["ward"].strip()) <= 40
            or not b["safety_confirmed"]
            or not any(c["id"] == b["contractor_id"] for c in self.contractors)
            or not any(p["id"] == b["provider_id"] for p in self.providers)
        ):
            return "Verify site, work order, parties and contractor safety readiness."
        return ""

    @rx.var
    def officer_approval_block(self) -> str:
        b = self._officer_booking(self.officer_booking_id)
        return (
            self._officer_approval_error(b) if b else "Select a valid booking."
        )

    @rx.var
    def officer_partial(self) -> bool:
        b = self.officer_current
        return sum(l["quantity"] for l in b["lines"]) < sum(
            l["quantity"] for l in b["requested_lines"]
        )

    @rx.var
    def officer_can_reject(self) -> bool:
        b = self.officer_current
        return (
            bool(b["id"])
            and b["status"] in {"pending_approval", "approved"}
            and not b["started_at"]
            and not b["ended_at"]
        )

    @rx.var
    def officer_can_reassign(self) -> bool:
        b = self.officer_current
        return (
            bool(b["id"])
            and b["status"] in {"assigned", "in_transit", "problem"}
            and not b["started_at"]
            and not b["ended_at"]
            and not self._officer_quote_error(b)
        )

    @rx.var
    def officer_units(self) -> list[dict[str, str]]:
        if not self.officer_can_reassign:
            return []
        result: list[dict[str, str]] = []
        b = self.officer_current
        for l in b["lines"]:
            pairs = [
                a
                for a in b["assignments"]
                if a["equipment_id"] == l["equipment_id"]
            ]
            for i in range(l["quantity"]):
                pair = (
                    pairs[i]
                    if i < len(pairs)
                    else {"vehicle_id": "", "operator_id": ""}
                )
                result.append(
                    {
                        "key": f"{l['equipment_id']}_{i}",
                        "equipment_id": l["equipment_id"],
                        "name": f"{l['name']} · Unit {i + 1}",
                        "vehicle_id": pair["vehicle_id"],
                        "operator_id": pair["operator_id"],
                    }
                )
        return result

    def _officer_resource_ok(
        self, b: Booking, r: Vehicle | Operator, key: str
    ) -> bool:
        own = any(a[key] == r["id"] for a in b["assignments"])
        return (
            r["provider_id"] == b["provider_id"]
            and (
                r["status"] == "available"
                or (own and r["status"] == "assigned")
            )
            and not self._resource_conflict(b, key, r["id"])
        )

    @rx.var
    def officer_available_vehicles(self) -> list[Vehicle]:
        b = self._officer_booking(self.officer_booking_id)
        return (
            [
                v
                for v in self.vehicles
                if self._officer_resource_ok(b, v, "vehicle_id")
            ]
            if b and self.officer_can_reassign
            else []
        )

    @rx.var
    def officer_available_operators(self) -> list[Operator]:
        b = self._officer_booking(self.officer_booking_id)
        return (
            [
                o
                for o in self.operators
                if self._officer_resource_ok(b, o, "operator_id")
            ]
            if b and self.officer_can_reassign
            else []
        )

    @rx.event
    def open_officer_booking(self, booking_id: str):
        if not self._officer_allowed():
            return
        if not self._officer_booking(booking_id):
            self.error = "Booking not found or Officer access unavailable."
            return
        self.officer_booking_id = booking_id
        self.officer_panel = ""
        self.error = ""
        self.feedback = ""
        return rx.redirect(f"/officer/bookings/{booking_id}")

    @rx.event
    def filter_officer_bookings(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        value = str(form_data.get("date", ""))
        ward = str(form_data.get("ward", "All"))
        try:
            if value:
                date.fromisoformat(value)
        except ValueError:
            self.error = "Choose a valid date."
            return
        if ward not in self.officer_wards:
            self.error = "Choose a ward present in the sample bookings."
            return
        self.officer_date = value
        self.officer_ward = ward
        self.error = ""

    @rx.event
    def search_officer_bookings(self, value: str):
        if self._officer_allowed():
            self.officer_query = value[:120]

    @rx.event
    def set_officer_status(self, value: str):
        if self._officer_allowed() and value in {
            "All",
            "Awaiting provider",
            "Awaiting approval",
            "Approved",
            "Active",
            "Completed",
            "Closed",
            "Issues",
        }:
            self.officer_status = value

    @rx.event
    def clear_officer_filters(self):
        if self._officer_allowed():
            self.officer_query = ""
            self.officer_date = ""
            self.officer_ward = "All"
            self.officer_status = "All"
            self.error = ""

    @rx.event
    def set_officer_panel(self, panel: str):
        if not self._officer_booking(self.officer_booking_id) or panel not in {
            "",
            "approve",
            "reject",
            "reassign",
            "note",
        }:
            return
        if (
            (panel == "approve" and self.officer_approval_block)
            or (panel == "reject" and not self.officer_can_reject)
            or (panel == "reassign" and not self.officer_can_reassign)
        ):
            self.error = (
                "This action is not available in the current booking phase."
            )
            return
        self.officer_panel = panel
        self.error = ""
        self.feedback = ""

    @rx.event
    def approve_officer_booking(self, form_data: dict[str, Any]):
        b = self._officer_booking(self.officer_booking_id)
        if not b:
            return
        self.error = self._officer_approval_error(b)
        if self.error:
            return
        note = str(form_data.get("note", "")).strip()
        if not 5 <= len(note) <= 1000 or not all(
            form_data.get(k)
            for k in (
                "site_verified",
                "work_order_verified",
                "provider_verified",
                "safety_verified",
            )
        ):
            self.error = "Confirm all four verifications and enter a review note (5–1000 characters)."
            return
        if self.officer_partial and not form_data.get("partial_ack"):
            self.error = "Explicitly acknowledge the unfulfilled units before approving partial acceptance."
            return
        b["status"] = "approved"
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"],
            "approved",
            f"Site, work order, provider and safety verified; partial acknowledgement: {bool(form_data.get('partial_ack'))}. {note}",
        )
        self.officer_panel = ""
        self.error = ""
        self.feedback = "Approved. Provider allocation is a separate step; no work has started."

    @rx.event
    def add_officer_note(self, form_data: dict[str, Any]):
        b = self._officer_booking(self.officer_booking_id)
        if not b:
            return
        note = str(form_data.get("note", "")).strip()
        if not 5 <= len(note) <= 1000:
            self.error = "Enter a review note of 5–1000 characters."
            return
        self._audit(b["id"], "officer_review", note)
        self.officer_panel = ""
        self.error = ""
        self.feedback = (
            "Review note appended to audit evidence. Booking phase unchanged."
        )

    @rx.event
    def reject_officer_booking(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        b = self._officer_booking
        if not b or not self.officer_can_reject:
            self.error = "Only unstarted pending-approval or approved bookings can be rejected."
            return
        reason = str(form_data.get("reason", "")).strip()
        if not 5 <= len(reason) <= 500 or not form_data.get("confirm"):
            self.error = (
                "Enter a reason (5–500 characters) and confirm rejection."
            )
            return
        b["status"] = "rejected"
        b["reason"] = reason
        self._sync_booking_resources(b)
        self.bookings = deepcopy(self.bookings)
        self._audit(b["id"], "rejected", reason)
        self.officer_panel = ""
        self.error = ""
        self.feedback = "Booking rejected; only unreserved resources released."

    @rx.event
    def reassign_officer_booking(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        b = self._officer_booking
        if not b or not self.officer_can_reassign:
            self.error = "Reassignment is limited to assigned, in-transit or stopped problem bookings before work starts."
            return
        reason = str(form_data.get("reason", "")).strip()
        if not 5 <= len(reason) <= 500 or not form_data.get("confirm"):
            self.error = "Enter a reason (5–500 characters) and explicitly confirm replacement."
            return
        assignments: list[Assignment] = []
        vehicle_ids: set[str] = set()
        operator_ids: set[str] = set()
        for unit in self.officer_units:
            vid = str(form_data.get(f"vehicle_{unit['key']}", ""))
            oid = str(form_data.get(f"operator_{unit['key']}", ""))
            v = next((v for v in self.vehicles if v["id"] == vid), None)
            o = next((o for o in self.operators if o["id"] == oid), None)
            e = next(
                (e for e in self.catalogue if e["id"] == unit["equipment_id"]),
                None,
            )
            if (
                not v
                or not o
                or not e
                or v["equipment_id"] != unit["equipment_id"]
                or v["category"] != e["category"]
                or not self._officer_resource_ok(b, v, "vehicle_id")
                or not self._officer_resource_ok(b, o, "operator_id")
                or vid in vehicle_ids
                or oid in operator_ids
            ):
                self.error = "Select a compatible available pair from the booked Provider for every unit; duplicates and overlapping reservations are blocked."
                return
            vehicle_ids.add(vid)
            operator_ids.add(oid)
            assignments.append(
                {
                    "equipment_id": unit["equipment_id"],
                    "vehicle_id": vid,
                    "operator_id": oid,
                }
            )
        if not assignments:
            self.error = "No accepted units available to reassign."
            return
        old = deepcopy(b)
        if assignments != b["assignments"] or b["status"] != "assigned":
            b["start_pin"] = str(1000 + randbelow(9000))
            while b["start_pin"] == old["start_pin"]:
                b["start_pin"] = str(1000 + randbelow(9000))
        b["assignments"] = assignments
        b["status"] = "assigned"
        self._sync_booking_resources(old)
        self._sync_booking_resources(b)
        self.bookings = deepcopy(self.bookings)
        self._audit(
            b["id"],
            "officer_reassigned",
            f"{reason}. Old: {old['assignments']}; new: {assignments}. Quotes and end PIN retained.",
        )
        self.officer_panel = ""
        self.error = ""
        self.feedback = "Allocation recorded; status Assigned. Confirm arrival separately. Disputes remain separate; quotes are unchanged."

    @rx.var
    def officer_directory(self) -> list[dict[str, str]]:
        if not self._officer_allowed():
            return []
        records = (
            self.providers
            if self.officer_directory_tab == "Providers"
            else self.contractors
        )
        result: list[dict[str, str]] = []
        for r in records:
            if (
                self.officer_directory_query.lower()
                not in f"{r['id']} {r['name']} {r['company']} {r['phone']} {r['email']}".lower()
            ):
                continue
            key = "provider_id" if r["role"] == "Provider" else "contractor_id"
            books = [b for b in self.bookings if b[key] == r["id"]]
            ids = {b["id"] for b in books}
            fleet = sum(v["provider_id"] == r["id"] for v in self.vehicles)
            people = sum(o["provider_id"] == r["id"] for o in self.operators)
            result.append(
                {
                    **r,
                    "counts": f"{len(books)} bookings · {fleet} vehicles · {people} operators · {sum(d['booking_id'] in ids and d['status'] == 'open' for d in self.disputes)} open disputes",
                }
            )
        return result

    @rx.var
    def officer_entity_bookings(self) -> list[Booking]:
        if not self._officer_allowed() or not self.officer_entity_id:
            return []
        key = (
            "provider_id"
            if self.officer_directory_tab == "Providers"
            else "contractor_id"
        )
        return [b for b in self.bookings if b[key] == self.officer_entity_id]

    @rx.var
    def officer_entity_vehicles(self) -> list[Vehicle]:
        return (
            [
                v
                for v in self.vehicles
                if v["provider_id"] == self.officer_entity_id
            ]
            if self._officer_allowed()
            and self.officer_directory_tab == "Providers"
            else []
        )

    @rx.var
    def officer_entity_operators(self) -> list[Operator]:
        return (
            [
                o
                for o in self.operators
                if o["provider_id"] == self.officer_entity_id
            ]
            if self._officer_allowed()
            and self.officer_directory_tab == "Providers"
            else []
        )

    @rx.event
    def set_officer_directory_tab(self, value: str):
        if self._officer_allowed() and value in {"Providers", "Contractors"}:
            self.officer_directory_tab = value
            self.officer_entity_id = ""
            self.error = ""

    @rx.event
    def search_officer_directory(self, value: str):
        if self._officer_allowed():
            self.officer_directory_query = value[:120]

    @rx.event
    def open_officer_entity(self, entity_id: str):
        if not self._officer_allowed():
            return
        records = (
            self.providers
            if self.officer_directory_tab == "Providers"
            else self.contractors
        )
        if entity_id and not any(r["id"] == entity_id for r in records):
            self.error = "Directory identity not found."
            return
        self.officer_entity_id = entity_id
        self.error = ""

    @rx.event
    def set_officer_more_tab(self, value: str):
        if self._officer_allowed() and value in {
            "Reports",
            "Disputes",
            "Audit",
        }:
            self.officer_more_tab = value
            self.officer_dispute_id = ""
            self.error = ""
            self.feedback = ""

    @rx.var
    def officer_disputes(self) -> list[dict[str, str]]:
        if not self._officer_allowed():
            return []
        ids = {b["id"] for b in self.officer_scope}
        result: list[dict[str, str]] = []
        for d in self.disputes:
            if (
                d["booking_id"] not in ids
                or (
                    self.officer_dispute_filter != "All"
                    and d["status"] != self.officer_dispute_filter.lower()
                )
                or (
                    self.officer_dispute_category != "All"
                    and d["category"] != self.officer_dispute_category
                )
            ):
                continue
            reporter = next(
                (
                    a["actor_id"]
                    for a in self.audit
                    if a["booking_id"] == d["booking_id"]
                    and a["action"] == "issue_reported"
                    and d["description"] in a["note"]
                ),
                d["contractor_id"],
            )
            result.append(
                {
                    **d,
                    "reporter": f"{self._officer_name(reporter)} · {reporter}",
                }
            )
        return sorted(result, key=lambda d: d["created_at"], reverse=True)

    @rx.event
    def filter_officer_disputes(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        status = str(form_data.get("status", "All"))
        category = str(form_data.get("category", "All"))
        if status not in {"All", "Open", "Resolved"} or category not in {
            "All",
            "Breakdown",
            "Delay",
            "Safety",
            "Billing",
            "Other",
        }:
            self.error = "Select a valid dispute status and category."
            return
        self.officer_dispute_filter = status
        self.officer_dispute_category = category
        self.officer_dispute_id = ""
        self.error = ""

    @rx.event
    def open_officer_dispute(self, dispute_id: str):
        if not self._officer_allowed():
            return
        if dispute_id and not any(
            d["id"] == dispute_id and self._officer_booking(d["booking_id"])
            for d in self.disputes
        ):
            self.error = "Dispute or linked booking not found."
            return
        self.officer_dispute_id = dispute_id
        self.error = ""

    @rx.event
    def resolve_officer_dispute(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        d = next(
            (d for d in self.disputes if d["id"] == self.officer_dispute_id),
            None,
        )
        if (
            not d
            or not self._officer_booking(d["booking_id"])
            or d["status"] != "open"
        ):
            self.error = "Choose an open dispute with an existing booking."
            return
        note = str(form_data.get("note", "")).strip()
        if not 10 <= len(note) <= 1000 or not form_data.get("confirm"):
            self.error = "Enter a resolution (10–1000 characters) and confirm."
            return
        d["status"] = "resolved"
        d["resolution"] = note
        self.disputes = deepcopy(self.disputes)
        self._audit(d["booking_id"], "dispute_resolved", f"{d['id']}: {note}")
        self.officer_dispute_id = ""
        self.error = ""
        self.feedback = "Dispute resolved. Booking phase and timestamps unchanged; stopped equipment does not resume. Reassignment/review is separate."

    @rx.var
    def officer_audit_actions(self) -> list[str]:
        return (
            ["All", *sorted({a["action"] for a in self.audit})]
            if self._officer_allowed()
            else ["All"]
        )

    @rx.var
    def officer_audit_records(self) -> list[dict[str, str]]:
        if not self._officer_allowed():
            return []
        q = self.officer_audit_query.lower()
        return [
            {
                **a,
                "actor": f"{self._officer_name(a['actor_id'])} · {a['actor_id']}",
            }
            for a in sorted(
                self.audit, key=lambda a: a["timestamp"], reverse=True
            )
            if (
                not self.officer_audit_date
                or a["timestamp"].startswith(self.officer_audit_date)
            )
            and (
                self.officer_audit_action == "All"
                or a["action"] == self.officer_audit_action
            )
            and q
            in f"{a['booking_id']} {a['action']} {a['note']} {a['actor_id']} {self._officer_name(a['actor_id'])}".lower()
        ]

    @rx.var
    def officer_booking_audit(self) -> list[dict[str, str]]:
        if not self._officer_allowed() or not self.officer_current["id"]:
            return []
        return [
            {
                **a,
                "actor": f"{self._officer_name(a['actor_id'])} · {a['actor_id']}",
            }
            for a in sorted(
                self.audit, key=lambda a: a["timestamp"], reverse=True
            )
            if a["booking_id"] == self.officer_current["id"]
        ]

    @rx.var
    def officer_recent_audit(self) -> list[dict[str, str]]:
        ids = {b["id"] for b in self.officer_scope}
        return [
            {
                **a,
                "actor": f"{self._officer_name(a['actor_id'])} · {a['actor_id']}",
            }
            for a in sorted(
                self.audit, key=lambda a: a["timestamp"], reverse=True
            )
            if a["booking_id"] in ids
        ][:5]

    @rx.var
    def officer_booking_disputes(self) -> list[Dispute]:
        return (
            [
                d
                for d in self.disputes
                if d["booking_id"] == self.officer_current["id"]
            ]
            if self._officer_allowed() and self.officer_current["id"]
            else []
        )

    @rx.event
    def search_officer_audit(self, value: str):
        if self._officer_allowed():
            self.officer_audit_query = value[:120]

    @rx.event
    def filter_officer_audit(self, form_data: dict[str, Any]):
        if not self._officer_allowed():
            return
        value = str(form_data.get("date", ""))
        action = str(form_data.get("action", "All"))
        try:
            if value:
                date.fromisoformat(value)
        except ValueError:
            self.error = "Choose a valid evidence date."
            return
        if action not in self.officer_audit_actions:
            self.error = "Choose an existing audit action."
            return
        self.officer_audit_date = value
        self.officer_audit_action = action
        self.error = ""

    @rx.event
    def export_officer_report(self):
        if not self._officer_allowed():
            return
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(
            [
                "Sample data only — no payouts",
                "Booking",
                "Date",
                "Ward",
                "Status",
                "Contractor",
                "Provider",
                "Requested units",
                "Accepted units",
                "Requested estimate INR",
                "Accepted estimate INR",
                "Site",
                "Work order",
            ]
        )
        for b in self.officer_requests:
            values = [
                "Sample estimate",
                b["id"],
                b["date"],
                b["ward"],
                b["status"],
                self._officer_name(b["contractor_id"]),
                self._officer_name(b["provider_id"]),
                str(sum(l["quantity"] for l in b["requested_lines"])),
                str(sum(l["quantity"] for l in b["lines"]))
                if b["provider_reviewed"]
                else "Awaiting provider",
                f"{b['requested_total']:.2f}",
                f"{b['total']:.2f}" if b["provider_reviewed"] else "",
                b["address"],
                b["work_order"],
            ]
            writer.writerow(
                [
                    f"'{v}"
                    if v.lstrip().startswith(("=", "+", "-", "@"))
                    else v
                    for v in values
                ]
            )
        return rx.download(
            data=stream.getvalue().encode("utf-8-sig"),
            filename="bmc-officer-sample-report.csv",
        )

    @rx.event
    def request_end(self):
        booking = self._owned(self.active_booking_id)
        if not booking or booking["status"] != "working":
            return
        booking["status"] = "awaiting_end"
        self.bookings = deepcopy(self.bookings)
        self._audit(
            booking["id"],
            "awaiting_end",
            "Contractor requested end-code handoff.",
        )
        self.feedback = (
            "Share the end code after inspecting the completed work."
        )
