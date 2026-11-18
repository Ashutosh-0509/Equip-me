import reflex as rx

config = rx.Config(
    app_name="build_unified_four_domain_experience",
    default_color_mode="light",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
