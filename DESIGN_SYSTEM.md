# Design System: AI Operating System

This design system defines the visual language, typography, colors, and components for the developer dashboard of Sukhith M S.

---

## Section 1 — Theme

* **Selected Theme:** AI Operating System (Aesthetic inspired by system kernels, control panels, and terminal consoles).

---

## Section 2 — Color Palette

We derive the feeling of a high-tech operating system console with a dark background and high-contrast accent tones:

* **Primary:** Electric Cyan (`#00f0ff`) - representing energy, active processes, and cognitive focus.
* **Secondary:** Dark Blue/Slate (`#58a6ff`) - representing system architecture and structure.
* **Accent:** Neon Purple (`#d300c5`) - highlighting key interactive nodes and connections.
* **Success:** Emerald Green (`#2ea44f`) - system online, passing tests.
* **Warning:** Amber Gold (`#dbab09`) - attention required, deprecated features.
* **Danger:** Crimson Red (`#ff7b72`) - system failures, issues, blocking tasks.
* **Background:** Deep Space Black (`#0b0e14`) - main background context.
* **Surface:** Terminal Dark Grey (`#161b22`) - component cards and panel backgrounds.

---

## Section 3 — Typography Style

* **Selected Style:** Engineering + Modern
* **Implementation:** Clean modern Sans-serif (like Inter or Outfit) for body copy and headings, combined with Monospaced fonts (like Fira Code or JetBrains Mono) for code elements, stats, and command blocks.

---

## Section 4 — Icon Language

* **Standard Family:** Monochromatic, minimalist devicons and Octicons.
* **Rule:** Avoid mixing 3D icons, flat emoji icons, and colored badge families. Use clean line icons to represent technology stacks and tools.

---

## Section 5 — Motion

* **Typing Animation:** Smooth character-by-character typing SVG animation.
* **Glow/Pulse:** Soft neon-blue/cyan breathing glow effect for online status indicators.
* **Scroll/Interactive:** Standard clean static layout transitions without chaotic animations to keep the dashboard responsive and fast.

---

## Section 6 — Components

The dashboard is built from the following reusable visual structures:

1. **Hero Banner:** OS window style header with terminal mock control buttons.
2. **Status Card:** Real-time indicator box representing the system state (e.g. LLM runtime state).
3. **Project Card:** Two-column HTML grids showing flagship repo specs, unit test coverage, and documentation.
4. **Metric Card:** Clean, custom-themed SVG card showing core GitHub metrics.
5. **Tech Badge:** Cohesive, single-color pill badge showing tool and language proficiencies.
6. **Roadmap Card:** Automated step-by-step progress checklist component.
7. **Footer:** Terminal command-line shell interface with system closing logs.

---

## Section 7 — Dashboard Principles

1. **No unnecessary widgets:** If a widget does not directly demonstrate software engineering or system architecture capabilities, it is rejected.
2. **Every section must add value:** Do not repeat statistics or duplicate content. Keep descriptions brief and dense.
3. **Maximum readability:** Prioritize text contrast and vertical spacing.
4. **Dark theme only:** Color palette is designed specifically for dark environments.
5. **AI Operating System aesthetic:** Frame every personal update as a system event log, kernel statistic, or configuration property.
