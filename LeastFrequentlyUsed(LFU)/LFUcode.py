def lfu(pages, frames):
    memory = []        
    freq = {}           
    time = {}            
    page_faults = 0
    t = 0               

    for page in pages:
        t += 1
        print(f"\nRequest page: {page}")

        if page in memory:
            freq[page] += 1
            print("-> Hit")
        else:
            page_faults += 1
            print("-> Fault")

            if len(memory) < frames:
                memory.append(page)
            else:
                victim = memory[0]
                for p in memory:
                    if freq[p] < freq[victim]:
                        victim = p
                    elif freq[p] == freq[victim]:
                        if time[p] < time[victim]: 
                            victim = p

                print(f"   Replacing page: {victim}")
                memory[memory.index(victim)] = page
                del freq[victim]
                del time[victim]


            freq[page] = freq.get(page, 0) + 1
            time[page] = t

        print(f"   Memory: {memory}")
        print(f"   Freq:   {freq}")

    print("\nTotal Page Faults:", page_faults)


# Example usage
pages = [1, 2, 3, 2, 4, 1, 5, 2, 1, 2, 3, 4]
frames = 3

lfu(pages, frames)
