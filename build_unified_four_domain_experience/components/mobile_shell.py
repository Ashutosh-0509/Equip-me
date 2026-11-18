import reflex as rx

from build_unified_four_domain_experience.states.shared_state import SharedState

PRIMARY = "flex h-14 w-full items-center justify-center gap-2 rounded-xl bg-[#FFB400] px-4 text-lg font-semibold text-[#1C1C1E] transition-colors hover:bg-[#E5A000] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1C1C1E] disabled:cursor-not-allowed disabled:opacity-50"
SECONDARY = "flex min-h-12 items-center justify-center gap-2 rounded-xl border border-[#E5E5EA] bg-white px-4 py-2 font-semibold text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]"
CARD = "rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]"
INPUT = "h-14 w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] px-4 text-base text-[#1C1C1E] placeholder:text-[#6B6B6B] focus:border-[#FFB400] focus:outline-2 focus:outline-[#FFB400]"


def field(
    label: str, name: str, value: str, input_type: str = "text"
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
            type=input_type,
            required=True,
            class_name=INPUT,
        ),
        class_name="w-full",
    )


def select_field(label: str, name: str, options: list[str]) -> rx.Component:
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


def error_message() -> rx.Component:
    return rx.cond(
        SharedState.error != "",
        rx.el.div(
            rx.icon("circle-alert", class_name="h-5 w-5 shrink-0"),
            rx.el.p(SharedState.error),
            role="alert",
            class_name="flex items-start gap-2 rounded-xl bg-red-50 p-4 text-red-800",
        ),
        rx.fragment(),
    )


def feedback_message() -> rx.Component:
    return rx.cond(
        SharedState.feedback != "",
        rx.el.p(
            SharedState.feedback,
            role="status",
            class_name="rounded-xl bg-green-50 p-4 text-green-800",
        ),
        rx.fragment(),
    )


def nav_tab(label: str, icon: str, href: str, active: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-6 w-6"),
        rx.el.span(label, class_name="text-xs"),
        rx.el.span(
            class_name=rx.cond(
                active == label,
                "h-1 w-1 rounded-full bg-[#FFB400]",
                "h-1 w-1 rounded-full bg-transparent",
            )
        ),
        href=href,
        aria_current=rx.cond(active == label, "page", "false"),
        class_name=rx.cond(
            active == label,
            "flex h-16 flex-1 flex-col items-center justify-center gap-1 bg-white font-bold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
            "flex h-16 flex-1 flex-col items-center justify-center gap-1 bg-white font-medium text-[#6B6B6B] hover:text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def shell(
    content: rx.Component,
    title: str,
    active: str = "Home",
    back: str = "",
    footer: rx.Component = rx.fragment(),
    task: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            SharedState.role == "Contractor",
            rx.el.div(
                rx.el.header(
                    rx.el.div(
                        rx.cond(
                            back != "",
                            rx.el.a(
                                rx.icon("arrow-left", class_name="h-6 w-6"),
                                href=back,
                                aria_label="Go back",
                                class_name="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                            ),
                            rx.icon(
                                "construction",
                                class_name="h-6 w-6 shrink-0 text-[#1C1C1E]",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "BMC Heavy Logix",
                                class_name="text-sm font-bold text-[#1C1C1E]",
                            ),
                            rx.el.h1(
                                title,
                                class_name="text-xl font-bold text-[#1C1C1E]",
                            ),
                        ),
                        class_name="flex min-h-16 items-center gap-3",
                    ),
                    rx.cond(
                        task,
                        rx.fragment(),
                        rx.el.p(
                            SharedState.contractor_identity["company"],
                            class_name="border-t border-[#E5E5EA] py-2 text-sm font-semibold text-[#6B6B6B]",
                        ),
                    ),
                    class_name="shrink-0 border-b border-[#E5E5EA] bg-white px-4 md:px-8",
                ),
                rx.el.main(
                    content,
                    class_name="min-h-0 w-full flex-1 overflow-y-auto overscroll-contain p-4 pb-8 md:p-8",
                ),
                rx.el.div(footer, class_name="shrink-0 bg-white px-4 md:px-8"),
                rx.cond(
                    task,
                    rx.fragment(),
                    rx.el.nav(
                        nav_tab("Home", "house", "/contractor", active),
                        nav_tab(
                            "Bookings",
                            "calendar-days",
                            "/contractor/bookings",
                            active,
                        ),
                        nav_tab(
                            "Profile",
                            "user-round",
                            "/contractor/profile",
                            active,
                        ),
                        aria_label="Contractor navigation",
                        class_name="flex shrink-0 border-t border-[#E5E5EA] bg-white",
                    ),
                ),
                class_name="mx-auto flex h-full w-full max-w-5xl flex-col border-x border-[#E5E5EA] bg-white",
            ),
            rx.el.main(
                rx.el.p(
                    "Opening demo session…",
                    role="status",
                    class_name="text-[#6B6B6B]",
                ),
                class_name="flex h-full items-center justify-center bg-white",
            ),
        ),
        class_name="h-dvh w-full overflow-hidden bg-[#F5F5F5] font-['Noto_Sans'] text-base text-[#1C1C1E] selection:bg-[#FFB400] selection:text-[#1C1C1E]",
    )


def dock_action(label: str, href: str) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            label,
            rx.icon("arrow-right", class_name="h-5 w-5"),
            href=href,
            class_name=PRIMARY,
        ),
        class_name="border-t border-[#E5E5EA] py-4",
    )


def progress(step: int, label: str) -> rx.Component:
    return rx.el.section(
        rx.el.p(
            f"Step {step} of 3: {label}",
            class_name="mb-3 font-semibold text-[#1C1C1E]",
        ),
        rx.el.div(
            rx.foreach(
                [1, 2, 3],
                lambda n: rx.el.div(
                    class_name=rx.cond(
                        n <= step,
                        "h-1.5 rounded-full bg-[#FFB400]",
                        "h-1.5 rounded-full bg-[#E5E5EA]",
                    )
                ),
            ),
            class_name="grid grid-cols-3 gap-2",
        ),
        aria_label="Booking progress",
        class_name="mb-6",
    )


def badge(status: str) -> rx.Component:
    return rx.el.span(
        rx.match(
            status,
            ("draft", "Draft"),
            ("pending_provider", "Awaiting provider"),
            ("pending_approval", "Awaiting approval"),
            ("approved", "Approved · Unassigned"),
            ("assigned", "Assigned"),
            ("in_transit", "On the way"),
            ("arrived", "Arrived"),
            ("working", "Working"),
            ("awaiting_end", "End handoff"),
            ("completed", "Completed"),
            ("rejected", "Rejected"),
            ("cancelled", "Cancelled"),
            ("problem", "Issue reported"),
            "Status pending",
        ),
        class_name=rx.cond(
            (status == "completed") | (status == "arrived"),
            "w-fit rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-800",
            rx.cond(
                (status == "rejected")
                | (status == "cancelled")
                | (status == "problem"),
                "w-fit rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-800",
                rx.cond(
                    (status == "approved")
                    | (status == "assigned")
                    | (status == "in_transit")
                    | (status == "pending_approval"),
                    "w-fit rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-800",
                    "w-fit rounded-full bg-orange-100 px-3 py-1 text-xs font-semibold text-orange-800",
                ),
            ),
        ),
    )
