
"""
Dungeon of Words - Módulo 2: Otimização de Recursos: Espaço é Poder
"""
import random
import time
import heapq
from collections import defaultdict

# =============================================================================
#                    Compressão de Dados: Huffman e RLE
# =============================================================================
class CompressionModule:
    def __init__(self):
        self.huffman_codes = {}

    # -------------------------
    # Run-Length Encoding (RLE)
    # -------------------------
    def rle_compress(self, text):
        compressed = []
        i = 0
        while i < len(text):
            count = 1
            while i + 1 < len(text) and text[i] == text[i+1]:
                count += 1
                i += 1
            compressed.append(text[i] + str(count))
            i += 1
        return ''.join(compressed)

    def rle_decompress(self, compressed):
        decompressed = []
        i = 0
        while i < len(compressed):
            char = compressed[i]
            count = ''
            i += 1
            while i < len(compressed) and compressed[i].isdigit():
                count += compressed[i]
                i += 1
            decompressed.append(char * int(count))
        return ''.join(decompressed)

    # -------------------------
    # Huffman Compression (Corrigido)
    # -------------------------
    def huffman_compress(self, text):
        if not text:
            return "", {}
        freq = defaultdict(int)
        for char in text:
            freq[char] += 1
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        heapq.heapify(heap)

    
        if len(heap) == 1:
            char = heap[0][1][0]
            self.huffman_codes = {char: "0"}
            encoded = ''.join("0" for _ in text)
            return encoded, self.huffman_codes

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        root = heap[0]
        self.huffman_codes = {}
        self._generate_codes(root[1:], "")
        encoded = ''.join(self.huffman_codes[char] for char in text)
        return encoded, self.huffman_codes

    def _generate_codes(self, node, code):
        if isinstance(node[0], str) and len(node) == 2:
            char, _ = node
            self.huffman_codes[char] = code
        else:
            self._generate_codes(node[0], code + '0')
            self._generate_codes(node[1], code + '1')

    def huffman_decompress(self, encoded, codes):
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

# =============================================================================
#               Hash Table com múltiplas funções e encadeamento
# =============================================================================
class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.hash_function = self.multiplication_hash

    def set_hash_function(self, func_name):
        if func_name == 'multiplication':
            self.hash_function = self.multiplication_hash
        elif func_name == 'mid_square':
            self.hash_function = self.mid_square_hash
        elif func_name == 'extraction':
            self.hash_function = self.extraction_hash
        elif func_name == 'root_transformation':
            self.hash_function = self.root_transformation_hash
        else:
            raise ValueError("Função de hash desconhecida")

    # -------------------------
    #     Funções de Hash
    # -------------------------
    def multiplication_hash(self, key):
        A = 0.6180339887  # constante fracionária 
        return int(self.size * ((hash(key) * A) % 1))

    def mid_square_hash(self, key):
        squared = hash(key) ** 2
        mid = str(squared)[len(str(squared))//2:len(str(squared))//2+2]
        return int(mid) % self.size if mid else 0

    def extraction_hash(self, key):
        s = str(hash(key))
        extracted = s[1:3] if len(s) >= 3 else s
        return int(extracted) % self.size

    def root_transformation_hash(self, key):
        return int(abs(hash(key)) ** 0.5) % self.size

    # -------------------------
    # Inserção e Busca com Encadeamento
    # -------------------------
    def insert(self, key, value):
        index = self.hash_function(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

# =============================================================================
#                             Interface do Jogo
# =============================================================================
def print_header():
    print("="*70)
    print("DUNGEON OF WORDS - A MASMORRA DAS PALAVRAS".center(70))
    print("Módulo 2: Otimização de Recursos - Espaço é Poder".center(70))
    print("="*70)

def pacto_compacto():
    cm = CompressionModule()
    print("\n--- O PACTO COMPACTO ---")
    text = input("Digite uma mensagem a ser comprimida: ")

    print("\n[1] Compressão RLE")
    print("[2] Compressão Huffman")
    choice = input("Escolha o algoritmo de compressão: ")

    if choice == '1':
        compressed = cm.rle_compress(text)
        decompressed = cm.rle_decompress(compressed)
        print(f"\nTexto Comprimido (RLE): {compressed}")
    else:
        compressed, codes = cm.huffman_compress(text)
        decompressed = cm.huffman_decompress(compressed, codes)
        print(f"\nTexto Comprimido (Huffman): {compressed}")

    print(f"Tamanho Original: {len(text)*8} bits")
    print(f"Tamanho Comprimido: {len(compressed)} bits")
    print("Integridade:", "OK" if decompressed == text else "FALHA")
    input("\nPressione Enter para continuar...")

def cofre_rapido():
    ht = HashTable()
    print("\n--- O COFRE RÁPIDO ---")
    print("Escolha a função de hash:")
    print("[1] Multiplicação")
    print("[2] Meio-Quadrado")
    print("[3] Extração")
    print("[4] Transformação da Raiz")
    func_choice = input("Opção: ")

    funcs = {'1': 'multiplication', '2': 'mid_square', '3': 'extraction', '4': 'root_transformation'}
    ht.set_hash_function(funcs.get(func_choice, 'multiplication'))

    while True:
        print("\n[1] Inserir Fragmento")
        print("[2] Buscar Fragmento")
        print("[3] Voltar ao Menu")
        op = input("Opção: ")
        if op == '1':
            key = input("Chave do Fragmento: ")
            value = input("Conteúdo do Fragmento: ")
            ht.insert(key, value)
            print("Fragmento inserido com sucesso.")
        elif op == '2':
            key = input("Chave do Fragmento: ")
            value = ht.search(key)
            print("Conteúdo:", value if value else "Não encontrado.")
        elif op == '3':
            break

def main_menu():
    print_header()
    print("\n[1] O Pacto Compacto (Compressão)")
    print("[2] O Cofre Rápido (Hashing)")
    print("[3] Sair")
    return input("Escolha uma opção: ")

# =============================================================================
#                             Ponto de Entrada
# =============================================================================
if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == '1':
            pacto_compacto()
        elif choice == '2':
            cofre_rapido()
        elif choice == '3':
            print("\nSaindo... Até a próxima aventura!")
            break
        else:
            print("Opção inválida!")
