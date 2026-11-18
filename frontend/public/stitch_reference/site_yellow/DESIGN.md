---
name: Site Yellow
colors:
  surface: '#fbf9f8'
  surface-dim: '#dbdad9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#efeded'
  surface-container-high: '#e9e8e7'
  surface-container-highest: '#e4e2e2'
  on-surface: '#1b1c1c'
  on-surface-variant: '#514532'
  inverse-surface: '#303031'
  inverse-on-surface: '#f2f0f0'
  outline: '#847560'
  outline-variant: '#d6c4ac'
  surface-tint: '#7e5700'
  primary: '#7e5700'
  on-primary: '#ffffff'
  primary-container: '#ffb400'
  on-primary-container: '#6b4900'
  inverse-primary: '#ffba35'
  secondary: '#5f5e60'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfe1'
  on-secondary-container: '#636264'
  tertiary: '#5d5f5f'
  on-tertiary: '#ffffff'
  tertiary-container: '#c1c2c2'
  on-tertiary-container: '#4e5050'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdeac'
  primary-fixed-dim: '#ffba35'
  on-primary-fixed: '#281900'
  on-primary-fixed-variant: '#5f4100'
  secondary-fixed: '#e4e2e4'
  secondary-fixed-dim: '#c8c6c8'
  on-secondary-fixed: '#1b1b1d'
  on-secondary-fixed-variant: '#474649'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e2'
  surface-base: '#FFFFFF'
  surface-card: '#F5F5F5'
  stroke-card: '#E5E5EA'
  text-primary: '#1C1C1E'
  text-muted: '#6B6B6B'
  status-success: '#1E9E5A'
  status-warning: '#E67E22'
  status-error: '#D93025'
  status-info: '#2563EB'
typography:
  display-code:
    fontFamily: Noto Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: 4px
  headline-lg:
    fontFamily: Noto Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.2px
  headline-md:
    fontFamily: Noto Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-sm:
    fontFamily: Noto Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-md:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  button-text:
    fontFamily: Noto Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.1px
  label-md:
    fontFamily: Noto Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 18px
  label-sm:
    fontFamily: Noto Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system is crafted specifically for civil contractors, municipal supervisors, and on-site construction workers operating under intense direct sunlight, loud environments, and physical fatigue. The brand aesthetic merges industrial utility with modern micro-mobility patterns, evoking the visceral confidence and functional clarity of safety equipment and civil machinery.

### Aesthetic Direction: Industrial Functionalism
- **High Tactical Clarity:** Stark contrast ratios designed to overcome screen glare on active jobsites.
- **Physical Affordance:** Touch targets are oversized, uncrowded, and clearly bordered, prioritizing single-thumb ergonomics for one-handed operation.
- **One Screen, One Job:** Layouts minimize cognitive friction by isolating individual workflow tasks into singular actions anchored by prominent bottom sheets and clear persistent progress indicators.
- **Multilingual Balance:** Designed with flexible vertical spacing and generous horizontal headroom to seamlessly handle linguistic expansion in script-heavy languages such as Marathi and Hindi alongside English.

## Colors

The palette revolves around construction high-visibility safety yellow paired strictly with high-density charcoal typography for guaranteed outdoor readability. White text on yellow accents is strictly prohibited across all viewports and components.

### Application Roles
- **Primary Accent (`#FFB400`):** Reserved exclusively for active touchpoints, primary action buttons, key operational progress indicators, and active selection outlines. Never dilute its impact with decorative overuse.
- **Secondary / Ink (`#1C1C1E`):** Represents high-contrast charcoal for core headlines, primary body text, numerical readouts, and iconography. Acts as the required text color across yellow components.
- **Surfaces & Cards (`#F5F5F5`):** Distinguishes actionable modules, bottom sheets, and summary containers against the clean background canvas (`#FFFFFF`).
- **Borders & Dividers (`#E5E5EA`):** Delivers clean structural boundaries between nested cards without visual noise.
- **Muted Text (`#6B6B6B`):** Secondary metadata, inactive states, auxiliary timestamps, and caption labels.
- **Semantic Accents:** 
  - `status-success` (`#1E9E5A`): Booking approvals, verified arrivals, completed cycles.
  - `status-warning` (`#E67E22`): Active shift timers, pending user inputs, immediate urgency.
  - `status-error` (`#D93025`): Breakdowns, booking terminations, network disconnects.
  - `status-info` (`#2563EB`): Official municipal verifications and status checks.

## Typography

The design system enforces `Noto Sans` across all screen contexts to maintain complete typographical consistency and native legibility across English, Hindi (देवनागरी), and Marathi scripts.

### Typographic Principles
- **Floor Limit:** Standard body text never drops below 16px to protect outdoor scanability under harsh lighting conditions.
- **Vertical Line Metrics:** Increased line heights provide natural headroom for complex conjuncts and diacritics inherent to Indic scripts.
- **High-Impact Numerical Display:** Dedicated `display-code` styling formats critical handoff authentication tokens (such as 4-digit operator verification pins) with wide letter spacing for fast, error-free verbal confirmation.

## Layout & Spacing

Layouts adhere to an Android-first mobile viewport targeting standard 360px to 390px widths. A continuous vertical rhythm based on an 8px spatial grid standardizes touch accessibility.

### Spatial Guidelines
- **Screen Margins:** Fixed at 16px (`1rem`) on left and right borders to maximize screen estate for single-column card hierarchies and multi-select vehicle grids.
- **Vertical Hierarchy:** Standard vertical element gap is 16px (`1rem`), expanding to 24px (`1.5rem`) between unrelated form segments.
- **Primary Bottom Anchors:** Every screen pins critical actions to the lower safe area with an 80px safe clearance zone to protect against system gesture conflicts.
- **Bottom Navigation Clearances:** Bottom navigation surfaces maintain a fixed height of 64px, reserving structural separation from persistent modal bottom sheets.

## Elevation & Depth

Visual hierarchy leverages subtle tonal separation combined with soft, low-contrast ambient shadows rather than harsh drop shadows. This preserves interface lightness and keeps cards looking tactile without creating visual mud.

### Surface Tiers
- **Tier 0 (Base Canvas):** Pure white (`#FFFFFF`) surface backdrop.
- **Tier 1 (Cards & Modular Rows):** Elevated with `#F5F5F5` surface fill, bordered with 1px solid `#E5E5EA`, and cast with an ambient shadow: `box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04)`.
- **Tier 2 (Sticky Headers & Active Cards):** Elevated with a subtle diffused shadow: `box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08)`.
- **Tier 3 (Modals & Bottom Sheets):** Anchored with a robust containment shadow: `box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.12)`, set over a 40% black backdrop overlay (`rgba(0, 0, 0, 0.4)`).

## Shapes

The interface embraces balanced, tactile curvature with consistent edge radii across interactive components.

### Form Dimensions
- **Content Cards & Containers:** Standardized with `16px` border-radius (`rounded-2xl` / `1rem`), delivering a friendly yet industrial container aesthetic.
- **Primary Buttons:** Molded with `12px` border-radius (`rounded-xl` / `0.75rem`) to maintain structural tension across full-width spans.
- **Interactive Form Counters & Inputs:** Sized with `12px` border-radius for clear touch containment.
- **Filter Chips & Status Badges:** Fully rounded pill silhouettes (`rounded-full` / `9999px`) to distinguish actionable metadata from structural surface cards.

## Components

### Buttons
- **Primary Action Button:** Height is strictly `56px`, spans the full content width, and has a background of `#FFB400` with `#1C1C1E` semibold typography (18px). Exactly one primary action is permitted per screen, fixed at the bottom viewport boundary.
- **Secondary / Auxiliary Button:** Height of `48px` to `56px`, styled with a transparent surface, 1.5px stroke in `#E5E5EA` or `#1C1C1E`, and `#1C1C1E` text.
- **Ghost / Cancel Action:** Minimalist, zero-background text link with `#6B6B6B` body text for secondary and non-destructive exits.

### Form Controls & Touch Counters
- **Quantity Steppers (`[-] 1 [+]`):** Designed as an integrated unit of `56px` minimum height. Decrement and increment triggers measure at least `48px × 48px` with clear tactile borders (`#E5E5EA`), bracketing an oversized `20px` bold numerical counter.
- **Selection Chips:** Pill containers with `44px` minimum tap height. Inactive chips use a `#F5F5F5` background with `#6B6B6B` text. Active chips switch to `#FFFFFF` background, `#1C1C1E` bold text, and a crisp `2px` border in `#FFB400`.
- **Text Inputs & Search Fields:** `56px` height, padded with 16px horizontal breathing room, utilizing `#F5F5F5` surface fill, `#E5E5EA` resting border, and transitioning to a `2px` focus ring in `#FFB400`.

### Cards & Vehicle Grid Tiles
- **Vehicle Selection Tiles:** Two-column grid layouts featuring high-contrast mechanical imagery, a bold 16px label, and an optional availability subtext. Selected tiles display a persistent `2px` border in `#FFB400` with a subtle yellow tint layer (`rgba(255, 180, 0, 0.08)`).
- **Status Cards:** Padded with 16px spacing, containing clear state indicators, primary summary metrics, and explicit action links.

### Bottom Navigation Bar
- Fixed at the screen base with a rigid `64px` height above system gesture zones. 
- Features exactly three tabs: **Home**, **Bookings**, and **Profile**.
- Every tab combines a 24px icon with an unambiguous text label underneath in 12px Noto Sans. Active tabs highlight in `#1C1C1E` with a `#FFB400` indicator dot; inactive tabs rest in `#6B6B6B`.

### Status Banners & Verification Codes
- **Operational Banner:** Mounted to top container edges with semantic backgrounds (`#1E9E5A`, `#E67E22`, `#D93025`, `#2563EB`) and bold white typography.
- **Authentication Hand-off Box:** A centered `#F5F5F5` display card presenting oversized 36px 4-digit numeric verification pins with 4px letter tracking for unambiguous site operator sign-offs.