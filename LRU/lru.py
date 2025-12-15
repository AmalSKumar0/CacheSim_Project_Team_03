def find_lru(time_stamps):
    return time_stamps.index(min(time_stamps))

f = int(input("Enter number of frames: "))
p = int(input("Enter number of pages: "))
pages = list(map(int, input("Enter page reference string: ").split()))
frames = [-1] * f
time_stamps = [0] * f
count = 0
hits = 0
misses = 0

print("\nPage\tCache Content\t\tStatus")
print("-" * 40)

for page in pages:
    count += 1

    # Page Hit
    if page in frames:
        idx = frames.index(page)
        time_stamps[idx] = count
        hits += 1
        status = "HIT"
    else:
        if -1 in frames:
            idx = frames.index(-1)
        else:
            idx = find_lru(time_stamps)

        frames[idx] = page
        time_stamps[idx] = count
        misses += 1
        status = "MISS"

    print(f"{page}\t{frames}\t{status}")

total_references = len(pages)
hit_ratio = hits / total_references

print("\nSummary")
print("-" * 20)
print("Total Hits   :", hits)
print("Total Misses :", misses)
print("Hit Ratio    :", round(hit_ratio, 2))

