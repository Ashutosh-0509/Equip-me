import reflex as rx

import unittest
from copy import deepcopy
from datetime import date

from test_utils import run_event
from build_unified_four_domain_experience.states.demo_data import (
    CATALOGUE,
    IDENTITIES,
    PROVIDERS,
    CONTRACTORS,
    sample_fixtures,
)
from build_unified_four_domain_experience.states.shared_state import SharedState


def fresh_officer() -> SharedState:
    state = SharedState(_reflex_internal_init=True)
    state.role = "Officer"
    state.identity_id = "officer-1"
    (
        state.bookings,
        state.vehicles,
        state.operators,
        state.audit,
        state.disputes,
    ) = deepcopy(sample_fixtures())
    state.catalogue = deepcopy(CATALOGUE)
    state.identities = deepcopy(IDENTITIES)
    state.providers = deepcopy(PROVIDERS)
    state.contractors = deepcopy(CONTRACTORS)
    return state


def booking(state: SharedState, entity_id: str):
    return next(b for b in state.bookings if b["id"] == entity_id)


def verified_form():
    return {
        "site_verified": "on",
        "work_order_verified": "on",
        "provider_verified": "on",
        "safety_verified": "on",
        "note": "Verified site access and original work-order evidence.",
    }


class OfficerNavigationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = fresh_officer()

    async def test_review_navigation_partial_approval_and_provider_integration(
        self,
    ):
        s = self.state
        b = booking(s, "BMC-8842")
        b["requested_lines"][0]["quantity"] = 2
        b["requested_lines"][0]["amount"] *= 2
        b["requested_total"] *= 2
        original = deepcopy(b)
        await run_event(s.open_officer_booking, b["id"])
        self.assertEqual(s.officer_booking_id, b["id"])
        await run_event(s.set_officer_panel, "approve")
        self.assertEqual(s.officer_panel, "approve")
        form = verified_form()
        await run_event(s.approve_officer_booking, form)
        self.assertIn("acknowledge", s.error)
        self.assertEqual(booking(s, b["id"]), original)
        form["partial_ack"] = "on"
        await run_event(s.approve_officer_booking, form)
        current = booking(s, b["id"])
        self.assertEqual(current["status"], "approved")
        for key in (
            "requested_lines",
            "requested_total",
            "lines",
            "total",
            "provider_id",
            "assignments",
            "start_pin",
            "end_pin",
        ):
            self.assertEqual(current[key], original[key])
        self.assertFalse(current["started_at"])
        self.assertEqual(s.audit[-1]["actor_id"], "officer-1")
        n = len(s.audit)
        await run_event(s.approve_officer_booking, form)
        self.assertEqual(len(s.audit), n)
        s.role, s.identity_id = "Provider", "provider-1"
        await run_event(s.open_provider_booking, current["id"])
        self.assertEqual(s.provider_current["status"], "approved")
        unit = s.provider_allocation_units[0]
        vehicle = next(
            v
            for v in s.provider_available_vehicles
            if v["equipment_id"] == unit["equipment_id"]
        )
        operator = s.provider_available_operators[0]
        await run_event(
            s.confirm_provider_assignment,
            {
                f"vehicle_{unit['key']}": vehicle["id"],
                f"operator_{unit['key']}": operator["id"],
            },
        )
        self.assertEqual(booking(s, current["id"])["status"], "assigned")
        self.assertEqual(booking(s, "BMC-8845")["status"], "arrived")

    async def test_reassignment_navigation_atomic_validation_and_resource_release(
        self,
    ):
        s = self.state
        await run_event(s.open_officer_booking, "BMC-8843")
        await run_event(s.set_officer_panel, "reassign")
        self.assertEqual(s.officer_panel, "reassign")
        b = deepcopy(booking(s, "BMC-8843"))
        unit = s.officer_units[0]
        form = {
            "reason": "Replace dispatch allocation before site work.",
            "confirm": "on",
            f"vehicle_{unit['key']}": "vehicle-1",
            f"operator_{unit['key']}": "operator-13",
        }
        before = deepcopy((s.bookings, s.vehicles, s.operators, s.audit))
        await run_event(s.reassign_officer_booking, form)
        self.assertTrue(s.error)
        self.assertEqual((s.bookings, s.vehicles, s.operators, s.audit), before)
        replacement = next(
            v
            for v in s.officer_available_vehicles
            if v["equipment_id"] == unit["equipment_id"]
            and v["id"] != b["assignments"][0]["vehicle_id"]
        )
        form[f"vehicle_{unit['key']}"] = replacement["id"]
        await run_event(s.reassign_officer_booking, form)
        self.assertFalse(s.error)
        current = booking(s, b["id"])
        self.assertEqual(current["status"], "assigned")
        self.assertNotEqual(current["start_pin"], b["start_pin"])
        for key in (
            "lines",
            "requested_lines",
            "total",
            "requested_total",
            "provider_id",
            "end_pin",
            "started_at",
            "ended_at",
        ):
            self.assertEqual(current[key], b[key])
        self.assertEqual(
            next(
                v
                for v in s.vehicles
                if v["id"] == b["assignments"][0]["vehicle_id"]
            )["status"],
            "available",
        )
        self.assertEqual(
            next(v for v in s.vehicles if v["id"] == replacement["id"])[
                "status"
            ],
            "assigned",
        )
        await run_event(s.open_officer_booking, "BMC-8846")
        before = deepcopy(s.bookings)
        await run_event(s.reassign_officer_booking, form)
        self.assertEqual(s.bookings, before)
        self.assertFalse(s.officer_can_reassign)

    async def test_directory_dispute_reports_audit_navigation_and_logout(self):
        s = self.state
        await run_event(s.set_officer_directory_tab, "Providers")
        await run_event(s.open_officer_entity, "provider-2")
        self.assertFalse(s.officer_entity_bookings)
        self.assertFalse(s.officer_entity_vehicles)
        self.assertFalse(s.officer_entity_operators)
        await run_event(s.set_officer_directory_tab, "Contractors")
        await run_event(s.open_officer_entity, "contractor-2")
        self.assertFalse(s.officer_entity_bookings)
        await run_event(s.set_officer_more_tab, "Disputes")
        await run_event(s.open_officer_dispute, "dispute-1")
        before = deepcopy(s.bookings)
        await run_event(
            s.resolve_officer_dispute, {"note": "short", "confirm": "on"}
        )
        self.assertTrue(s.error)
        self.assertEqual(s.disputes[0]["status"], "open")
        await run_event(
            s.resolve_officer_dispute,
            {
                "note": "Repair evidence reviewed; dispatch replacement is separate.",
                "confirm": "on",
            },
        )
        self.assertEqual(s.disputes[0]["status"], "resolved")
        self.assertEqual(s.bookings, before)
        self.assertEqual(booking(s, "BMC-8851")["status"], "problem")
        await run_event(s.set_officer_more_tab, "Reports")
        await run_event(s.set_officer_status, "Completed")
        self.assertEqual(
            s.officer_report_totals["completed"],
            sum(b["total"] for b in s.bookings if b["status"] == "completed"),
        )
        self.assertEqual(s.officer_report_totals["planned"], 0.0)
        await run_event(s.export_officer_report)
        await run_event(s.set_officer_more_tab, "Audit")
        await run_event(s.search_officer_audit, "dispute_resolved")
        self.assertEqual(len(s.officer_audit_records), 1)
        self.assertIn("Anita Joshi", s.officer_audit_records[0]["actor"])
        records = deepcopy(
            (s.bookings, s.vehicles, s.operators, s.audit, s.disputes)
        )
        await run_event(s.logout)
        self.assertFalse(
            s.officer_booking_id
            or s.officer_entity_id
            or s.officer_dispute_id
            or s.officer_panel
        )
        self.assertEqual(
            (s.bookings, s.vehicles, s.operators, s.audit, s.disputes), records
        )

    async def test_identity_missing_ids_and_lifecycle_guards(self):
        s = self.state
        await run_event(s.open_officer_booking, "BMC-8842")
        selected = s.officer_booking_id
        await run_event(s.open_officer_booking, "missing")
        self.assertEqual(s.officer_booking_id, selected)
        for role, identity in (
            ("Provider", "provider-1"),
            ("Officer", "officer-2"),
        ):
            s.role, s.identity_id = role, identity
            before = deepcopy((s.bookings, s.audit, s.disputes))
            await run_event(s.approve_officer_booking, verified_form())
            await run_event(
                s.add_officer_note,
                {"note": "Attempted review without proper identity."},
            )
            await run_event(s.set_officer_status, "Issues")
            self.assertEqual((s.bookings, s.audit, s.disputes), before)
            self.assertFalse(s.officer_requests)
            self.assertFalse(s.officer_directory)
        s.role, s.identity_id = "Officer", "officer-1"
        for entity_id in ("BMC-8845", "BMC-8846", "BMC-8847", "BMC-8848"):
            await run_event(s.open_officer_booking, entity_id)
            before = deepcopy(s.bookings)
            await run_event(
                s.reject_officer_booking,
                {"reason": "Not eligible for rejection.", "confirm": "on"},
            )
            await run_event(
                s.reassign_officer_booking,
                {"reason": "Not eligible for replacement.", "confirm": "on"},
            )
            await run_event(s.approve_officer_booking, verified_form())
            self.assertEqual(s.bookings, before)

    async def test_corrupt_quotes_safety_verifications_and_review_notes(self):
        for corruption in (
            "total",
            "quantity",
            "rate",
            "safety",
            "schedule",
            "provider_reviewed",
        ):
            s = fresh_officer()
            b = booking(s, "BMC-8842")
            if corruption == "total":
                b["total"] = float("inf")
            elif corruption == "quantity":
                b["lines"][0]["quantity"] = 2
            elif corruption == "rate":
                b["lines"][0]["rate"] += 100
            elif corruption == "safety":
                b["safety_confirmed"] = False
            elif corruption == "schedule":
                b["date"] = "not-a-date"
            else:
                b["provider_reviewed"] = False
            await run_event(s.open_officer_booking, b["id"])
            await run_event(s.approve_officer_booking, verified_form())
            self.assertTrue(s.error, corruption)
            self.assertEqual(booking(s, b["id"])["status"], "pending_approval")
        s = self.state
        await run_event(s.open_officer_booking, "BMC-8842")
        n = len(s.audit)
        form = verified_form()
        del form["site_verified"]
        await run_event(s.approve_officer_booking, form)
        self.assertEqual(len(s.audit), n)
        await run_event(s.add_officer_note, {"note": "tiny"})
        self.assertEqual(len(s.audit), n)
        before = deepcopy(s.bookings)
        await run_event(
            s.add_officer_note,
            {"note": "Asked for additional site access documentation."},
        )
        self.assertEqual(s.bookings, before)
        self.assertEqual(s.audit[-1]["action"], "officer_review")

    async def test_overlapping_replacement_and_rejection_shared_reservation(
        self,
    ):
        s = self.state
        await run_event(s.open_officer_booking, "BMC-8843")
        b = booking(s, "BMC-8843")
        unit = s.officer_units[0]
        other = deepcopy(b)
        other["id"] = "BMC-TEST-OVERLAP"
        s.bookings.append(other)
        before = deepcopy((s.bookings, s.vehicles, s.audit))
        await run_event(
            s.reassign_officer_booking,
            {
                "reason": "Keeping original pair conflicts with other shift.",
                "confirm": "on",
                f"vehicle_{unit['key']}": b["assignments"][0]["vehicle_id"],
                f"operator_{unit['key']}": b["assignments"][0]["operator_id"],
            },
        )
        self.assertTrue(s.error)
        self.assertEqual((s.bookings, s.vehicles, s.audit), before)
        approved = booking(s, "BMC-8852")
        approved["assignments"] = deepcopy(b["assignments"])
        await run_event(s.open_officer_booking, approved["id"])
        await run_event(
            s.reject_officer_booking,
            {
                "reason": "Duplicate unstarted reservation rejected.",
                "confirm": "on",
            },
        )
        self.assertEqual(booking(s, approved["id"])["status"], "rejected")
        self.assertEqual(
            next(
                v
                for v in s.vehicles
                if v["id"] == b["assignments"][0]["vehicle_id"]
            )["status"],
            "assigned",
        )

    async def test_duplicate_units_and_document_reset(self):
        s = self.state
        b = booking(s, "BMC-8843")
        for key in ("lines", "requested_lines"):
            b[key][0]["quantity"] = 2
            b[key][0]["amount"] *= 2
        b["total"] *= 2
        b["requested_total"] *= 2
        await run_event(s.open_officer_booking, b["id"])
        form = {
            "reason": "Duplicate pair must never allocate twice.",
            "confirm": "on",
        }
        for unit in s.officer_units:
            form[f"vehicle_{unit['key']}"] = b["assignments"][0]["vehicle_id"]
            form[f"operator_{unit['key']}"] = b["assignments"][0]["operator_id"]
        before = deepcopy((s.bookings, s.vehicles, s.operators, s.audit))
        await run_event(s.reassign_officer_booking, form)
        self.assertTrue(s.error)
        self.assertEqual((s.bookings, s.vehicles, s.operators, s.audit), before)
        s.document_token = "same-document"
        s.officer_query = "persistent query"
        s.officer_more_tab = "Audit"
        await run_event(s.initialize, "same-document")
        self.assertEqual(s.officer_query, "persistent query")
        self.assertEqual(s.officer_more_tab, "Audit")
        self.assertEqual(s.bookings, before[0])
        await run_event(s.initialize, "new-document")
        self.assertFalse(
            s.role
            or s.identity_id
            or s.officer_query
            or s.officer_entity_id
            or s.officer_dispute_id
            or s.officer_panel
        )
        self.assertEqual(s.officer_more_tab, "Reports")
        self.assertEqual(booking(s, "BMC-8843")["lines"][0]["quantity"], 1)

    async def test_filters_keep_pair_and_wrong_provider(self):
        s = self.state
        await run_event(
            s.filter_officer_bookings, {"date": "invalid", "ward": "H/West"}
        )
        self.assertTrue(s.error)
        self.assertEqual(s.officer_date, "")
        await run_event(
            s.filter_officer_bookings,
            {"date": date.today().isoformat(), "ward": "H/West"},
        )
        self.assertTrue(
            all(b["date"] == date.today().isoformat() for b in s.officer_scope)
        )
        await run_event(s.clear_officer_filters)
        await run_event(s.search_officer_bookings, "Desai")
        self.assertEqual(len(s.officer_requests), len(s.bookings))
        await run_event(s.clear_officer_filters)
        await run_event(s.open_officer_booking, "BMC-8843")
        b = deepcopy(booking(s, "BMC-8843"))
        unit = s.officer_units[0]
        form = {
            "reason": "Retain the verified original dispatch pair.",
            "confirm": "on",
            f"vehicle_{unit['key']}": b["assignments"][0]["vehicle_id"],
            f"operator_{unit['key']}": b["assignments"][0]["operator_id"],
        }
        await run_event(s.reassign_officer_booking, form)
        self.assertFalse(s.error)
        self.assertEqual(booking(s, b["id"])["start_pin"], b["start_pin"])
        s.vehicles[0]["provider_id"] = "provider-2"
        form[f"vehicle_{unit['key']}"] = s.vehicles[0]["id"]
        before = deepcopy(s.bookings)
        await run_event(s.reassign_officer_booking, form)
        self.assertTrue(s.error)
        self.assertEqual(s.bookings, before)


if __name__ == "__main__":
    unittest.main()
