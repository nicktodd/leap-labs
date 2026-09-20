# Read this silently for 90 seconds before it's explained.
# What does flag_clients() return, and why?

def flag_clients(trades, min_count=3):
    counts = {}
    for t in trades:
        counts[t["client_name"]] = counts.get(t["client_name"], 0) + 1
    return {name: n for name, n in counts.items() if n >= min_count}


if __name__ == "__main__":
    sample = [
        {"client_name": "Alice Chen"},
        {"client_name": "Ben Whitfield"},
        {"client_name": "Alice Chen"},
        {"client_name": "Alice Chen"},
    ]
    print(flag_clients(sample))
