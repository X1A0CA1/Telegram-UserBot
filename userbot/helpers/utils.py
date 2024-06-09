def format_time(seconds: float) -> str:
    if seconds < 1e-6:
        return f"{seconds * 1e9:.3f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.3f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.3f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        minutes = seconds / 60
        return f"{minutes:.2f} m"
