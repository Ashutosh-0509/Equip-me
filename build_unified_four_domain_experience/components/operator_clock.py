import reflex as rx

from build_unified_four_domain_experience.states.shared_state import SharedState


def elapsed_clock() -> rx.Component:
    return rx.el.div(
        "00:00:00",
        id="operator-elapsed",
        custom_attrs={
            "data-started-at": SharedState.operator_current["started_at"],
            "data-ended-at": SharedState.operator_current["ended_at"],
        },
        on_mount=rx.call_script("window.heavyLogixClock?.mount()"),
        on_unmount=rx.call_script("window.heavyLogixClock?.stop()"),
        aria_label="Elapsed time since recorded shift start",
        class_name="my-4 text-center text-4xl font-bold tabular-nums tracking-[4px] text-[#1C1C1E]",
    )
