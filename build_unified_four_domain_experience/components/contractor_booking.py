import reflex as rx

from build_unified_four_domain_experience.components.mobile_shell import (
    CARD,
    INPUT,
    PRIMARY,
    SECONDARY,
    error_message,
    field,
    progress,
    shell,
)
from build_unified_four_domain_experience.states.demo_data import Equipment, Line
from build_unified_four_domain_experience.states.shared_state import SharedState


MAP_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuDHjdS8kjJn-6Y8lBbzifVrxCMrqIqCMFmUKts3Zl-4FjQbQN4VM30xllp1VbbLHtZmvkx30NA4GmPWHwEPOd1q7BbtEfM_RUtO4WWG6G0FhNxcJHfVNHCygXUBTkJKc9zMqSgGo6zl4L_FIwrbQ2pIA6KA_U7MlqM8F8NV4Rsn391sGEI2wlJRUNcsR55p8V9utTUpL6EiWZXo0fj8P0JASfewDw7VxgHrwqX8nA"


def equipment_card(item: Equipment) -> rx.Component:
    return rx.el.article(
        rx.el.img(
            src=item["image"],
            alt=item["name"],
            loading="lazy",
            referrer_policy="no-referrer",
            class_name="mb-3 h-32 w-full rounded-lg bg-[#E5E5EA] object-cover sm:h-44",
        ),
        rx.el.h2(
            item["name"],
            class_name="text-base font-bold leading-6 text-[#1C1C1E]",
        ),
        rx.el.p(
            item["description"],
            class_name="mt-1 flex-1 text-sm leading-5 text-[#6B6B6B]",
        ),
        rx.el.p(
            f"₹{item['rate']:,.2f}/hr",
            class_name="mt-3 font-bold text-[#1C1C1E]",
        ),
        rx.el.button(
            rx.cond(
                SharedState.selected.keys().contains(item["id"]),
                rx.icon("check", class_name="h-4 w-4"),
                rx.icon("plus", class_name="h-4 w-4"),
            ),
            rx.cond(
                SharedState.selected.keys().contains(item["id"]),
                "Added · Remove",
                "Add",
            ),
            on_click=lambda: SharedState.toggle_equipment(item["id"]),
            aria_pressed=SharedState.selected.keys().contains(item["id"]),
            aria_label=f"Add or remove {item['name']}",
            class_name=rx.cond(
                SharedState.selected.keys().contains(item["id"]),
                "mt-3 flex min-h-12 w-full items-center justify-center gap-1 rounded-lg border border-[#FFB400] bg-[#FFF3D1] px-2 text-sm font-semibold text-[#1C1C1E] hover:bg-[#FFE4A3] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
                "mt-3 flex min-h-12 w-full items-center justify-center gap-1 rounded-lg border border-[#E5E5EA] bg-white px-2 text-sm font-semibold text-[#1C1C1E] hover:bg-[#E5E5EA] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
            ),
        ),
        class_name=rx.cond(
            SharedState.selected.keys().contains(item["id"]),
            "flex h-full min-w-0 flex-col rounded-xl border-2 border-[#FFB400] bg-[#FFFBF0] p-3",
            "flex h-full min-w-0 flex-col rounded-xl border-2 border-[#E5E5EA] bg-[#F5F5F5] p-3",
        ),
        key=item["id"],
    )


def category_chip(category: str) -> rx.Component:
    return rx.el.button(
        category,
        type="button",
        on_click=lambda: SharedState.choose_category(category),
        aria_pressed=SharedState.category == category,
        class_name=rx.cond(
            SharedState.category == category,
            "min-h-12 shrink-0 rounded-full border-2 border-[#FFB400] bg-white px-4 text-sm font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "min-h-12 shrink-0 rounded-full border-2 border-[#E5E5EA] bg-[#F5F5F5] px-4 text-sm font-medium text-[#6B6B6B] hover:border-[#6B6B6B] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def catalogue_screen() -> rx.Component:
    return shell(
        rx.el.div(
            rx.el.label(
                "Search equipment",
                html_for="equipment-search",
                class_name="mb-2 block font-semibold text-[#1C1C1E]",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="pointer-events-none absolute left-4 top-4 h-6 w-6 text-[#6B6B6B]",
                ),
                rx.el.input(
                    id="equipment-search",
                    type="search",
                    placeholder="Machinery, tonnage, JCB…",
                    default_value=SharedState.query,
                    on_change=SharedState.search.debounce(500),
                    class_name="h-14 w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] pl-12 pr-4 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
                ),
                class_name="relative mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    [
                        "All",
                        "Earthmoving",
                        "Haulage",
                        "Compaction & RMC",
                        "Cranes",
                    ],
                    category_chip,
                ),
                aria_label="Equipment categories",
                class_name="mb-6 flex gap-2 overflow-x-auto pb-2",
            ),
            error_message(),
            rx.cond(
                SharedState.filtered_equipment.length() > 0,
                rx.el.div(
                    rx.foreach(SharedState.filtered_equipment, equipment_card),
                    class_name="grid grid-cols-2 gap-3 lg:grid-cols-3",
                ),
                rx.el.section(
                    rx.icon(
                        "search-x", class_name="mx-auto h-8 w-8 text-[#6B6B6B]"
                    ),
                    rx.el.h2(
                        "No matching equipment",
                        class_name="mt-4 text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.button(
                        "Clear search & filters",
                        on_click=SharedState.clear_filters,
                        class_name=SECONDARY,
                    ),
                    class_name="flex flex-col items-center gap-4 rounded-xl bg-[#F5F5F5] p-8 text-center",
                ),
            ),
            class_name="w-full",
        ),
        "Equipment catalogue",
        back="/contractor",
        footer=rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"{SharedState.selected_count} units selected",
                    class_name="font-semibold text-[#1C1C1E]",
                ),
                rx.el.p(
                    f"₹{SharedState.hourly_total:,.2f}/hr",
                    class_name="text-sm text-[#6B6B6B]",
                ),
                class_name="mb-3 flex items-center justify-between gap-2",
            ),
            rx.el.button(
                "Proceed to Booking",
                rx.icon("arrow-right", class_name="h-5 w-5"),
                on_click=SharedState.proceed_booking,
                disabled=SharedState.selected_count == 0,
                class_name=PRIMARY,
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )


def quantity_row(line: Line) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h2(line["name"], class_name="font-bold text-[#1C1C1E]"),
            rx.el.p(
                f"₹{line['rate']:,.2f} / hr / unit",
                class_name="mt-1 text-sm text-[#6B6B6B]",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("minus", class_name="h-5 w-5"),
                type="button",
                on_click=lambda: SharedState.change_quantity(
                    line["equipment_id"], -1
                ),
                disabled=line["quantity"] <= 1,
                aria_label=f"Decrease {line['name']} quantity",
                class_name="flex h-12 w-12 items-center justify-center rounded-lg border border-[#E5E5EA] bg-white text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400] disabled:opacity-40",
            ),
            rx.el.span(
                line["quantity"],
                aria_live="polite",
                class_name="w-8 text-center text-xl font-bold text-[#1C1C1E]",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-5 w-5"),
                type="button",
                on_click=lambda: SharedState.change_quantity(
                    line["equipment_id"], 1
                ),
                disabled=line["quantity"] >= 10,
                aria_label=f"Increase {line['name']} quantity",
                class_name="flex h-12 w-12 items-center justify-center rounded-lg border border-[#E5E5EA] bg-white text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400] disabled:opacity-40",
            ),
            class_name="flex shrink-0 items-center gap-1 rounded-xl bg-[#F5F5F5] p-1",
        ),
        class_name="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[#E5E5EA] bg-white p-4",
        key=line["equipment_id"],
    )


def shift_option(shift: str) -> rx.Component:
    return rx.el.button(
        shift,
        type="button",
        aria_pressed=SharedState.draft_shift == shift,
        on_click=lambda: SharedState.choose_shift(shift),
        class_name=rx.cond(
            SharedState.draft_shift == shift,
            "min-h-14 w-full rounded-xl border-2 border-[#FFB400] bg-[#FFF8E6] p-3 text-left font-semibold text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
            "min-h-14 w-full rounded-xl border-2 border-[#E5E5EA] bg-white p-3 text-left font-medium text-[#1C1C1E] hover:bg-[#F5F5F5] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
        ),
    )


def step_one() -> rx.Component:
    return shell(
        rx.el.div(
            progress(1, "Equipment & Schedule"),
            error_message(),
            rx.el.div(
                rx.foreach(SharedState.draft_lines, quantity_row),
                class_name="mb-4 flex flex-col gap-3",
            ),
            rx.el.a(
                "Add or remove equipment",
                href="/contractor/equipment",
                class_name=SECONDARY,
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Booking date",
                        html_for="date",
                        class_name="mb-2 block font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.input(
                        id="date",
                        name="date",
                        type="date",
                        default_value=SharedState.draft_date,
                        key=SharedState.draft_date,
                        min=SharedState.today,
                        required=True,
                        class_name=INPUT,
                    ),
                ),
                rx.el.fieldset(
                    rx.el.legend(
                        "Choose shift",
                        class_name="mb-3 font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.div(
                        rx.foreach(
                            [
                                "Shift A · 08:00–16:00",
                                "Shift B · 16:00–00:00",
                                "Full day · 08:00–20:00",
                            ],
                            shift_option,
                        ),
                        class_name="grid gap-2 md:grid-cols-3",
                    ),
                ),
                rx.el.input(
                    type="hidden",
                    name="shift",
                    default_value=SharedState.draft_shift,
                    key=SharedState.draft_shift,
                ),
                id="schedule-form",
                on_submit=SharedState.save_schedule,
                class_name="mt-6 flex flex-col gap-6",
            ),
            class_name="w-full",
        ),
        "New Booking",
        back="/contractor/equipment",
        task=True,
        footer=rx.el.div(
            rx.el.p(
                f"Estimated subtotal · {SharedState.draft_hours} hours",
                class_name="text-center text-sm text-[#6B6B6B]",
            ),
            rx.el.p(
                f"₹{SharedState.draft_total:,.2f}",
                class_name="mb-3 text-center text-xl font-bold text-[#1C1C1E]",
            ),
            rx.el.button(
                "Choose Site Location",
                rx.icon("arrow-right", class_name="h-5 w-5"),
                type="submit",
                form="schedule-form",
                disabled=SharedState.selected_count == 0,
                class_name=PRIMARY,
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )


def location_preview() -> rx.Component:
    return rx.el.figure(
        rx.el.div(
            rx.el.img(
                src=MAP_IMAGE,
                alt="Reference location illustration of Mumbai; not an interactive or live map",
                referrer_policy="no-referrer",
                class_name="h-48 w-full bg-[#E5E5EA] object-cover opacity-70 md:h-56",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-8 w-8 text-[#1C1C1E]"),
                class_name="absolute left-1/2 top-1/2 flex h-14 w-14 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border-4 border-white bg-[#FFB400]",
            ),
            rx.el.span(
                "Reference preview · Not a live map",
                class_name="absolute bottom-3 left-3 right-3 w-fit rounded-lg bg-white px-3 py-2 text-xs font-semibold text-[#1C1C1E]",
            ),
            class_name="relative overflow-hidden rounded-xl border border-[#E5E5EA] bg-[#F5F5F5]",
        ),
        rx.el.figcaption(
            "Coordinates are entered manually. No location tracking.",
            class_name="mt-2 text-sm text-[#6B6B6B]",
        ),
        class_name="mb-6",
    )


def step_two() -> rx.Component:
    return shell(
        rx.el.div(
            progress(2, "Site Location"),
            error_message(),
            location_preview(),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Site address",
                        html_for="address",
                        class_name="mb-2 block font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.textarea(
                        id="address",
                        name="address",
                        default_value=SharedState.draft_address,
                        key=SharedState.draft_address,
                        required=True,
                        min_length=12,
                        max_length=500,
                        rows=3,
                        class_name="w-full rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4 text-[#1C1C1E] focus:outline-2 focus:outline-[#FFB400]",
                    ),
                ),
                field("BMC ward", "ward", SharedState.draft_ward),
                rx.el.div(
                    field("Latitude", "latitude", SharedState.draft_latitude),
                    field(
                        "Longitude", "longitude", SharedState.draft_longitude
                    ),
                    class_name="grid grid-cols-2 gap-3",
                ),
                field(
                    "Work order / Project",
                    "work_order",
                    SharedState.draft_work_order,
                ),
                id="site-form",
                on_submit=SharedState.save_site,
                class_name="flex flex-col gap-6",
            ),
            class_name="w-full",
        ),
        "New Booking",
        back="/contractor/booking/step-1",
        task=True,
        footer=rx.el.div(
            rx.el.button(
                "Review & Confirm",
                rx.icon("arrow-right", class_name="h-5 w-5"),
                type="submit",
                form="site-form",
                class_name=PRIMARY,
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )


def review_line(line: Line) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(line["name"], class_name="font-semibold text-[#1C1C1E]"),
            rx.el.p(
                f"{line['quantity']} units × {line['hours']} hr × ₹{line['rate']:,.2f}",
                class_name="mt-1 text-sm text-[#6B6B6B]",
            ),
        ),
        rx.el.p(
            f"₹{line['amount']:,.2f}",
            class_name="shrink-0 font-bold text-[#1C1C1E]",
        ),
        class_name="flex flex-wrap items-start justify-between gap-2 border-b border-[#E5E5EA] py-3 last:border-0",
        key=line["equipment_id"],
    )


def step_three() -> rx.Component:
    return shell(
        rx.el.div(
            progress(3, "Review & Confirm"),
            error_message(),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Order Summary",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.a(
                        "Edit",
                        href="/contractor/booking/step-1",
                        aria_label="Edit equipment and schedule",
                        class_name="flex min-h-12 items-center px-3 font-semibold text-[#6B6B6B] hover:text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                    ),
                    class_name="flex items-center justify-between border-b border-[#E5E5EA]",
                ),
                rx.foreach(SharedState.draft_lines, review_line),
                rx.el.div(
                    rx.el.p(
                        SharedState.draft_date,
                        class_name="font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        SharedState.draft_shift,
                        class_name="mt-1 text-[#6B6B6B]",
                    ),
                    class_name="border-t border-[#E5E5EA] pt-4",
                ),
                class_name=CARD,
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Site & Work Order",
                        class_name="text-lg font-bold text-[#1C1C1E]",
                    ),
                    rx.el.a(
                        "Edit",
                        href="/contractor/booking/step-2",
                        aria_label="Edit site location",
                        class_name="flex min-h-12 items-center px-3 font-semibold text-[#6B6B6B] hover:text-[#1C1C1E] focus-visible:outline-2 focus-visible:outline-[#FFB400]",
                    ),
                    class_name="flex items-center justify-between",
                ),
                rx.el.p(
                    SharedState.draft_address, class_name="mt-2 text-[#1C1C1E]"
                ),
                rx.el.p(
                    f"Ward {SharedState.draft_ward} · {SharedState.draft_latitude}, {SharedState.draft_longitude}",
                    class_name="mt-2 text-sm text-[#6B6B6B]",
                ),
                rx.el.p(
                    SharedState.draft_work_order,
                    class_name="mt-4 font-semibold text-[#1C1C1E]",
                ),
                class_name=CARD,
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Estimated total",
                        class_name="font-semibold text-[#1C1C1E]",
                    ),
                    rx.el.p(
                        f"₹{SharedState.draft_total:,.2f}",
                        class_name="text-2xl font-bold text-[#1C1C1E]",
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-2",
                ),
                rx.el.p(
                    "Demo estimate · No payment is collected",
                    class_name="mt-2 text-sm text-[#6B6B6B]",
                ),
                class_name="rounded-xl border border-[#E5E5EA] bg-[#F5F5F5] p-4",
            ),
            rx.el.form(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        id="safety",
                        name="safety",
                        required=True,
                        class_name="mt-1 h-6 w-6 shrink-0 accent-[#FFB400] focus-visible:outline-2 focus-visible:outline-[#1C1C1E]",
                    ),
                    rx.el.span(
                        "I confirm site access, safe working conditions and a responsible site supervisor are ready."
                    ),
                    html_for="safety",
                    class_name="flex min-h-12 items-start gap-3 rounded-xl border border-[#E5E5EA] bg-white p-4 text-[#1C1C1E]",
                ),
                id="review-form",
                on_submit=SharedState.submit_booking,
            ),
            class_name="flex w-full flex-col gap-4",
        ),
        "Review Booking",
        back="/contractor/booking/step-2",
        task=True,
        footer=rx.el.div(
            rx.el.button(
                "Book Now · Pay After Work",
                rx.icon("arrow-right", class_name="h-5 w-5"),
                type="submit",
                form="review-form",
                class_name=PRIMARY,
            ),
            class_name="border-t border-[#E5E5EA] py-4",
        ),
    )
