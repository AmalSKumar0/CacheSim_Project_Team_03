def find_lru(time_stamps, frames):
   
    min_time = min(time_stamps)
    return time_stamps.index(min_time)


frames = []
time_stamps = []
count = 0

f = int(input("Enter number of frames: "))
p = int(input("Enter number of pages: "))

pages = list(map(int, input("Enter page reference string: ").split()))


frames = [-1] * f
time_stamps = [0] * f

faults = 0

print("\nPage\tFrames")

for page in pages:
    count += 1

  
    if page in frames:
        idx = frames.index(page)
        time_stamps[idx] = count

    else:
     
        if -1 in frames:
            idx = frames.index(-1)
            frames[idx] = page
            time_stamps[idx] = count
        else:
            
            idx = find_lru(time_stamps, frames)
            frames[idx] = page
            time_stamps[idx] = count
        
        faults += 1

    
    print(page, "\t", frames)

print("\nTotal Page Faults:", faults)
