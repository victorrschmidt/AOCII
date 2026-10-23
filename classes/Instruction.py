class Instruction:
    def __init__(self, line: str):
        try:
            address = int(line)
        except:
            print("ERRO. Endereço de memória inválido.")
            raise
        if address < 2**29:
            self.kind = 'D'
        elif address < 2**32:
            self.kind = 'I'
        else:
            raise ValueError("ERRO. Endereço de memória inválido.")
        self.address = address
