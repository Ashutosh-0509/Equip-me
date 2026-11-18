import reflex as rx

from build_unified_four_domain_experience.components.contractor_booking import review_line
from build_unified_four_domain_experience.components.acceptance_summary import acceptance_summary
from build_unified_four_domain_experience.components.mobile_shell import (
    CARD,
    PRIMARY,
    SECONDARY,
    badge,
    dock_action,
    error_message,
    feedback_message,
    field,
    select_field,
    shell,
)
from build_unified_four_domain_experience.states.demo_data import Audit, Booking, Dispute
from build_unified_four_domain_experience.states.shared_state import SharedState


def booking_row(booking: Booking) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon("truck", class_name="h-5 w-5 text-[#6B6B6B]"),
            class_name="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-[#E5E5EA] bg-[#F5F5F5]",
        ),
        rx.el.div(
            rx.el.p(
                booking["id"],
                class_name="mb-1 text-xs font-semibold text-[#6B6B6B]",
            ),
            rx.foreach(
                booking["lines"],
                lambda line: rx.el.p(
                    f"{line['quantity']}× {line['name']}",
                    class_name="font-semibold leading-6 text-[#1C1C1E]",
                ),
            ),
            rx.el.p(
                f"Ward {booking['ward']} · {booking['date']}",
                class_name="mt-1 text-sm text-[#6B6B6B]",
            ),
            rx.el.div(
                badge(booking["status"]),
                rx.el.p(
                    f"₹{booking['total']:,.2f}",
                    class_name="font-bold text-[#1C1C1E]",
                ),
                class_name="mt-3 flex flex-wrap items-center justify-between gap-2",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.icon("chevron-right", class_name="h-5 w-5 shrink-0 text-[#6B6B6B]"),
        href=f"/contractor/bookings/{booking['id']}",
        class_name="flex items-start gap-3 border-b border-[#E5E5EA] bg-white py-4 first:pt-2 last:border-0 last:pb-2 hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        key=booking["id"],
    )


def home_screen() -> rx.Component:
    return shell(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    "Recent Bookings",
                    class_name="text-lg font-bold text-[#1C1C1E]",
                ),
                rx.el.a(
                    "View all",
                    rx.icon("chevron-right", class_name="h-4 w-4"),
                    href="/contractor/bookings",
                    class_name="flex min-h-12 items-center gap-1 font-semibold text-[#6B6B6B] hover:text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                ),
                class_name="mb-2 flex items-center justify-between",
            ),
            rx.cond(
                SharedState.recent_bookings.length() > 0,
                rx.foreach(SharedState.recent_bookings, booking_row),
                rx.el.p(
                    "No bookings yet. Order equipment to get started.",
                    class_name="py-6 text-[#6B6B6B]",
                ),
            ),
            class_name=CARD,
        ),
        "Contractor",
        footer=dock_action("Order Equipment", "/contractor/equipment"),
    )


def booking_filter(value: str) -> rx.Component:
    return rx.el.button(
        value,
        type="button",
        on_click=lambda: SharedState.filter_bookings(value),
        aria_pressed=SharedState.booking_filter == value,
        class_name=rx.cond(
            SharedState.booking_filter == value,
            "min-h-12 shrink-0 rounded-full border-2 border-[#FFB400] bg-white px-4 text-sm font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "min-h-12 shrink-0 rounded-full border-2 border-[#E5E5EA] bg-[#F5F5F5] px-4 text-sm font-medium text-[#6B6B6B] hover:border-[#6B6B6B] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def bookings_screen() -> rx.Component:
    return shell(
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["All", "Active", "Completed", "Drafts", "Closed"],
                    booking_filter,
                ),
                aria_label="Booking filters",
                class_name="mb-4 flex gap-2 overflow-x-auto pb-2",
            ),
            rx.cond(
                SharedState.filtered_bookings.length() > 0,
                rx.el.div(
                    rx.foreach(SharedState.filtered_bookings, booking_row),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.icon(
                        "calendar-days",
                        class_name="mx-auto h-8 w-8 text-[#6B6B6B]",
                    ),
                    rx.el.h2(
                        "No bookings here",
                        class_name="mt-4 text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.button(
                        "View all bookings",
                        on_click=lambda: SharedState.filter_bookings("All"),
                        class_name=SECONDARY,
                    ),
                    class_name="flex flex-col items-center gap-4 rounded-xl bg-[#F5F5F5] p-8",
                ),
            ),
        ),
        "My Bookings",
        "Bookings",
        footer=dock_action("Order Equipment", "/contractor/equipment"),
    )


def audit_row(entry: Audit) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            badge(entry["action"]),
            rx.el.time(
                entry["timestamp"].split("T")[0],
                date_time=entry["timestamp"],
                class_name="text-xs text-[#6B6B6B]",
            ),
            class_name="flex flex-wrap items-center justify-between gap-2",
        ),
        rx.el.p(
            entry["note"], class_name="mt-2 text-sm leading-6 text-[#6B6B6B]"
        ),
        class_name="border-b border-[#E5E5EA] py-3 last:border-0",
        key=entry["id"],
    )


def dispute_card(dispute: Dispute) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            f"{dispute['category']} · {dispute['status']}",
            class_name="font-semibold text-red-800",
        ),
        rx.el.p(dispute["description"], class_name="mt-2 text-[#1C1C1E]"),
        rx.cond(
            dispute["resolution"] != "",
            rx.el.p(dispute["resolution"], class_name="mt-2 text-[#6B6B6B]"),
            rx.fragment(),
        ),
        class_name="rounded-xl border border-red-200 bg-red-50 p-4",
        key=dispute["id"],
    )


def cancellation_panel() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Cancel Booking", class_name="mb-2 text-lg font-bold text-[#1C1C1E]"
        ),
        rx.el.p(
            "This action releases the assigned equipment and cannot be undone.",
            class_name="mb-4 text-[#6B6B6B]",
        ),
        rx.el.form(
            field("Cancellation reason", "reason", ""),
            rx.el.label(
                rx.el.input(
                    id="cancel-confirm",
                    type="checkbox",
                    name="confirm",
                    required=True,
                    class_name="h-6 w-6 shrink-0 accent-[#FFB400]",
                ),
                "I confirm cancellation of this booking.",
                html_for="cancel-confirm",
                class_name="flex min-h-12 items-center gap-3 text-[#1C1C1E]",
            ),
            rx.el.div(
                rx.el.button(
                    "Keep booking",
                    type="button",
                    on_click=SharedState.close_action,
                    class_name=SECONDARY,
                ),
                rx.el.button(
                    "Confirm cancellation",
                    type="submit",
                    class_name="min-h-12 rounded-xl bg-red-700 px-4 py-2 font-semibold text-white hover:bg-red-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-700",
                ),
                class_name="flex flex-wrap gap-3",
            ),
            on_submit=SharedState.cancel_booking,
            class_name="flex flex-col gap-4",
        ),
        class_name="rounded-xl border-2 border-red-200 bg-white p-4",
    )


def report_panel() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Report an Issue",
            class_name="mb-4 text-lg font-bold text-[#1C1C1E]",
        ),
        rx.el.form(
            select_field(
                "Issue type",
                "category",
                ["Breakdown", "Delay", "Safety", "Billing", "Other"],
            ),
            rx.el.div(
                rx.el.label(
                    "What happened?",
                    html_for="description",
                    class_name="mb-2 block font-semibold text-[#1C1C1E]",
                ),
                rx.el.textarea(
                    id="description",
                    name="description",
                    required=True,
                    min_length=10,
                    max_length=1000,
                    rows=4,
                    placeholder="Describe the issue and site conditions…",
                    class_name="w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    "Back",
                    type="button",
                    on_click=SharedState.close_action,
                    class_name=SECONDARY,
                ),
                rx.el.button(
                    "Submit issue", type="submit", class_name=SECONDARY
                ),
                class_name="flex gap-3",
            ),
            on_submit=SharedState.report_issue,
            class_name="flex flex-col gap-4",
        ),
        class_name=CARD,
    )


def start_card() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Verify Arrival PIN", class_name="text-xl font-bold text-[#1C1C1E]"
        ),
        rx.el.p(
            "Share this code with the assigned operator only after checking site arrival.",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.div(
            rx.foreach(
                SharedState.current_booking["start_pin"].split(""),
                lambda digit: rx.el.span(
                    digit,
                    class_name="flex h-16 w-14 items-center justify-center rounded-xl border-2 border-[#FFB400] bg-[#F5F5F5] text-4xl font-bold text-[#1C1C1E]",
                ),
            ),
            aria_label=f"Start PIN {SharedState.current_booking['start_pin']}",
            class_name="my-6 flex justify-center gap-3",
        ),
        rx.el.form(
            rx.el.label(
                rx.el.input(
                    type="checkbox",
                    name="arrival_confirmed",
                    id="arrival-confirmed",
                    required=True,
                    class_name="mt-1 h-6 w-6 shrink-0 accent-[#FFB400]",
                ),
                "Equipment and operator are on site; I have checked safe access.",
                html_for="arrival-confirmed",
                class_name="flex items-start gap-3 text-left text-[#1C1C1E]",
            ),
            id="start-form",
            on_submit=SharedState.confirm_start,
        ),
        rx.el.p(
            "Demo shortcut · This confirmation starts the same shift as Operator code verification. Share the code only after checking arrival and safe access. Not production authentication.",
            class_name="mt-4 text-sm text-[#6B6B6B]",
        ),
        class_name="rounded-xl border border-[#FFB400] bg-white p-4 text-center sm:p-6",
    )


def end_card() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "End-code handoff", class_name="text-xl font-bold text-[#1C1C1E]"
        ),
        rx.el.p(
            "Inspect the work, then share this code with the assigned operator.",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.el.p(
            SharedState.current_booking["end_pin"],
            aria_label=f"End code {SharedState.current_booking['end_pin']}",
            class_name="my-6 rounded-xl border-2 border-[#FFB400] bg-[#F5F5F5] py-4 text-center text-4xl font-bold tracking-[4px] text-[#1C1C1E]",
        ),
        rx.el.form(
            rx.el.label(
                rx.el.input(
                    type="checkbox",
                    id="end-confirmed",
                    name="end_confirmed",
                    required=True,
                    class_name="mt-1 h-6 w-6 shrink-0 accent-[#FFB400]",
                ),
                "I have inspected the work and handed over the end code.",
                html_for="end-confirmed",
                class_name="flex items-start gap-3 text-[#1C1C1E]",
            ),
            on_submit=SharedState.confirm_end,
            id="end-form",
        ),
        rx.el.p(
            "Demo shortcut · Inspection confirmation completes the same shift as Operator end-code verification. No payment is processed.",
            class_name="mt-4 text-sm text-[#6B6B6B]",
        ),
        class_name="rounded-xl border border-[#FFB400] bg-white p-4 sm:p-6",
    )


def live_controls() -> rx.Component:
    return rx.match(
        SharedState.current_booking["status"],
        ("arrived", start_card()),
        ("awaiting_end", end_card()),
        (
            "working",
            rx.el.section(
                rx.icon("hard-hat", class_name="mb-3 h-8 w-8 text-orange-800"),
                rx.el.h2(
                    "Work in progress",
                    class_name="text-xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    f"Scheduled shift · {SharedState.current_booking['hours']} hours",
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    "Request an end handoff once the site work is ready for inspection.",
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
        ),
        (
            "completed",
            rx.el.section(
                rx.icon(
                    "circle-check", class_name="mb-3 h-8 w-8 text-green-800"
                ),
                rx.el.h2(
                    "Shift completed",
                    class_name="text-xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    "The work handoff is recorded. The amount below is a demo estimate, not a payment receipt.",
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
        ),
        rx.el.section(
            rx.el.h2(
                SharedState.status_label,
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            rx.el.p(
                rx.match(
                    SharedState.current_booking["status"],
                    (
                        "pending_provider",
                        "Your request is waiting for the provider to review equipment availability.",
                    ),
                    (
                        "pending_approval",
                        "The booking is waiting for municipal review.",
                    ),
                    (
                        "approved",
                        "Officer approval is recorded. The provider still needs to allocate vehicles and operators before deployment.",
                    ),
                    (
                        "assigned",
                        "Vehicle and operator details are ready. The arrival PIN is shown once they arrive.",
                    ),
                    (
                        "in_transit",
                        "The assigned operator is on the way. This demo does not track GPS or estimate a live arrival time.",
                    ),
                    (
                        "problem",
                        "An issue is recorded for review. Check the issue details below.",
                    ),
                    "Check the booking details and recorded reason below.",
                ),
                class_name="mt-2 text-[#6B6B6B]",
            ),
            class_name=CARD,
        ),
    )


def booking_content(execution: bool = False) -> rx.Component:
    return rx.el.div(
        feedback_message(),
        error_message(),
        rx.el.div(
            badge(SharedState.current_booking["status"]),
            rx.el.p(
                SharedState.current_booking["id"],
                class_name="text-sm font-bold text-[#6B6B6B]",
            ),
            class_name="flex flex-wrap items-center justify-between gap-2",
        ),
        rx.cond(execution, live_controls(), rx.fragment()),
        acceptance_summary(SharedState.current_booking),
        rx.el.section(
            rx.el.h2(
                "Equipment & Schedule",
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            rx.foreach(SharedState.current_booking["lines"], review_line),
            rx.el.p(
                SharedState.current_booking["date"],
                class_name="mt-4 font-semibold text-[#1C1C1E]",
            ),
            rx.el.p(
                SharedState.current_booking["shift"],
                class_name="mt-1 text-[#6B6B6B]",
            ),
            rx.el.div(
                rx.el.span("Estimated total", class_name="text-[#6B6B6B]"),
                rx.el.p(
                    f"₹{SharedState.current_booking['total']:,.2f}",
                    class_name="text-xl font-bold text-[#1C1C1E]",
                ),
                class_name="mt-4 flex flex-wrap justify-between gap-2 border-t border-[#E5E5EA] pt-4",
            ),
            class_name=CARD,
        ),
        rx.el.section(
            rx.el.h2(
                "Site & Work Order",
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            rx.el.p(
                SharedState.current_booking["address"],
                class_name="mt-3 text-[#1C1C1E]",
            ),
            rx.el.p(
                f"Ward {SharedState.current_booking['ward']} · {SharedState.current_booking['latitude']}, {SharedState.current_booking['longitude']}",
                class_name="mt-2 text-sm text-[#6B6B6B]",
            ),
            rx.el.p(
                SharedState.current_booking["work_order"],
                class_name="mt-4 font-semibold text-[#1C1C1E]",
            ),
            class_name=CARD,
        ),
        rx.el.section(
            rx.el.h2(
                "Vehicle & Operator",
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            rx.cond(
                SharedState.assigned_people.length() > 0,
                rx.foreach(
                    SharedState.assigned_people,
                    lambda person: rx.el.div(
                        rx.el.p(
                            person["equipment"],
                            class_name="font-bold text-[#1C1C1E]",
                        ),
                        rx.el.p(
                            person["vehicle"], class_name="mt-1 text-[#6B6B6B]"
                        ),
                        rx.el.p(
                            person["operator"],
                            class_name="mt-2 font-semibold text-[#1C1C1E]",
                        ),
                        class_name="border-b border-[#E5E5EA] py-4 last:border-0",
                        key=person["id"],
                    ),
                ),
                rx.el.p("Assignment pending", class_name="mt-3 text-[#6B6B6B]"),
            ),
            class_name=CARD,
        ),
        rx.cond(
            SharedState.current_booking["reason"] != "",
            rx.el.section(
                rx.el.h2(
                    "Recorded reason", class_name="font-bold text-[#1C1C1E]"
                ),
                rx.el.p(
                    SharedState.current_booking["reason"],
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
            rx.fragment(),
        ),
        rx.cond(
            SharedState.booking_disputes.length() > 0,
            rx.el.section(
                rx.el.h2(
                    "Reported issues",
                    class_name="mb-3 text-lg font-bold text-[#1C1C1E]",
                ),
                rx.foreach(SharedState.booking_disputes, dispute_card),
                class_name="flex flex-col gap-3",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.cond(
                SharedState.can_report,
                rx.el.button(
                    rx.icon("triangle-alert", class_name="h-5 w-5"),
                    "Report issue",
                    on_click=lambda: SharedState.open_action("report"),
                    class_name=SECONDARY,
                ),
                rx.fragment(),
            ),
            rx.cond(
                SharedState.can_cancel,
                rx.el.button(
                    "Cancel booking",
                    on_click=lambda: SharedState.open_action("cancel"),
                    class_name="min-h-12 rounded-xl border border-red-200 bg-white px-4 py-2 font-semibold text-red-700 hover:bg-red-50 focus-visible:outline-2 focus-visible:outline-red-700",
                ),
                rx.fragment(),
            ),
            class_name="flex flex-wrap gap-3",
        ),
        rx.match(
            SharedState.action_panel,
            ("cancel", cancellation_panel()),
            ("report", report_panel()),
            rx.fragment(),
        ),
        rx.el.details(
            rx.el.summary(
                "Booking history · Sample evidence",
                class_name="min-h-12 cursor-pointer py-3 font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
            ),
            rx.el.ol(
                rx.foreach(SharedState.booking_audit, audit_row),
                class_name="list-none",
            ),
            class_name=CARD,
        ),
        class_name="flex w-full flex-col gap-4",
    )


def missing_booking() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Booking not found", class_name="text-xl font-bold text-[#1C1C1E]"
        ),
        rx.el.p(
            "This booking is not available in your demo workspace.",
            class_name="my-4 text-[#6B6B6B]",
        ),
        rx.el.a(
            "Return to bookings",
            href="/contractor/bookings",
            class_name=SECONDARY,
        ),
        class_name=CARD,
    )


def detail_screen() -> rx.Component:
    return shell(
        rx.cond(
            SharedState.current_booking["id"] != "",
            booking_content(),
            missing_booking(),
        ),
        "Booking Details",
        "Bookings",
        back="/contractor/bookings",
        footer=rx.cond(
            SharedState.current_booking["id"] != "",
            rx.cond(
                SharedState.current_booking["status"] == "draft",
                rx.el.div(
                    rx.el.button(
                        "Continue draft",
                        rx.icon("arrow-right", class_name="h-5 w-5"),
                        on_click=lambda: SharedState.resume_draft(
                            SharedState.current_booking["id"]
                        ),
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
                dock_action(
                    "View booking status",
                    f"/contractor/bookings/{SharedState.current_booking['id']}/live",
                ),
            ),
            rx.fragment(),
        ),
    )


def live_screen() -> rx.Component:
    return shell(
        rx.cond(
            SharedState.current_booking["id"] != "",
            booking_content(True),
            missing_booking(),
        ),
        "Live Booking",
        "Bookings",
        back=f"/contractor/bookings/{SharedState.current_booking['id']}",
        footer=rx.match(
            SharedState.current_booking["status"],
            (
                "arrived",
                rx.el.div(
                    rx.el.button(
                        "Confirm & Start Work",
                        rx.icon("play", class_name="h-5 w-5"),
                        type="submit",
                        form="start-form",
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            (
                "working",
                rx.el.div(
                    rx.el.button(
                        "Request End-code Handoff",
                        on_click=SharedState.request_end,
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            (
                "awaiting_end",
                rx.el.div(
                    rx.el.button(
                        "Confirm End Handoff",
                        type="submit",
                        form="end-form",
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            rx.fragment(),
        ),
    )


def profile_screen() -> rx.Component:
    return shell(
        rx.el.div(
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Contractor · Demo identity",
                            class_name="mb-2 text-sm font-semibold text-[#6B6B6B]",
                        ),
                        rx.el.h2(
                            SharedState.contractor_identity["company"],
                            class_name="text-2xl font-bold leading-8 text-[#1C1C1E]",
                        ),
                        rx.el.p(
                            SharedState.contractor_identity["name"],
                            class_name="mt-3 font-semibold text-[#1C1C1E]",
                        ),
                    ),
                    rx.icon(
                        "building-2",
                        class_name="h-8 w-8 shrink-0 text-[#6B6B6B]",
                    ),
                    class_name="flex justify-between gap-4",
                ),
                rx.el.p(
                    SharedState.contractor_identity["phone"],
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    SharedState.contractor_identity["email"],
                    class_name="mt-1 break-all text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.p(
                        "Active Tasks",
                        class_name="text-sm font-semibold text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        SharedState.active_count,
                        class_name="mt-2 text-4xl font-bold text-[#1C1C1E]",
                    ),
                    href="/contractor/bookings",
                    on_click=lambda: SharedState.filter_bookings("Active"),
                    class_name="rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 hover:border-[#FFB400] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                ),
                rx.el.a(
                    rx.el.p(
                        "Completed",
                        class_name="text-sm font-semibold text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        SharedState.completed_count,
                        class_name="mt-2 text-4xl font-bold text-[#1C1C1E]",
                    ),
                    href="/contractor/bookings",
                    on_click=lambda: SharedState.filter_bookings("Completed"),
                    class_name="rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 hover:border-[#FFB400] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                ),
                class_name="grid grid-cols-2 gap-4",
            ),
            rx.el.section(
                rx.el.h2(
                    "Demo session",
                    class_name="text-lg font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    "Sample data · Not production authentication",
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    "Logout keeps this session’s bookings for role switching. A full reload resets the demo.",
                    class_name="mt-2 text-sm leading-6 text-[#6B6B6B]",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="h-5 w-5"),
                    "Logout / Switch role",
                    on_click=SharedState.logout,
                    class_name=SECONDARY,
                ),
                class_name="flex flex-col gap-3 rounded-xl border border-[#E5E5EA] bg-white p-4",
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Contractor Profile",
        "Profile",
    )
