import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import CARD
from build_unified_four_domain_experience.states.demo_data import Booking, Line


def acceptance_line(original: Line, booking: Booking) -> rx.Component:
    return rx.el.div(
        rx.el.h3(original["name"], class_name="font-semibold text-[#1C1C1E]"),
        rx.foreach(
            booking["lines"],
            lambda accepted: rx.cond(
                accepted["equipment_id"] == original["equipment_id"],
                rx.el.div(
                    rx.el.p(
                        f"Requested {original['quantity']} · Accepted {accepted['quantity']} · Unfulfilled {original['quantity'] - accepted['quantity']}",
                        class_name="mt-1 text-[#6B6B6B]",
                    ),
                    rx.el.p(
                        f"Unfulfilled estimate ₹{(original['quantity'] - accepted['quantity']) * original['rate'] * original['hours']:,.2f} · ₹{original['rate']:,.2f}/hr per unit",
                        class_name="mt-1 text-sm text-[#6B6B6B]",
                    ),
                ),
                rx.fragment(),
            ),
        ),
        class_name="border-b border-[#E5E5EA] py-3 last:border-0",
    )


def acceptance_summary(booking: Booking) -> rx.Component:
    return rx.cond(
        booking["provider_reviewed"],
        rx.el.section(
            rx.el.h2(
                "Provider acceptance & remainder",
                class_name="text-lg font-bold text-[#1C1C1E]",
            ),
            rx.foreach(
                booking["requested_lines"],
                lambda line: acceptance_line(line, booking),
            ),
            rx.el.p(
                f"Original request ₹{booking['requested_total']:,.2f} · Accepted ₹{booking['total']:,.2f}",
                class_name="mt-3 font-semibold text-[#1C1C1E]",
            ),
            rx.el.p(
                "Unfulfilled units remain recorded for Contractor / Officer review. They are not assigned or billed in the accepted total.",
                class_name="mt-2 text-[#6B6B6B]",
            ),
            class_name=CARD,
        ),
        rx.fragment(),
    )
