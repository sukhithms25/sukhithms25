# System Architecture

This repository uses a template-based code generation engine to render the profile documentation.

```
profile-dashboard/
├── config/             <-- YAML parameters defining data and theme
├── generator/          <-- Python logic querying GitHub APIs and mapping configurations
└── README.template.md  <-- Layout model with token substitution variables
```
