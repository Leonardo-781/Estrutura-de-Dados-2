# Dungeon of Words – O Arquivista Desesperado


---

## 📌 Visão Geral

O **Dungeon of Words** é um programa em Python (console) que reúne implementações clássicas para fins didáticos e de apresentação:

* **Buscas**: Sequencial, Binária, Rabin–Karp
* **Compressão/Hash**: Huffman (mínimo funcional), Validador por conjunto (hash set)
* **Programação Dinâmica**: Distância de Edição (Levenshtein)
* **Grafos**: Lista e Matriz de adjacências, **DFS**, **BFS**, **Dijkstra**, **Ordenação Topológica (Kahn)**, **Coloração (Welch–Powell)**, **Árvore Geradora Mínima (Kruskal)**
* **Gulosos**: Troco, Escalonamento de Intervalos, Mochila Fracionária

Inclui **submenu de Grafos** e **submenu de Gulosos**, além de uma opção para **preencher um grafo de demonstração**.

---

## 🧩 Recursos

* Menus com entradas guiadas
* Representações de grafo (lista + matriz sob demanda)
* Dijkstra protegido contra pesos negativos
* Modo **demo** para grafos
* Exemplos reproduzíveis e notas de complexidade

---

## ⚙️ Requisitos

* **Python 3.8+**
* Sem dependências externas (somente biblioteca padrão)

### Instalação opcional de ambiente virtual

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

---

## ▶️ Como Executar

1. Salve o código como `dungeon_of_words.py` (ou outro nome).
2. Execute:

```bash
python dungeon_of_words.py
```

Você verá o **menu principal**:

```
[1] Iniciar o Módulo de Busca Completo
[2] Executar Desafio 1: Busca Sequencial
[3] Executar Desafio 2: Busca Binária
[4] Executar Desafio 3: Rabin-Karp
[5] Testar Compressão Huffman
[6] Testar Validação de Palavras
[7] Distância de Edição (Levenshtein)  (PD)
[8] Fase 3: Grafos ⚙️
[9] Etapa 4: Algoritmos Gulosos ⚡ (Troco, Intervalos, Mochila Frac.)
[10] Sair da Masmorra
```

---

## 🗂️ Mapa do Código (Arquitetura)

* `ModuloBusca`: busca sequencial/binária; Rabin–Karp; Levenshtein (PD)
* `CompactadorHuffman`: compressão e descompressão mínima (didática)
* `ValidadorPalavras`: verificação rápida via conjunto (hash set)
* `Gulosos`: Troco (greedy), Interval Scheduling, Mochila Fracionária
* `Grafo`: lista de adjacências (`dict[str, dict[str,int]]`), geração de matriz, DFS/BFS, Dijkstra, Topológica (Kahn), Coloração (Welch–Powell), AGM (Kruskal)
* `preencher_demo(grafo)`: popula um mapa de exemplo para apresentações

---

## 📚 Uso (com Exemplos)

### 1) Busca Sequencial

Gera 10.000 fragmentos e procura um alvo existente.

```
DESAFIO 1: Busca Sequencial
Alvo escolhido: FRAG-48213
Posição: 7342, Comparações: 7343
```

### 2) Busca Binária

Cria 3 catálogos ordenados e busca alvos existentes.

```
DESAFIO 2: Busca Binária
Cat 0: alvo=CAT-65123 pos=437 comps=14
Cat 1: alvo=CAT-71234 pos=902 comps=13
Cat 2: alvo=CAT-84567 pos=1234 comps=14
```

### 3) Rabin–Karp

Procura um padrão aleatório (3–7 letras) em um “tomo” de texto grande.

```
DESAFIO 3: Rabin-Karp
Padrao: QWE | Ocorrências: 5 | Comparações: 99994
```

### 4) Compressão de Huffman

```
Digite um texto para comprimir: ABRACADABRA
Tabela: {'A': '0', 'B': '111', 'R': '110', 'C': '101', 'D': '100'}
Codificado: 0 111 110 0 101 0 100 0 111 110 0
Decodificado: ABRACADABRA
```

### 5) Validador de Palavras (Hash Set)

```
Palavra para validar: wood
Existe?  Sim
```

### 6) Distância de Edição (Levenshtein)

```
DESAFIO (PD): Distância de Edição (Levenshtein)
Digite a 1ª palavra/frase: GATO
Digite a 2ª palavra/frase: PATO

Distância de edição entre 'GATO' e 'PATO': 1
```

---

## 🌐 Fase 3: Grafos (submenu)

Abra `[8]` para o **submenu de Grafos**:

```
[1] Criar novo grafo
[2] Adicionar vértice
[3] Remover vértice
[4] Adicionar aresta
[5] Remover aresta
[6] Mostrar lista de adjacências
[7] Mostrar matriz de adjacência
[8] DFS
[9] BFS
[10] Dijkstra
[11] Ordenação Topológica (Kahn)
[12] Coloração (Welch-Powell)
[13] AGM (Kruskal)
[14] Preencher grafo de demonstração
[0] Voltar
```

### Criar grafo e preencher demo (recomendado)

```
[1] Criar novo grafo
Grafo direcionado? (s/n): n
Grafo criado.

[14] Preencher grafo de demonstração
Demo carregada. Use DFS/BFS/Dijkstra etc.
```

**Arestas do demo (não-direcionado):**

```
A-B(4), A-C(2), B-C(5), B-D(10), C-E(3), E-D(4), D-F(11)
```

### Visualizações

**Lista de adjacências**

```
[6] Mostrar lista de adjacências

A -> B(4), C(2)
B -> A(4), C(5), D(10)
C -> A(2), B(5), E(3)
D -> B(10), E(4), F(11)
E -> C(3), D(4)
F -> D(11)
```

**Matriz de adjacência**

```
[7] Mostrar matriz de adjacência

[Matriz de Adjacência] (ordem de vértices: ['A', 'B', 'C', 'D', 'E', 'F'] )
  0   4   2   0   0   0
  4   0   5  10   0   0
  2   5   0   0   3   0
  0  10   0   0   4  11
  0   0   3   4   0   0
  0   0   0  11   0   0
```

### DFS

```
[8] DFS
Origem: A
DFS: ['A', 'B', 'C', 'E', 'D', 'F']
```

### BFS

```
[9] BFS
Origem: A
BFS: ['A', 'B', 'C', 'D', 'E', 'F']
Distâncias (saltos): {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 3}
```

### Dijkstra (custos mínimos)

```
[10] Dijkstra
Origem: A
Distâncias: {'A': 0, 'B': 4, 'C': 2, 'D': 9, 'E': 5, 'F': 20}
Reconstruir caminho até (opcional): F
Caminho: ['A', 'C', 'E', 'D', 'F']
```

> Observação: Dijkstra **exige pesos ≥ 0** (o programa valida).

### Ordenação Topológica (Kahn) — **DAG**

```
[1] Criar novo grafo
Grafo direcionado? (s/n): s
[4] Adicionar aresta  A -> B
[4] Adicionar aresta  B -> C
[11] Ordenação Topológica (Kahn)
Ordem topológica: ['A', 'B', 'C']
```

### Coloração (Welch–Powell)

```
[12] Coloração (Welch-Powell)
Coloração (vértice -> cor): {'B': 1, 'D': 2, 'C': 3, 'A': 2, 'E': 1, 'F': 3} | nº de cores: 3
```

### AGM (Kruskal)

```
[13] AGM (Kruskal)
AGM (Kruskal): [('A', 'C', 2), ('C', 'E', 3), ('A', 'B', 4), ('E', 'D', 4), ('D', 'F', 11)]
Custo total: 24
```

---

## ⚡ Etapa 4: Algoritmos Gulosos (submenu)

Abra `[9]`:

```
[1] Problema do Troco (greedy)
[2] Escalonamento de Intervalos (greedy)
[3] Mochila Fracionária (greedy)
[4] Mostrar complexidades e notas
[0] Voltar
```

### Troco (Greedy)

```
Valor do troco (inteiro, ex.: 289): 289
Moedas/cédulas disponíveis (ex.: 100,50,20,10,5,2,1): 100,50,20,10,5,2,1
Solução ótima: {100: 2, 50: 1, 20: 1, 10: 1, 5: 1, 2: 2} | soma=289
```

> Em sistemas **não canônicos** o greedy pode não fechar exato — o programa avisa.

### Escalonamento de Intervalos

```
Quantidade de tarefas (ex.: 6): 6
Tarefa 1 (inicio,fim,nome): 1,4,T1
Tarefa 2: 3,5,T2
Tarefa 3: 0,6,T3
Tarefa 4: 5,7,T4
Tarefa 5: 8,9,T5
Tarefa 6: 5,9,T6
Selecionadas (3): [(1, 4, 'T1'), (5, 7, 'T4'), (8, 9, 'T5')]
```

### Mochila Fracionária

```
Capacidade (ex.: 15): 15
Quantidade de itens (ex.: 3): 3
Item 1 (valor,peso,nome): 10,5,Ouro
Item 2 (valor,peso,nome): 7,7,Prata
Item 3 (valor,peso,nome): 6,6,Bronze

Valor total: 23.4000
Composição (nome, fração): [('Ouro', 1.0), ('Prata', 1.0), ('Bronze', 0.5)]
```

---

## ⏱️ Complexidades (Big-O)

| Algoritmo                | Tempo                 | Observações                     |   |   |   |       |
| ------------------------ | --------------------- | ------------------------------- | - | - | - | ----- |
| Busca Sequencial         | O(n)                  | —                               |   |   |   |       |
| Busca Binária            | O(log n)              | vetor ordenado                  |   |   |   |       |
| Rabin–Karp               | O(n + m) amortizado   | rolling hash                    |   |   |   |       |
| Huffman (construção)     | O(k log k)            | k = nº de símbolos com freq > 0 |   |   |   |       |
| Validador (hash set)     | O(1) média (consulta) | —                               |   |   |   |       |
| Levenshtein              | O(                    | s                               | · | t | ) | DP 2D |
| DFS / BFS                | O(V + E)              | —                               |   |   |   |       |
| Dijkstra (min-heap)      | O((V + E) log V)      | pesos **≥ 0**                   |   |   |   |       |
| Topológica (Kahn)        | O(V + E)              | DAG                             |   |   |   |       |
| Coloração (Welch–Powell) | \~O(V²)               | heurística                      |   |   |   |       |
| AGM (Kruskal)            | O(E log E)            | DSU                             |   |   |   |       |
| Troco (greedy)           | O(k log k) + O(k)     | ótimo em sistemas canônicos     |   |   |   |       |
| Interval Scheduling      | O(n log n)            | ordena por fim                  |   |   |   |       |
| Mochila Fracionária      | O(n log n)            | ordena por valor/peso           |   |   |   |       |

---

## 🧪 Demonstrações Reproduzíveis

### Dijkstra no grafo demo

1. `[8] Grafos` → `[1]` **não-direcionado**
2. `[14]` Preencher demo
3. `[10]` Dijkstra → Origem `A` → Reconstruir até `F`

**Saída esperada:**

```
Distâncias: {'A': 0, 'B': 4, 'C': 2, 'D': 9, 'E': 5, 'F': 20}
Caminho: ['A', 'C', 'E', 'D', 'F']
```

### Ordenação Topológica

1. `[8] Grafos` → `[1]` **direcionado**
2. Arestas: `A->B`, `B->C`, `A->C`
3. `[11]` Topológica (Kahn)

**Saída esperada:**

```
Ordem topológica: ['A', 'B', 'C']
```

### Coloração em grafo completo K4

1. Crie vértices `V1..V4`
2. Conecte todos com todos
3. `[12]` Coloração

**Saída esperada:** 4 cores (mapeamento qualquer 1..4).

---

## 🧠 Boas Práticas e Decisões

* **Grafo** principal em **lista de adjacências** para eficiência em grafos esparsos; **matriz** gerada apenas para visualização.
* **Dijkstra** valida pesos (não aceita negativos).
* **Huffman** minimalista, adequado para demonstração (sem I/O binária).
* Entradas guiadas por **menus** para facilitar a apresentação.

---

## 🚀 Como Estender

* **Bellman–Ford** (pesos negativos)
* **Floyd–Warshall** (todos os pares)
* AGMs adicionais: **Prim**, **Borůvka**, **Exclusão Reversa**
* **Reconstrução de operações** no Levenshtein
* **Salvar/Carregar** grafos (JSON)
* Visualização com `networkx`/`matplotlib` (opcional)

---

## 🐞 Problemas Comuns

* **Dijkstra com peso negativo** → erro: “Dijkstra requer pesos não negativos.”
* **Troco não fecha exato** → sistema de moedas não canônico; use PD para solução ótima geral.
* **Topológica em grafo não-direcionado/cíclico** → impossível; precisa ser **DAG**.

---

## 📜 Licença

Use como quiser (Nada se cria. O negócio é copiar) by: Xuxa 2006
