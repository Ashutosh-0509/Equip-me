import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.db import db

class TestUnifiedAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        db.reset()

    def test_shared_health_and_overview(self):
        health_res = self.client.get("/api/shared/health")
        self.assertEqual(health_res.status_code, 200)
        self.assertEqual(health_res.json()["status"], "ok")

        overview_res = self.client.get("/api/shared/overview")
        self.assertEqual(overview_res.status_code, 200)
        overview = overview_res.json()
        self.assertIn("total_bookings", overview)
        self.assertIn("active", overview)

    def test_contractor_endpoints(self):
        # 1. Catalogue
        cat_res = self.client.get("/api/contractor/catalogue")
        self.assertEqual(cat_res.status_code, 200)
        items = cat_res.json()
        self.assertGreater(len(items), 0)
        self.assertEqual(items[0]["name"], "Heavy Excavator")

        # 2. Profile
        prof_res = self.client.get("/api/contractor/profile")
        self.assertEqual(prof_res.status_code, 200)
        profile = prof_res.json()
        self.assertIn("company", profile)

        # 3. Bookings list
        bookings_res = self.client.get("/api/contractor/bookings")
        self.assertEqual(bookings_res.status_code, 200)
        bookings = bookings_res.json()
        self.assertIsInstance(bookings, list)
        self.assertGreater(len(bookings), 0)

        # 4. Single booking
        b_id = bookings[0]["id"]
        single_res = self.client.get(f"/api/contractor/bookings/{b_id}")
        self.assertEqual(single_res.status_code, 200)
        self.assertEqual(single_res.json()["id"], b_id)

    def test_provider_endpoints(self):
        # 1. Schedule
        sched_res = self.client.get("/api/provider/schedule")
        self.assertEqual(sched_res.status_code, 200)
        sched = sched_res.json()
        self.assertIsInstance(sched, list)

        # 2. Profile
        prof_res = self.client.get("/api/provider/profile")
        self.assertEqual(prof_res.status_code, 200)
        prof = prof_res.json()
        self.assertEqual(prof["name"], "Mahalaxmi Earthmovers & Fleet")

        # 3. Fleet
        fleet_res = self.client.get("/api/provider/fleet")
        self.assertEqual(fleet_res.status_code, 200)
        self.assertIn("vehicles", fleet_res.json())
        self.assertIn("operators", fleet_res.json())

        # 4. Save Equipment (Create new when id is None)
        save_eq_res = self.client.post("/api/provider/equipment", json={
            "equipment_id": "eq-2",
            "model": "Tata Prima 16T Tipper Extra",
            "category": "Haulage",
            "registration": "MH-02-EQ-9988",
            "rate": 1200.0,
            "overtime": 200.0,
            "depot": "Depot Bandra West, S.V. Road"
        })
        self.assertEqual(save_eq_res.status_code, 200)

        # 5. Save Equipment (Update existing)
        veh_id = save_eq_res.json()["id"]
        update_eq_res = self.client.post("/api/provider/equipment", json={
            "id": veh_id,
            "equipment_id": "eq-2",
            "model": "Tata Prima 16T Tipper Extra (Updated)",
            "category": "Haulage",
            "registration": "MH-02-EQ-9988",
            "rate": 1350.0,
            "overtime": 210.0,
            "depot": "Bandra Municipal Yard"
        })
        self.assertEqual(update_eq_res.status_code, 200)

    def test_operator_endpoints(self):
        # 1. Today assignment
        today_res = self.client.get("/api/operator/today")
        self.assertEqual(today_res.status_code, 200)
        today = today_res.json()
        self.assertIn("operator", today)

        # 2. History
        hist_res = self.client.get("/api/operator/history")
        self.assertEqual(hist_res.status_code, 200)
        hist = hist_res.json()
        self.assertIsInstance(hist, list)

        # 3. Profile
        prof_res = self.client.get("/api/operator/profile")
        self.assertEqual(prof_res.status_code, 200)
        self.assertEqual(prof_res.json()["name"], "Ramesh Solanki")

    def test_officer_endpoints(self):
        # 1. Dashboard
        dash_res = self.client.get("/api/officer/dashboard")
        self.assertEqual(dash_res.status_code, 200)
        pulse = dash_res.json()["pulse"]
        self.assertIn("waiting_approval", pulse)

        # 2. Requests list
        reqs_res = self.client.get("/api/officer/requests")
        self.assertEqual(reqs_res.status_code, 200)
        reqs = reqs_res.json()
        self.assertIsInstance(reqs, list)
        self.assertGreater(len(reqs), 0)

        # 3. Directory
        dir_res = self.client.get("/api/officer/directory")
        self.assertEqual(dir_res.status_code, 200)
        self.assertIn("providers", dir_res.json())

        # 4. Disputes
        disp_res = self.client.get("/api/officer/disputes")
        self.assertEqual(disp_res.status_code, 200)
        disputes = disp_res.json()
        self.assertGreater(len(disputes), 0)
        disp_id = disputes[0]["id"]

        resolve_res = self.client.post(
            f"/api/officer/disputes/{disp_id}/resolve",
            json={"note": "Verified telemetry and settled case."}
        )
        self.assertEqual(resolve_res.status_code, 200)

        # 5. Export CSV
        export_res = self.client.get("/api/officer/export")
        self.assertEqual(export_res.status_code, 200)
        self.assertIn("text/csv", export_res.headers["content-type"])

    def test_full_cross_domain_lifecycle(self):
        # 1. Contractor creates booking
        payload = {
            "equipment_id": "eq-2",
            "quantity": 2,
            "date": "2026-10-25",
            "shift": "Shift A · 08:00–16:00",
            "hours": 8,
            "address": "Plot 42-B, SV Road Ext, Santacruz (W)",
            "ward": "H/West",
            "work_order": "WO-2026-8842 · Storm Water Drain Widening",
            "safety_confirmed": True
        }
        create_res = self.client.post("/api/contractor/bookings", json=payload)
        self.assertEqual(create_res.status_code, 200)
        booking = create_res.json()
        booking_id = booking["id"]
        self.assertEqual(booking["status"], "pending_provider")

        # 2. Provider receives request and accepts
        accept_res = self.client.post(
            f"/api/provider/requests/{booking_id}/accept",
            json={"quantities": {"eq-2": 2}}
        )
        self.assertEqual(accept_res.status_code, 200)
        self.assertEqual(accept_res.json()["status"], "pending_approval")

        # 3. Officer reviews and approves requisition
        officer_res = self.client.post(
            f"/api/officer/bookings/{booking_id}/approve",
            json={"note": "Verified by Municipal Control Room"}
        )
        self.assertEqual(officer_res.status_code, 200)
        self.assertEqual(officer_res.json()["status"], "approved")

        # 4. Provider assigns vehicle & operator
        fleet_res = self.client.get("/api/provider/fleet")
        vehs = fleet_res.json()["vehicles"]
        ops = fleet_res.json()["operators"]

        assign_res = self.client.post(
            f"/api/provider/assign/{booking_id}",
            json={
                "assignments": [
                    {"unit_key": "u-1", "equipment_id": "eq-2", "vehicle_id": vehs[0]["id"], "operator_id": ops[0]["id"]},
                    {"unit_key": "u-2", "equipment_id": "eq-2", "vehicle_id": vehs[1]["id"], "operator_id": ops[1]["id"]},
                ]
            }
        )
        self.assertEqual(assign_res.status_code, 200)
        self.assertEqual(assign_res.json()["status"], "assigned")

        # 5. Operator starts transit and arrives
        transit_res = self.client.post(f"/api/operator/transit/{booking_id}")
        self.assertEqual(transit_res.status_code, 200)
        self.assertEqual(transit_res.json()["status"], "in_transit")

        arrive_res = self.client.post(f"/api/operator/arrive/{booking_id}")
        self.assertEqual(arrive_res.status_code, 200)
        self.assertEqual(arrive_res.json()["status"], "arrived")

        # 6. Operator enters start PIN
        start_pin = arrive_res.json()["start_pin"]
        start_res = self.client.post(
            f"/api/operator/verify_start/{booking_id}",
            json={"code": start_pin, "safety_confirmed": True}
        )
        self.assertEqual(start_res.status_code, 200)
        self.assertEqual(start_res.json()["status"], "working")

        # 7. Operator completes shift with end code
        end_pin = start_res.json()["end_pin"]
        end_res = self.client.post(
            f"/api/operator/verify_end/{booking_id}",
            json={"code": end_pin, "inspection_confirmed": True}
        )
        self.assertEqual(end_res.status_code, 200)
        self.assertEqual(end_res.json()["status"], "completed")

    def test_unified_frontend_serving(self):
        # 1. Root serves index.html
        root_res = self.client.get("/")
        self.assertEqual(root_res.status_code, 200)
        self.assertIn("text/html", root_res.headers.get("content-type", ""))
        self.assertIn("<div id=\"root\">", root_res.text)

        # 2. Client-side SPA routes serve index.html
        contractor_res = self.client.get("/contractor")
        self.assertEqual(contractor_res.status_code, 200)
        self.assertIn("<div id=\"root\">", contractor_res.text)

        officer_res = self.client.get("/officer")
        self.assertEqual(officer_res.status_code, 200)
        self.assertIn("<div id=\"root\">", officer_res.text)

        # 3. Static asset serving
        static_img = self.client.get("/assets/machinery/excavator.jpg")
        self.assertEqual(static_img.status_code, 200)
        self.assertIn("image/jpeg", static_img.headers.get("content-type", ""))

        # 4. Direct API health
        api_health = self.client.get("/api/health")
        self.assertEqual(api_health.status_code, 200)
        self.assertEqual(api_health.json()["status"], "healthy")

if __name__ == "__main__":
    unittest.main()
