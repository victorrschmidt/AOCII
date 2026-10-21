import sys
import time
import random
from pathlib import Path

# Tamanho máximo da cache (em bytes)
MAX_CACHE_SIZE = 2**30
# Configuração de cache padrão <nsets>:<bsize>:<assoc>
DEFAULT_CACHE_CONFIG = "64:32:1"

# -------------------------------- Verificador --------------------------------

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
            raise ValueError(f"ERRO. O tamanho máximo de cada cache é de {MAX_CACHE_SIZE} B.")
        return [nsets, bsize, assoc]

# -------------------------------- Instrução --------------------------------

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

# -------------------------------- Cache --------------------------------

class BlockSet:
    def __init__(self, assoc: int):
        self.assoc = assoc
        self.blocks = []
        self.index = dict()
    def has(self, block: int) -> bool:
        return block in self.index
    def is_full(self) -> bool:
        return len(self.blocks) == self.assoc
    def insert(self, block: int) -> int:
        self.index[block] = len(self.blocks)
        self.blocks.append(block)
    def remove(self) -> None:
        i = random.randrange(len(self.blocks))
        block = self.blocks[i]
        last_block = self.blocks[-1]
        self.blocks[i] = last_block
        self.index[last_block] = i
        self.blocks.pop()
        del self.index[block]

class CacheSet:
    def __init__(self, nsets: int, bsize: int, assoc: int):
        self.nsets = nsets
        self.bsize = bsize
        self.assoc = assoc
        self.total_size = nsets * bsize * assoc
        self.content = [BlockSet(assoc) for _ in range(nsets)]
    def insert(self, block: int) -> int:
        line = block % self.nsets
        cache = self.content[line]
        if cache.has(block):
            return 0
        else:
            if cache.is_full():
                cache.remove()
            cache.insert(block)
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

# -------------------------------- Programa --------------------------------

class Program:
    def __init__(self):
        self.START_TIME = time.perf_counter()
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
        self.instruction_acesses = 0
        self.instruction_misses = 0
        self.data_acesses = 0
        self.data_misses = 0
    def run(self):
        print("Processando...")
        for instruction in self.instructions:
            if instruction.kind == 'I':
                self.instruction_acesses += 1
                self.instruction_misses += self.cache.insert(instruction.kind, instruction.address)
            else:
                self.data_acesses += 1
                self.data_misses += self.cache.insert(instruction.kind, instruction.address)
        self.END_TIME = time.perf_counter()
        print("\nSimulação finalizada com sucesso!")
        print('-' * 40)
        print(f"Número total de acessos: {Checker.format(self.acesses)}")
        print('-' * 40)
        print('CACHE DE INSTRUÇÕES:')
        print(f"Acessos: {Checker.format(self.instruction_acesses)}")
        print(f"Hits: {Checker.format(self.instruction_acesses - self.instruction_misses)}")
        print(f"Misses: {Checker.format(self.instruction_misses)}")
        print(f"Miss rate: {(self.instruction_misses / self.instruction_acesses * 100):.2f}%")
        print('-' * 40)
        print('CACHE DE DADOS:')
        print(f"Acessos: {Checker.format(self.data_acesses)}")
        print(f"Hits: {Checker.format(self.data_acesses - self.data_misses)}")
        print(f"Misses: {Checker.format(self.data_misses)}")
        print(f"Miss rate: {(self.data_misses / self.data_acesses * 100):.2f}%")
        print('-' * 40)
        print(f"Tempo de execução: {str(round(self.END_TIME - self.START_TIME, 2)).replace('.', ',')} segundos")
        print('-' * 40)

program = Program()
program.run()
