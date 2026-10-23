from .Cache import Cache
from .Instruction import Instruction
from .Checker import Checker
import sys
import time
from pathlib import Path

class Program:
    def __init__(self):
        self.START_TIME = time.perf_counter()
        print("Criando caches...")
        self.argv = sys.argv
        self.argc = len(self.argv)
        Checker.valid_argc(self.argc)
        self.file = Path(self.argv[-1])
        Checker.valid_file(self.file, self.argv[-1])
        self.has_l2 = False
        if self.argc == 2:
            self.icache = Cache()
            self.dcache = Cache()
        else:
            self.icache = Cache(self.argv[1])
            self.dcache = Cache(self.argv[2])
            if self.argc == 5:
                self.l2 = Cache(self.argv[3])
                self.has_l2 = True
        file_content = self.file.read_text().strip().split('\n')
        self.instructions = [Instruction(line) for line in file_content]
        self.acesses = len(self.instructions)
    def run(self):
        print("Processando...")
        for instruction in self.instructions:
            had_miss = False
            if instruction.kind == 'I':
                block = instruction.address // self.icache.bsize
                if not self.icache.has_block(block):
                    had_miss = True
            else:
                block = instruction.address // self.dcache.bsize
                if not self.dcache.has_block(block):
                    had_miss = True
            if self.has_l2 and had_miss:
                block = instruction.address // self.l2.bsize
                self.l2.has_block(block)
        self.END_TIME = time.perf_counter()
        print("\nSimulação finalizada com sucesso!")
        print('-' * 40)
        print(f"Número total de acessos: {Checker.format_number(self.acesses)}")
        print('-' * 40)
        self.icache.debug('CACHE DE INSTRUÇÕES')
        self.dcache.debug('CACHE DE DADOS')
        if self.has_l2:
            self.l2.debug('CACHE L2')
        print(f"Tempo de execução: {str(round(self.END_TIME - self.START_TIME, 2)).replace('.', ',')} segundos")
        print('-' * 40)
