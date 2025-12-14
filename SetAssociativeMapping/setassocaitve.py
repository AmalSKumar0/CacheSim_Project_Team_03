import math
import random

class CacheSimulator:
    def __init__(self, cache_size, block_size, associativity):
        
        self.cache_size = cache_size      
        self.block_size = block_size      
        self.associativity = associativity


        self.num_sets = cache_size // (block_size * associativity)
        
        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_sets))
        
        self.sets = [[] for _ in range(self.num_sets)]

        self.hits = 0
        self.misses = 0

    def get_address_parts(self, address):
       
        address_no_offset = address >> self.offset_bits
       
        index_mask = (1 << self.index_bits) - 1
        set_index = address_no_offset & index_mask
        
        tag = address_no_offset >> self.index_bits
        
        return tag, set_index

    def access(self, address):
       
        tag, set_index = self.get_address_parts(address)
        current_set = self.sets[set_index]

       
        if tag in current_set:
            self.hits += 1
            current_set.remove(tag)
            current_set.append(tag)
            return "HIT"

        self.misses += 1
        
       
        if len(current_set) >= self.associativity:
            current_set.pop(0) 
            
        current_set.append(tag) 
        return "MISS"

    def print_stats(self):
        total = self.hits + self.misses
        rate = (self.hits / total) * 100 if total > 0 else 0
        print(f"Total Accesses: {total}")
        print(f"Hits: {self.hits} | Misses: {self.misses}")
        print(f"Hit Rate: {rate:.2f}%")

sim = CacheSimulator(cache_size=1024, block_size=64, associativity=2)

print(f"Config: {sim.num_sets} Sets, {sim.associativity}-Way")

addresses = [
    0x0000, 
    0x0040,
    0x0000,
    0x0080, 
    0x00C0, 
    0x0000, 
]

for addr in addresses:
    result = sim.access(addr)
    tag, idx = sim.get_address_parts(addr)
    print(f"Addr: {hex(addr)} | Set: {idx} | Tag: {tag} -> {result}")

sim.print_stats()