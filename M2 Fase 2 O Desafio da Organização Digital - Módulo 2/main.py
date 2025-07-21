import random
import time
import heapq
from collections import defaultdict

class ModuloBusca:
    def __init__(self):
        self.fragmentos = []
        self.catalogos_ordenados = []
        self.tomos = []
        self.marcas_corrupcao = []

    def gerar_fragmentos_aleatorios(self, quantidade=10000):
        self.fragmentos = [f"FRAG-{random.randint(10000, 99999)}" for _ in range(quantidade)]
        return random.choice(self.fragmentos)

    def busca_sequencial(self, alvo):
        comparacoes = 0
        for i, fragmento in enumerate(self.fragmentos):
            comparacoes += 1
            if fragmento == alvo:
                return i, comparacoes
        return -1, comparacoes

    def gerar_catalogos_ordenados(self, n=3, tamanho=10000):
        self.catalogos_ordenados = []
        for _ in range(n):
            catalogo = sorted([f"CAT-{random.randint(10000, 99999)}" for _ in range(tamanho)])
            self.catalogos_ordenados.append(catalogo)
        return [random.choice(catalogo) for catalogo in self.catalogos_ordenados]

    def busca_binaria(self, catalogo, alvo):
        baixo, alto = 0, len(catalogo) - 1
        comparacoes = 0
        while baixo <= alto:
            meio = (baixo + alto) // 2
            comparacoes += 1
            if catalogo[meio] == alvo:
                return meio, comparacoes
            elif catalogo[meio] < alvo:
                baixo = meio + 1
            else:
                alto = meio - 1
        return -1, comparacoes

    def carregar_tomos_e_marcas(self, tamanho_tomo=100000, qtd_padroes=5):
        self.tomos = [''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ ', k=tamanho_tomo))]
        self.marcas_corrupcao = [
            ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(3, 7)))
            for _ in range(qtd_padroes)
        ]
        return self.tomos, self.marcas_corrupcao

    def busca_rabin_karp(self, texto, padrao):
        d = 256
        q = 101
        n = len(texto)
        m = len(padrao)
        h = pow(d, m - 1) % q
        posicoes = []
        comparacoes = 0
        hash_padroes = 0
        hash_texto = 0
        for i in range(m):
            hash_padroes = (d * hash_padroes + ord(padrao[i])) % q
            hash_texto = (d * hash_texto + ord(texto[i])) % q
        for i in range(n - m + 1):
            comparacoes += 1
            if hash_padroes == hash_texto and texto[i:i + m] == padrao:
                posicoes.append(i)
            if i < n - m:
                hash_texto = (d * (hash_texto - ord(texto[i]) * h) + ord(texto[i + m])) % q
                if hash_texto < 0:
                    hash_texto += q
        return posicoes, comparacoes

class ModuloCompactacao:
    def __init__(self):
        self.huffman_codigos = {}

    def construir_arvore_huffman(self, freq):
        heap = [[peso, [char, ""]] for char, peso in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            menor = heapq.heappop(heap)
            maior = heapq.heappop(heap)
            for par in menor[1:]:
                par[1] = '0' + par[1]
            for par in maior[1:]:
                par[1] = '1' + par[1]
            heapq.heappush(heap, [menor[0] + maior[0]] + menor[1:] + maior[1:])
        return heap[0]

    def gerar_codigos_huffman(self, no, prefixo=""):
        if len(no) == 2:
            char, _ = no
            self.huffman_codigos[char] = prefixo
        else:
            self.gerar_codigos_huffman(no[1], prefixo + '0')
            self.gerar_codigos_huffman(no[2], prefixo + '1')

    def comprimir_huffman(self, dados):
        freq = defaultdict(int)
        for char in dados:
            freq[char] += 1
        arvore = self.construir_arvore_huffman(freq)
        self.huffman_codigos.clear()
        self.gerar_codigos_huffman(arvore[1:])
        codificado = ''.join(self.huffman_codigos[c] for c in dados)
        return codificado, dict(self.huffman_codigos)

    def descomprimir_huffman(self, codificado, codigos):
        codigos_invertidos = {v: k for k, v in codigos.items()}
        atual = ""
        resultado = []
        for bit in codificado:
            atual += bit
            if atual in codigos_invertidos:
                resultado.append(codigos_invertidos[atual])
                atual = ""
        return ''.join(resultado)

    def comprimir_rle(self, dados):
        resultado = ""
        i = 0
        while i < len(dados):
            count = 1
            while i + 1 < len(dados) and dados[i] == dados[i + 1]:
                i += 1
                count += 1
            resultado += dados[i] + str(count)
            i += 1
        return resultado

    def descomprimir_rle(self, dados):
        resultado = ""
        i = 0
        while i < len(dados):
            char = dados[i]
            i += 1
            count = ""
            while i < len(dados) and dados[i].isdigit():
                count += dados[i]
                i += 1
            resultado += char * int(count)
        return resultado

class ModuloHashing:
    def __init__(self, tamanho=1009):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]

    def hash_extracao(self, chave):
        return int(chave[-2:]) % self.tamanho

    def hash_transformacao_raiz(self, chave):
        valor = sum(ord(c) for c in chave)
        return int((valor ** 0.5) * 100) % self.tamanho

    def inserir(self, chave, valor, metodo='extracao'):
        h = self.hash_extracao(chave) if metodo == 'extracao' else self.hash_transformacao_raiz(chave)
        for par in self.tabela[h]:
            if par[0] == chave:
                par[1] = valor
                return
        self.tabela[h].append([chave, valor])

    def buscar(self, chave, metodo='extracao'):
        h = self.hash_extracao(chave) if metodo == 'extracao' else self.hash_transformacao_raiz(chave)
        for par in self.tabela[h]:
            if par[0] == chave:
                return par[1]
        return None

    def estatisticas_colisoes(self):
        colisoes = sum(1 for lista in self.tabela if len(lista) > 1)
        max_lista = max(len(lista) for lista in self.tabela)
        print(f"Total de slots com colisão: {colisoes}")
        print(f"Comprimento máximo de uma lista encadeada: {max_lista}")

    def simular_insercoes(self, n=1000, metodo='extracao'):
        print(f"\nSimulando {n} inserções com hash '{metodo}'...")
        for _ in range(n):
            chave = f"K-{random.randint(10000, 99999)}"
            valor = f"VAL-{random.randint(10000, 99999)}"
            self.inserir(chave, valor, metodo)
        self.estatisticas_colisoes()

def cabecalho():
    print("=" * 70)
    print("DUNGEON OF WORDS - A MASMORRA DAS PALAVRAS".center(70))
    print("Módulo 2: Espaço é Poder".center(70))
    print("=" * 70)
    print()

def mostrar_complexidade(algoritmo):
    complexidades = {
        'sequencial': 'O(n)',
        'binaria': 'O(log n)',
        'rabin-karp': 'O(n + m)',
        'huffman': 'O(n log n)',
        'rle': 'O(n)',
        'hash': 'O(1) média / O(n) pior caso'
    }
    print(f"Complexidade teórica ({algoritmo}): {complexidades.get(algoritmo)}")

def menu_principal():
    cabecalho()
    print(" [1] Iniciar o Módulo de Busca Completo")
    print(" [2] Executar Desafio 1: Busca Sequencial")
    print(" [3] Executar Desafio 2: Busca Binária")
    print(" [4] Executar Desafio 3: Rabin-Karp")
    print(" [5] Testar Compressão Huffman e RLE")
    print(" [6] Testar Tabela Hash (Extração/Raiz)")
    print(" [7] Sair da Masmorra")
    return input("\nEscolha sua missão: ")

if __name__ == "__main__":
    busca = ModuloBusca()
    compactacao = ModuloCompactacao()
    hashing = ModuloHashing()

    while True:
        escolha = menu_principal()
        if escolha == '1':
            print("\nIniciando jornada completa do Arquivista Desesperado!")
        elif escolha == '2':
            print("\nDESAFIO 1: Busca Sequencial")
            alvo = busca.gerar_fragmentos_aleatorios()
            inicio = time.time()
            idx, comps = busca.busca_sequencial(alvo)
            duracao = time.time() - inicio
            print(f"Fragmento encontrado em {idx} após {comps} comparações.")
            print(f"Tempo gasto: {duracao:.6f} segundos")
            mostrar_complexidade('sequencial')
        elif escolha == '3':
            print("\nDESAFIO 2: Busca Binária")
            alvos = busca.gerar_catalogos_ordenados()
            for i, alvo in enumerate(alvos):
                inicio = time.time()
                idx, comps = busca.busca_binaria(busca.catalogos_ordenados[i], alvo)
                duracao = time.time() - inicio
                print(f"Catálogo {i+1}: Encontrado em {idx}, {comps} comparações, {duracao:.6f} segundos")
            mostrar_complexidade('binaria')
        elif escolha == '4':
            print("\nDESAFIO 3: Rabin-Karp")
            tomos, marcas = busca.carregar_tomos_e_marcas()
            for marca in marcas:
                inicio = time.time()
                pos, comps = busca.busca_rabin_karp(tomos[0], marca)
                duracao = time.time() - inicio
                print(f"Marca '{marca}' encontrada em {len(pos)} posições com {comps} comparações, {duracao:.6f} segundos")
            mostrar_complexidade('rabin-karp')
        elif escolha == '5':
            print("\nTeste de Compressão Huffman e RLE")
            texto = input("Digite o texto a ser comprimido: ")
            huff, codigos = compactacao.comprimir_huffman(texto)
            original_huffman = compactacao.descomprimir_huffman(huff, codigos)
            print(f"Tamanho original: {len(texto)}")
            print(f"Tamanho comprimido (bits): {len(huff)}")
            print(f"Huffman descomprimido: {original_huffman}")
            mostrar_complexidade('huffman')
            rle = compactacao.comprimir_rle(texto)
            original_rle = compactacao.descomprimir_rle(rle)
            print(f"RLE comprimido: {rle}")
            print(f"RLE descomprimido: {original_rle}")
            mostrar_complexidade('rle')
        elif escolha == '6':
            print("\nTeste de Tabela Hash (Extração/Raiz)")
            while True:
                op = input("[I]nserir, [B]uscar, [S]imular ou [Q]uitar? ").lower()
                if op == 'i':
                    chave = input("Chave: ")
                    valor = input("Valor: ")
                    metodo = input("Método (extracao/raiz): ")
                    hashing.inserir(chave, valor, metodo)
                elif op == 'b':
                    chave = input("Chave: ")
                    metodo = input("Método (extracao/raiz): ")
                    val = hashing.buscar(chave, metodo)
                    print(f"Valor encontrado: {val}")
                elif op == 's':
                    metodo = input("Método (extracao/raiz): ")
                    hashing.simular_insercoes(1000, metodo)
                    mostrar_complexidade('hash')
                elif op == 'q':
                    break
        elif escolha == '7':
            print("\nSaindo da Masmorra das Palavras... Até a próxima aventura!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(1)
