INVALID_CHARS = ('\'', '/', '\0', ':', '|', '*', '?',
                 '<', '>', '\n', '\r', '\t', '"', "'", '\v')


def key_is_valid(key: str) -> bool:
    for l in key:
        if l in INVALID_CHARS:
            return False
        
    return True
