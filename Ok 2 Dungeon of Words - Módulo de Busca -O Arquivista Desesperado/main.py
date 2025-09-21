"""
Dungeon of Words - Módulo de Busca: O Arquivista Desesperado
Fase 3: Grafos (representação, DFS, BFS, Dijkstra, Topológica, Coloração, AGM)
Etapa 4: Algoritmos Gulosos (Troco, Escalonamento de Intervalos, Mochila Fracionária)
         + Programação Dinâmica (Distância de Edição)
"""

import random
import time
import heapq
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Any

# =========================================
#        Utilidades / Stubs necessários
# =========================================
class CompactadorHuffman:
    """Implementação mínima para suportar a opção 5 do menu."""
    class _Nodo:
        def __init__(self, ch=None, freq=0, esq=None, dir=None):
            self.ch, self.freq, self.esq, self.dir = ch, freq, esq, dir
        def __lt__(self, other): return self.freq < other.freq

    def _construir_arvore(self, texto: str):
        if not texto:
            return None
        freq = defaultdict(int)
        for c in texto:
            freq[c] += 1

        h = []
        for ch, f in freq.items():
            heapq.heappush(h, self._Nodo(ch, f))

        if len(h) == 1:  # caso degenerado
            unico = heapq.heappop(h)
            return self._Nodo(None, unico.freq, unico, None)

        while len(h) > 1:
            a = heapq.heappop(h)
            b = heapq.heappop(h)
            heapq.heappush(h, self._Nodo(None, a.freq + b.freq, a, b))
        return heapq.heappop(h)

    def _mapear_codigos(self, raiz):
        cod = {}
        def dfs(n, caminho):
            if n is None:
                return
            if n.ch is not None:
                cod[n.ch] = caminho or "0"
            else:
                dfs(n.esq, caminho + "0")
                dfs(n.dir, caminho + "1")
        dfs(raiz, "")
        return cod

    def comprimir(self, texto: str):
        raiz = self._construir_arvore(texto)
        if raiz is None:
            return "", {}
        tabela = self._mapear_codigos(raiz)
        codificado = "".join(tabela[c] for c in texto)
        return codificado, tabela

    def descomprimir(self, bits: str, tabela: Dict[str, str]):
        if not bits or not tabela:
            return ""
        inv = {v: k for k, v in tabela.items()}
        out, buf = [], ""
        for b in bits:
            buf += b
            if buf in inv:
                out.append(inv[buf])
                buf = ""
        return "".join(out)

class ValidadorPalavras:
    """Implementação mínima para suportar a opção 6 do menu."""
    def __init__(self, dicio: List[str]):
        self._set = set(dicio)
    def validar(self, palavra: str) -> bool:
        return palavra.upper() in self._set

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
        if m == 0 or m > n:
            return [], 0
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
            if hash_padroes == hash_texto and texto[i:i+m] == padrao:
                posicoes.append(i)
            if i < n - m:
                hash_texto = (d * (hash_texto - ord(texto[i]) * h) + ord(texto[i+m])) % q
                if hash_texto < 0:
                    hash_texto += q
        return posicoes, comparacoes

    # ===== Programação Dinâmica: Distância de Edição (Levenshtein) =====
    def distancia_edicao(self, s, t):
        m, n = len(s), len(t)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0] = i
        for j in range(n+1): dp[0][j] = j
        for i in range(1, m+1):
            for j in range(1, n+1):
                custo = 0 if s[i-1] == t[j-1] else 1
                dp[i][j] = min(
                    dp[i-1][j] + 1,        # deletar
                    dp[i][j-1] + 1,        # inserir
                    dp[i-1][j-1] + custo   # substituir
                )
        return dp[m][n], dp

# =========================================
#        Gulosos (Etapa 4 - Módulo)
# =========================================
class Gulosos:
    @staticmethod
    def troco_guloso(valor: int, moedas: List[int]) -> Dict[int, int]:
        """
        Problema do Troco (greedy) — O(n log n + m), n=len(moedas), m=#tipos usados
        Supõe sistema canônico para otimalidade (ex.: BRL {100,50,20,10,5,2,1}).
        """
        if valor < 0:
            raise ValueError("Valor inválido.")
        moedas = sorted([m for m in moedas if m > 0], reverse=True)
        resultado = {}
        restante = valor
        for m in moedas:
            if restante == 0:
                break
            qtd = restante // m
            if qtd > 0:
                resultado[m] = qtd
                restante -= qtd * m
        return resultado  # se não canônico, pode sobrar troco

    @staticmethod
    def interval_scheduling_greedy(intervalos: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        """
        Escalonamento de Intervalos (greedy por horário de término) — O(k log k)
        intervalos: [(inicio, fim, nome)]
        """
        intervalos_ordenados = sorted(intervalos, key=lambda x: x[1])
        selecionados = []
        fim_atual = -10**18
        for ini, fim, nome in intervalos_ordenados:
            if ini >= fim_atual:
                selecionados.append((ini, fim, nome))
                fim_atual = fim
        return selecionados

    @staticmethod
    def fractional_knapsack(capacidade: float, itens: List[Tuple[float, float, str]]) -> Tuple[float, List[Tuple[str, float]]]:
        """
        Mochila Fracionária (greedy por valor/peso) — O(n log n)
        itens: [(valor, peso, nome)]  | retorna (valor_total, [(nome, fração_usada)])
        """
        if capacidade <= 0:
            return 0.0, []
        itens_ordenados = sorted(itens, key=lambda x: (x[0] / x[1]) if x[1] > 0 else float('inf'), reverse=True)
        total = 0.0
        comp = []
        cap = float(capacidade)
        for valor, peso, nome in itens_ordenados:
            if cap <= 0:
                break
            if peso <= 0:  # ignora pesos não-positivos
                if valor > 0:
                    comp.append((nome, 1.0))
                    total += valor
                continue
            if peso <= cap:
                comp.append((nome, 1.0))
                total += valor
                cap -= peso
            else:
                frac = cap / peso
                comp.append((nome, frac))
                total += valor * frac
                cap = 0
        return total, comp

# =========================================
#              GRAFOS - FASE 3
# =========================================
class Grafo:
    """
    Representação principal: lista de adjacências (dict de dict).
    Para matriz de adjacência, geramos sob demanda.
    """
    def __init__(self, direcionado=False):
        self.dir = direcionado
        self.adj = defaultdict(dict)   # u -> {v: peso}

    # ---------- operações básicas ----------
    def adicionar_vertice(self, v):
        self.adj[v]  # força a criação

    def remover_vertice(self, v):
        if v in self.adj:
            del self.adj[v]
        for u in list(self.adj.keys()):
            self.adj[u].pop(v, None)

    def adicionar_aresta(self, u, v, peso=1):
        self.adj[u][v] = peso
        if not self.dir:
            self.adj[v][u] = peso

    def remover_aresta(self, u, v):
        self.adj[u].pop(v, None)
        if not self.dir:
            self.adj[v].pop(u, None)

    def vertices(self):
        return list(self.adj.keys())

    def arestas(self):
        E = []
        vistos = set()
        for u in self.adj:
            for v, w in self.adj[u].items():
                if self.dir or (v, u) not in vistos:
                    E.append((u, v, w))
                    vistos.add((u, v))
        return E

    # ---------- visualização ----------
    def imprimir_lista(self):
        print("\n[Lista de Adjacências]")
        for u in sorted(self.adj.keys()):
            viz = ", ".join(f"{v}({w})" for v, w in self.adj[u].items())
            print(f"{u} -> {viz}")
        print()

    def matriz_adjacencia(self):
        V = sorted(self.adj.keys())
        idx = {v:i for i, v in enumerate(V)}
        n = len(V)
        M = [[0]*n for _ in range(n)]
        for u in V:
            for v, w in self.adj[u].items():
                M[idx[u]][idx[v]] = w
        return V, M

    def imprimir_matriz(self):
        V, M = self.matriz_adjacencia()
        print("\n[Matriz de Adjacência] (ordem de vértices:", V, ")")
        for linha in M:
            print(" ".join(f"{x:3d}" for x in linha))
        print()

    # ---------- DFS / BFS ----------
    def dfs(self, origem):
        visit = set()
        ordem = []
        def _dfs(u):
            visit.add(u)
            ordem.append(u)
            for v in self.adj[u]:
                if v not in visit:
                    _dfs(v)
        if origem not in self.adj:
            return []
        _dfs(origem)
        return ordem

    def bfs(self, origem):
        if origem not in self.adj:
            return [], {}
        visit = {origem}
        fila = deque([origem])
        ordem = []
        dist = {origem: 0}
        while fila:
            u = fila.popleft()
            ordem.append(u)
            for v in self.adj[u]:
                if v not in visit:
                    visit.add(v)
                    dist[v] = dist[u] + 1
                    fila.append(v)
        return ordem, dist

    # ---------- Dijkstra ----------
    def dijkstra(self, origem):
        # guarda: pesos não-negativos
        for u in self.adj:
            for v, w in self.adj[u].items():
                if w < 0:
                    raise ValueError("Dijkstra requer pesos não negativos.")

        dist = {v: float('inf') for v in self.adj}
        prev = {v: None for v in self.adj}
        if origem not in self.adj:
            return dist, prev
        dist[origem] = 0
        pq = [(0, origem)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in self.adj[u].items():
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

    @staticmethod
    def reconstruir_caminho(prev, alvo):
        cam = []
        u = alvo
        while u is not None:
            cam.append(u)
            u = prev[u]
        return list(reversed(cam))

    # ---------- Ordenação Topológica (Kahn) ----------
    def topologica_kahn(self):
        if not self.dir:
            raise ValueError("Topológica: grafo precisa ser direcionado.")
        indeg = {v: 0 for v in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                indeg[v] = indeg.get(v, 0) + 1
                indeg.setdefault(u, indeg.get(u, 0))
        fila = deque([v for v, g in indeg.items() if g == 0])
        ordem = []
        while fila:
            u = fila.popleft()
            ordem.append(u)
            for v in list(self.adj[u].keys()):
                indeg[v] -= 1
                if indeg[v] == 0:
                    fila.append(v)
        if len(ordem) != len(indeg):
            return None  # tem ciclo
        return ordem

    # ---------- Coloração (Welch-Powell) ----------
    def coloracao_welch_powell(self):
        # ordena vértices por grau decrescente
        V = sorted(self.adj.keys(), key=lambda v: len(self.adj[v]), reverse=True)
        cor = {}
        cor_atual = 0
        for v in V:
            if v in cor:
                continue
            cor_atual += 1
            cor[v] = cor_atual
            for u in V:
                if u not in cor:
                    # u não adjacente a nenhum já pintado com cor_atual
                    if all((u not in self.adj[x] and x not in self.adj[u]) for x in cor if cor[x]==cor_atual):
                        cor[u] = cor_atual
        return cor  # dict: vértice -> cor (1..k)

    # ---------- AGM (Kruskal) ----------
    def agm_kruskal(self):
        if self.dir:
            raise ValueError("AGM: use grafo não-direcionado.")
        # estrutura de união-busca (DSU)
        parent = {}
        rank = {}
        def find(x):
            parent.setdefault(x, x)
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb: return False
            if rank.get(ra,0) < rank.get(rb,0):
                ra, rb = rb, ra
            parent[rb] = ra
            if rank.get(ra,0) == rank.get(rb,0):
                rank[ra] = rank.get(ra,0) + 1
            return True

        arestas = sorted(self.arestas(), key=lambda e: e[2])
        mst = []
        total = 0
        for u, v, w in arestas:
            if union(u, v):
                mst.append((u, v, w))
                total += w
        return mst, total

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
    print(" [7] Distância de Edição (Levenshtein)  (PD)")
    print(" [8] Fase 3: Grafos ⚙️")
    print(" [9] Etapa 4: Algoritmos Gulosos ⚡ (Troco, Intervalos, Mochila Frac.)")
    print(" [10] Sair da Masmorra")
    return input("\nEscolha sua missão: ")

def submenu_grafos():
    print("\n=== FASE 3: GRAFOS ===")
    print(" [1] Criar novo grafo")
    print(" [2] Adicionar vértice")
    print(" [3] Remover vértice")
    print(" [4] Adicionar aresta")
    print(" [5] Remover aresta")
    print(" [6] Mostrar lista de adjacências")
    print(" [7] Mostrar matriz de adjacência")
    print(" [8] DFS")
    print(" [9] BFS")
    print(" [10] Dijkstra")
    print(" [11] Ordenação Topológica (Kahn)")
    print(" [12] Coloração (Welch-Powell)")
    print(" [13] AGM (Kruskal)")
    print(" [14] Preencher grafo de demonstração")
    print(" [0] Voltar")
    return input("\nEscolha: ")

def submenu_gulosos():
    print("\n=== ETAPA 4: ALGORITMOS GULOSOS ===")
    print(" [1] Problema do Troco (greedy)")
    print(" [2] Escalonamento de Intervalos (greedy)")
    print(" [3] Mochila Fracionária (greedy)")
    print(" [4] Mostrar complexidades e notas")
    print(" [0] Voltar")
    return input("\nEscolha: ")

def executar_troco():
    print("\n--- Problema do Troco (Greedy) ---")
    try:
        valor = int(input("Valor do troco (inteiro, ex.: 289): ").strip())
    except:
        print("Entrada inválida."); return
    entrada_moedas = input("Moedas/cédulas disponíveis (ex.: 100,50,20,10,5,2,1): ").strip()
    if not entrada_moedas:
        moedas = [100,50,20,10,5,2,1]
    else:
        try:
            moedas = [int(x.strip()) for x in entrada_moedas.split(",")]
        except:
            print("Entrada inválida."); return
    sol = Gulosos.troco_guloso(valor, moedas)
    total = sum(k*v for k, v in sol.items())
    if total != valor:
        print(f"Solução parcial: {sol} | soma={total} "
              f"(sistema não canônico; pode não fechar exato)")
    else:
        print(f"Solução ótima: {sol} | soma={total}")

def executar_interval_scheduling():
    print("\n--- Escalonamento de Intervalos (Greedy por término) ---")
    try:
        n = int(input("Quantidade de tarefas (ex.: 6): ").strip())
    except:
        print("Entrada inválida."); return
    intervalos = []
    for i in range(n):
        linha = input(f"Tarefa {i+1} (inicio,fim,nome) ex.: 1,4,T1: ").strip()
        try:
            ini_s, fim_s, nome = [x.strip() for x in linha.split(",")]
            ini, fim = int(ini_s), int(fim_s)
        except:
            print("Entrada inválida."); return
        intervalos.append((ini, fim, nome))
    escolhidos = Gulosos.interval_scheduling_greedy(intervalos)
    print(f"Selecionadas ({len(escolhidos)}): {escolhidos}")

def executar_mochila_fracionaria():
    print("\n--- Mochila Fracionária (Greedy por valor/peso) ---")
    try:
        cap = float(input("Capacidade (ex.: 15): ").strip())
        n = int(input("Quantidade de itens (ex.: 4): ").strip())
    except:
        print("Entrada inválida."); return
    itens = []
    for i in range(n):
        linha = input(f"Item {i+1} (valor,peso,nome) ex.: 10,5,Ouro: ").strip()
        try:
            v_s, p_s, nome = [x.strip() for x in linha.split(",")]
            v, p = float(v_s), float(p_s)
        except:
            print("Entrada inválida."); return
        itens.append((v, p, nome))
    total, comp = Gulosos.fractional_knapsack(cap, itens)
    print(f"Valor total: {total:.4f}\nComposição (nome, fração): {comp}")

def mostrar_notas_gulosos():
    print("\n--- Notas/Complexidades (Big-O) ---")
    print("Troco (greedy): ordenar moedas O(k log k); seleção O(k). Ótimo se sistema canônico.")
    print("Escalonamento de Intervalos: ordenar por fim O(n log n); seleção linear O(n). Ótimo.")
    print("Mochila Fracionária: ordenar por valor/peso O(n log n); preenchimento O(n). Ótimo (fracionável).")

def preencher_demo(grafo: Grafo):
    """Carrega um pequeno mapa para demonstração rápida de todos os algoritmos."""
    edges = [
        ("A","B",4),("A","C",2),("B","C",5),("B","D",10),
        ("C","E",3),("E","D",4),("D","F",11)
    ]
    for u, v, w in edges:
        grafo.adicionar_aresta(u, v, w)

# ===========================================
#        Ponto de Entrada Principal
# ===========================================
if __name__ == "__main__":
    modulo = ModuloBusca()
    grafo = None

    while True:
        escolha = menu_principal()
        
        if escolha == '1':
            print("\nIniciando jornada completa do Arquivista Desesperado!")
    
        elif escolha == '2':
            print("\nDESAFIO 1: Busca Sequencial")
            alvo = modulo.gerar_fragmentos_aleatorios()
            print(f"Alvo escolhido: {alvo}")
            pos, comp = modulo.busca_sequencial(alvo)
            print(f"Posição: {pos}, Comparações: {comp}")

        elif escolha == '3':
            print("\nDESAFIO 2: Busca Binária")
            alvos = modulo.gerar_catalogos_ordenados()
            for i, catalogo in enumerate(modulo.catalogos_ordenados):
                alvo = alvos[i]
                pos, comp = modulo.busca_binaria(catalogo, alvo)
                print(f"Cat {i}: alvo={alvo} pos={pos} comps={comp}")
          
        elif escolha == '4':
            print("\nDESAFIO 3: Rabin-Karp")
            (texto,), padroes = modulo.carregar_tomos_e_marcas(10000, 3)
            padrao = random.choice(padroes)
            pos, comp = modulo.busca_rabin_karp(texto, padrao)
            print(f"Padrao: {padrao} | Ocorrências: {len(pos)} | Comparações: {comp}")
           
        elif escolha == '5':
            print("\nTeste de Compressão Huffman")
            dados = input("Digite um texto para comprimir: ")
            comp_h = CompactadorHuffman()
            cod, tabela = comp_h.comprimir(dados)
            print("Tabela:", tabela)
            print("Codificado:", cod)
            print("Decodificado:", comp_h.descomprimir(cod, tabela))
           
        elif escolha == '6':
            print("\nTeste de Validação de Palavras")
            dicio = ["FIRE", "ICE", "STONE", "WOOD", "WATER"]
            val = ValidadorPalavras(dicio)
            p = input("Palavra para validar: ").strip().upper()
            print("Existe?" , "Sim" if val.validar(p) else "Não")

        elif escolha == '7':
            print("\nDESAFIO (PD): Distância de Edição (Levenshtein)")
            s = input("Digite a 1ª palavra/frase: ")
            t = input("Digite a 2ª palavra/frase: ")
            distancia, _ = modulo.distancia_edicao(s, t)
            print(f"\nDistância de edição entre '{s}' e '{t}': {distancia}\n")

        elif escolha == '8':
            while True:
                op = submenu_grafos()
                if op == '1':
                    d = input("Grafo direcionado? (s/n): ").lower().startswith('s')
                    grafo = Grafo(direcionado=d)
                    print("Grafo criado.")
                elif op == '2':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    v = input("Vértice: ")
                    grafo.adicionar_vertice(v)
                    print("OK.")
                elif op == '3':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    v = input("Vértice: ")
                    grafo.remover_vertice(v)
                    print("OK.")
                elif op == '4':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    u = input("Origem: "); v = input("Destino: ")
                    try:
                        w = int(input("Peso (>=1): ") or "1")
                    except:
                        print("Peso inválido."); continue
                    grafo.adicionar_aresta(u, v, w)
                    print("OK.")
                elif op == '5':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    u = input("Origem: "); v = input("Destino: ")
                    grafo.remover_aresta(u, v)
                    print("OK.")
                elif op == '6':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    grafo.imprimir_lista()
                elif op == '7':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    grafo.imprimir_matriz()
                elif op == '8':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    s = input("Origem: ")
                    print("DFS:", grafo.dfs(s))
                elif op == '9':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    s = input("Origem: ")
                    ordem, dist = grafo.bfs(s)
                    print("BFS:", ordem)
                    print("Distâncias (saltos):", dist)
                elif op == '10':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    s = input("Origem: ")
                    try:
                        dist, prev = grafo.dijkstra(s)
                    except ValueError as e:
                        print(e); continue
                    print("Distâncias:", dist)
                    alvo = input("Reconstruir caminho até (opcional): ").strip()
                    if alvo:
                        print("Caminho:", Grafo.reconstruir_caminho(prev, alvo))
                elif op == '11':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    try:
                        ordem = grafo.topologica_kahn()
                        if ordem is None:
                            print("O grafo possui ciclo; topológica impossível.")
                        else:
                            print("Ordem topológica:", ordem)
                    except ValueError as e:
                        print(e)
                elif op == '12':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    cores = grafo.coloracao_welch_powell()
                    print("Coloração (vértice -> cor):", cores, "| nº de cores:", len(set(cores.values())))
                elif op == '13':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    try:
                        mst, total = grafo.agm_kruskal()
                        print("AGM (Kruskal):", mst)
                        print("Custo total:", total)
                    except ValueError as e:
                        print(e)
                elif op == '14':
                    if grafo is None: print("Crie um grafo primeiro!"); continue
                    preencher_demo(grafo); print("Demo carregada. Use DFS/BFS/Dijkstra etc.")
                elif op == '0':
                    break
                else:
                    print("Opção inválida.")

        elif escolha == '9':
            while True:
                op = submenu_gulosos()
                if op == '1':
                    executar_troco()
                elif op == '2':
                    executar_interval_scheduling()
                elif op == '3':
                    executar_mochila_fracionaria()
                elif op == '4':
                    mostrar_notas_gulosos()
                elif op == '0':
                    break
                else:
                    print("Opção inválida.")

        elif escolha == '10':
            print("\nSaindo da Masmorra das Palavras... Até a próxima aventura!")
            break

        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(1)
