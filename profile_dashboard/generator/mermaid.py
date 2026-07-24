def generate_mermaid_diagram(projects_data):
    lines = [
        "```mermaid",
        "graph TD",
        "  classDef default fill:#0b0e14,stroke:#30363d,stroke-width:1px,color:#c9d1d9;",
        "  classDef active fill:#0b0e14,stroke:#00f0ff,stroke-width:2px,color:#00f0ff;"
    ]
    
    nodes = set()
    links = []
    
    featured = projects_data.get("featured_projects", [])
    for project in featured:
        name = project.get("name")
        sanitized_name = name.replace("-", "_")
        # Handle custom emojis in names if needed
        nodes.add(f"  {sanitized_name}[{name}]:::default")
        
        relations = project.get("relations", {})
        parent = relations.get("parent", "")
        children = relations.get("children", [])
        
        if parent:
            parent_sanitized = parent.replace("-", "_")
            links.append(f"  {parent_sanitized} --> {sanitized_name}")
            
        for child in children:
            child_sanitized = child.replace("-", "_")
            nodes.add(f"  {child_sanitized}[{child}]:::default")
            links.append(f"  {sanitized_name} --> {child_sanitized}")
            
    for node in sorted(nodes):
        lines.append(node)
        
    for link in sorted(list(set(links))):
        lines.append(link)
        
    if featured:
        flagship_sanitized = featured[0].get("name").replace("-", "_")
        lines.append(f"  class {flagship_sanitized} active;")
        
    lines.append("```")
    return "\n".join(lines)
