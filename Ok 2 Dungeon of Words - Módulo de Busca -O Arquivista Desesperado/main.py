"""
Dungeon of Words - Módulo de Busca: O Arquivista Desesperado
"""

import random
import time
import heapq
from collections import defaultdict

# =========================================
#        Implementação dos Algoritmos
# =========================================
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
        h = pow(d, m-1) % q
        posicoes = []
        comparacoes = 0
        
        hash_padroes = 0
        hash_texto = 0
        for i in range(m):
            hash_padroes = (d * hash_padroes + ord(padrao[i])) % q
            hash_texto = (d * hash_texto + ord(texto[i])) % q

        for i in range(n - m + 1):
            comparacoes += 1
            if hash_padroes == hash_texto:
                if texto[i:i+m] == padrao:
                    posicoes.append(i)
            
            if i < n - m:
                hash_texto = (d * (hash_texto - ord(texto[i]) * h) + ord(texto[i+m])) % q
                if hash_texto < 0:
                    hash_texto += q
                
        return posicoes, comparacoes

class CompactadorHuffman:
    def __init__(self):
        self.codigos = {}
    
    def construir_arvore(self, freq):
        heap = [[peso, [caractere, ""]] for caractere, peso in freq.items()]
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
    
    def gerar_codigos(self, no, prefixo=""):
        if len(no) == 2:
            caractere, _ = no
            self.codigos[caractere] = prefixo
        else:
            self.gerar_codigos(no[1], prefixo + '0')
            self.gerar_codigos(no[2], prefixo + '1')
    
    def comprimir(self, dados):
        if not dados:
            return "", {}
            
        freq = defaultdict(int)
        for caractere in dados:
            freq[caractere] += 1
        
        arvore = self.construir_arvore(freq)
        self.codigos = {}
        self.gerar_codigos(arvore[1:])
        
        codificado = ''.join(self.codigos.get(c, '') for c in dados)
        return codificado, self.codigos
    
    def descomprimir(self, codificado, codigos):
        if not codificado or not codigos:
            return ""
            
        codigos_invertidos = {v: k for k, v in codigos.items()}
        atual = ""
        decodificado = []
        
        for bit in codificado:
            atual += bit
            if atual in codigos_invertidos:
                decodificado.append(codigos_invertidos[atual])
                atual = ""
        
        return ''.join(decodificado)

class ValidadorPalavras:
    def __init__(self, lista_palavras):
        self.tamanho = 10007
        self.tabela = [[] for _ in range(self.tamanho)]
        self._construir_tabela(lista_palavras)
    
    def _hash(self, palavra):
        hash_valor = 0
        for caractere in palavra:
            hash_valor = (hash_valor * 31 + ord(caractere)) % self.tamanho
        return hash_valor
    
    def _construir_tabela(self, palavras):
        for palavra in palavras:
            indice = self._hash(palavra)
            if palavra not in self.tabela[indice]:
                self.tabela[indice].append(palavra)
    
    def validar(self, palavra):
        indice = self._hash(palavra)
        return palavra in self.tabela[indice]

# ===========================================
#             Interface do Jogo
# ===========================================
def cabecalho():
    print("="*70)
    print("DUNGEON OF WORDS - A MASMORRA DAS PALAVRAS".center(70))
    print("Módulo: O Arquivista Desesperado".center(70))
    print("="*70)
    print()

def menu_principal():
    cabecalho()
    print(" [1] Iniciar o Módulo de Busca Completo")
    print(" [2] Executar Desafio 1: Busca Sequencial")
    print(" [3] Executar Desafio 2: Busca Binária")
    print(" [4] Executar Desafio 3: Rabin-Karp")
    print(" [5] Testar Compressão Huffman")
    print(" [6] Testar Validação de Palavras")
    print(" [7] Sair da Masmorra")
    return input("\nEscolha sua missão: ")

# ===========================================
#        Ponto de Entrada Principal
# ===========================================
if __name__ == "__main__":
    while True:
        escolha = menu_principal()
        
        if escolha == '1':
            print("\nIniciando jornada completa do Arquivista Desesperado!")
    
        elif escolha == '2':
            print("\nDESAFIO 1: Busca Sequencial")
           
        elif escolha == '3':
            print("\nDESAFIO 2: Busca Binária")
          
        elif escolha == '4':
            print("\nDESAFIO 3: Rabin-Karp")
           
        elif escolha == '5':
            print("\nTeste de Compressão Huffman")
           
        elif escolha == '6':
            print("\nTeste de Validação de Palavras")
          
        elif escolha == '7':
            print("\nSaindo da Masmorra das Palavras... Até a próxima aventura!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(1)
