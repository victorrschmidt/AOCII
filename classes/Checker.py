from pathlib import Path

# Tamanho máximo da cache (em bytes)
MAX_CACHE_SIZE = 2**30

class Checker:
    @staticmethod
    def is_power_of_two(n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
    @staticmethod
    def format_number(n: str) -> str:
        return f"{n:,}".replace(',', '.')
    @staticmethod
    def valid_argc(argc: int) -> None:
        if argc != 2 and argc != 4 and argc != 5:
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
