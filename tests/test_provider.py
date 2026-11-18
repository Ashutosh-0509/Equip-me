import reflex as rx

import unittest
from copy import deepcopy

from build_unified_four_domain_experience.states.shared_state import SharedState
from test_utils import run_event


class ProviderNavigationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = SharedState(_reflex_internal_init=True)
        self.state.role = "Provider"
        self.state.identity_id = "provider-1"

    async def test_review_accept_navigation_and_remainder(self):
        s = self.state
        booking = next(
            b for b in s.bookings if b["status"] == "pending_provider"
        )
        booking["lines"][0]["quantity"] = 2
        booking["lines"][0]["amount"] *= 2
        booking["requested_lines"] = deepcopy(booking["lines"])
        booking["total"] = booking["lines"][0]["amount"]
        booking["requested_total"] = booking["total"]
        await run_event(s.open_provider_booking, booking["id"])
        self.assertEqual(s.provider_booking_id, booking["id"])
        await run_event(
            s.accept_provider_request,
            {booking["lines"][0]["equipment_id"]: "1"},
        )
        current = s.provider_current
        self.assertEqual(current["status"], "pending_approval")
        self.assertEqual(current["requested_lines"][0]["quantity"], 2)
        self.assertEqual(current["lines"][0]["quantity"], 1)
        self.assertEqual(current["requested_total"], 2 * current["total"])
        await run_event(s.confirm_provider_assignment, {})
        self.assertEqual(s.provider_current["status"], "pending_approval")
        self.assertIn("approval", s.error.lower())

    async def test_vehicle_editor_navigation_and_rate_snapshot(self):
        s = self.state
        vehicle = s.provider_vehicles[0]
        original_totals = [b["total"] for b in s.bookings]
        await run_event(s.open_provider_vehicle, vehicle["id"])
        self.assertEqual(s.provider_vehicle_id, vehicle["id"])
        form = dict(s.provider_vehicle_form)
        form["rate"] = "1999.50"
        await run_event(s.save_provider_vehicle, form)
        self.assertFalse(s.error)
        self.assertEqual(
            next(e for e in s.catalogue if e["id"] == vehicle["equipment_id"])[
                "rate"
            ],
            1999.50,
        )
        self.assertEqual([b["total"] for b in s.bookings], original_totals)
        s.role = "Contractor"
        before = deepcopy(s.vehicles)
        await run_event(s.save_provider_vehicle, form)
        self.assertEqual(s.vehicles, before)

    async def test_approved_assignment_navigation_and_fixture_retention(self):
        s = self.state
        arrived = deepcopy(next(b for b in s.bookings if b["id"] == "BMC-8845"))
        approved = next(b for b in s.bookings if b["status"] == "approved")
        await run_event(s.open_provider_booking, approved["id"])
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
        self.assertFalse(s.error)
        self.assertEqual(s.provider_current["status"], "assigned")
        self.assertEqual(s.provider_date, approved["date"])
        self.assertEqual(
            next(b for b in s.bookings if b["id"] == "BMC-8845"), arrived
        )
        self.assertEqual(arrived["assignments"][0]["operator_id"], "operator-1")
        await run_event(s.logout)
        self.assertEqual(s.role, "")
        self.assertEqual(
            next(b for b in s.bookings if b["id"] == approved["id"])["status"],
            "assigned",
        )
