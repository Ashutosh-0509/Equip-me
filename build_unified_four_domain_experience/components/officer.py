import reflex as rx

from build_unified_four_domain_experience.components.acceptance_summary import acceptance_summary
from build_unified_four_domain_experience.components.mobile_shell import CARD, INPUT, PRIMARY, SECONDARY, badge
from build_unified_four_domain_experience.components.officer_shell import officer_shell
from build_unified_four_domain_experience.states.demo_data import Booking, Line, Dispute
from build_unified_four_domain_experience.states.shared_state import SharedState


STATUSES = [
    "All",
    "Awaiting provider",
    "Awaiting approval",
    "Approved",
    "Active",
    "Completed",
    "Closed",
    "Issues",
]


def heading(label: str) -> rx.Component:
    return rx.el.h2(label, class_name="text-lg font-bold text-[#1C1C1E]")


def empty(label: str) -> rx.Component:
    return rx.el.p(
        label,
        class_name="rounded-xl border border-dashed border-[#E5E5EA] bg-white p-4 text-[#6B6B6B]",
    )


def officer_input(
    label: str,
    name: str,
    value: str = "",
    kind: str = "text",
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.input(
            id=name,
            name=name,
            default_value=value,
            key=value,
            type=kind,
            required=required,
            class_name=INPUT,
        ),
        class_name="w-full min-w-0",
    )


def dropdown(
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
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                id=name,
                name=name,
                default_value=value,
                key=value,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-white pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
        class_name="w-full min-w-0",
    )


def check(label: str, name: str) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            name=name,
            id=name,
            class_name="h-5 w-5 shrink-0 accent-[#FFB400] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
        ),
        rx.el.span(label, class_name="text-[#1C1C1E]"),
        html_for=name,
        class_name="flex min-h-12 cursor-pointer items-center gap-3 rounded-xl border border-[#E5E5EA] bg-white p-3",
    )


def note_field(
    label: str = "Review note (5–1000 characters)",
    name: str = "note",
    minimum: int = 5,
    maximum: int = 1000,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.textarea(
            id=name,
            name=name,
            required=True,
            min_length=minimum,
            max_length=maximum,
            rows=4,
            class_name="w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
        ),
    )


def filters() -> rx.Component:
    return rx.el.section(
        rx.el.form(
            officer_input(
                "Booking date · blank for all",
                "date",
                SharedState.officer_date,
                "date",
            ),
            dropdown(
                "Ward",
                "ward",
                SharedState.officer_wards,
                SharedState.officer_ward,
            ),
            rx.el.button(
                "Apply date / ward", type="submit", class_name=SECONDARY
            ),
            rx.el.button(
                "Clear filters",
                type="button",
                on_click=SharedState.clear_officer_filters,
                class_name=SECONDARY,
            ),
            on_submit=SharedState.filter_officer_bookings,
            class_name="grid grid-cols-1 items-end gap-4 sm:grid-cols-2",
        ),
        rx.el.p(
            "Filters use the booking's scheduled date and ward. Blank date includes all sample records.",
            class_name="mt-3 text-sm text-[#6B6B6B]",
        ),
        class_name=CARD,
    )


def search_box(
    label: str, value: str, handler: rx.event.EventType
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for="officer-search",
            class_name="mb-2 block font-semibold text-[#1C1C1E]",
        ),
        rx.el.input(
            id="officer-search",
            type="search",
            default_value=value,
            on_change=handler.debounce(500),
            class_name=INPUT,
        ),
    )


def status_chips() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            STATUSES,
            lambda label: rx.el.button(
                label,
                type="button",
                on_click=lambda: SharedState.set_officer_status(label),
                aria_pressed=SharedState.officer_status == label,
                class_name=rx.cond(
                    SharedState.officer_status == label,
                    "min-h-12 shrink-0 rounded-full border-2 border-[#FFB400] bg-white px-4 font-bold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
                    "min-h-12 shrink-0 rounded-full border border-[#E5E5EA] bg-white px-4 text-[#6B6B6B] hover:text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                ),
            ),
        ),
        aria_label="Booking status filters",
        class_name="flex w-full gap-2 overflow-x-auto pb-2",
    )


def booking_card(b: Booking) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(b["id"], class_name="font-bold text-[#1C1C1E]"),
            badge(b["status"]),
            class_name="flex flex-wrap items-center justify-between gap-2",
        ),
        rx.el.p(
            SharedState.officer_cards.get(
                b["id"], {"parties": "", "units": "", "assignment": ""}
            )["parties"],
            class_name="mt-3 font-semibold text-[#1C1C1E]",
        ),
        rx.el.p(b["work_order"], class_name="mt-2 break-words text-[#1C1C1E]"),
        rx.el.p(b["address"], class_name="mt-2 break-words text-[#6B6B6B]"),
        rx.el.p(
            f"{b['date']} · {b['shift']} · Ward {b['ward']}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.p(
            SharedState.officer_cards.get(
                b["id"], {"parties": "", "units": "", "assignment": ""}
            )["units"],
            class_name="mt-2 font-semibold text-[#1C1C1E]",
        ),
        rx.el.p(
            f"Requested estimate ₹{b['requested_total']:,.2f}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.cond(
            b["provider_reviewed"],
            rx.el.p(
                f"Accepted quote ₹{b['total']:,.2f}",
                class_name="font-bold text-[#1C1C1E]",
            ),
            rx.el.p(
                "Accepted quote awaiting Provider review",
                class_name="text-[#6B6B6B]",
            ),
        ),
        rx.el.p(
            SharedState.officer_cards.get(
                b["id"], {"parties": "", "units": "", "assignment": ""}
            )["assignment"],
            class_name="mt-2 break-words text-[#6B6B6B]",
        ),
        rx.el.button(
            "Review / Details",
            type="button",
            on_click=lambda: SharedState.open_officer_booking(b["id"]),
            class_name="mt-4 flex min-h-12 w-full items-center justify-center rounded-xl border border-[#E5E5EA] bg-white px-4 font-semibold text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
        key=b["id"],
        class_name=CARD,
    )


def booking_list(
    records: list[Booking], message: str = "No bookings match these filters."
) -> rx.Component:
    return rx.cond(
        records.length() > 0,
        rx.el.div(
            rx.foreach(records, booking_card),
            class_name="grid w-full grid-cols-1 gap-4 md:grid-cols-2",
        ),
        empty(message),
    )


def metric(label: str, value: int) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm font-semibold text-[#6B6B6B]"),
        rx.el.p(value, class_name="mt-2 text-2xl font-bold text-[#1C1C1E]"),
        class_name=CARD,
    )


def audit_card(a: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.p(a["action"], class_name="font-bold text-[#1C1C1E]"),
        rx.el.p(a["actor"], class_name="mt-2 text-[#1C1C1E]"),
        rx.el.p(
            a["timestamp"], class_name="mt-1 break-words text-sm text-[#6B6B6B]"
        ),
        rx.el.p(
            a["note"],
            class_name="mt-2 whitespace-pre-wrap break-words text-[#6B6B6B]",
        ),
        rx.cond(
            a["booking_id"] != "",
            rx.el.button(
                a["booking_id"],
                type="button",
                on_click=lambda: SharedState.open_officer_booking(
                    a["booking_id"]
                ),
                class_name=SECONDARY,
            ),
            rx.el.p(
                "Account / fleet evidence",
                class_name="mt-2 text-sm text-[#6B6B6B]",
            ),
        ),
        rx.el.p(a["id"], class_name="mt-2 text-xs text-[#6B6B6B]"),
        key=a["id"],
        class_name=CARD,
    )


def audit_list(records: list[dict[str, str]]) -> rx.Component:
    return rx.cond(
        records.length() > 0,
        rx.el.div(
            rx.foreach(records, audit_card), class_name="flex flex-col gap-4"
        ),
        empty("No audit evidence matches."),
    )


def officer_dashboard_screen() -> rx.Component:
    return officer_shell(
        rx.el.div(
            filters(),
            rx.el.p(
                "Session records only · no GPS map, live feed or remote monitoring.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.div(
                metric(
                    "Pending approval", SharedState.officer_metrics["pending"]
                ),
                metric(
                    "Active deployments", SharedState.officer_metrics["active"]
                ),
                metric(
                    "Open disputes", SharedState.officer_metrics["disputes"]
                ),
                metric("Completed", SharedState.officer_metrics["completed"]),
                class_name="grid w-full grid-cols-2 gap-4 md:grid-cols-4",
            ),
            heading("Needs your review · earliest scheduled first"),
            booking_list(
                SharedState.officer_queue,
                "No pending approvals in this date / ward.",
            ),
            heading("Exceptions & allocation notices"),
            rx.el.p(
                "Awaiting Provider, approved-but-unassigned, stopped problem bookings and open disputes require separate review.",
                class_name="text-[#6B6B6B]",
            ),
            booking_list(
                SharedState.officer_exceptions,
                "No exceptions in this date / ward.",
            ),
            heading("Active deployments"),
            booking_list(
                SharedState.officer_deployments,
                "No active deployments in this date / ward.",
            ),
            heading("Recent audit evidence"),
            audit_list(SharedState.officer_recent_audit),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
        "Control Room Dashboard",
    )


def officer_requests_screen() -> rx.Component:
    return officer_shell(
        rx.el.div(
            filters(),
            search_box(
                "Search booking, work order, site or parties",
                SharedState.officer_query,
                SharedState.search_officer_bookings,
            ),
            status_chips(),
            rx.el.p(
                f"{SharedState.officer_requests.length()} matching bookings",
                role="status",
                class_name="text-[#6B6B6B]",
            ),
            booking_list(SharedState.officer_requests),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
        "All Ward Bookings",
        "Requests",
    )


def quote_line(l: Line) -> rx.Component:
    return rx.el.div(
        rx.el.h3(l["name"], class_name="font-semibold text-[#1C1C1E]"),
        rx.el.p(
            f"{l['quantity']} units × {l['hours']} hours × ₹{l['rate']:,.2f}/hr = ₹{l['amount']:,.2f}",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        class_name="border-b border-[#E5E5EA] py-3 last:border-0",
    )


def review_form() -> rx.Component:
    return rx.el.form(
        heading("Verify before approval"),
        rx.el.p(
            "Approval preserves the Provider's quoted rates and accepted units. Unfulfilled units are not deployed or billed.",
            class_name="text-[#6B6B6B]",
        ),
        check("Site address, access and schedule verified", "site_verified"),
        check(
            "Work order and Contractor identity verified", "work_order_verified"
        ),
        check("Booked Provider and acceptance verified", "provider_verified"),
        check("Contractor safety readiness verified", "safety_verified"),
        rx.cond(
            SharedState.officer_partial,
            check(
                "I acknowledge partial acceptance and all unfulfilled units",
                "partial_ack",
            ),
            rx.fragment(),
        ),
        note_field(),
        rx.el.button(
            "Cancel review",
            type="button",
            on_click=lambda: SharedState.set_officer_panel(""),
            class_name=SECONDARY,
        ),
        id="officer-approval",
        on_submit=SharedState.approve_officer_booking,
        class_name="flex flex-col gap-4 rounded-xl border border-[#FFB400] bg-white p-4 text-[#1C1C1E]",
    )


def rejection_form() -> rx.Component:
    return rx.el.form(
        heading("Reject booking"),
        note_field("Rejection reason (5–500 characters)", "reason", 5, 500),
        check(
            "I confirm rejection; Contractor and Provider will see this reason",
            "confirm",
        ),
        rx.el.button("Confirm rejection", type="submit", class_name=SECONDARY),
        rx.el.button(
            "Cancel",
            type="button",
            on_click=lambda: SharedState.set_officer_panel(""),
            class_name=SECONDARY,
        ),
        on_submit=SharedState.reject_officer_booking,
        class_name="flex flex-col gap-4 rounded-xl border border-red-200 bg-white p-4 text-[#1C1C1E]",
    )


def allocation_unit(unit: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.h3(unit["name"], class_name="font-semibold text-[#1C1C1E]"),
        rx.el.label(
            "Vehicle",
            html_for=f"vehicle_{unit['key']}",
            class_name="block text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("Select compatible vehicle", value=""),
                rx.foreach(
                    SharedState.officer_available_vehicles,
                    lambda v: rx.cond(
                        v["equipment_id"] == unit["equipment_id"],
                        rx.el.option(
                            f"{v['registration']} · {v['model']}", value=v["id"]
                        ),
                        rx.fragment(),
                    ),
                ),
                name=f"vehicle_{unit['key']}",
                id=f"vehicle_{unit['key']}",
                default_value=unit["vehicle_id"],
                key=f"vehicle_{unit['key']}_{unit['vehicle_id']}",
                required=True,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-white pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
        rx.el.label(
            "Operator",
            html_for=f"operator_{unit['key']}",
            class_name="block text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("Select available operator", value=""),
                rx.foreach(
                    SharedState.officer_available_operators,
                    lambda o: rx.el.option(
                        f"{o['name']} · {o['license']}", value=o["id"]
                    ),
                ),
                name=f"operator_{unit['key']}",
                id=f"operator_{unit['key']}",
                default_value=unit["operator_id"],
                key=f"operator_{unit['key']}_{unit['operator_id']}",
                required=True,
                class_name="h-14 w-full appearance-none rounded-xl border border-[#E5E5EA] bg-white pl-4 pr-12 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-6 w-6 text-[#1C1C1E]",
            ),
            class_name="relative",
        ),
        key=unit["key"],
        class_name="flex flex-col gap-3 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
    )


def reassignment_form() -> rx.Component:
    return rx.el.form(
        heading("Replace allocation · booked Provider only"),
        rx.el.p(
            "Choose one pair per accepted unit. Existing pairs may be kept; overlapping reservations and duplicate selections are rejected together. No work may have started.",
            class_name="text-[#6B6B6B]",
        ),
        rx.foreach(SharedState.officer_units, allocation_unit),
        note_field("Reassignment reason (5–500 characters)", "reason", 5, 500),
        check(
            "I confirm the complete replacement allocation and separate arrival handoff",
            "confirm",
        ),
        rx.el.button(
            "Confirm reassignment", type="submit", class_name=SECONDARY
        ),
        rx.el.button(
            "Cancel",
            type="button",
            on_click=lambda: SharedState.set_officer_panel(""),
            class_name=SECONDARY,
        ),
        on_submit=SharedState.reassign_officer_booking,
        class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]",
    )


def officer_note_form() -> rx.Component:
    return rx.el.form(
        heading("Record review / request clarification"),
        note_field(),
        rx.el.p(
            "Appends local audit evidence only; no message is transmitted and booking status is unchanged.",
            class_name="text-[#6B6B6B]",
        ),
        rx.el.button("Add audit note", type="submit", class_name=SECONDARY),
        rx.el.button(
            "Cancel",
            type="button",
            on_click=lambda: SharedState.set_officer_panel(""),
            class_name=SECONDARY,
        ),
        on_submit=SharedState.add_officer_note,
        class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]",
    )


def detail_dispute(d: Dispute) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            f"{d['category']} · {d['status']} · {d['id']}",
            class_name="font-semibold text-[#1C1C1E]",
        ),
        rx.el.p(d["description"], class_name="mt-2 text-[#6B6B6B]"),
        rx.el.p(d["resolution"], class_name="mt-2 text-[#6B6B6B]"),
        rx.el.a(
            "Review disputes in More",
            href="/officer/more",
            class_name=SECONDARY,
        ),
        class_name=CARD,
    )


def officer_detail_screen() -> rx.Component:
    return officer_shell(
        rx.cond(
            SharedState.officer_current["id"] != "",
            rx.el.div(
                rx.el.a(
                    "Back to Requests",
                    href="/officer/requests",
                    class_name=SECONDARY,
                ),
                rx.el.section(
                    heading("Verification Summary"),
                    rx.el.p(
                        SharedState.officer_current["id"],
                        class_name="mt-2 font-bold text-[#1C1C1E]",
                    ),
                    badge(SharedState.officer_current["status"]),
                    rx.el.p(
                        SharedState.officer_parties,
                        class_name="mt-4 font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        f"Contractor ID: {SharedState.officer_current['contractor_id']} · Provider ID: {SharedState.officer_current['provider_id']}",
                        class_name="mt-2 text-sm text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        SharedState.officer_current["work_order"],
                        class_name="mt-3 text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        SharedState.officer_current["address"],
                        class_name="mt-3 text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        f"Ward {SharedState.officer_current['ward']} · {SharedState.officer_current['date']} · {SharedState.officer_current['shift']}",
                        class_name="mt-3 text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        rx.cond(
                            SharedState.officer_current["safety_confirmed"],
                            "Contractor safety readiness: Confirmed",
                            "Contractor safety readiness: Not confirmed",
                        ),
                        class_name="mt-3 font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        SharedState.officer_current["reason"],
                        class_name="mt-2 text-red-800",
                    ),
                    class_name=CARD,
                ),
                acceptance_summary(SharedState.officer_current),
                rx.el.section(
                    heading("Original requested rate snapshots"),
                    rx.foreach(
                        SharedState.officer_current["requested_lines"],
                        quote_line,
                    ),
                    rx.el.p(
                        f"Requested estimate ₹{SharedState.officer_current['requested_total']:,.2f}",
                        class_name="mt-3 font-bold text-[#1C1C1E]",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    heading("Accepted lines / financial lock"),
                    rx.foreach(
                        SharedState.officer_current["lines"], quote_line
                    ),
                    rx.el.p(
                        f"Recorded total ₹{SharedState.officer_current['total']:,.2f}",
                        class_name="mt-3 font-bold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        "Sample estimates only. Until Provider review, lines remain the request, not an agreed acceptance. No payout or extra fees.",
                        class_name="mt-2 text-[#6B6B6B]",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    heading("Resolved allocation & lifecycle evidence"),
                    rx.cond(
                        SharedState.officer_assignment_details.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                SharedState.officer_assignment_details,
                                lambda a: rx.el.div(
                                    rx.el.h3(
                                        a["equipment"],
                                        class_name="font-semibold text-[#1C1C1E]",
                                    ),
                                    rx.el.p(
                                        a["vehicle"],
                                        class_name="mt-2 text-[#1C1C1E]",
                                    ),
                                    rx.el.p(
                                        a["operator"],
                                        class_name="mt-2 text-[#1C1C1E]",
                                    ),
                                    rx.cond(
                                        a["phone"] != "",
                                        rx.el.a(
                                            f"Call sample operator contact {a['phone']}",
                                            href=f"tel:{a['phone']}",
                                            class_name=SECONDARY,
                                        ),
                                        rx.fragment(),
                                    ),
                                    class_name="border-b border-[#E5E5EA] py-3 last:border-0",
                                ),
                            )
                        ),
                        rx.el.p(
                            "No allocation recorded",
                            class_name="mt-3 text-[#6B6B6B]",
                        ),
                    ),
                    rx.el.p(
                        f"Started: {SharedState.officer_current['started_at']} · Ended: {SharedState.officer_current['ended_at']}",
                        class_name="mt-2 break-words text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        "Unstarted stopped bookings need explicit reassignment. Arrived / started / completed work cannot be rejected or reassigned here.",
                        class_name="mt-2 text-[#6B6B6B]",
                    ),
                    class_name=CARD,
                ),
                rx.el.div(
                    rx.el.button(
                        "Record review / Ask for info",
                        type="button",
                        on_click=lambda: SharedState.set_officer_panel("note"),
                        class_name=SECONDARY,
                    ),
                    rx.el.button(
                        "Reject / Remarks",
                        type="button",
                        disabled=~SharedState.officer_can_reject,
                        on_click=lambda: SharedState.set_officer_panel(
                            "reject"
                        ),
                        class_name=SECONDARY,
                    ),
                    rx.el.button(
                        "Reassign vehicle & operator",
                        type="button",
                        disabled=~SharedState.officer_can_reassign,
                        on_click=lambda: SharedState.set_officer_panel(
                            "reassign"
                        ),
                        class_name=SECONDARY,
                    ),
                    class_name="flex flex-col gap-3 sm:flex-row sm:flex-wrap",
                ),
                rx.match(
                    SharedState.officer_panel,
                    ("approve", review_form()),
                    ("reject", rejection_form()),
                    ("reassign", reassignment_form()),
                    ("note", officer_note_form()),
                    rx.fragment(),
                ),
                heading("Disputes"),
                rx.cond(
                    SharedState.officer_booking_disputes.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            SharedState.officer_booking_disputes, detail_dispute
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    empty("No disputes for this booking."),
                ),
                heading("Booking audit · read-only evidence"),
                audit_list(SharedState.officer_booking_audit),
                class_name="flex w-full min-w-0 flex-col gap-4 break-words",
            ),
            rx.el.div(
                empty("Booking not found. No review actions are available."),
                rx.el.a(
                    "Open Requests",
                    href="/officer/requests",
                    class_name=SECONDARY,
                ),
                class_name="flex flex-col gap-4",
            ),
        ),
        "Booking Verification & Details",
        "Requests",
        rx.cond(
            SharedState.officer_current["id"] != "",
            rx.el.div(
                rx.cond(
                    SharedState.officer_panel == "approve",
                    rx.el.button(
                        "Approve verified booking",
                        type="submit",
                        form="officer-approval",
                        disabled=SharedState.officer_approval_block != "",
                        class_name=PRIMARY,
                    ),
                    rx.el.button(
                        "Review verification & approve",
                        type="button",
                        disabled=SharedState.officer_approval_block != "",
                        on_click=lambda: SharedState.set_officer_panel(
                            "approve"
                        ),
                        class_name=PRIMARY,
                    ),
                ),
                rx.cond(
                    SharedState.officer_approval_block != "",
                    rx.el.p(
                        SharedState.officer_approval_block,
                        class_name="mt-2 text-sm text-[#6B6B6B]",
                    ),
                    rx.fragment(),
                ),
                class_name="border-t border-[#E5E5EA] py-3",
            ),
            rx.fragment(),
        ),
    )


def directory_card(r: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.h2(r["company"], class_name="text-lg font-bold text-[#1C1C1E]"),
        rx.el.p(f"{r['name']} · {r['id']}", class_name="mt-2 text-[#6B6B6B]"),
        rx.el.p(r["counts"], class_name="mt-3 text-[#1C1C1E]"),
        rx.el.p(
            "Sample contact · not masked or verified",
            class_name="mt-3 text-sm text-[#6B6B6B]",
        ),
        rx.el.div(
            rx.el.a(
                f"Call {r['phone']}",
                href=f"tel:{r['phone']}",
                class_name=SECONDARY,
            ),
            rx.el.a(
                "Email sample contact",
                href=f"mailto:{r['email']}",
                class_name=SECONDARY,
            ),
            class_name="mt-2 flex flex-col gap-2",
        ),
        rx.el.button(
            "Inspect records",
            type="button",
            on_click=lambda: SharedState.open_officer_entity(r["id"]),
            class_name=SECONDARY,
        ),
        rx.cond(
            SharedState.officer_entity_id == r["id"],
            rx.el.div(
                heading("Own bookings"),
                booking_list(
                    SharedState.officer_entity_bookings,
                    "No bookings for this identity.",
                ),
                rx.cond(
                    SharedState.officer_directory_tab == "Providers",
                    rx.el.div(
                        heading("Own fleet"),
                        rx.cond(
                            SharedState.officer_entity_vehicles.length() > 0,
                            rx.el.div(
                                rx.foreach(
                                    SharedState.officer_entity_vehicles,
                                    lambda v: rx.el.p(
                                        f"{v['registration']} · {v['model']} · {v['status']} · {v['depot']}",
                                        class_name="border-b border-[#E5E5EA] py-3 text-[#1C1C1E]",
                                    ),
                                )
                            ),
                            empty("No fleet records for this Provider."),
                        ),
                        heading("Own operators"),
                        rx.cond(
                            SharedState.officer_entity_operators.length() > 0,
                            rx.el.div(
                                rx.foreach(
                                    SharedState.officer_entity_operators,
                                    lambda o: rx.el.p(
                                        f"{o['name']} · {o['license']} · {o['status']} · {o['phone']}",
                                        class_name="border-b border-[#E5E5EA] py-3 text-[#1C1C1E]",
                                    ),
                                )
                            ),
                            empty("No operator records for this Provider."),
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    "Close detail",
                    type="button",
                    on_click=lambda: SharedState.open_officer_entity(""),
                    class_name=SECONDARY,
                ),
                class_name="mt-4 flex flex-col gap-4 border-t border-[#E5E5EA] pt-4",
            ),
            rx.fragment(),
        ),
        key=r["id"],
        class_name="flex flex-col gap-2 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]",
    )


def officer_directory_screen() -> rx.Component:
    return officer_shell(
        rx.el.div(
            rx.el.p(
                f"{SharedState.providers.length()} sample Providers · {SharedState.contractors.length()} sample Contractors. No compliance scores or verification claims.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.div(
                rx.foreach(
                    ["Providers", "Contractors"],
                    lambda label: rx.el.button(
                        label,
                        type="button",
                        aria_pressed=SharedState.officer_directory_tab == label,
                        on_click=lambda: SharedState.set_officer_directory_tab(
                            label
                        ),
                        class_name=rx.cond(
                            SharedState.officer_directory_tab == label,
                            "min-h-12 flex-1 rounded-xl border-2 border-[#FFB400] bg-white px-4 font-bold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
                            SECONDARY,
                        ),
                    ),
                ),
                class_name="flex gap-2",
            ),
            search_box(
                "Search firm, identity or contact",
                SharedState.officer_directory_query,
                SharedState.search_officer_directory,
            ),
            rx.cond(
                SharedState.officer_directory.length() > 0,
                rx.el.div(
                    rx.foreach(SharedState.officer_directory, directory_card),
                    class_name="flex flex-col gap-4",
                ),
                empty("No directory identities match."),
            ),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
        "Providers & Contractors",
        "Directory",
    )


def report_row(b: Booking) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.button(
                b["id"],
                type="button",
                on_click=lambda: SharedState.open_officer_booking(b["id"]),
                class_name=SECONDARY,
            ),
            class_name="p-3",
        ),
        rx.el.td(f"{b['date']} · {b['ward']}", class_name="p-3 text-[#6B6B6B]"),
        rx.el.td(badge(b["status"]), class_name="p-3"),
        rx.el.td(
            SharedState.officer_cards.get(
                b["id"], {"parties": "", "units": "", "assignment": ""}
            )["units"],
            class_name="p-3 text-[#1C1C1E]",
        ),
        rx.el.td(
            f"₹{b['requested_total']:,.2f}",
            class_name="p-3 text-right text-[#1C1C1E]",
        ),
        rx.el.td(
            rx.cond(
                b["provider_reviewed"], f"₹{b['total']:,.2f}", "Awaiting review"
            ),
            class_name="p-3 text-right text-[#1C1C1E]",
        ),
        key=b["id"],
        class_name="border-b border-[#E5E5EA] bg-white even:bg-[#F5F5F5] hover:bg-gray-100",
    )


def reports_panel() -> rx.Component:
    return rx.el.div(
        filters(),
        status_chips(),
        search_box(
            "Search report bookings or parties",
            SharedState.officer_query,
            SharedState.search_officer_bookings,
        ),
        rx.el.section(
            heading("Sample financial estimates"),
            rx.el.p(
                f"Agreed completed earnings estimate ₹{SharedState.officer_report_totals['completed']:,.2f}",
                class_name="mt-3 font-semibold text-[#1C1C1E]",
            ),
            rx.el.p(
                f"Accepted planned totals (not completed) ₹{SharedState.officer_report_totals['planned']:,.2f}",
                class_name="mt-2 text-[#1C1C1E]",
            ),
            rx.el.p(
                "These sum the filtered booking quotes, not actual payouts or measured work. Closed and draft records are excluded from planned totals.",
                class_name="mt-2 text-[#6B6B6B]",
            ),
            class_name=CARD,
        ),
        rx.el.button(
            "Download filtered sample CSV",
            type="button",
            on_click=SharedState.export_officer_report,
            class_name=SECONDARY,
        ),
        rx.cond(
            SharedState.officer_requests.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.caption(
                            "Filtered booking report · INR sample estimates",
                            class_name="p-4 text-left font-semibold text-[#1C1C1E]",
                        ),
                        rx.el.thead(
                            rx.el.tr(
                                rx.foreach(
                                    [
                                        "Booking",
                                        "Date / Ward",
                                        "Status",
                                        "Units",
                                        "Requested",
                                        "Accepted",
                                    ],
                                    lambda label: rx.el.th(
                                        label,
                                        scope="col",
                                        class_name="bg-[#F5F5F5] p-3 text-left font-semibold text-[#1C1C1E]",
                                    ),
                                )
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(SharedState.officer_requests, report_row)
                        ),
                        class_name="table-auto w-full min-w-[700px]",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="w-full overflow-hidden rounded-xl border border-[#E5E5EA] bg-white",
            ),
            empty("No report records match."),
        ),
        class_name="flex w-full min-w-0 flex-col gap-4",
    )


def dispute_card(d: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.h3(
            f"{d['category']} · {d['status']}",
            class_name="font-bold text-[#1C1C1E]",
        ),
        rx.el.p(
            f"{d['id']} · {d['created_at']}",
            class_name="mt-2 break-words text-sm text-[#6B6B6B]",
        ),
        rx.el.p(
            f"Original reporter: {d['reporter']}",
            class_name="mt-2 text-[#1C1C1E]",
        ),
        rx.el.p(
            d["description"],
            class_name="mt-3 whitespace-pre-wrap text-[#1C1C1E]",
        ),
        rx.cond(
            d["resolution"] != "",
            rx.el.p(
                f"Resolution: {d['resolution']}",
                class_name="mt-3 whitespace-pre-wrap text-[#6B6B6B]",
            ),
            rx.fragment(),
        ),
        rx.el.button(
            f"Booking {d['booking_id']}",
            type="button",
            on_click=lambda: SharedState.open_officer_booking(d["booking_id"]),
            class_name=SECONDARY,
        ),
        rx.cond(
            d["status"] == "open",
            rx.el.button(
                "Open & resolve case",
                type="button",
                on_click=lambda: SharedState.open_officer_dispute(d["id"]),
                class_name=SECONDARY,
            ),
            rx.fragment(),
        ),
        rx.cond(
            SharedState.officer_dispute_id == d["id"],
            rx.el.form(
                heading("Resolution record"),
                note_field("Resolution (10–1000 characters)", "note", 10),
                check(
                    "I confirm resolution; booking phase and timestamps stay unchanged",
                    "confirm",
                ),
                rx.el.p(
                    "A stopped problem booking does not resume. Reassignment or review is a separate action on Booking Details.",
                    class_name="text-[#6B6B6B]",
                ),
                rx.el.button(
                    "Confirm resolution", type="submit", class_name=PRIMARY
                ),
                rx.el.button(
                    "Cancel",
                    type="button",
                    on_click=lambda: SharedState.open_officer_dispute(""),
                    class_name=SECONDARY,
                ),
                on_submit=SharedState.resolve_officer_dispute,
                class_name="mt-4 flex flex-col gap-4 border-t border-[#E5E5EA] pt-4",
            ),
            rx.fragment(),
        ),
        key=d["id"],
        class_name="flex flex-col gap-2 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]",
    )


def disputes_panel() -> rx.Component:
    return rx.el.div(
        filters(),
        rx.el.form(
            dropdown(
                "Case status",
                "status",
                ["Open", "Resolved", "All"],
                SharedState.officer_dispute_filter,
            ),
            dropdown(
                "Category",
                "category",
                ["All", "Breakdown", "Delay", "Safety", "Billing", "Other"],
                SharedState.officer_dispute_category,
            ),
            rx.el.button(
                "Apply case filters", type="submit", class_name=SECONDARY
            ),
            on_submit=SharedState.filter_officer_disputes,
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2",
        ),
        rx.cond(
            SharedState.officer_disputes.length() > 0,
            rx.el.div(
                rx.foreach(SharedState.officer_disputes, dispute_card),
                class_name="flex flex-col gap-4",
            ),
            empty(
                "No disputes match. Choose All or clear date / ward filters."
            ),
        ),
        class_name="flex flex-col gap-4",
    )


def audit_panel() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Read-only session audit evidence. No edit or delete controls. This demo does not claim production tamper-proof storage.",
            class_name="text-[#6B6B6B]",
        ),
        search_box(
            "Search audit booking, actor, action or note",
            SharedState.officer_audit_query,
            SharedState.search_officer_audit,
        ),
        rx.el.form(
            officer_input(
                "Evidence date · blank for all",
                "date",
                SharedState.officer_audit_date,
                "date",
            ),
            dropdown(
                "Action",
                "action",
                SharedState.officer_audit_actions,
                SharedState.officer_audit_action,
            ),
            rx.el.button(
                "Apply audit filters", type="submit", class_name=SECONDARY
            ),
            on_submit=SharedState.filter_officer_audit,
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2",
        ),
        audit_list(SharedState.officer_audit_records),
        class_name="flex flex-col gap-4",
    )


def officer_more_screen() -> rx.Component:
    return officer_shell(
        rx.el.div(
            rx.el.p(
                "Anita Joshi · Municipal review · Sample data only. No messaging, bank settlement or telemetry integration.",
                class_name="text-[#6B6B6B]",
            ),
            rx.el.div(
                rx.foreach(
                    ["Reports", "Disputes", "Audit"],
                    lambda label: rx.el.button(
                        label,
                        type="button",
                        aria_pressed=SharedState.officer_more_tab == label,
                        on_click=lambda: SharedState.set_officer_more_tab(
                            label
                        ),
                        class_name=rx.cond(
                            SharedState.officer_more_tab == label,
                            "min-h-12 flex-1 rounded-xl border-2 border-[#FFB400] bg-white px-3 font-bold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
                            SECONDARY,
                        ),
                    ),
                ),
                class_name="flex gap-2",
            ),
            rx.match(
                SharedState.officer_more_tab,
                ("Reports", reports_panel()),
                ("Disputes", disputes_panel()),
                ("Audit", audit_panel()),
                rx.fragment(),
            ),
            rx.el.button(
                "Log Out from Officer Console",
                type="button",
                on_click=SharedState.logout,
                class_name=SECONDARY,
            ),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
        "Reports, Disputes & Audit",
        "More",
    )
