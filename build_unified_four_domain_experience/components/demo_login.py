import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import PRIMARY
from build_unified_four_domain_experience.states.shared_state import SharedState


def role_option(role: str) -> rx.Component:
    return rx.el.button(
        rx.match(
            role,
            ("Contractor", rx.icon("hard-hat", class_name="h-6 w-6")),
            ("Provider", rx.icon("truck", class_name="h-6 w-6")),
            ("Operator", rx.icon("construction", class_name="h-6 w-6")),
            rx.icon("clipboard-check", class_name="h-6 w-6"),
        ),
        role,
        type="button",
        on_click=lambda: SharedState.select_role(role),
        aria_pressed=SharedState.selected_role == role,
        class_name=rx.cond(
            SharedState.selected_role == role,
            "flex min-h-16 items-center gap-3 rounded-xl border-2 border-[#FFB400] bg-[#FFF8E6] px-4 font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "flex min-h-16 items-center gap-3 rounded-xl border-2 border-[#E5E5EA] bg-[#F5F5F5] px-4 font-medium text-[#1C1C1E] hover:border-[#6B6B6B] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def login_screen() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.header(
                rx.icon(
                    "construction", class_name="mb-4 h-8 w-8 text-[#1C1C1E]"
                ),
                rx.el.h1(
                    "BMC Heavy Logix",
                    class_name="text-2xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    "Demo access · Sample data",
                    class_name="mt-2 text-base text-[#6B6B6B]",
                ),
                class_name="mb-8",
            ),
            rx.el.h2(
                "Choose your workspace",
                class_name="mb-4 text-lg font-semibold text-[#1C1C1E]",
            ),
            rx.el.div(
                rx.foreach(
                    ["Contractor", "Provider", "Operator", "Officer"],
                    role_option,
                ),
                class_name="grid grid-cols-2 gap-3",
            ),
            rx.el.section(
                rx.el.p(
                    SharedState.selected_role,
                    class_name="mb-2 text-sm font-semibold text-[#6B6B6B]",
                ),
                rx.el.h2(
                    SharedState.login_identity["name"],
                    class_name="text-xl font-bold text-[#1C1C1E]",
                ),
                rx.el.p(
                    SharedState.login_identity["company"],
                    class_name="mt-1 text-[#6B6B6B]",
                ),
                rx.el.p(
                    rx.match(
                        SharedState.selected_role,
                        ("Contractor", "Equipment requests & site bookings"),
                        (
                            "Provider",
                            "Requests, fleet, daily schedule & earnings",
                        ),
                        (
                            "Operator",
                            "Today's assignments, live shifts & code handoffs",
                        ),
                        "Municipal reviews, directory, reports & disputes",
                    ),
                    class_name="mt-4 text-sm text-[#6B6B6B]",
                ),
                class_name="my-6 rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
            ),
            rx.el.button(
                rx.match(
                    SharedState.selected_role,
                    ("Contractor", "Enter Contractor workspace"),
                    ("Provider", "Enter Provider workspace"),
                    ("Operator", "Enter Operator workspace"),
                    "Enter Officer workspace",
                ),
                rx.icon("arrow-right", class_name="h-5 w-5 shrink-0"),
                on_click=SharedState.login,
                class_name=PRIMARY,
            ),
            rx.el.p(
                "No password required. Data resets when you reload; switching roles keeps this session’s changes.",
                class_name="mt-4 text-sm leading-6 text-[#6B6B6B]",
            ),
            class_name="mx-auto w-full max-w-lg rounded-2xl border border-[#E5E5EA] bg-white p-4 sm:p-8",
        ),
        class_name="flex min-h-dvh items-center bg-[#F5F5F5] p-4 font-['Noto_Sans'] text-[#1C1C1E]",
    )
