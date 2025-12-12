def fifo(pages, frames):
    memory = []
    index = 0          # To track which frame to replace (FIFO)
    page_faults = 0

    for page in pages:
        print(f"\nRequest page: {page}")

        if page in memory:
            print("-> Hit")
        else:
            print("-> Fault")
            page_faults += 1

            if len(memory) < frames:
                memory.append(page)
            else:
                victim = memory[index]
                print(f"   Replacing page: {victim}")

                memory[index] = page
                index = (index + 1) % frames

        print(f"   Memory: {memory}")

    print("\nTotal Page Faults:", page_faults)


# Example usage
pages = [1, 2, 3, 2, 4, 1, 5, 2, 1, 2, 3, 4]
frames = 3

fifo(pages, frames)
