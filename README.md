# Simulador de Cache

# Como utilizar

## Passo 1
Instale o programa através do comando git clone:

```bash
git clone https://github.com/victorrschmidt/AOCII.git
```

Em seguida, entre no diretório do projeto que contém o arquivo:

```bash
main.py
```

## Passo 2
Insira a sequência de acessos a memória (um endereço por linha) no arquivo:

```bash
in.txt
```

## Passo 3
O programa pode executar de três formas:

### Forma 1 (padrão)
O programa roda com uma cache L1 de instruções e uma cache L1 de dados, com as
configurações padrão.

```bash
py main.py in.txt
```

sendo equivalente a:
```bash
py main.py 64:32:1 64:32:1 in.txt
```

### Forma 2 (somente L1)
O programa roda com uma cache L1 de instruções e uma cache L1 de dados, com as
configurações definidas nos argumentos. A primeira cache é a de instruções e a
segunda cache é a de dados. Exemplo:

```bash
py main.py 128:16:2 256:32:4 in.txt
```

### Forma 3 (L1 e L2)
O programa roda com uma cache L1 de instruções, uma cache L1 de dados e com uma
cache L2 mista. As configurações das caches são definidas nos argumentos. A
primeira cache é a de instruções, a segunda cache é a de dados e a terceira
cache é a cache L2 mista. Exemplo:

```bash
py main.py 128:16:2 256:32:4 512:64:4 in.txt
```
