import random

class DirectMappedCache:
    """
    Simulates a Direct Mapped Cache.
    Main memory addresses are mapped directly to a single cache line index.
    """

    def __init__(self, cache_size, block_size, main_memory_size):
        """
        Initializes the cache parameters and structures.

        Args:
            cache_size (int): Total size of the cache (in bytes).
            block_size (int): Size of one cache line/block (in bytes).
            main_memory_size (int): Total size of the main memory (in bytes).
        """
        self.cache_size = cache_size
        self.block_size = block_size
        self.main_memory_size = main_memory_size

        # Number of lines in the cache
        self.num_cache_lines = cache_size // block_size

        # Initialize the cache structure: a list of dictionaries
        # Each entry stores the 'valid' bit, 'tag', and 'data' (simulated)
        self.cache = [
            {'valid': 0, 'tag': -1, 'data': None}
            for _ in range(self.num_cache_lines)
        ]

        # Statistics
        self.hits = 0
        self.misses = 0

        # Calculate bit requirements for address partitioning
        # Assuming byte-addressable memory for simplicity
        # Block Offset (W): log2(block_size)
        # Index (I): log2(num_cache_lines)
        # Tag (T): Total_Address_Bits - Index_Bits - Block_Offset_Bits
        # For this simulation, we'll use integer arithmetic based on the calculated sizes
        print(f"--- Cache Configuration ---")
        print(f"Cache Size: {cache_size} bytes")
        print(f"Block Size: {block_size} bytes")
        print(f"Number of Cache Lines (I): {self.num_cache_lines}")
        print(f"Main Memory Size: {main_memory_size} bytes")
        print("---------------------------\n")

    def _address_partitioning(self, address):
        """
        Partitions the memory address into Tag, Index, and Block Offset.
        The block offset is ignored for this simple block-level mapping simulation.

        Address = [ Tag | Index | Block Offset ]
        """
        if address >= self.main_memory_size:
            raise ValueError("Address is outside of Main Memory range.")

        # 1. Calculate the Block Number (which block in main memory)
        block_number_in_memory = address // self.block_size

        # 2. Calculate the Cache Index (I): (Block Number) MOD (Number of Cache Lines)
        cache_index = block_number_in_memory % self.num_cache_lines

        # 3. Calculate the Tag (T): (Block Number) DIV (Number of Cache Lines)
        # This is equivalent to block_number_in_memory // self.num_cache_lines
        tag = block_number_in_memory // self.num_cache_lines

        return tag, cache_index

    def access_memory(self, address):
        """
        Simulates an access to the given memory address (read operation).
        """
        try:
            tag, cache_index = self._address_partitioning(address)
        except ValueError as e:
            print(f"ERROR: {e}")
            return

        cache_line = self.cache[cache_index]

        print(f"Accessing Address: {address} -> [Tag: {tag}, Index: {cache_index}]")

        # --- Check for CACHE HIT ---
        # A hit occurs if the line is valid AND the tag matches the requested tag.
        if cache_line['valid'] == 1 and cache_line['tag'] == tag:
            self.hits += 1
            print(f"  ✅ HIT! Data retrieved: {cache_line['data']}")
            return True

        # --- CACHE MISS ---
        else:
            self.misses += 1
            print(f"  ❌ MISS. Need to fetch block from Main Memory.")

            # 1. Fetch data from Main Memory (simulated fetch)
            # We use the address as the simulated data content for simplicity
            fetched_data = f"Data_for_Block_at_{address // self.block_size}"

            # 2. Write the new block into the cache line
            cache_line['tag'] = tag
            cache_line['valid'] = 1
            cache_line['data'] = fetched_data
            
            print(f"  ---> Block loaded into Cache Index {cache_index}. New Tag: {tag}")
            return False

    def print_stats(self):
        """Prints the simulation statistics."""
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            hit_rate = 0.0
        else:
            hit_rate = (self.hits / total_accesses) * 100

        print("\n=== Simulation Results ===")
        print(f"Total Accesses: {total_accesses}")
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")
        print(f"Hit Rate: {hit_rate:.2f}%")
        print("==========================")

    def print_cache_state(self):
        """Prints the current state of the cache."""
        print("\n--- Current Cache State ---")
        print(f"{'Index':<6} | {'Valid':<6} | {'Tag':<6} | Data")
        print("-" * 30)
        for i, line in enumerate(self.cache):
            data_preview = str(line['data']) if line['data'] else 'None'
            print(f"{i:<6} | {line['valid']:<6} | {line['tag']:<6} | {data_preview}")
        print("---------------------------\n")

# --- Simulation Run ---

# Parameters
CACHE_SIZE = 32  # 32 bytes
BLOCK_SIZE = 8   # 8 bytes per block
MAIN_MEMORY_SIZE = 128 # 128 bytes


dm_cache = DirectMappedCache(CACHE_SIZE, BLOCK_SIZE, MAIN_MEMORY_SIZE)


accesses = [
    0,   # Block 0 -> Index 0. MISS. (T=0, I=0)
    8,   # Block 1 -> Index 1. MISS. (T=0, I=1)
    0,   # Block 0 -> Index 0. HIT. (T=0, I=0)
    16,  # Block 2 -> Index 2. MISS. (T=0, I=2)
    32,  # Block 4 -> Index 0. MISS (Conflict). (T=1, I=0). Block 0 is evicted.
    12,  # Access in Block 1 (Address 8-15). Block 1 -> Index 1. HIT. (T=0, I=1)
    0    # Block 0 -> Index 0. MISS. (T=0, I=0). Block 4 is evicted (Conflict again).
]

print(">>> Starting Memory Access Simulation <<<")
for addr in accesses:
    dm_cache.access_memory(addr)
    #abcd

dm_cache.print_stats()
dm_cache.print_cache_state()