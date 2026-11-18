import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import (
    CARD,
    PRIMARY,
    SECONDARY,
    INPUT,
    badge,
    field,
    select_field,
)
from build_unified_four_domain_experience.components.operator_shell import operator_shell
from build_unified_four_domain_experience.components.operator_clock import elapsed_clock
from build_unified_four_domain_experience.components.contractor import audit_row, dispute_card
from build_unified_four_domain_experience.states.demo_data import Booking
from build_unified_four_domain_experience.states.shared_state import SharedState


def empty_assignment() -> rx.Component:
    return rx.el.section(
        rx.icon("calendar-days", class_name="h-8 w-8 text-[#6B6B6B]"),
        rx.el.h2(
            "No assignment available",
            class_name="text-xl font-bold text-[#1C1C1E]",
        ),
        rx.el.p(
            "Only work assigned to your operator identity appears here. Your provider must allocate approved work before you can begin.",
            class_name="leading-6 text-[#6B6B6B]",
        ),
        rx.el.a(
            "View assignment history",
            href="/operator/history",
            class_name=SECONDARY,
        ),
        class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
    )


def assignment_card() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.p(
                SharedState.operator_current["id"],
                class_name="font-bold text-[#1C1C1E]",
            ),
            badge(SharedState.operator_current["status"]),
            class_name="flex flex-wrap items-center justify-between gap-2",
        ),
        rx.el.p(
            f"{SharedState.operator_current['date']} · {SharedState.operator_current['shift']}",
            class_name="mt-4 font-semibold text-[#1C1C1E]",
        ),
        rx.el.p(
            f"Planned duration · {SharedState.operator_current['hours']} hours",
            class_name="mt-2 text-[#6B6B6B]",
        ),
        rx.foreach(
            SharedState.operator_units,
            lambda unit: rx.el.div(
                rx.icon("truck", class_name="h-6 w-6 shrink-0 text-[#1C1C1E]"),
                rx.el.div(
                    rx.el.p(
                        unit["equipment"], class_name="font-bold text-[#1C1C1E]"
                    ),
                    rx.el.p(unit["vehicle"], class_name="mt-1 text-[#6B6B6B]"),
                    rx.el.p(
                        unit["registration"],
                        class_name="mt-2 font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.p(unit["rate"], class_name="mt-2 text-[#6B6B6B]"),
                    class_name="min-w-0 flex-1",
                ),
                class_name="mt-4 flex gap-3 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
                key=unit["id"],
            ),
        ),
        rx.el.div(
            rx.el.p(
                "Assigned work site", class_name="font-semibold text-[#1C1C1E]"
            ),
            rx.el.p(
                SharedState.operator_current["address"],
                class_name="mt-2 leading-6 text-[#1C1C1E]",
            ),
            rx.el.p(
                f"Ward {SharedState.operator_current['ward']}",
                class_name="mt-2 text-[#6B6B6B]",
            ),
            rx.el.p(
                SharedState.operator_current["work_order"],
                class_name="mt-2 text-[#6B6B6B]",
            ),
            class_name="mt-4 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
        ),
        rx.el.div(
            rx.el.h2(
                "Site supervisor · Contractor",
                class_name="font-semibold text-[#1C1C1E]",
            ),
            rx.el.p(
                SharedState.operator_supervisor["name"],
                class_name="mt-2 font-bold text-[#1C1C1E]",
            ),
            rx.el.p(
                SharedState.operator_supervisor["company"],
                class_name="mt-1 text-[#6B6B6B]",
            ),
            rx.el.p(
                SharedState.operator_supervisor["phone"],
                class_name="mt-2 text-[#6B6B6B]",
            ),
            rx.el.p(
                "Sample contact only · No call or message is transmitted by this demo.",
                class_name="mt-2 text-sm leading-6 text-[#6B6B6B]",
            ),
            class_name="mt-4 border-t border-[#E5E5EA] pt-4",
        ),
        rx.el.p(
            "Lifecycle status is shared for the whole booking. Only your allocated unit is shown here.",
            class_name="mt-4 text-sm leading-6 text-[#6B6B6B]",
        ),
        class_name=CARD,
    )


def assignment_row(booking: Booking) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.p(booking["id"], class_name="font-bold text-[#1C1C1E]"),
            rx.el.p(
                f"{booking['date']} · {booking['shift']}",
                class_name="mt-2 text-[#6B6B6B]",
            ),
            rx.el.p(
                booking["address"],
                class_name="mt-2 line-clamp-2 text-[#6B6B6B]",
            ),
            badge(booking["status"]),
            class_name="flex min-w-0 flex-1 flex-col items-start gap-2 text-left",
        ),
        rx.icon("chevron-right", class_name="h-5 w-5 shrink-0 text-[#6B6B6B]"),
        on_click=lambda: SharedState.open_operator_booking(
            booking["id"], "detail"
        ),
        class_name="flex w-full items-center gap-3 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        key=booking["id"],
    )


def operational_action() -> rx.Component:
    return rx.el.div(
        rx.match(
            SharedState.operator_current["status"],
            (
                "assigned",
                rx.el.button(
                    "Start transit",
                    rx.icon("navigation", class_name="h-5 w-5"),
                    on_click=SharedState.operator_transit,
                    disabled=SharedState.operator_current["date"]
                    != SharedState.today,
                    class_name=PRIMARY,
                ),
            ),
            (
                "in_transit",
                rx.el.button(
                    "I've arrived at site",
                    on_click=SharedState.operator_arrive,
                    class_name=PRIMARY,
                ),
            ),
            (
                "arrived",
                rx.el.button(
                    "Enter start code",
                    on_click=lambda: SharedState.open_operator_booking(
                        SharedState.operator_current["id"], "start"
                    ),
                    class_name=PRIMARY,
                ),
            ),
            (
                "working",
                rx.el.button(
                    "Open live shift",
                    on_click=lambda: SharedState.open_operator_booking(
                        SharedState.operator_current["id"], "shift"
                    ),
                    class_name=PRIMARY,
                ),
            ),
            (
                "awaiting_end",
                rx.el.button(
                    "Enter end handoff code",
                    on_click=lambda: SharedState.open_operator_booking(
                        SharedState.operator_current["id"], "shift"
                    ),
                    class_name=PRIMARY,
                ),
            ),
            rx.fragment(),
        ),
        class_name="border-t border-[#E5E5EA] py-4",
    )


def operator_today_screen() -> rx.Component:
    return operator_shell(
        rx.el.div(
            rx.el.section(
                rx.el.p(
                    "Operator · Demo identity",
                    class_name="text-sm font-semibold text-[#6B6B6B]",
                ),
                rx.el.h2(
                    SharedState.operator_record["name"],
                    class_name="mt-2 text-xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    SharedState.operator_duty,
                    class_name="mt-2 font-semibold text-green-800",
                ),
                rx.el.p(SharedState.today, class_name="mt-2 text-[#6B6B6B]"),
                class_name=CARD,
            ),
            rx.cond(
                SharedState.operator_current["id"] != "",
                assignment_card(),
                empty_assignment(),
            ),
            rx.cond(
                SharedState.operator_current["status"] == "in_transit",
                rx.el.p(
                    "Transit is manually recorded. No GPS tracking, navigation service or live arrival estimate is connected.",
                    class_name="rounded-xl bg-orange-50 p-4 text-orange-800",
                ),
                rx.fragment(),
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Upcoming roster",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.a(
                        "View all",
                        href="/operator/history",
                        class_name=SECONDARY,
                    ),
                    class_name="mb-4 flex flex-wrap items-center justify-between gap-2",
                ),
                rx.cond(
                    SharedState.operator_upcoming.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            SharedState.operator_upcoming, assignment_row
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    rx.el.p(
                        "No further shifts assigned yet.",
                        class_name="text-[#6B6B6B]",
                    ),
                ),
                class_name=CARD,
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Today's Assignment",
        footer=operational_action(),
    )


def keypad() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            rx.cond(
                SharedState.operator_current["status"] == "arrived",
                "Enter start code",
                "Enter end code",
            ),
            class_name="text-xl font-bold text-[#1C1C1E]",
        ),
        rx.el.p(
            rx.cond(
                SharedState.operator_current["status"] == "arrived",
                "Ask the contractor for the start code after arrival and site safety checks. The code is available in their Live Booking screen.",
                "Secure the equipment and ask the contractor to inspect the work before sharing the end code from their Live Booking screen.",
            ),
            class_name="mt-2 leading-6 text-[#6B6B6B]",
        ),
        rx.el.output(
            SharedState.operator_code_display,
            aria_label="Entered four-digit code",
            class_name="my-6 block rounded-xl border-2 border-[#FFB400] bg-[#F5F5F5] py-4 text-center text-4xl font-bold tracking-[16px] text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.foreach(
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "clear",
                    "0",
                    "backspace",
                ],
                lambda key: rx.el.button(
                    rx.cond(
                        key == "backspace",
                        rx.icon("delete", class_name="h-6 w-6"),
                        rx.match(
                            key,
                            ("clear", "Clear"),
                            key,
                        ),
                    ),
                    type="button",
                    aria_label=rx.match(
                        key,
                        ("clear", "Clear code"),
                        ("backspace", "Delete last digit"),
                        f"Digit {key}",
                    ),
                    on_click=lambda: SharedState.operator_key(key),
                    class_name="flex h-14 min-w-12 items-center justify-center rounded-xl border border-[#E5E5EA] bg-white text-xl font-semibold text-[#1C1C1E] hover:bg-[#F5F5F5] active:bg-[#FFB400] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                ),
            ),
            class_name="grid grid-cols-3 gap-2 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-2",
        ),
        rx.cond(
            SharedState.operator_current["status"] == "awaiting_end",
            rx.el.label(
                rx.el.input(
                    id="operator-inspection",
                    name="inspection",
                    type="checkbox",
                    required=True,
                    class_name="h-6 w-6 shrink-0 accent-[#FFB400]",
                ),
                "The contractor has inspected the work, shared the code and equipment is secured.",
                html_for="operator-inspection",
                class_name="mt-4 flex items-start gap-3 text-[#1C1C1E]",
            ),
            rx.fragment(),
        ),
        rx.el.p(
            "Demo code handoff · Not production authentication.",
            class_name="mt-4 text-sm text-[#6B6B6B]",
        ),
        id="operator-code-form",
        on_submit=SharedState.verify_operator_code,
        class_name=CARD,
    )


def verify_dock(label: str) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            label,
            type="submit",
            form="operator-code-form",
            disabled=SharedState.operator_code.length() != 4,
            class_name=PRIMARY,
        ),
        class_name="border-t border-[#E5E5EA] py-4",
    )


def operator_start_screen() -> rx.Component:
    return operator_shell(
        rx.el.div(
            rx.el.a(
                "Back to Today", href="/operator/today", class_name=SECONDARY
            ),
            rx.cond(
                SharedState.operator_current["status"] == "arrived",
                keypad(),
                empty_assignment(),
            ),
            rx.cond(
                SharedState.operator_current["id"] != "",
                assignment_card(),
                rx.fragment(),
            ),
            class_name="flex flex-col gap-4",
        ),
        "Arrived · Start Code",
        footer=rx.cond(
            SharedState.operator_current["status"] == "arrived",
            verify_dock("Verify & Start Work"),
            rx.fragment(),
        ),
    )


def issue_panel() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Report a problem",
            class_name="mb-4 text-xl font-bold text-[#1C1C1E]",
        ),
        rx.el.form(
            select_field(
                "Issue type",
                "category",
                ["Breakdown", "Delay", "Safety", "Other"],
            ),
            rx.el.label(
                "What happened?",
                html_for="operator-description",
                class_name="font-semibold text-[#1C1C1E]",
            ),
            rx.el.textarea(
                id="operator-description",
                name="description",
                required=True,
                min_length=10,
                max_length=1000,
                rows=4,
                class_name="w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
            ),
            rx.el.p(
                "Stop unsafe work and contact site supervision directly. This records a local dispute, not an emergency message. The operational phase remains unchanged.",
                class_name="leading-6 text-[#6B6B6B]",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    type="button",
                    on_click=lambda: SharedState.set_operator_panel(""),
                    class_name=SECONDARY,
                ),
                rx.el.button(
                    "Record issue", type="submit", class_name=SECONDARY
                ),
                class_name="flex flex-wrap gap-2",
            ),
            on_submit=SharedState.operator_report_issue,
            reset_on_submit=False,
            class_name="flex flex-col gap-4",
        ),
        class_name=CARD,
    )


def operator_shift_screen() -> rx.Component:
    return operator_shell(
        rx.cond(
            SharedState.operator_current["id"] != "",
            rx.el.div(
                rx.el.a(
                    "Back to Today",
                    href="/operator/today",
                    class_name=SECONDARY,
                ),
                rx.cond(
                    SharedState.operator_current["started_at"] != "",
                    rx.el.section(
                        badge(SharedState.operator_current["status"]),
                        rx.el.h2(
                            "Elapsed shift time",
                            class_name="mt-4 text-lg font-semibold text-[#1C1C1E]",
                        ),
                        elapsed_clock(),
                        rx.el.p(
                            f"Planned shift · {SharedState.operator_current['hours']} hours",
                            class_name="text-center text-[#6B6B6B]",
                        ),
                        rx.el.p(
                            "Time since the recorded start; not machine telemetry. Frozen when the end handoff is completed.",
                            class_name="mt-4 text-sm leading-6 text-[#6B6B6B]",
                        ),
                        class_name=CARD,
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    SharedState.operator_current["status"] == "awaiting_end",
                    keypad(),
                    rx.fragment(),
                ),
                rx.cond(
                    SharedState.operator_current["status"] == "completed",
                    rx.el.p(
                        "Shift completed · Resources released where no other assignment reserves them. View History for recorded evidence.",
                        class_name="rounded-xl bg-green-50 p-4 text-green-800",
                    ),
                    rx.fragment(),
                ),
                assignment_card(),
                rx.cond(
                    SharedState.operator_can_report,
                    rx.el.button(
                        "Report problem",
                        rx.icon("triangle-alert", class_name="h-5 w-5"),
                        on_click=lambda: SharedState.set_operator_panel(
                            "report"
                        ),
                        class_name=SECONDARY,
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    SharedState.operator_panel == "report",
                    issue_panel(),
                    rx.fragment(),
                ),
                rx.foreach(SharedState.operator_issues, dispute_card),
                class_name="flex flex-col gap-4",
            ),
            empty_assignment(),
        ),
        "Live Shift",
        footer=rx.match(
            SharedState.operator_current["status"],
            (
                "working",
                rx.el.div(
                    rx.el.button(
                        "Shift Complete · Request End Code",
                        on_click=SharedState.operator_request_end,
                        class_name=PRIMARY,
                    ),
                    class_name="border-t border-[#E5E5EA] py-4",
                ),
            ),
            ("awaiting_end", verify_dock("Verify & Complete Shift")),
            ("arrived", operational_action()),
            ("assigned", operational_action()),
            ("in_transit", operational_action()),
            rx.fragment(),
        ),
    )


def history_filter(value: str) -> rx.Component:
    return rx.el.button(
        value,
        on_click=lambda: SharedState.filter_operator_history(value),
        aria_pressed=SharedState.operator_filter == value,
        class_name=rx.cond(
            SharedState.operator_filter == value,
            "min-h-12 rounded-full border-2 border-[#FFB400] bg-white px-4 font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "min-h-12 rounded-full border-2 border-[#E5E5EA] bg-[#F5F5F5] px-4 text-[#6B6B6B] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def operator_history_screen() -> rx.Component:
    return operator_shell(
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["All", "Active", "Completed", "Closed"], history_filter
                ),
                class_name="flex flex-wrap gap-2",
            ),
            rx.el.label(
                "Assignment date",
                html_for="operator-history-date",
                class_name="font-semibold text-[#1C1C1E]",
            ),
            rx.el.input(
                id="operator-history-date",
                type="date",
                default_value=SharedState.operator_date,
                on_change=SharedState.set_operator_date.debounce(500),
                class_name=INPUT,
            ),
            rx.el.button(
                "Clear filters",
                on_click=SharedState.clear_operator_filters,
                class_name=SECONDARY,
            ),
            rx.cond(
                SharedState.operator_history.length() > 0,
                rx.foreach(SharedState.operator_history, assignment_row),
                rx.el.section(
                    rx.el.h2(
                        "No matching assignments",
                        class_name="text-xl font-bold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        "Try clearing the date or status filter. Completed shifts will appear here after their end-code handoff.",
                        class_name="mt-2 leading-6 text-[#6B6B6B]",
                    ),
                    class_name=CARD,
                ),
            ),
            class_name="flex flex-col gap-4",
        ),
        "Assignment History",
        "History",
    )


def operator_detail_screen() -> rx.Component:
    return operator_shell(
        rx.cond(
            SharedState.operator_current["id"] != "",
            rx.el.div(
                rx.el.a(
                    "Back to History",
                    href="/operator/history",
                    class_name=SECONDARY,
                ),
                assignment_card(),
                rx.el.section(
                    rx.el.h2(
                        "Recorded shift · Read only",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        f"Start: {SharedState.operator_current['started_at']}",
                        class_name="mt-4 break-all text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        f"End: {SharedState.operator_current['ended_at']}",
                        class_name="mt-2 break-all text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        SharedState.operator_duration,
                        class_name="mt-4 font-semibold tabular-nums text-[#1C1C1E]",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.el.h2(
                        "Booking audit",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.ol(
                        rx.foreach(SharedState.operator_audit, audit_row),
                        class_name="list-none",
                    ),
                    class_name=CARD,
                ),
                rx.foreach(SharedState.operator_issues, dispute_card),
                class_name="flex flex-col gap-4",
            ),
            empty_assignment(),
        ),
        "Assignment Details",
        "History",
    )


def operator_profile_screen() -> rx.Component:
    return operator_shell(
        rx.el.div(
            rx.el.section(
                rx.el.p(
                    "Operator · Demo identity",
                    class_name="text-sm font-semibold text-[#6B6B6B]",
                ),
                rx.el.h2(
                    SharedState.operator_record["name"],
                    class_name="mt-2 text-2xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    SharedState.operator_company,
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    f"Licence · {SharedState.operator_record['license']}",
                    class_name="mt-4 text-[#1C1C1E]",
                ),
                rx.el.p(
                    f"Availability · {SharedState.operator_record['status']}",
                    class_name="mt-2 text-[#6B6B6B]",
                ),
                rx.el.p(
                    SharedState.operator_duty, class_name="mt-2 text-[#6B6B6B]"
                ),
                rx.el.p(
                    "Availability and licence are controlled by provider allocation. You can update your own contact below.",
                    class_name="mt-4 leading-6 text-[#6B6B6B]",
                ),
                class_name=CARD,
            ),
            rx.el.form(
                field(
                    "Contact number",
                    "phone",
                    SharedState.operator_record["phone"],
                    "tel",
                ),
                rx.el.button(
                    "Save contact", type="submit", class_name=SECONDARY
                ),
                on_submit=SharedState.save_operator_phone,
                class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-white p-4",
            ),
            rx.el.button(
                "Support · Local sample panel",
                on_click=lambda: SharedState.set_operator_panel("support"),
                class_name=SECONDARY,
            ),
            rx.cond(
                SharedState.operator_panel == "support",
                rx.el.section(
                    rx.el.h2(
                        "Demo support",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        "For an assignment issue, use Report problem from the shift screen. For immediate safety concerns, stop work and contact your site supervisor directly.",
                        class_name="mt-2 leading-6 text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        "This is a local guidance panel. No support request, emergency call or message is sent.",
                        class_name="mt-4 leading-6 text-[#6B6B6B]",
                    ),
                    rx.el.button(
                        "Close support",
                        on_click=lambda: SharedState.set_operator_panel(""),
                        class_name=SECONDARY,
                    ),
                    class_name="flex flex-col gap-4 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
                ),
                rx.fragment(),
            ),
            rx.el.p(
                "Logout preserves shared records for demo role switching in this tab. A full reload resets the demo; this is not production authentication.",
                class_name="leading-6 text-[#6B6B6B]",
            ),
            rx.el.button(
                "Logout / Switch role",
                rx.icon("log-out", class_name="h-5 w-5"),
                on_click=SharedState.logout,
                class_name=SECONDARY,
            ),
            class_name="flex flex-col gap-4",
        ),
        "Operator Profile",
        "Profile",
    )
