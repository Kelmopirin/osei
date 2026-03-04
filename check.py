import re

def check(content):
    """
    Extract available appointment datetime from HTML content.
    Returns datetime string if found, None otherwise.
    """
    # Search for card-time class containing datetime
    # Pattern: <p class="card-time">2026-03-04 17:20</p>
    match = re.search(r'<p class="card-time">([\d\-\s:]+)</p>', content)
    
    if match:
        return match.group(1)
    else:
        return None
    

