import re


def sanitize_code(code: str):
    if not code:
        return code

    code = re.sub(
        r"import\s+([A-Za-z0-9_]+)from\s+",
        r"import \1 from ",
        code
    )

    code = re.sub(
        r"<textarea([^>]*)/>\s*</textarea>",
        r"<textarea\1></textarea>",
        code
    )

    code = code.replace("```jsx", "").replace("```javascript", "").replace("```", "")

    return code.strip() + "\n"

def sanitize_file_changes(changes: dict):
    sanitized = {}

    for path, content in changes.items():
        sanitized[path] = sanitize_code(content)

    return sanitized