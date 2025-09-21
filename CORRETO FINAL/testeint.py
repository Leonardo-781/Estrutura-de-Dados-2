# -*- coding: utf-8 -*-
"""
Dungeon of Words - GUI (Tkinter)
Adiciona interface gráfica às funcionalidades:
- Fase 3: Grafos (lista, matriz, DFS, BFS, Dijkstra, Topológica, Coloração, AGM)
- Etapa 4: Gulosos (Troco, Intervalos, Mochila Fracionária)
- PD: Levenshtein
- Busca sequencial, binária, Rabin-Karp
- Huffman (compressão) e Validador de palavras

Requisitos: Python 3.x (apenas biblioteca padrão)
Execução: python dungeon_gui.py
"""

import random
import time
import heapq
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Any

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

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
    def formatar_lista(self):
        linhas = ["[Lista de Adjacências]"]
        for u in sorted(self.adj.keys()):
            viz = ", ".join(f"{v}({w})" for v, w in self.adj[u].items())
            linhas.append(f"{u} -> {viz}")
        return "\n".join(linhas)

    def matriz_adjacencia(self):
        V = sorted(self.adj.keys())
        idx = {v:i for i, v in enumerate(V)}
        n = len(V)
        M = [[0]*n for _ in range(n)]
        for u in V:
            for v, w in self.adj[u].items():
                M[idx[u]][idx[v]] = w
        return V, M

    def formatar_matriz(self):
        V, M = self.matriz_adjacencia()
        out = [f"[Matriz de Adjacência] (ordem de vértices: {V})"]
        for linha in M:
            out.append(" ".join(f"{x:3d}" for x in linha))
        return "\n".join(out)

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
#             GUI (Tkinter)
# ===========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dungeon of Words — GUI")
        self.geometry("1040x680")
        self.minsize(920, 600)
        try:
            self.iconbitmap("")  # opcional (adicione um .ico se quiser)
        except Exception:
            pass

        self.modulo = ModuloBusca()
        self.grafo: Grafo | None = None
        self.comp_huff = CompactadorHuffman()
        self.validador = ValidadorPalavras(["FIRE","ICE","STONE","WOOD","WATER"])

        self._build_ui()

    # ---------- helpers ----------
    @staticmethod
    def _add_labeled_entry(parent, label, default="", width=18):
        frm = ttk.Frame(parent)
        ttk.Label(frm, text=label).pack(side=tk.LEFT, padx=(0,6))
        var = tk.StringVar(value=str(default))
        ent = ttk.Entry(frm, textvariable=var, width=width)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frm.pack(fill=tk.X, pady=2)
        return var, ent

    @staticmethod
    def _append_text(widget: scrolledtext.ScrolledText, text: str, newline=True):
        widget.configure(state="normal")
        widget.insert(tk.END, text + ("\n" if newline else ""))
        widget.see(tk.END)
        widget.configure(state="disabled")

    def _build_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_busca = ttk.Frame(nb)
        self.tab_rk = ttk.Frame(nb)
        self.tab_huff = ttk.Frame(nb)
        self.tab_lev = ttk.Frame(nb)
        self.tab_grafos = ttk.Frame(nb)
        self.tab_gulosos = ttk.Frame(nb)

        nb.add(self.tab_busca, text="Busca")
        nb.add(self.tab_rk, text="Rabin–Karp")
        nb.add(self.tab_huff, text="Huffman / Validador")
        nb.add(self.tab_lev, text="Levenshtein (PD)")
        nb.add(self.tab_grafos, text="Grafos (Fase 3)")
        nb.add(self.tab_gulosos, text="Gulosos (Etapa 4)")

        self._build_tab_busca()
        self._build_tab_rk()
        self._build_tab_huff()
        self._build_tab_lev()
        self._build_tab_grafos()
        self._build_tab_gulosos()

    # ------------------ Tab: Busca ------------------
    def _build_tab_busca(self):
        left = ttk.LabelFrame(self.tab_busca, text="Busca Sequencial / Binária")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        right = ttk.LabelFrame(self.tab_busca, text="Saída")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.out_busca = scrolledtext.ScrolledText(right, height=22, wrap=tk.WORD, state="disabled")
        self.out_busca.pack(fill=tk.BOTH, expand=True)

        # Sequencial
        frm_seq = ttk.LabelFrame(left, text="Sequencial")
        frm_seq.pack(fill=tk.X, padx=8, pady=6)

        self.var_qtd_frag, _ = self._add_labeled_entry(frm_seq, "Qtd. fragmentos:", 10000)
        ttk.Button(frm_seq, text="Gerar fragmentos",
                   command=self._on_gerar_fragmentos).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(frm_seq, text="Sortear alvo e buscar",
                   command=self._on_busca_sequencial).pack(side=tk.LEFT, padx=4, pady=4)

        # Binária
        ttk.Separator(left).pack(fill=tk.X, pady=8)
        frm_bin = ttk.LabelFrame(left, text="Binária")
        frm_bin.pack(fill=tk.X, padx=8, pady=6)

        self.var_n_cat, _ = self._add_labeled_entry(frm_bin, "Qtd. catálogos:", 3)
        self.var_tam_cat, _ = self._add_labeled_entry(frm_bin, "Tam. catálogo:", 10000)

        ttk.Button(frm_bin, text="Gerar catálogos",
                   command=self._on_gerar_catalogos).pack(side=tk.LEFT, padx=4, pady=4)

        self.var_idx_cat = tk.StringVar(value="0")
        ttk.Label(frm_bin, text="Índice catálogo:").pack(side=tk.LEFT, padx=(8,4))
        ttk.Spinbox(frm_bin, from_=0, to=999, width=6, textvariable=self.var_idx_cat).pack(side=tk.LEFT, padx=4)

        self.var_alvo_bin, _ = self._add_labeled_entry(frm_bin, "Alvo (CAT-XXXXX):", "", width=22)
        ttk.Button(frm_bin, text="Sortear alvo desse catálogo",
                   command=self._on_sortear_alvo_catalogo).pack(side=tk.LEFT, padx=4)
        ttk.Button(frm_bin, text="Buscar binária",
                   command=self._on_busca_binaria).pack(side=tk.LEFT, padx=4)

    def _on_gerar_fragmentos(self):
        try:
            qtd = int(self.var_qtd_frag.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return
        alvo = self.modulo.gerar_fragmentos_aleatorios(qtd)
        self._append_text(self.out_busca, f"[Sequencial] {qtd} fragmentos gerados. Exemplo de alvo: {alvo}")

    def _on_busca_sequencial(self):
        if not self.modulo.fragmentos:
            self._append_text(self.out_busca, "Gere os fragmentos primeiro.")
            return
        alvo = random.choice(self.modulo.fragmentos)
        pos, comp = self.modulo.busca_sequencial(alvo)
        self._append_text(self.out_busca, f"[Sequencial] Alvo={alvo} | pos={pos} | comparações={comp}")

    def _on_gerar_catalogos(self):
        try:
            n = int(self.var_n_cat.get()); tam = int(self.var_tam_cat.get())
        except ValueError:
            messagebox.showerror("Erro", "Parâmetros inválidos.")
            return
        alvos = self.modulo.gerar_catalogos_ordenados(n, tam)
        self._append_text(self.out_busca, f"[Binária] {n} catálogos gerados (tam={tam}). Alvos sorteados: {alvos}")

    def _on_sortear_alvo_catalogo(self):
        try:
            i = int(self.var_idx_cat.get())
        except ValueError:
            messagebox.showerror("Erro", "Índice inválido.")
            return
        if i < 0 or i >= len(self.modulo.catalogos_ordenados):
            messagebox.showerror("Erro", "Índice fora do intervalo.")
            return
        alvo = random.choice(self.modulo.catalogos_ordenados[i])
        self.var_alvo_bin.set(alvo)
        self._append_text(self.out_busca, f"[Binária] Alvo sugerido para cat[{i}]: {alvo}")

    def _on_busca_binaria(self):
        try:
            i = int(self.var_idx_cat.get())
        except ValueError:
            messagebox.showerror("Erro", "Índice inválido.")
            return
        if i < 0 or i >= len(self.modulo.catalogos_ordenados):
            messagebox.showerror("Erro", "Índice fora do intervalo.")
            return
        alvo = self.var_alvo_bin.get().strip()
        if not alvo:
            messagebox.showwarning("Aviso", "Informe um alvo (ex.: CAT-12345).")
            return
        pos, comp = self.modulo.busca_binaria(self.modulo.catalogos_ordenados[i], alvo)
        self._append_text(self.out_busca, f"[Binária] cat[{i}] alvo={alvo} | pos={pos} | comps={comp}")

    # ------------------ Tab: Rabin–Karp ------------------
    def _build_tab_rk(self):
        top = ttk.Frame(self.tab_rk)
        top.pack(fill=tk.X, padx=8, pady=8)
        self.var_tam_tomo, _ = self._add_labeled_entry(top, "Tamanho do tomo:", 10000)
        self.var_qtd_padroes, _ = self._add_labeled_entry(top, "Qtd. padrões:", 3)
        ttk.Button(top, text="Carregar tomos e padrões", command=self._on_carregar_tomos).pack(side=tk.LEFT, padx=6)

        self.var_padrao = tk.StringVar(value="")
        ttk.Label(top, text="Padrão:").pack(side=tk.LEFT, padx=(12,4))
        ttk.Entry(top, textvariable=self.var_padrao, width=24).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Buscar (Rabin–Karp)", command=self._on_buscar_rk).pack(side=tk.LEFT, padx=6)

        right = ttk.LabelFrame(self.tab_rk, text="Saída")
        right.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.out_rk = scrolledtext.ScrolledText(right, height=22, wrap=tk.WORD, state="disabled")
        self.out_rk.pack(fill=tk.BOTH, expand=True)

    def _on_carregar_tomos(self):
        try:
            tam = int(self.var_tam_tomo.get()); qtd = int(self.var_qtd_padroes.get())
        except ValueError:
            messagebox.showerror("Erro", "Parâmetros inválidos.")
            return
        (texto,), padroes = self.modulo.carregar_tomos_e_marcas(tam, qtd)
        exemplo = random.choice(padroes) if padroes else ""
        self.var_padrao.set(exemplo)
        self._append_text(self.out_rk, f"Tomos carregados. Padrões: {padroes}")

    def _on_buscar_rk(self):
        if not self.modulo.tomos:
            self._append_text(self.out_rk, "Carregue os tomos primeiro.")
            return
        padrao = self.var_padrao.get().strip().upper()
        if not padrao:
            messagebox.showwarning("Aviso", "Informe um padrão (ex.: ABC).")
            return
        texto = self.modulo.tomos[0]
        pos, comp = self.modulo.busca_rabin_karp(texto, padrao)
        resumo = pos[:10]
        self._append_text(self.out_rk, f"Padrão: {padrao} | Ocorrências: {len(pos)} | Comparações: {comp} | primeiras pos: {resumo}")

    # ------------------ Tab: Huffman / Validador ------------------
    def _build_tab_huff(self):
        frm = ttk.Frame(self.tab_huff)
        frm.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left = ttk.LabelFrame(frm, text="Huffman")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        right = ttk.LabelFrame(frm, text="Validador de Palavras")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=4)

        # Huffman
        self.txt_huff_in = scrolledtext.ScrolledText(left, height=8, wrap=tk.WORD)
        self.txt_huff_in.pack(fill=tk.X, padx=8, pady=(8,4))
        btns = ttk.Frame(left); btns.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btns, text="Comprimir", command=self._on_huff_comprimir).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Descomprimir", command=self._on_huff_descomprimir).pack(side=tk.LEFT, padx=4)
        self.out_huff = scrolledtext.ScrolledText(left, height=14, wrap=tk.WORD, state="disabled")
        self.out_huff.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4,8))

        self._huff_last_bits = ""
        self._huff_last_table: Dict[str,str] = {}

        # Validador
        val_top = ttk.Frame(right); val_top.pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(val_top, text="Dicionário atual: FIRE, ICE, STONE, WOOD, WATER").pack(anchor="w")
        self.var_val_pal = tk.StringVar()
        row = ttk.Frame(right); row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Label(row, text="Palavra:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.var_val_pal, width=24).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="Validar", command=self._on_validar_palavra).pack(side=tk.LEFT, padx=6)
        self.out_val = scrolledtext.ScrolledText(right, height=20, wrap=tk.WORD, state="disabled")
        self.out_val.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _on_huff_comprimir(self):
        texto = self.txt_huff_in.get("1.0", tk.END).rstrip("\n")
        bits, tabela = self.comp_huff.comprimir(texto)
        self._huff_last_bits = bits
        self._huff_last_table = tabela
        self._append_text(self.out_huff, f"[Tabela] {tabela}")
        self._append_text(self.out_huff, f"[Codificado] {bits}")

    def _on_huff_descomprimir(self):
        if not self._huff_last_bits or not self._huff_last_table:
            self._append_text(self.out_huff, "Nada para descomprimir. Comprima algo primeiro.")
            return
        dec = self.comp_huff.descomprimir(self._huff_last_bits, self._huff_last_table)
        self._append_text(self.out_huff, f"[Decodificado] {dec}")

    def _on_validar_palavra(self):
        p = self.var_val_pal.get().strip()
        if not p:
            return
        ok = self.validador.validar(p)
        self._append_text(self.out_val, f"'{p.upper()}' -> {'SIM' if ok else 'NÃO'}")

    # ------------------ Tab: Levenshtein ------------------
    def _build_tab_lev(self):
        top = ttk.Frame(self.tab_lev); top.pack(fill=tk.X, padx=8, pady=8)
        self.var_lev_a, _ = self._add_labeled_entry(top, "Texto A:", "")
        self.var_lev_b, _ = self._add_labeled_entry(top, "Texto B:", "")
        ttk.Button(top, text="Calcular distância", command=self._on_lev_calc).pack(side=tk.LEFT, padx=6)

        self.chk_show_matrix = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text="Mostrar matriz (pode ser grande)", variable=self.chk_show_matrix).pack(side=tk.LEFT, padx=12)

        self.out_lev = scrolledtext.ScrolledText(self.tab_lev, height=26, wrap=tk.NONE, state="disabled")
        self.out_lev.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _on_lev_calc(self):
        s = self.var_lev_a.get()
        t = self.var_lev_b.get()
        dist, dp = self.modulo.distancia_edicao(s, t)
        self._append_text(self.out_lev, f"Distância entre '{s}' e '{t}': {dist}")
        if self.chk_show_matrix.get():
            linhas = []
            for row in dp:
                linhas.append(" ".join(f"{c:3d}" for c in row))
            self._append_text(self.out_lev, "\n".join(linhas))

    # ------------------ Tab: Grafos ------------------
    def _build_tab_grafos(self):
        left = ttk.LabelFrame(self.tab_grafos, text="Controles")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        right = ttk.LabelFrame(self.tab_grafos, text="Saída")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.out_g = scrolledtext.ScrolledText(right, height=28, wrap=tk.WORD, state="disabled")
        self.out_g.pack(fill=tk.BOTH, expand=True)

        # criação / básico
        frm1 = ttk.LabelFrame(left, text="Criar / Básico")
        frm1.pack(fill=tk.X, padx=6, pady=6)
        self.var_dirigido = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm1, text="Grafo direcionado", variable=self.var_dirigido).pack(anchor="w", padx=4, pady=2)
        ttk.Button(frm1, text="Criar novo grafo", command=self._on_g_criar).pack(fill=tk.X, padx=4, pady=4)

        # vértices
        frm2 = ttk.LabelFrame(left, text="Vértices")
        frm2.pack(fill=tk.X, padx=6, pady=6)
        self.var_vertice, _ = self._add_labeled_entry(frm2, "Vértice:", "", width=12)
        ttk.Button(frm2, text="Adicionar", command=self._on_g_add_v).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm2, text="Remover", command=self._on_g_rem_v).pack(fill=tk.X, padx=4, pady=2)

        # arestas
        frm3 = ttk.LabelFrame(left, text="Arestas")
        frm3.pack(fill=tk.X, padx=6, pady=6)
        self.var_u, _ = self._add_labeled_entry(frm3, "Origem:", "", width=10)
        self.var_v, _ = self._add_labeled_entry(frm3, "Destino:", "", width=10)
        self.var_w, _ = self._add_labeled_entry(frm3, "Peso:", 1, width=6)
        ttk.Button(frm3, text="Adicionar aresta", command=self._on_g_add_e).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm3, text="Remover aresta", command=self._on_g_rem_e).pack(fill=tk.X, padx=4, pady=2)

        # execuções
        frm4 = ttk.LabelFrame(left, text="Execuções")
        frm4.pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(frm4, text="Lista de adj.", command=self._on_g_lista).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm4, text="Matriz de adj.", command=self._on_g_matriz).pack(fill=tk.X, padx=4, pady=2)

        self.var_src, _ = self._add_labeled_entry(frm4, "Origem:", "", width=10)
        ttk.Button(frm4, text="DFS", command=self._on_g_dfs).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm4, text="BFS", command=self._on_g_bfs).pack(fill=tk.X, padx=4, pady=2)

        ttk.Separator(frm4).pack(fill=tk.X, pady=4)
        ttk.Button(frm4, text="Dijkstra (distâncias)", command=self._on_g_dijkstra).pack(fill=tk.X, padx=4, pady=2)
        self.var_target, _ = self._add_labeled_entry(frm4, "Alvo (reconstr.):", "", width=10)

        ttk.Separator(frm4).pack(fill=tk.X, pady=4)
        ttk.Button(frm4, text="Topológica (Kahn)", command=self._on_g_topo).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm4, text="Coloração (Welch-Powell)", command=self._on_g_color).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(frm4, text="AGM (Kruskal)", command=self._on_g_agm).pack(fill=tk.X, padx=4, pady=2)

        ttk.Separator(frm4).pack(fill=tk.X, pady=4)
        ttk.Button(frm4, text="Preencher DEMO", command=self._on_g_demo).pack(fill=tk.X, padx=4, pady=2)

    def _require_grafo(self) -> bool:
        if self.grafo is None:
            self._append_text(self.out_g, "Crie um grafo primeiro.")
            return False
        return True

    def _on_g_criar(self):
        self.grafo = Grafo(direcionado=self.var_dirigido.get())
        self._append_text(self.out_g, f"Novo grafo criado. Direcionado={self.grafo.dir}")

    def _on_g_add_v(self):
        if not self._require_grafo(): return
        v = self.var_vertice.get().strip()
        if not v: return
        self.grafo.adicionar_vertice(v)
        self._append_text(self.out_g, f"Vértice '{v}' adicionado.")

    def _on_g_rem_v(self):
        if not self._require_grafo(): return
        v = self.var_vertice.get().strip()
        if not v: return
        self.grafo.remover_vertice(v)
        self._append_text(self.out_g, f"Vértice '{v}' removido.")

    def _on_g_add_e(self):
        if not self._require_grafo(): return
        u = self.var_u.get().strip(); v = self.var_v.get().strip()
        if not u or not v:
            return
        try:
            w = int(self.var_w.get())
        except ValueError:
            messagebox.showerror("Erro", "Peso inválido.")
            return
        self.grafo.adicionar_aresta(u, v, w)
        self._append_text(self.out_g, f"Aresta {u} -> {v} (w={w}) adicionada.")

    def _on_g_rem_e(self):
        if not self._require_grafo(): return
        u = self.var_u.get().strip(); v = self.var_v.get().strip()
        if not u or not v:
            return
        self.grafo.remover_aresta(u, v)
        self._append_text(self.out_g, f"Aresta {u} - {v} removida.")

    def _on_g_lista(self):
        if not self._require_grafo(): return
        self._append_text(self.out_g, self.grafo.formatar_lista())

    def _on_g_matriz(self):
        if not self._require_grafo(): return
        self._append_text(self.out_g, self.grafo.formatar_matriz())

    def _on_g_dfs(self):
        if not self._require_grafo(): return
        s = self.var_src.get().strip()
        ordem = self.grafo.dfs(s)
        self._append_text(self.out_g, f"DFS({s}): {ordem}")

    def _on_g_bfs(self):
        if not self._require_grafo(): return
        s = self.var_src.get().strip()
        ordem, dist = self.grafo.bfs(s)
        self._append_text(self.out_g, f"BFS({s}): {ordem} | dist: {dist}")

    def _on_g_dijkstra(self):
        if not self._require_grafo(): return
        s = self.var_src.get().strip()
        try:
            dist, prev = self.grafo.dijkstra(s)
        except ValueError as e:
            self._append_text(self.out_g, str(e))
            return
        self._append_text(self.out_g, f"Dijkstra({s}) distâncias: {dist}")
        alvo = self.var_target.get().strip()
        if alvo:
            caminho = Grafo.reconstruir_caminho(prev, alvo)
            self._append_text(self.out_g, f"Caminho {s} -> {alvo}: {caminho}")

    def _on_g_topo(self):
        if not self._require_grafo(): return
        try:
            ordem = self.grafo.topologica_kahn()
            if ordem is None:
                self._append_text(self.out_g, "O grafo possui ciclo; topológica impossível.")
            else:
                self._append_text(self.out_g, f"Ordem topológica: {ordem}")
        except ValueError as e:
            self._append_text(self.out_g, str(e))

    def _on_g_color(self):
        if not self._require_grafo(): return
        cores = self.grafo.coloracao_welch_powell()
        self._append_text(self.out_g, f"Coloração (v->cor): {cores} | nº cores={len(set(cores.values()))}")

    def _on_g_agm(self):
        if not self._require_grafo(): return
        try:
            mst, total = self.grafo.agm_kruskal()
            self._append_text(self.out_g, f"AGM (Kruskal): {mst}\nCusto total: {total}")
        except ValueError as e:
            self._append_text(self.out_g, str(e))

    def _on_g_demo(self):
        if not self._require_grafo(): return
        edges = [
            ("A","B",4),("A","C",2),("B","C",5),("B","D",10),
            ("C","E",3),("E","D",4),("D","F",11)
        ]
        for u, v, w in edges:
            self.grafo.adicionar_aresta(u, v, w)
        self._append_text(self.out_g, "DEMO carregada. Use DFS/BFS/Dijkstra/Topológica/Coloração/AGM etc.")

    # ------------------ Tab: Gulosos ------------------
    def _build_tab_gulosos(self):
        container = ttk.Frame(self.tab_gulosos)
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Troco
        gb1 = ttk.LabelFrame(container, text="Troco (Greedy)")
        gb1.pack(fill=tk.X, padx=6, pady=6)
        self.var_troco_valor, _ = self._add_labeled_entry(gb1, "Valor (inteiro):", 289)
        self.var_troco_moedas, _ = self._add_labeled_entry(gb1, "Moedas (csv):", "100,50,20,10,5,2,1", width=32)
        ttk.Button(gb1, text="Calcular troco", command=self._on_troco).pack(side=tk.LEFT, padx=6)

        # Interval Scheduling
        gb2 = ttk.LabelFrame(container, text="Escalonamento de Intervalos")
        gb2.pack(fill=tk.X, padx=6, pady=6)
        self._intervalos: List[Tuple[int,int,str]] = []
        self.var_int_ini, _ = self._add_labeled_entry(gb2, "Início:", 1, width=8)
        self.var_int_fim, _ = self._add_labeled_entry(gb2, "Fim:", 4, width=8)
        self.var_int_nome, _ = self._add_labeled_entry(gb2, "Nome:", "T1", width=10)
        ttk.Button(gb2, text="Adicionar tarefa", command=self._on_add_intervalo).pack(side=tk.LEFT, padx=6)
        ttk.Button(gb2, text="Selecionar maximamente compatíveis", command=self._on_run_intervalos).pack(side=tk.LEFT, padx=6)

        # Mochila Fracionária
        gb3 = ttk.LabelFrame(container, text="Mochila Fracionária")
        gb3.pack(fill=tk.X, padx=6, pady=6)
        self._itens: List[Tuple[float,float,str]] = []
        self.var_cap, _ = self._add_labeled_entry(gb3, "Capacidade:", 15, width=8)
        self.var_item_val, _ = self._add_labeled_entry(gb3, "Valor:", 10, width=8)
        self.var_item_peso, _ = self._add_labeled_entry(gb3, "Peso:", 5, width=8)
        self.var_item_nome, _ = self._add_labeled_entry(gb3, "Nome:", "Ouro", width=10)
        ttk.Button(gb3, text="Adicionar item", command=self._on_add_item).pack(side=tk.LEFT, padx=6)
        ttk.Button(gb3, text="Resolver mochila", command=self._on_run_mochila).pack(side=tk.LEFT, padx=6)

        # saída
        outf = ttk.LabelFrame(container, text="Saída")
        outf.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.out_gulosos = scrolledtext.ScrolledText(outf, height=14, wrap=tk.WORD, state="disabled")
        self.out_gulosos.pack(fill=tk.BOTH, expand=True)

    def _on_troco(self):
        try:
            valor = int(self.var_troco_valor.get())
            moedas = [int(x.strip()) for x in self.var_troco_moedas.get().split(",") if x.strip()]
        except Exception:
            messagebox.showerror("Erro", "Parâmetros inválidos.")
            return
        sol = Gulosos.troco_guloso(valor, moedas)
        total = sum(k*v for k, v in sol.items())
        msg = (f"Solução: {sol} | soma={total}" +
               ("" if total == valor else " (sistema não canônico: pode sobrar)"))
        self._append_text(self.out_gulosos, "[Troco] " + msg)

    def _on_add_intervalo(self):
        try:
            ini = int(self.var_int_ini.get()); fim = int(self.var_int_fim.get())
            nome = self.var_int_nome.get().strip() or f"T{len(self._intervalos)+1}"
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")
            return
        if fim < ini:
            messagebox.showwarning("Atenção", "Fim deve ser >= início.")
            return
        self._intervalos.append((ini, fim, nome))
        self._append_text(self.out_gulosos, f"[Intervalos] Adicionado: ({ini},{fim},{nome})")

    def _on_run_intervalos(self):
        if not self._intervalos:
            self._append_text(self.out_gulosos, "[Intervalos] Adicione tarefas primeiro.")
            return
        escolhidos = Gulosos.interval_scheduling_greedy(self._intervalos)
        self._append_text(self.out_gulosos, f"[Intervalos] Selecionadas ({len(escolhidos)}): {escolhidos}")

    def _on_add_item(self):
        try:
            v = float(self.var_item_val.get()); p = float(self.var_item_peso.get())
            nome = self.var_item_nome.get().strip() or f"I{len(self._itens)+1}"
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")
            return
        self._itens.append((v, p, nome))
        self._append_text(self.out_gulosos, f"[Mochila] Item adicionado: (v={v}, p={p}, nome={nome})")

    def _on_run_mochila(self):
        if not self._itens:
            self._append_text(self.out_gulosos, "[Mochila] Adicione itens primeiro.")
            return
        try:
            cap = float(self.var_cap.get())
        except ValueError:
            messagebox.showerror("Erro", "Capacidade inválida.")
            return
        total, comp = Gulosos.fractional_knapsack(cap, self._itens)
        self._append_text(self.out_gulosos, f"[Mochila] Valor total: {total:.4f} | composição: {comp}")

# ===========================================
#        Ponto de entrada
# ===========================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
