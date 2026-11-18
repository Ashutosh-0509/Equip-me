import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import (
    CARD,
    INPUT,
    PRIMARY,
    SECONDARY,
    badge,
    field,
)
from build_unified_four_domain_experience.components.provider_shell import provider_shell
from build_unified_four_domain_experience.components.acceptance_summary import acceptance_summary
from build_unified_four_domain_experience.components.contractor_booking import review_line
from build_unified_four_domain_experience.components.contractor import audit_row
from build_unified_four_domain_experience.states.demo_data import Booking, Line, Vehicle, Operator
from build_unified_four_domain_experience.states.shared_state import SharedState


def empty(message: str) -> rx.Component:
    return rx.el.p(
        message,
        class_name="rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-6 text-[#6B6B6B]",
    )


def metric(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm text-[#6B6B6B]"),
        rx.el.p(value, class_name="mt-2 text-2xl font-bold text-[#1C1C1E]"),
        class_name=CARD,
    )


def provider_booking_card(booking: Booking) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            badge(booking["status"]),
            rx.el.p(
                booking["id"], class_name="text-sm font-semibold text-[#6B6B6B]"
            ),
            class_name="flex flex-wrap justify-between gap-2",
        ),
        rx.foreach(booking["lines"], review_line),
        rx.el.p(
            f"{booking['date']} · {booking['shift']}",
            class_name="mt-3 font-semibold text-[#1C1C1E]",
        ),
        rx.el.p(
            f"Ward {booking['ward']} · {booking['address']}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.p(
            f"₹{booking['total']:,.2f}",
            class_name="my-3 text-xl font-bold text-[#1C1C1E]",
        ),
        rx.cond(
            booking["assignments"].length() > 0,
            rx.el.div(
                rx.foreach(
                    booking["assignments"],
                    lambda a: rx.el.div(
                        rx.foreach(
                            SharedState.provider_vehicles,
                            lambda v: rx.cond(
                                v["id"] == a["vehicle_id"],
                                rx.el.p(
                                    v["registration"],
                                    class_name="font-semibold text-[#1C1C1E]",
                                ),
                                rx.fragment(),
                            ),
                        ),
                        rx.foreach(
                            SharedState.provider_operators,
                            lambda o: rx.cond(
                                o["id"] == a["operator_id"],
                                rx.el.p(
                                    f"Operator: {o['name']}",
                                    class_name="text-[#6B6B6B]",
                                ),
                                rx.fragment(),
                            ),
                        ),
                        class_name="mb-3 rounded-xl bg-[#F5F5F5] p-3",
                    ),
                ),
            ),
            rx.el.p("Allocation pending", class_name="mb-3 text-[#6B6B6B]"),
        ),
        rx.el.button(
            rx.cond(
                booking["status"] == "pending_provider",
                "Review / Accept / Reject",
                "View allocation details",
            ),
            on_click=lambda: SharedState.open_provider_booking(booking["id"]),
            class_name=SECONDARY,
        ),
        class_name=CARD,
        key=booking["id"],
    )


def requests_screen() -> rx.Component:
    return provider_shell(
        rx.el.div(
            rx.el.p(
                "Demo dispatch console · Requests share the Contractor's session records. No expiry timer or GPS tracking is simulated.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.div(
                metric(
                    "New requests",
                    SharedState.provider_requests.length().to_string(),
                ),
                metric(
                    "Today's jobs", SharedState.provider_today_jobs.to_string()
                ),
                class_name="my-4 grid grid-cols-2 gap-4",
            ),
            rx.el.h2(
                "Incoming Requests",
                class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
            ),
            rx.cond(
                SharedState.provider_requests.length() > 0,
                rx.el.div(
                    rx.foreach(
                        SharedState.provider_requests, provider_booking_card
                    ),
                    class_name="grid gap-4 md:grid-cols-2",
                ),
                empty(
                    "No incoming requests. New Contractor bookings will appear here."
                ),
            ),
            rx.el.h2(
                "Approval & allocation queue",
                class_name="my-4 text-lg font-bold text-[#1C1C1E]",
            ),
            rx.cond(
                SharedState.provider_review_queue.length() > 0,
                rx.el.div(
                    rx.foreach(
                        SharedState.provider_review_queue, provider_booking_card
                    ),
                    class_name="grid gap-4 md:grid-cols-2",
                ),
                empty("No requests awaiting approval or allocation."),
            ),
            class_name="w-full",
        ),
        "Incoming Requests",
    )


def acceptance_input(line: Line) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            f"{line['name']} · requested {line['quantity']}",
            html_for=line["equipment_id"],
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.input(
            id=line["equipment_id"],
            name=line["equipment_id"],
            type="number",
            min=0,
            max=line["quantity"],
            step=1,
            required=True,
            default_value=line["quantity"].to_string(),
            key=line["equipment_id"],
            class_name=INPUT,
        ),
        rx.el.p(
            f"₹{line['rate']:,.2f}/unit/hr × {line['hours']} hr. Enter 0 for units you cannot supply.",
            class_name="mt-2 text-sm text-[#6B6B6B]",
        ),
    )


def request_controls() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.h2(
                "Accept full or partial request",
                class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
            ),
            rx.el.form(
                rx.foreach(
                    SharedState.provider_current["requested_lines"],
                    acceptance_input,
                ),
                rx.el.p(
                    "At least one unit must be accepted. The original request and any remainder stay visible. Acceptance sends the booking to Officer review, not deployment.",
                    class_name="text-[#6B6B6B]",
                ),
                id="provider-accept",
                on_submit=SharedState.accept_provider_request,
                class_name="flex flex-col gap-4",
            ),
            class_name=CARD,
        ),
        rx.el.details(
            rx.el.summary(
                "Reject request",
                class_name="min-h-12 cursor-pointer py-3 font-semibold text-red-700 focus-visible:outline-2 focus-visible:outline-[#FFB400]",
            ),
            rx.el.form(
                field("Reason for rejection", "reason", ""),
                rx.el.label(
                    rx.el.input(
                        id="reject-confirm",
                        name="confirm",
                        type="checkbox",
                        required=True,
                        class_name="h-6 w-6 accent-[#FFB400]",
                    ),
                    "I confirm rejection; the Contractor will see this reason.",
                    html_for="reject-confirm",
                    class_name="flex min-h-12 items-center gap-3 text-[#1C1C1E]",
                ),
                rx.el.button(
                    "Confirm rejection",
                    type="submit",
                    class_name="min-h-12 rounded-xl bg-red-700 px-4 text-white font-semibold hover:bg-red-800 focus-visible:outline-2 focus-visible:outline-red-700",
                ),
                on_submit=SharedState.reject_provider_request,
                class_name="flex flex-col gap-4",
            ),
            class_name=CARD,
        ),
        class_name="flex flex-col gap-4",
    )


def resource_select(unit: dict[str, str], kind: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.cond(
                kind == "vehicle",
                "Select compatible vehicle",
                "Select operator",
            ),
            html_for=f"{kind}_{unit['key']}",
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("Choose available resource", value=""),
                rx.cond(
                    kind == "vehicle",
                    rx.foreach(
                        SharedState.provider_available_vehicles,
                        lambda v: rx.cond(
                            v["equipment_id"] == unit["equipment_id"],
                            rx.el.option(
                                f"{v['registration']} · {v['model']} · {v['depot']}",
                                value=v["id"],
                            ),
                            rx.fragment(),
                        ),
                    ),
                    rx.foreach(
                        SharedState.provider_available_operators,
                        lambda o: rx.el.option(
                            f"{o['name']} · {o['license']}", value=o["id"]
                        ),
                    ),
                ),
                id=f"{kind}_{unit['key']}",
                name=f"{kind}_{unit['key']}",
                required=True,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
    )


def allocation_unit(unit: dict[str, str]) -> rx.Component:
    return rx.el.section(
        rx.el.h3(unit["name"], class_name="text-lg font-bold text-[#1C1C1E]"),
        resource_select(unit, "vehicle"),
        resource_select(unit, "operator"),
        class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-white p-4",
        key=unit["key"],
    )


def assignment_content() -> rx.Component:
    return rx.el.div(
        rx.el.a("Back to requests", href="/provider", class_name=SECONDARY),
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    SharedState.provider_current["id"],
                    class_name="text-xl font-bold text-[#1C1C1E]",
                ),
                badge(SharedState.provider_current["status"]),
                class_name="flex flex-wrap justify-between gap-2",
            ),
            rx.foreach(SharedState.provider_current["lines"], review_line),
            rx.el.p(
                f"{SharedState.provider_current['date']} · {SharedState.provider_current['shift']}",
                class_name="mt-3 font-semibold text-[#1C1C1E]",
            ),
            rx.el.p(
                SharedState.provider_current["address"],
                class_name="mt-2 text-[#6B6B6B]",
            ),
            rx.el.p(
                f"Ward {SharedState.provider_current['ward']} · {SharedState.provider_current['work_order']}",
                class_name="mt-2 text-[#6B6B6B]",
            ),
            rx.el.p(
                f"Accepted / current total ₹{SharedState.provider_current['total']:,.2f}",
                class_name="mt-3 font-bold text-[#1C1C1E]",
            ),
            class_name=CARD,
        ),
        acceptance_summary(SharedState.provider_current),
        rx.match(
            SharedState.provider_current["status"],
            ("pending_provider", request_controls()),
            (
                "pending_approval",
                empty(
                    "Awaiting Officer approval. You can review the acceptance here, but cannot allocate or deploy equipment."
                ),
            ),
            (
                "approved",
                rx.el.div(
                    rx.el.h2(
                        "Required Allocations",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        "One unique pair per accepted unit. Only compatible, available resources without overlapping day/shift bookings are listed. Duplicate selections are rejected on confirmation.",
                        class_name="text-[#6B6B6B]",
                    ),
                    rx.el.form(
                        rx.foreach(
                            SharedState.provider_allocation_units,
                            allocation_unit,
                        ),
                        id="provider-allocate",
                        on_submit=SharedState.confirm_provider_assignment,
                        class_name="flex flex-col gap-4",
                    ),
                    class_name="flex flex-col gap-4",
                ),
            ),
            rx.el.section(
                rx.el.h2(
                    "Recorded vehicle & operator pairs",
                    class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
                ),
                rx.cond(
                    SharedState.provider_assignment_details.length() > 0,
                    rx.foreach(
                        SharedState.provider_assignment_details,
                        lambda a: rx.el.div(
                            rx.el.p(
                                f"{a['equipment']} · {a['vehicle']}",
                                class_name="font-semibold text-[#1C1C1E]",
                            ),
                            rx.el.p(
                                f"{a['operator']} · {a['phone']}",
                                class_name="mt-2 text-[#6B6B6B]",
                            ),
                            class_name="border-b border-[#E5E5EA] py-3 last:border-0",
                            key=a["id"],
                        ),
                    ),
                    empty("No allocation recorded for this booking."),
                ),
                rx.el.p(
                    SharedState.provider_current["reason"],
                    class_name="mt-3 text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
        ),
        rx.el.details(
            rx.el.summary(
                "Booking audit · Sample evidence",
                class_name="min-h-12 cursor-pointer py-3 font-semibold text-[#1C1C1E]",
            ),
            rx.el.ol(rx.foreach(SharedState.provider_history, audit_row)),
            class_name=CARD,
        ),
        class_name="flex w-full flex-col gap-4",
    )


def assignment_screen() -> rx.Component:
    return provider_shell(
        rx.cond(
            SharedState.provider_current["id"] != "",
            assignment_content(),
            empty("Booking not found or not owned by this Provider."),
        ),
        "Assign Vehicle & Operator",
        footer=rx.match(
            SharedState.provider_current["status"],
            (
                "pending_provider",
                rx.el.div(
                    rx.el.button(
                        "Accept Request · Send for Approval",
                        type="submit",
                        form="provider-accept",
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            (
                "approved",
                rx.el.div(
                    rx.el.button(
                        "Confirm Assignment",
                        type="submit",
                        form="provider-allocate",
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            rx.fragment(),
        ),
    )


def schedule_screen() -> rx.Component:
    return provider_shell(
        rx.el.div(
            rx.el.label(
                "Schedule date",
                html_for="provider-date",
                class_name="mb-2 block font-semibold text-[#1C1C1E]",
            ),
            rx.el.input(
                id="provider-date",
                type="date",
                default_value=SharedState.provider_date,
                on_change=SharedState.set_provider_date.debounce(500),
                class_name=INPUT,
            ),
            rx.el.p(
                f"{SharedState.provider_schedule.length()} bookings · {SharedState.provider_date}",
                class_name="my-4 font-semibold text-[#1C1C1E]",
            ),
            rx.cond(
                SharedState.provider_schedule.length() > 0,
                rx.el.div(
                    rx.foreach(
                        SharedState.provider_schedule, provider_booking_card
                    ),
                    class_name="grid gap-4 md:grid-cols-2",
                ),
                empty("No deployments or reviewed bookings for this date."),
            ),
        ),
        "Daily Schedule",
        "Schedule",
    )


def fleet_chip(value: str) -> rx.Component:
    return rx.el.button(
        value,
        type="button",
        on_click=lambda: SharedState.filter_provider_fleet(value),
        aria_pressed=SharedState.provider_filter == value,
        class_name=rx.cond(
            SharedState.provider_filter == value,
            "min-h-12 shrink-0 rounded-full border-2 border-[#FFB400] bg-white px-4 font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "min-h-12 shrink-0 rounded-full border-2 border-[#E5E5EA] bg-[#F5F5F5] px-4 font-medium text-[#6B6B6B] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def vehicle_card(v: Vehicle) -> rx.Component:
    return rx.el.article(
        rx.el.h3(v["model"], class_name="text-lg font-bold text-[#1C1C1E]"),
        rx.el.p(
            f"{v['registration']} · {v['category']}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.p(
            f"Status: {v['status']} · {v['depot']}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.p(
            f"₹{v['rate']:,.2f}/hr · Overtime ₹{v['overtime']:,.2f}/hr",
            class_name="my-3 font-semibold text-[#1C1C1E]",
        ),
        rx.el.button(
            "Edit equipment / rates",
            on_click=lambda: SharedState.open_provider_vehicle(v["id"]),
            class_name=SECONDARY,
        ),
        class_name=CARD,
        key=v["id"],
    )


def operator_card(o: Operator) -> rx.Component:
    return rx.el.article(
        rx.el.h3(o["name"], class_name="text-lg font-bold text-[#1C1C1E]"),
        rx.el.p(
            f"{o['license']} · {o['phone']}", class_name="mt-2 text-[#6B6B6B]"
        ),
        rx.el.p(
            f"Availability: {o['status']}",
            class_name="my-3 font-semibold text-[#1C1C1E]",
        ),
        rx.el.button(
            "Edit operator",
            on_click=lambda: SharedState.open_provider_operator(o["id"]),
            class_name=SECONDARY,
        ),
        class_name=CARD,
        key=o["id"],
    )


def form_select(
    label: str, name: str, options: list[str], value: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(options, lambda o: rx.el.option(o, value=o)),
                id=name,
                name=name,
                default_value=value,
                key=value,
                required=True,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
    )


def operator_form() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Operator details",
            class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
        ),
        rx.el.form(
            field(
                "Full name", "name", SharedState.provider_operator_form["name"]
            ),
            field(
                "Contact number",
                "phone",
                SharedState.provider_operator_form["phone"],
                "tel",
            ),
            field(
                "Licence reference",
                "license",
                SharedState.provider_operator_form["license"],
            ),
            form_select(
                "Availability",
                "status",
                ["available", "unavailable", "assigned"],
                SharedState.provider_operator_form["status"],
            ),
            rx.el.p(
                "Assigned identity and availability are locked. Contact updates are allowed. These are demo licence records, not verified documents.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.button("Save operator", type="submit", class_name=SECONDARY),
            rx.el.button(
                "Close",
                type="button",
                on_click=lambda: SharedState.open_provider_panel(""),
                class_name=SECONDARY,
            ),
            on_submit=SharedState.save_provider_operator,
            class_name="flex flex-col gap-4",
        ),
        class_name=CARD,
    )


def fleet_screen() -> rx.Component:
    return provider_shell(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    f"Vehicles ({SharedState.provider_vehicles.length()})",
                    on_click=lambda: SharedState.set_provider_tab("Vehicles"),
                    aria_pressed=SharedState.provider_tab == "Vehicles",
                    class_name=SECONDARY,
                ),
                rx.el.button(
                    f"Operators ({SharedState.provider_operators.length()})",
                    on_click=lambda: SharedState.set_provider_tab("Operators"),
                    aria_pressed=SharedState.provider_tab == "Operators",
                    class_name=SECONDARY,
                ),
                class_name="grid grid-cols-2 gap-3",
            ),
            rx.el.div(
                metric(
                    "Available",
                    SharedState.provider_counts["available"].to_string(),
                ),
                metric(
                    "Assigned",
                    SharedState.provider_counts["assigned"].to_string(),
                ),
                metric(
                    "Unavailable",
                    SharedState.provider_counts["unavailable"].to_string(),
                ),
                class_name="my-4 grid grid-cols-3 gap-3",
            ),
            rx.el.label(
                "Search fleet or operators",
                html_for="provider-search",
                class_name="mb-2 block font-semibold text-[#1C1C1E]",
            ),
            rx.el.input(
                id="provider-search",
                type="search",
                placeholder="Registration, model, operator or licence…",
                default_value=SharedState.provider_query,
                on_change=SharedState.search_provider_fleet.debounce(500),
                class_name=INPUT,
            ),
            rx.el.div(
                rx.foreach(
                    [
                        "All",
                        "available",
                        "assigned",
                        "maintenance",
                        "unavailable",
                    ],
                    fleet_chip,
                ),
                class_name="my-4 flex gap-2 overflow-x-auto pb-2",
            ),
            rx.cond(
                SharedState.provider_panel == "operator",
                operator_form(),
                rx.fragment(),
            ),
            rx.cond(
                SharedState.provider_tab == "Vehicles",
                rx.cond(
                    SharedState.provider_filtered_vehicles.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            SharedState.provider_filtered_vehicles, vehicle_card
                        ),
                        class_name="grid gap-4 md:grid-cols-2",
                    ),
                    empty("No vehicles match these filters."),
                ),
                rx.cond(
                    SharedState.provider_filtered_operators.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            SharedState.provider_filtered_operators,
                            operator_card,
                        ),
                        class_name="grid gap-4 md:grid-cols-2",
                    ),
                    empty("No operators match these filters."),
                ),
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Fleet & Operators",
        "Fleet",
        footer=rx.el.div(
            rx.cond(
                SharedState.provider_tab == "Vehicles",
                rx.el.button(
                    "Add Machine",
                    on_click=lambda: SharedState.open_provider_vehicle(""),
                    class_name=PRIMARY,
                ),
                rx.el.button(
                    "Add Operator",
                    on_click=lambda: SharedState.open_provider_operator(""),
                    class_name=PRIMARY,
                ),
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )


def equipment_selector() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Catalogue equipment type",
            html_for="equipment_id",
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    SharedState.provider_equipment,
                    lambda e: rx.el.option(e["name"], value=e["id"]),
                ),
                id="equipment_id",
                name="equipment_id",
                default_value=SharedState.provider_vehicle_form["equipment_id"],
                key=SharedState.provider_vehicle_form["equipment_id"],
                required=True,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
    )


def equipment_screen() -> rx.Component:
    return provider_shell(
        rx.el.div(
            rx.el.a(
                "Back to fleet", href="/provider/fleet", class_name=SECONDARY
            ),
            rx.el.p(
                "Base rates apply to this catalogue equipment type for future requests. Existing requested/agreed rates and totals never change. Overtime is a demo fleet rate; no automatic extra hours are billed.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.form(
                equipment_selector(),
                form_select(
                    "Matching category",
                    "category",
                    ["Earthmoving", "Haulage", "Compaction & RMC", "Cranes"],
                    SharedState.provider_vehicle_form["category"],
                ),
                field(
                    "Make & full model name",
                    "model",
                    SharedState.provider_vehicle_form["model"],
                ),
                field(
                    "Vehicle registration",
                    "registration",
                    SharedState.provider_vehicle_form["registration"],
                ),
                field(
                    "Base hourly rate (INR)",
                    "rate",
                    SharedState.provider_vehicle_form["rate"],
                ),
                field(
                    "Overtime hourly rate (INR)",
                    "overtime",
                    SharedState.provider_vehicle_form["overtime"],
                ),
                field(
                    "Base depot address",
                    "depot",
                    SharedState.provider_vehicle_form["depot"],
                ),
                form_select(
                    "Vehicle availability",
                    "status",
                    ["available", "maintenance", "assigned"],
                    SharedState.provider_vehicle_form["status"],
                ),
                rx.el.p(
                    "Assigned assets: only future rates may change. Registration, model, type, depot and availability remain locked until released.",
                    class_name="text-[#6B6B6B]",
                ),
                id="provider-equipment",
                on_submit=SharedState.save_provider_vehicle,
                class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-white p-4",
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Add / Edit Equipment",
        "Fleet",
        footer=rx.el.div(
            rx.el.button(
                "Save Equipment Changes",
                type="submit",
                form="provider-equipment",
                class_name=PRIMARY,
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )


def profile_panel_button(panel: str, label: str) -> rx.Component:
    return rx.el.button(
        label,
        rx.icon("chevron-right", class_name="h-5 w-5"),
        on_click=lambda: SharedState.open_provider_panel(panel),
        class_name=SECONDARY,
    )


def earnings_panel() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Detailed earnings statement",
            class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
        ),
        rx.el.p(
            "Completed booking lines only. No tax, settlement or bank payout has been processed; all completed earnings remain pending clearance in this demo.",
            class_name="mb-4 text-[#6B6B6B]",
        ),
        rx.cond(
            SharedState.provider_completed.length() > 0,
            rx.el.div(
                rx.foreach(
                    SharedState.provider_completed, provider_booking_card
                ),
                class_name="grid gap-4 md:grid-cols-2",
            ),
            empty("No completed shifts yet."),
        ),
        class_name=CARD,
    )


def demo_profile_panel() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            rx.match(
                SharedState.provider_panel,
                ("bank", "Bank & settlement demo"),
                ("compliance", "Compliance demo"),
                "Support demo",
            ),
            class_name="text-lg font-bold text-[#1C1C1E]",
        ),
        rx.el.p(
            "Sample details only. Do not enter real bank details. Saving does not verify documents, send support messages or trigger payments.",
            class_name="my-4 text-[#6B6B6B]",
        ),
        rx.el.form(
            field(
                "Editable demo reference / note",
                "value",
                SharedState.provider_demo.get(SharedState.provider_panel, ""),
            ),
            rx.el.button(
                "Save demo detail", type="submit", class_name=SECONDARY
            ),
            on_submit=SharedState.save_provider_demo,
            class_name="flex flex-col gap-4",
        ),
        class_name=CARD,
    )


def provider_profile_screen() -> rx.Component:
    return provider_shell(
        rx.el.div(
            rx.el.section(
                rx.el.p(
                    "Provider · Demo identity",
                    class_name="mb-2 text-sm text-[#6B6B6B]",
                ),
                rx.el.h2(
                    SharedState.provider_identity["company"],
                    class_name="text-2xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    SharedState.provider_identity["name"],
                    class_name="mt-3 font-semibold text-[#1C1C1E]",
                ),
                rx.el.p(
                    SharedState.provider_identity["phone"],
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    SharedState.provider_identity["email"],
                    class_name="mt-2 break-all text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
            rx.el.div(
                metric(
                    "Completed earnings · sample",
                    f"₹{SharedState.provider_earnings:,.2f}",
                ),
                metric(
                    "Pending clearance · sample",
                    f"₹{SharedState.provider_earnings:,.2f}",
                ),
                metric(
                    "Completed unit shifts",
                    SharedState.provider_completed_shifts.to_string(),
                ),
                class_name="grid gap-4 sm:grid-cols-3",
            ),
            rx.el.p(
                "No actual bank payout. Pending clearance equals completed agreed totals because no settlement service is connected.",
                class_name="text-[#6B6B6B]",
            ),
            profile_panel_button(
                "earnings", "View detailed earnings statement"
            ),
            rx.el.h2(
                "Account, Compliance & Support",
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            profile_panel_button("bank", "Bank Account & Settlement · sample"),
            profile_panel_button(
                "compliance", "Fleet Compliance Papers · unverified demo"
            ),
            profile_panel_button(
                "support", "Support & Ward Help · demo contact"
            ),
            rx.match(
                SharedState.provider_panel,
                ("earnings", earnings_panel()),
                ("bank", demo_profile_panel()),
                ("compliance", demo_profile_panel()),
                ("support", demo_profile_panel()),
                rx.fragment(),
            ),
            rx.cond(
                SharedState.provider_panel != "",
                rx.el.button(
                    "Close panel",
                    on_click=lambda: SharedState.open_provider_panel(""),
                    class_name=SECONDARY,
                ),
                rx.fragment(),
            ),
            rx.el.p(
                "Logout keeps this session's records for role switching. A full reload resets the demo.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.button(
                "Logout / Switch role",
                rx.icon("log-out", class_name="h-5 w-5"),
                on_click=SharedState.logout,
                class_name=SECONDARY,
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Provider Profile & Earnings",
        "Profile",
    )
