import sys
import random
from pathlib import Path

# Tamanho máximo da cache (em bytes)
MAX_CACHE_SIZE = 2**30
# Configuração de cache padrão <nsets>:<bsize>:<assoc>
DEFAULT_CACHE_CONFIG = "64:32:1"

class Checker:
    @staticmethod
    def is_power_of_two(n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
    @staticmethod
    def format(n: str) -> str:
        return f"{n:,}".replace(',', '.')
    @staticmethod
    def valid_argc(argc: int) -> None:
        if argc != 2 and argc != 4:
            raise ValueError("ERRO. Número de argumentos inválido.")
    @staticmethod
    def valid_file(file: Path, filename: str) -> None:
        if not file.exists():
            raise FileNotFoundError(f"ERRO. Arquivo '{filename}' não encontrado.")
    @staticmethod
    def valid_cache(cache_config: str) -> list[int]:
        try:
            nsets, bsize, assoc = [int(x) for x in cache_config.split(':')]
        except:
            print("ERRO. Cache inválida.")
            raise
        if (not Checker.is_power_of_two(nsets) or
            not Checker.is_power_of_two(bsize) or
            not Checker.is_power_of_two(assoc)):
            raise ValueError("ERRO. Os tamanhos de cada campo da cache deve ser uma potência de 2.")
        if nsets * bsize * assoc > MAX_CACHE_SIZE:
            raise ValueError(f"ERRO. O tamanho máximo de cada cache é de {MAX_CACHE_SIZE}B.")
        return [nsets, bsize, assoc]

class Instruction:
    def __init__(self, line: str):
        try:
            kind, address = line.split()
            address = int(address)
        except:
            print("ERRO. Endereço de memória ou tipo de instrução inválido.")
            raise
        if kind != 'I' and kind != 'D':
            raise ValueError("ERRO. Tipo de instrução inválida.")
        if int(address) < 0 or int(address) > 2**32 - 1:
            raise ValueError("ERRO. Endereço de memória inválido.")
        self.kind = kind
        self.address = address

class CacheSet:
    def __init__(self, nsets: int, bsize: int, assoc: int):
        self.nsets = nsets
        self.bsize = bsize
        self.assoc = assoc
        self.total_size = nsets * bsize * assoc
        self.content = [set() for _ in range(nsets)]
    def insert(self, block: int) -> int:
        line = block % self.nsets
        cache = self.content[line]
        if block in cache:
            return 0
        else:
            if len(cache) == self.assoc:
                cache.remove(random.choice(tuple(cache)))
            self.content[line].add(block)
            return 1

class Cache:
    def __init__(self, is_default: bool=True, il1: str=None, dl1: str=None):
        if is_default:
            il1 = DEFAULT_CACHE_CONFIG
            dl1 = DEFAULT_CACHE_CONFIG
        self.icache = CacheSet(*Checker.valid_cache(il1))
        self.dcache = CacheSet(*Checker.valid_cache(dl1))
    def insert(self, kind: str, address: int) -> int:
        if kind == 'I':
            block = address // self.icache.bsize
            return self.icache.insert(block)
        else:
            block = address // self.dcache.bsize
            return self.dcache.insert(block)

class Program:
    def __init__(self):
        print("Criando caches...")
        self.argv = sys.argv
        self.argc = len(self.argv)
        Checker.valid_argc(self.argc)
        self.file = Path(self.argv[-1])
        Checker.valid_file(self.file, self.argv[-1])
        if self.argc == 2:
            self.cache = Cache()
        else:
            self.cache = Cache(False, self.argv[1], self.argv[2])
        file_content = self.file.read_text().strip().split('\n')
        self.instructions = [Instruction(line) for line in file_content]
        self.acesses = len(self.instructions)
        self.misses = 0
    def run(self):
        print("Processando...")
        for instruction in self.instructions:
            self.misses += self.cache.insert(instruction.kind, instruction.address)
        print(f"\nSimulação finalizada com sucesso!\n{'-' * 40}")
        print(f"Número de acessos: {Checker.format(self.acesses)}")
        print(f"Número de hits: {Checker.format(self.acesses - self.misses)}")
        print(f"Número de misses: {Checker.format(self.misses)}")
        print(f"Miss rate: {(self.misses / self.acesses * 100):.2f}%")
        print('-' * 40)

program = Program()
program.run()
