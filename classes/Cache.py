from .Checker import Checker
import random

# Configuração de cache padrão <nsets>:<bsize>:<assoc>
DEFAULT_CACHE_CONFIG = "64:32:1"

class BlockSet:
    def __init__(self, assoc: int):
        self.assoc = assoc
        self.blocks = list()
        self.index = dict()
    def __is_full(self) -> bool:
        return len(self.blocks) == self.assoc
    def __remove(self) -> None:
        i = random.randrange(len(self.blocks))
        block = self.blocks[i]
        last_block = self.blocks[-1]
        self.blocks[i] = last_block
        self.index[last_block] = i
        self.blocks.pop()
        del self.index[block]
    def has(self, block: int) -> bool:
        return block in self.index
    def insert(self, block: int) -> bool:
        miss_type = False  # Compulsório
        if self.__is_full():
            self.__remove()
            miss_type = True  # Conflito
        self.index[block] = len(self.blocks)
        self.blocks.append(block)
        return miss_type

class Cache:
    def __init__(self, cache_config: str=None):
        if cache_config is not None:
            nsets, bsize, assoc = Checker.valid_cache(cache_config)
        else:
            nsets, bsize, assoc = Checker.valid_cache(DEFAULT_CACHE_CONFIG)
        self.nsets = nsets
        self.bsize = bsize
        self.assoc = assoc
        self.content = [BlockSet(assoc) for _ in range(nsets)]
        self.acesses = 0
        self.hits = 0
        self.misses = 0
        self.comp_misses = 0
        self.conf_misses = 0
    def __has(self, block_set: BlockSet, block: int) -> bool:
        return block_set.has(block)
    def __insert(self, block_set: BlockSet, block: int) -> None:
        block_set.insert(block)
    def has_block(self, block: int) -> bool:
        self.acesses += 1
        line = block % self.nsets
        cache = self.content[line]
        if self.__has(cache, block):
            self.hits += 1
            return True
        else:
            miss_type = self.__insert(cache, block)
            self.misses += 1
            if miss_type:
                self.conf_misses += 1
            else:
                self.comp_misses += 1
            return False
    def debug(self, name: str) -> None:
        print(f"{name}:")
        print(f"Acessos: {Checker.format_number(self.acesses)}")
        if self.acesses > 0:
            print(f"Hits: {Checker.format_number(self.hits)}")
            print(f"Misses totais: {Checker.format_number(self.misses)}")
            print(f"Misses compulsórios: {Checker.format_number(self.comp_misses)}")
            print(f"Misses de conflito/capacidade: {Checker.format_number(self.conf_misses)}")
            print(f"Hit rate: {(self.hits / self.acesses * 100):.2f}%")
            print(f"Miss rate: {(self.misses / self.acesses * 100):.2f}%")
        print('-' * 40)
