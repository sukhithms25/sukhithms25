# Statistics Widgets Research

To turn the profile into a "living dashboard," we need live-refreshing widgets. We researched the top tools:

| Widget Name | Creator | Purpose | Customization |
| ----------- | ------- | ------- | ------------- |
| `github-readme-stats` | anuraghazra | Displays overall commits, PRs, stars, and language breakdown | Highly customizable themes, layouts, hides specific stats |
| `github-readme-streak-stats` | DenverCoder1 | Displays current contribution streak, total contributions, and longest streak | Unified themes, card format |
| `github-profile-trophy` | ryo-ma | Gamifies contributions with trophies based on rank (SSS, SS, A, B...) | Theme-aware, grid layouts |
| `github-profile-summary-cards` | vn7n24fzkq | Generates visual SVG charts of repository stats using GitHub Actions | Theme-aware, requires local action execution |

## Theme Coordination
To prevent the "cluttered badge soup" look, we must enforce a strict design rule:
**Every single widget must use the exact same theme configuration.**
- Background: `#0d1117` (GitHub Dark default) or `#0b0e14` (Sleek dark)
- Title Color: `#58a6ff` (Neon blue)
- Text Color: `#c9d1d9` (Slate grey)
- Accent Color: `#ff7b72` or `#2ea44f`
- Hide borders to integrate seamlessly into the page background.\n