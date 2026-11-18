import reflex as rx

from build_unified_four_domain_experience.components.contractor import (
    bookings_screen,
    detail_screen,
    home_screen,
    live_screen,
    profile_screen,
)
from build_unified_four_domain_experience.components.contractor_booking import (
    catalogue_screen,
    step_one,
    step_two,
    step_three,
)
from build_unified_four_domain_experience.components.demo_login import login_screen
from build_unified_four_domain_experience.components.provider import (
    requests_screen,
    schedule_screen,
    fleet_screen,
    equipment_screen,
    assignment_screen,
    provider_profile_screen,
)
from build_unified_four_domain_experience.components.operator import (
    operator_today_screen,
    operator_start_screen,
    operator_shift_screen,
    operator_history_screen,
    operator_detail_screen,
    operator_profile_screen,
)
from build_unified_four_domain_experience.components.officer import (
    officer_dashboard_screen,
    officer_requests_screen,
    officer_detail_screen,
    officer_directory_screen,
    officer_more_screen,
)
from build_unified_four_domain_experience.states.shared_state import SharedState


def index() -> rx.Component:
    return login_screen()


app = rx.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(src="/image_fallback.js"),
        rx.el.script(src="/operator_clock.js"),
    ],
)
app.add_page(
    index,
    route="/",
    title="BMC Heavy Logix · Demo Login",
    on_load=SharedState.bootstrap,
)
app.add_page(
    login_screen,
    route="/login",
    title="BMC Heavy Logix · Demo Login",
    on_load=SharedState.bootstrap,
)
app.add_page(
    live_screen,
    route="/contractor/bookings/[booking_id]/live",
    title="BMC Heavy Logix · Live Booking",
    on_load=SharedState.bootstrap,
)
app.add_page(
    detail_screen,
    route="/contractor/bookings/[booking_id]",
    title="BMC Heavy Logix · Booking Details",
    on_load=SharedState.bootstrap,
)
app.add_page(
    home_screen,
    route="/contractor",
    title="BMC Heavy Logix · Contractor",
    on_load=SharedState.bootstrap,
)
app.add_page(
    catalogue_screen,
    route="/contractor/equipment",
    title="BMC Heavy Logix · Equipment",
    on_load=SharedState.bootstrap,
)
app.add_page(
    step_one,
    route="/contractor/booking/step-1",
    title="BMC Heavy Logix · Equipment & Schedule",
    on_load=SharedState.bootstrap,
)
app.add_page(
    step_two,
    route="/contractor/booking/step-2",
    title="BMC Heavy Logix · Site Location",
    on_load=SharedState.bootstrap,
)
app.add_page(
    step_three,
    route="/contractor/booking/step-3",
    title="BMC Heavy Logix · Review Booking",
    on_load=SharedState.bootstrap,
)
app.add_page(
    bookings_screen,
    route="/contractor/bookings",
    title="BMC Heavy Logix · My Bookings",
    on_load=SharedState.bootstrap,
)
app.add_page(
    profile_screen,
    route="/contractor/profile",
    title="BMC Heavy Logix · Contractor Profile",
    on_load=SharedState.bootstrap,
)
app.add_page(
    equipment_screen,
    route="/provider/equipment/[equipment_id]/edit",
    title="BMC Heavy Logix · Edit Equipment",
    on_load=SharedState.bootstrap,
)
app.add_page(
    assignment_screen,
    route="/provider/assign/[booking_id]",
    title="BMC Heavy Logix · Provider Allocation",
    on_load=SharedState.bootstrap,
)
app.add_page(
    equipment_screen,
    route="/provider/equipment/new",
    title="BMC Heavy Logix · Add Equipment",
    on_load=SharedState.bootstrap,
)
app.add_page(
    requests_screen,
    route="/provider",
    title="BMC Heavy Logix · Provider Requests",
    on_load=SharedState.bootstrap,
)
app.add_page(
    requests_screen,
    route="/provider/requests",
    title="BMC Heavy Logix · Provider Requests",
    on_load=SharedState.bootstrap,
)
app.add_page(
    schedule_screen,
    route="/provider/schedule",
    title="BMC Heavy Logix · Daily Schedule",
    on_load=SharedState.bootstrap,
)
app.add_page(
    fleet_screen,
    route="/provider/fleet",
    title="BMC Heavy Logix · Fleet & Operators",
    on_load=SharedState.bootstrap,
)
app.add_page(
    provider_profile_screen,
    route="/provider/profile",
    title="BMC Heavy Logix · Provider Profile & Earnings",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_start_screen,
    route="/operator/bookings/[booking_id]/start",
    title="BMC Heavy Logix · Operator Start Code",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_shift_screen,
    route="/operator/bookings/[booking_id]/shift",
    title="BMC Heavy Logix · Operator Live Shift",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_detail_screen,
    route="/operator/bookings/[booking_id]",
    title="BMC Heavy Logix · Operator Assignment Details",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_start_screen,
    route="/operator/start",
    title="BMC Heavy Logix · Operator Start Code",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_shift_screen,
    route="/operator/shift",
    title="BMC Heavy Logix · Operator Live Shift",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_today_screen,
    route="/operator",
    title="BMC Heavy Logix · Operator Today",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_today_screen,
    route="/operator/today",
    title="BMC Heavy Logix · Operator Today",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_history_screen,
    route="/operator/history",
    title="BMC Heavy Logix · Operator History",
    on_load=SharedState.bootstrap,
)
app.add_page(
    operator_profile_screen,
    route="/operator/profile",
    title="BMC Heavy Logix · Operator Profile",
    on_load=SharedState.bootstrap,
)
app.add_page(
    officer_detail_screen,
    route="/officer/bookings/[booking_id]",
    title="BMC Heavy Logix · Officer Booking Verification",
    on_load=SharedState.bootstrap,
)
app.add_page(
    officer_dashboard_screen,
    route="/officer",
    title="BMC Heavy Logix · Officer Control Room",
    on_load=SharedState.bootstrap,
)
app.add_page(
    officer_requests_screen,
    route="/officer/requests",
    title="BMC Heavy Logix · Officer Requests",
    on_load=SharedState.bootstrap,
)
app.add_page(
    officer_directory_screen,
    route="/officer/directory",
    title="BMC Heavy Logix · Providers & Contractors",
    on_load=SharedState.bootstrap,
)
app.add_page(
    officer_more_screen,
    route="/officer/more",
    title="BMC Heavy Logix · Officer Reports, Disputes & Audit",
    on_load=SharedState.bootstrap,
)
