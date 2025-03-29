def parse_multiple_entries(text, delimiter=','):
    if not text:
        return ""
    
    entries = [entry.strip() for entry in text.split(delimiter) if entry.strip()]
    return "\n".join(f"- [ ] {entry}" for entry in entries)