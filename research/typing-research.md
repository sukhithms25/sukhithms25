# Typing Animation Research

Typing animations are highly effective for making the profile feel interactive. We analyzed three main ways developers implement typing text in Markdown.

## Method 1: Animated SVG (Recommended)
Using a service or self-hosted GitHub action that generates a dynamic SVG containing CSS keyframe animations.
* **Tool:** `readme-typing-svg` (by DenverCoder1)
* **Example URL:** `https://readme-typing-svg.herokuapp.com/?lines=AI+Systems+Architect;First-Principles+Coder`
* **Pros:**
  - Works natively in GitHub markdown (SVG images are allowed).
  - Respects dark/light mode.
  - Highly customizable fonts, colors, and delay.
  - Zero performance impact on the client (browser handles SVG CSS).
* **Cons:**
  - Relies on an external Heroku app (can have downtime) unless self-hosted.

## Method 2: Animated GIFs
Creating or generating a custom GIF using local software and uploading it to the repository.
* **Pros:**
  - 100% reliable; no dependency on external hosting.
  - Can include custom terminal mockups or graphical backgrounds.
* **Cons:**
  - Fixed color palette (cannot adapt to GitHub's light/dark mode switch).
  - High file size compared to SVGs, increasing load time.

## Method 3: Markdown Code Blocks with Console Simulation
Using standard markdown code blocks with comments and commands written as text.
* **Pros:**
  - 100% native, zero dependencies.
  - Clean and readable.
* **Cons:**
  - No actual animation. It is static and relies on the user's imagination to read it as a terminal command.

## Selection for ULTRON Dashboard
We will use **Method 1 (Animated SVG)** with a customized theme that matches our dark slate / neon blue palette.
Lines to rotate:
1. `System.load("specter-core")`
2. `Cognition: Active [Local Ollama]`
3. `No Frameworks. First Principles.`\n