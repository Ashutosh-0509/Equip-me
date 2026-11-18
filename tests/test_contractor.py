import reflex as rx

import unittest
from copy import deepcopy
from datetime import date, timedelta

from build_unified_four_domain_experience.states.demo_data import CATALOGUE, STATUSES, sample_fixtures
from build_unified_four_domain_experience.states.shared_state import SharedState


class ContractorTests(unittest.TestCase):
    def setUp(self):
        self.state = SharedState(_reflex_internal_init=True)
        self.state.role = "Contractor"
        self.state.identity_id = "contractor-1"
        (
            self.state.bookings,
            self.state.vehicles,
            self.state.operators,
            self.state.audit,
            self.state.disputes,
        ) = deepcopy(sample_fixtures())

    def test_seed_integrity(self):
        bookings, vehicles, operators, audit, disputes = sample_fixtures()
        self.assertEqual({b["status"] for b in bookings}, set(STATUSES))
        self.assertEqual(len(CATALOGUE), 6)
        vehicle_ids = {v["id"] for v in vehicles}
        operator_ids = {o["id"] for o in operators}
        for booking in bookings:
            self.assertEqual(
                booking["total"],
                sum(line["amount"] for line in booking["lines"]),
            )
            for line in booking["lines"]:
                self.assertEqual(
                    line["amount"],
                    line["rate"] * line["quantity"] * booking["hours"],
                )
            for assignment in booking["assignments"]:
                self.assertIn(assignment["vehicle_id"], vehicle_ids)
                self.assertIn(assignment["operator_id"], operator_ids)
        booking_ids = {b["id"] for b in bookings}
        self.assertTrue(all(a["booking_id"] in booking_ids for a in audit))
        self.assertTrue(all(d["booking_id"] in booking_ids for d in disputes))

    def test_role_guards(self):
        self.state.role = "Provider"
        previous = deepcopy(self.state.selected)
        self.state.toggle_equipment("eq-2")
        self.state.change_quantity("eq-1", 1)
        self.state.submit_booking({"safety": "on"})
        self.assertEqual(self.state.selected, previous)
        self.assertEqual(len(self.state.bookings), 12)

    def test_quantity_bounds_and_totals(self):
        self.state.selected = {"eq-1": 1, "eq-2": 2}
        self.state.change_quantity("eq-1", -1)
        self.assertEqual(self.state.selected["eq-1"], 1)
        self.state.selected["eq-1"] = 10
        self.state.change_quantity("eq-1", 1)
        self.assertEqual(self.state.selected["eq-1"], 10)
        self.assertEqual(self.state.draft_total, (1850 * 10 + 1250 * 2) * 8)
        self.state.choose_shift("Full day · 08:00–20:00")
        self.assertEqual(self.state.draft_total, (1850 * 10 + 1250 * 2) * 12)

    def test_schedule_and_coordinates_validation(self):
        self.state.save_schedule(
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "shift": self.state.draft_shift,
            }
        )
        self.assertFalse(self.state.schedule_saved)
        self.assertTrue(self.state.error)
        self.state.save_schedule(
            {"date": date.today().isoformat(), "shift": self.state.draft_shift}
        )
        self.assertTrue(self.state.schedule_saved)
        self.state.save_site(
            {
                "address": "Plot 42-B, Santacruz West, Mumbai",
                "ward": "H/West",
                "latitude": "NaN",
                "longitude": "72.837",
                "work_order": "WO-8842",
            }
        )
        self.assertFalse(self.state.site_saved)

    def test_submit_once_and_safety(self):
        self.state.schedule_saved = True
        self.state.site_saved = True
        self.state.submit_booking({})
        self.assertTrue(self.state.error)
        self.assertEqual(len(self.state.bookings), 12)
        self.state.submit_booking({"safety": "on"})
        self.assertEqual(len(self.state.bookings), 13)
        self.assertEqual(self.state.bookings[-1]["status"], "pending_provider")
        self.assertEqual(self.state.bookings[-1]["total"], 1850 * 8)
        self.state.submit_booking({"safety": "on"})
        self.assertEqual(len(self.state.bookings), 13)

    def test_resume_keeps_booking_id(self):
        self.state.resume_draft("BMC-8840")
        self.assertEqual(self.state.draft_source_id, "BMC-8840")
        self.state.schedule_saved = True
        self.state.site_saved = True
        self.state.submit_booking({"safety": "on"})
        self.assertEqual(len(self.state.bookings), 12)
        self.assertEqual(self.state.bookings[0]["status"], "pending_provider")

    def test_start_and_end_guards(self):
        self.state.active_booking_id = "BMC-8845"
        self.state.confirm_start({})
        self.assertEqual(self.state.current_booking["status"], "arrived")
        self.state.confirm_start({"arrival_confirmed": "on"})
        self.assertEqual(self.state.current_booking["status"], "working")
        self.state.request_end()
        self.assertEqual(self.state.current_booking["status"], "awaiting_end")
        self.state.confirm_end({"end_confirmed": "on"})
        self.assertEqual(self.state.current_booking["status"], "completed")
        count = len(self.state.audit)
        self.state.confirm_end({"end_confirmed": "on"})
        self.assertEqual(len(self.state.audit), count)

    def test_cancellation_and_issue(self):
        self.state.active_booking_id = "BMC-8843"
        self.state.cancel_booking({"reason": "Site not ready", "confirm": "on"})
        self.assertEqual(self.state.current_booking["status"], "cancelled")
        self.state.active_booking_id = "BMC-8846"
        self.state.cancel_booking({"reason": "Site not ready", "confirm": "on"})
        self.assertEqual(self.state.current_booking["status"], "working")
        self.state.report_issue(
            {
                "category": "Safety",
                "description": "Unsafe access near the site entrance.",
            }
        )
        self.assertEqual(self.state.disputes[-1]["booking_id"], "BMC-8846")
        self.assertEqual(self.state.disputes[-1]["status"], "open")
        self.assertEqual(self.state.current_booking["status"], "working")

    def test_logout_keeps_data(self):
        self.state.active_booking_id = "BMC-8843"
        self.state.cancel_booking({"reason": "Site not ready", "confirm": "on"})
        self.state.logout()
        self.assertEqual(self.state.role, "")
        self.assertEqual(self.state.bookings[3]["status"], "cancelled")


if __name__ == "__main__":
    unittest.main()
