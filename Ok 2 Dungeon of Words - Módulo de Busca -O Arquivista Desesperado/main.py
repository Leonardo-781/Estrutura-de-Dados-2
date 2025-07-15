
"""
Dungeon of Words - Módulo de Busca: O Arquivista Desesperado
"""
import random
import time
import heapq
from collections import defaultdict
import sys

# =========================================
#      Implementações dos Algoritmos
# =========================================
class SearchModule:
    def __init__(self):
        self.fragments = []
        self.ordered_catalogs = []
        self.tomes = []
        self.corruption_marks = []
    
    def generate_random_fragments(self, n=10000):
        self.fragments = [f"FRAG-{random.randint(10000,99999)}" for _ in range(n)]
        return random.choice(self.fragments)
    
    def sequential_search(self, target):
        comparisons = 0
        for i, fragment in enumerate(self.fragments):
            comparisons += 1
            if fragment == target:
                return i, comparisons
        return -1, comparisons

    def generate_ordered_catalogs(self, n=3, size=10000):
        self.ordered_catalogs = []
        for _ in range(n):
            catalog = sorted([f"CAT-{random.randint(10000,99999)}" for _ in range(size)])
            self.ordered_catalogs.append(catalog)
        return [random.choice(catalog) for catalog in self.ordered_catalogs]
    
    def binary_search(self, catalog, target):
        low, high = 0, len(catalog) - 1
        comparisons = 0
        
        while low <= high:
            mid = (low + high) // 2
            comparisons += 1
            if catalog[mid] == target:
                return mid, comparisons
            elif catalog[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1, comparisons

    def load_tomes_and_marks(self, tome_size=100000, pattern_count=5):
        self.tomes = [''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ ', k=tome_size))]
        self.corruption_marks = [
            ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(3,7))) 
            for _ in range(pattern_count)
        ]
        return self.tomes, self.corruption_marks

    def rabin_karp_search(self, text, pattern):
        d = 256
        q = 101
        n = len(text)
        m = len(pattern)
        h = pow(d, m-1) % q
        positions = []
        comparisons = 0
        
        p_hash = 0
        t_hash = 0
        for i in range(m):
            p_hash = (d * p_hash + ord(pattern[i])) % q
            t_hash = (d * t_hash + ord(text[i])) % q

        for i in range(n - m + 1):
            comparisons += 1
            if p_hash == t_hash:
                if text[i:i+m] == pattern:
                    positions.append(i)
            
            if i < n - m:
                t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i+m])) % q
                if t_hash < 0:
                    t_hash += q
                
        return positions, comparisons

class HuffmanCompressor:
    def __init__(self):
        self.codes = {}
    
    def build_tree(self, freq):
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return heap[0]
    
    def generate_codes(self, node, prefix=""):
        if len(node) == 2:
            char, _ = node
            self.codes[char] = prefix
        else:
            self.generate_codes(node[1], prefix + '0')
            self.generate_codes(node[2], prefix + '1')
    
    def compress(self, data):
        if not data:
            return "", {}
            
        freq = defaultdict(int)
        for char in data:
            freq[char] += 1
        
        tree = self.build_tree(freq)
        self.codes = {}
        self.generate_codes(tree[1:])
        
        encoded = ''.join(self.codes.get(char, '') for char in data)
        return encoded, self.codes
    
    def decompress(self, encoded, codes):
        if not encoded or not codes:
            return ""
            
        reverse_codes = {v: k for k, v in codes.items()}
        current = ""
        decoded = []
        
        for bit in encoded:
            current += bit
            if current in reverse_codes:
                decoded.append(reverse_codes[current])
                current = ""
        
        return ''.join(decoded)

class WordValidator:
    def __init__(self, word_list):
        self.size = 10007
        self.table = [[] for _ in range(self.size)]
        self._build_table(word_list)
    
    def _hash(self, word):
        hash_val = 0
        for char in word:
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val
    
    def _build_table(self, words):
        for word in words:
            index = self._hash(word)
            if word not in self.table[index]:
                self.table[index].append(word)
    
    def validate(self, word):
        index = self._hash(word)
        return word in self.table[index]

# ===========================================
#            Interface do Jogo
# ===========================================
def print_header():
    print("="*70)
    print("DUNGEON OF WORDS - A MASMORRA DAS PALAVRAS".center(70))
    print("Módulo 1: O Arquivista Desesperado".center(70))
    print("="*70)
    print()

def desafio1():
    searcher = SearchModule()
    print("\n--- DESAFIO 1: PILHA DE PERGAMINHOS ---")
    print("Você encontrou uma seção caótica da biblioteca!")
    print("Fragmentos de conhecimento estão espalhados sem nenhuma ordem...")
    print()
    
    vital_scroll = searcher.generate_random_fragments(15000)
    print(f"Pergaminho Vital a ser encontrado: {vital_scroll}")
    
    input("\nPressione Enter para iniciar a busca sequencial...")
    
    start_time = time.time()
    position, comparisons = searcher.sequential_search(vital_scroll)
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    if position != -1:
        print(f"SUCESSO! Pergaminho encontrado na posição {position}")
    else:
        print("FRACASSO! Pergaminho não encontrado")
    
    print(f"Comparações realizadas: {comparisons}")
    print(f"Tempo de busca: {elapsed:.6f} segundos")
    print("="*50)
    return position != -1

def desafio2():
    searcher = SearchModule()
    print("\n--- DESAFIO 2: CATÁLOGOS ORDENADOS ---")
    print("Você restaurou parte da ordem! Agora os fragmentos estão organizados.")
    print("Encontre rapidamente os fragmentos especiais nos catálogos digitais...")
    print()
    
    targets = searcher.generate_ordered_catalogs(3, 20000)
    print(f"Fragmentos a serem encontrados: {', '.join(targets)}")
    
    input("\nPressione Enter para iniciar a busca binária...")
    
    total_comparisons = 0
    start_time = time.time()
    
    results = []
    for i, target in enumerate(targets):
        catalog = searcher.ordered_catalogs[i]
        position, comparisons = searcher.binary_search(catalog, target)
        total_comparisons += comparisons
        results.append(position != -1)
        print(f"\nCatálogo {i+1}: {'ENCONTRADO' if position != -1 else 'NÃO ENCONTRADO'}")

    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print(f"Total de comparações: {total_comparisons}")
    print(f"Tempo total de busca: {elapsed:.6f} segundos")
    print("="*50)
    return all(results)

def desafio3():
    searcher = SearchModule()
    print("\n--- DESAFIO 3: CÓDIGOS DO VAZIO ---")
    print("O Vazio deixou marcas de corrupção nos tomos antigos!")
    print("Use o algoritmo Rabin-Karp para encontrar e purificar os textos...")
    print()
    
    tomes, marks = searcher.load_tomes_and_marks(500000, 8)
    print(f"Marcas de corrupção: {', '.join(marks)}")
    
    input("\nPressione Enter para iniciar a busca de padrões...")
    
    total_positions = 0
    total_comparisons = 0
    start_time = time.time()
    
    for i, tome in enumerate(tomes):
        print(f"\nAnalisando Tomo {i+1}...")
        for mark in marks:
            positions, comparisons = searcher.rabin_karp_search(tome, mark)
            total_positions += len(positions)
            total_comparisons += comparisons
            print(f"  Padrão '{mark}': {len(positions)} ocorrências encontradas")
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print(f"Total de marcas encontradas: {total_positions}")
    print(f"Comparações realizadas: {total_comparisons}")
    print(f"Tempo total de processamento: {elapsed:.6f} segundos")
    print("="*50)
    return total_positions > 0

def test_huffman():
    print("\n--- TESTE DE COMPRESSÃO HUFFMAN ---")
    text = "ESTRUTURAS_DE_DADOS_II_2025"
    print(f"Texto original: {text}")
    print(f"Tamanho original: {len(text) * 8} bits")
    
    compressor = HuffmanCompressor()
    compressed, codes = compressor.compress(text)
    
    if compressed:
        print(f"Texto comprimido: {compressed}")
        print(f"Tamanho comprimido: {len(compressed)} bits")
        
        
        original_size = len(text) * 8
        compressed_size = len(compressed)
        compression_ratio = 100 * (1 - compressed_size / original_size)
        print(f"Taxa de compressão: {compression_ratio:.2f}%")
        
        decompressed = compressor.decompress(compressed, codes)
        print(f"Texto descomprimido: {decompressed}")
        print("Sucesso!" if decompressed == text else "Falha!")
    else:
        print("Falha na compressão!")

def test_hashing():
    print("\n--- TESTE DE VALIDAÇÃO DE PALAVRAS ---")
    words = ["PYTHON", "ALGORITMO", "HASHING", "ESTRUTURAS", "DADOS"]
    validator = WordValidator(words)
    
    test_words = ["PYTHON", "ALGORITMO", "JAVA", "HASH", "DADOS"]
    print("Palavras no dicionário: " + ", ".join(words))
    print("\nTestes:")
    for word in test_words:
        valid = validator.validate(word)
        print(f"  '{word}': {'VÁLIDA' if valid else 'INVÁLIDA'}")

def main_menu():
    print_header()
    print(" [1] Iniciar Módulo de Busca Completo")
    print(" [2] Executar Desafio 1: Busca Sequencial")
    print(" [3] Executar Desafio 2: Busca Binária")
    print(" [4] Executar Desafio 3: Rabin-Karp")
    print(" [5] Testar Compressão Huffman")
    print(" [6] Testar Validação de Palavras")
    print(" [7] Sair")
    print()
    
    choice = input("Escolha uma opção: ")
    return choice

# ===========================================
#        Ponto de Entrada Principal
# ===========================================
if __name__ == "__main__":
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("\n" + "="*70)
            print("INICIANDO MÓDULO COMPLETO: O ARQUIVISTA DESESPERADO".center(70))
            print("="*70)
            
            success1 = desafio1()
            if not success1:
                print("\nFALHA NO DESAFIO 1! Você não pode avançar.")
                continue
                
            success2 = desafio2()
            if not success2:
                print("\nFALHA NO DESAFIO 2! Você não pode avançar.")
                continue
                
            success3 = desafio3()
            if success3:
                print("\nPARABÉNS! Você completou todos os desafios e restaurou a ordem na biblioteca!")
            else:
                print("\nFALHA NO DESAFIO 3! As marcas de corrupção permanecem.")
            
            input("\nPressione Enter para voltar ao menu...")
        
        elif choice == '2':
            print("\n" + "="*70)
            print("DESAFIO 1: BUSCA SEQUENCIAL".center(70))
            print("="*70)
            desafio1()
            input("\nPressione Enter para voltar ao menu...")
            
        elif choice == '3':
            print("\n" + "="*70)
            print("DESAFIO 2: BUSCA BINÁRIA".center(70))
            print("="*70)
            desafio2()
            input("\nPressione Enter para voltar ao menu...")
            
        elif choice == '4':
            print("\n" + "="*70)
            print("DESAFIO 3: RABIN-KARP".center(70))
            print("="*70)
            desafio3()
            input("\nPressione Enter para voltar ao menu...")
            
        elif choice == '5':
            print("\n" + "="*70)
            print("TESTE DE COMPRESSÃO HUFFMAN".center(70))
            print("="*70)
            test_huffman()
            input("\nPressione Enter para voltar ao menu...")
            
        elif choice == '6':
            print("\n" + "="*70)
            print("TESTE DE VALIDAÇÃO DE PALAVRAS".center(70))
            print("="*70)
            test_hashing()
            input("\nPressione Enter para voltar ao menu...")
            
        elif choice == '7':
            print("\nSaindo da Masmorra das Palavras... Até a próxima aventura!")
            break
            
        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(1)