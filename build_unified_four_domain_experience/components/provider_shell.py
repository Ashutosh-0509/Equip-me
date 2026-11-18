import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import nav_tab, error_message, feedback_message
from build_unified_four_domain_experience.states.shared_state import SharedState


def provider_shell(
    content: rx.Component,
    title: str,
    active: str = "Requests",
    footer: rx.Component = rx.fragment(),
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            (SharedState.role == "Provider")
            & (SharedState.identity_id == "provider-1"),
            rx.el.div(
                rx.el.header(
                    rx.el.div(
                        rx.icon(
                            "truck",
                            class_name="h-6 w-6 shrink-0 text-[#1C1C1E]",
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
                    rx.el.p(
                        SharedState.provider_identity["company"],
                        class_name="border-t border-[#E5E5EA] py-2 text-sm font-semibold text-[#6B6B6B]",
                    ),
                    class_name="shrink-0 border-b border-[#E5E5EA] bg-white px-4 md:px-8",
                ),
                rx.el.main(
                    rx.el.div(
                        feedback_message(),
                        error_message(),
                        content,
                        class_name="flex w-full flex-col gap-4",
                    ),
                    class_name="min-h-0 w-full min-w-0 flex-1 overflow-y-auto overscroll-contain p-4 pb-8 md:p-8",
                ),
                rx.el.div(footer, class_name="shrink-0 bg-white px-4 md:px-8"),
                rx.el.nav(
                    nav_tab("Requests", "clipboard-list", "/provider", active),
                    nav_tab(
                        "Schedule",
                        "calendar-days",
                        "/provider/schedule",
                        active,
                    ),
                    nav_tab("Fleet", "truck", "/provider/fleet", active),
                    nav_tab(
                        "Profile", "user-round", "/provider/profile", active
                    ),
                    aria_label="Provider navigation",
                    class_name="flex shrink-0 border-t border-[#E5E5EA] bg-white pb-[env(safe-area-inset-bottom)]",
                ),
                class_name="mx-auto flex h-full w-full max-w-5xl flex-col border-x border-[#E5E5EA] bg-white",
            ),
            rx.el.p(
                "Opening demo session…",
                role="status",
                class_name="flex h-full items-center justify-center text-[#6B6B6B]",
            ),
        ),
        class_name="h-dvh w-full overflow-hidden bg-[#F5F5F5] font-['Noto_Sans'] text-base text-[#1C1C1E] selection:bg-[#FFB400]",
    )
