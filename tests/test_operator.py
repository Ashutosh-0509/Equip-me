import reflex as rx

import unittest
from copy import deepcopy

from build_unified_four_domain_experience.states.demo_data import sample_fixtures
from build_unified_four_domain_experience.states.shared_state import SharedState
from test_utils import run_event


class OperatorNavigationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = SharedState(_reflex_internal_init=True)
        self.state.role = "Operator"
        self.state.identity_id = "operator-1"
        (
            self.state.bookings,
            self.state.vehicles,
            self.state.operators,
            self.state.audit,
            self.state.disputes,
        ) = deepcopy(sample_fixtures())

    async def test_today_start_shift_end_history_navigation(self):
        s = self.state
        self.assertEqual(s.operator_today_booking["id"], "BMC-8845")
        await run_event(s.open_operator_booking, "BMC-8845", "start")
        booking = next(b for b in s.bookings if b["id"] == "BMC-8845")
        self.assertEqual(s.operator_current["start_pin"], "")
        before = deepcopy(s.bookings)
        await run_event(s.verify_operator_start, {"code": "0000"})
        self.assertEqual(s.bookings, before)
        self.assertTrue(s.error)
        booking["safety_confirmed"] = False
        await run_event(s.verify_operator_start, {"code": booking["start_pin"]})
        self.assertEqual(s.operator_current["status"], "arrived")
        booking["safety_confirmed"] = True
        for digit in booking["start_pin"]:
            await run_event(s.operator_key, digit)
        await run_event(s.verify_operator_start, {})
        self.assertEqual(s.operator_current["status"], "working")
        started = s.operator_current["started_at"]
        self.assertTrue(started)
        await run_event(s.verify_operator_start, {})
        self.assertEqual(s.operator_current["started_at"], started)
        await run_event(s.operator_request_end)
        self.assertEqual(s.operator_current["status"], "awaiting_end")
        await run_event(
            s.verify_operator_end, {"code": "0000", "inspection": "on"}
        )
        self.assertEqual(s.operator_current["status"], "awaiting_end")
        end_code = next(b for b in s.bookings if b["id"] == "BMC-8845")[
            "end_pin"
        ]
        await run_event(s.verify_operator_end, {"code": end_code})
        self.assertEqual(s.operator_current["status"], "awaiting_end")
        await run_event(
            s.verify_operator_end, {"code": end_code, "inspection": "on"}
        )
        self.assertEqual(s.operator_current["status"], "completed")
        self.assertTrue(s.operator_current["ended_at"])
        count = len(s.audit)
        await run_event(
            s.verify_operator_end, {"code": end_code, "inspection": "on"}
        )
        self.assertEqual(len(s.audit), count)
        self.assertEqual(s.operator_record["status"], "available")
        await run_event(s.filter_operator_history, "Completed")
        self.assertEqual([b["id"] for b in s.operator_history], ["BMC-8845"])
        await run_event(s.open_operator_booking, "BMC-8845", "detail")
        self.assertNotEqual(
            s.operator_duration, "Duration available after completion"
        )
        s.role = "Provider"
        s.identity_id = "provider-1"
        self.assertTrue(
            any(b["id"] == "BMC-8845" for b in s.provider_completed)
        )
        self.assertEqual(
            s.provider_earnings, sum(b["total"] for b in s.provider_completed)
        )
        s.role = "Contractor"
        s.identity_id = "contractor-1"
        s.active_booking_id = "BMC-8845"
        await run_event(s.confirm_start, {"arrival_confirmed": "on"})
        await run_event(s.confirm_end, {"end_confirmed": "on"})
        self.assertEqual(len(s.audit), count)

    async def test_roster_transit_guard_and_multiunit_privacy(self):
        s = self.state
        owned = next(b for b in s.bookings if b["id"] == "BMC-8845")
        owned["status"] = "assigned"
        owned["assignments"].append(
            {
                "equipment_id": "eq-1",
                "vehicle_id": "vehicle-4",
                "operator_id": "operator-4",
            }
        )
        await run_event(s.open_operator_booking, owned["id"], "shift")
        self.assertEqual(len(s.operator_current["assignments"]), 1)
        await run_event(s.operator_transit)
        self.assertEqual(s.operator_current["status"], "in_transit")
        await run_event(s.operator_arrive)
        self.assertEqual(s.operator_current["status"], "arrived")
        previous_id = s.operator_booking_id
        await run_event(s.open_operator_booking, "BMC-8846", "shift")
        self.assertEqual(s.operator_booking_id, previous_id)
        s.operator_booking_id = "BMC-8846"
        before = deepcopy(s.bookings)
        await run_event(s.operator_request_end)
        await run_event(s.verify_operator_start, {"code": "8426"})
        self.assertEqual(s.bookings, before)
        self.assertEqual(s.operator_current["id"], "")
        s.operator_booking_id = "BMC-8845"
        owned["status"] = "pending_approval"
        before = deepcopy(s.bookings)
        await run_event(s.operator_transit)
        self.assertEqual(s.bookings, before)
        s.role = "Provider"
        before = deepcopy(s.operators)
        await run_event(s.save_operator_phone, {"phone": "9876543210"})
        self.assertEqual(s.operators, before)
        self.assertEqual(s.operator_bookings, [])

    async def test_issue_profile_logout_and_code_controls(self):
        s = self.state
        await run_event(s.open_operator_booking, "BMC-8845", "start")
        for key in ["1", "2", "3", "4", "5"]:
            await run_event(s.operator_key, key)
        self.assertEqual(s.operator_code, "1234")
        await run_event(s.operator_key, "backspace")
        self.assertEqual(s.operator_code, "123")
        await run_event(s.operator_key, "clear")
        self.assertEqual(s.operator_code, "")
        before = deepcopy(s.bookings)
        issues = len(s.disputes)
        await run_event(
            s.operator_report_issue,
            {"category": "Safety", "description": "short"},
        )
        self.assertEqual(len(s.disputes), issues)
        await run_event(
            s.operator_report_issue,
            {
                "category": "Safety",
                "description": "Unsafe pedestrian access at the entrance.",
            },
        )
        self.assertEqual(len(s.disputes), issues + 1)
        self.assertEqual(s.bookings, before)
        self.assertEqual(s.disputes[-1]["contractor_id"], "contractor-1")
        await run_event(s.save_operator_phone, {"phone": "bad number"})
        self.assertTrue(s.error)
        await run_event(s.save_operator_phone, {"phone": "+91 98765 43210"})
        self.assertEqual(s.operator_record["phone"], "+91 98765 43210")
        await run_event(s.set_operator_panel, "support")
        self.assertEqual(s.operator_panel, "support")
        before = deepcopy(s.bookings)
        await run_event(s.logout)
        self.assertEqual(s.bookings, before)
        self.assertEqual(s.operator_code, "")
        self.assertEqual(s.operator_panel, "")
        self.assertEqual(s.operator_bookings, [])


if __name__ == "__main__":
    unittest.main()
