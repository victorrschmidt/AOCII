class Instruction:
    def __init__(self, line: str):
        try:
            address = int(line)
        except:
            print(f"ERRO. Endereço de memória inválido: {line}.")
            exit(1)
        if address < 2**29:
            self.kind = 'D'
        elif address < 2**32:
            self.kind = 'I'
        else:
            print(f"ERRO. Endereço de memória inválido: {address}.")
            exit(1)
        self.address = address
