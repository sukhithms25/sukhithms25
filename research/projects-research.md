# Featured Projects Layout Research

How you present your repositories determines if a recruiter clicks them. We analyzed 3 layouts:

## Layout A: Standard Repo Cards (Default)
Using `github-readme-stats` repository cards.
* **Pros:** Automated, displays stars and language, updates dynamically.
* **Cons:** Fixed layout, limited text length, look generic.

## Layout B: Custom Grid Tables (Recommended)
Using HTML tables containing customized markdown cells.
* **Structure:**
  ```html
  <table>
    <tr>
      <td><b>Project A</b><br>Description...</td>
      <td><b>Project B</b><br>Description...</td>
    </tr>
  </table>
  ```
* **Pros:** Perfect control over columns, can embed custom icons, screenshots, or badges, very high visual quality.
* **Cons:** Requires manual updating of descriptions.

## Layout C: Architectural Diagrams
Using a visual diagram of the project structure (like a ASCII/Mermaid flow) as the project card.
* **Pros:** Shows deep systems engineering knowledge immediately.
* **Cons:** Takes up significant vertical space.

## Selection for ULTRON Dashboard
We will use **Layout B (Custom Grid Tables)**. We will showcase **ULTRON (Specter Core)** as a flagship project, including:
1. Short first-principles summary.
2. Direct links to the Architecture RFCs.
3. System status badges (e.g. `tests: 274 passed`, `coverage: 98%`).\n