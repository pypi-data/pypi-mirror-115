def parse_time_to_sec(s: str) -> int:
    t = list(map(int, s.split(':')))
    return t[0] * 60 + t[1]
