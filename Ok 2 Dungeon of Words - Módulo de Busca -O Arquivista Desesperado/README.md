
# 🏰 Dungeon of Words – Módulo 1: O Arquivista Desesperado

**Trabalho de Estruturas de Dados II – 2025**  
**Autor:** Leonardo Cardoso  

---

## 📖 Sobre o Projeto

Este projeto faz parte do jogo educacional **Dungeon of Words**, que visa ensinar e demonstrar algoritmos clássicos de busca, compressão e validação de dados através de uma narrativa interativa.  

Neste módulo, **“O Arquivista Desesperado”**, o jogador assume o papel de um Guardião dos Dados que precisa restaurar a ordem em uma biblioteca digital caótica, atingida pelo Vazio.  

---

## 🎮 Fases e Algoritmos

O módulo é dividido em 3 desafios principais e 2 testes extras:

---

### 🔥 Desafio 1: A Pilha de Pergaminhos Desorganizados
**📝 Algoritmo:** Busca Sequencial (Linear Search)  
- Percorre uma lista aleatória de **Fragmentos de Conhecimento** para encontrar um **Pergaminho Vital**.  
- Exibe número de comparações e tempo de execução.  
- **Complexidade:** `O(n)`  

---

### ⚡ Desafio 2: Os Catálogos Ordenados
**📝 Algoritmo:** Busca Binária (Binary Search)  
- Fragmentos agora estão organizados em **Catálogos Digitais** (listas ordenadas).  
- O Guardião precisa localizar rapidamente vários IDs.  
- **Complexidade:** `O(log n)`  

---

### 🩸 Desafio 3: Decifrando os Códigos do Vazio
**📝 Algoritmo:** Rabin-Karp Matcher  
- Busca por **Marcas de Corrupção** (padrões curtos) em grandes **Tomos Antigos** (strings enormes).  
- Exibe todas as ocorrências encontradas.  
- **Complexidade:** `O(n + m)` no melhor caso, onde *n* é o tamanho do texto e *m* do padrão.  

---

### 🗜️ Teste Extra: Compressão Huffman
**📝 Algoritmo:** Huffman Coding  
- Compacta textos usando árvores de Huffman.  
- Também realiza descompressão e calcula taxa de compressão.  
- **Complexidade:** `O(n log n)` para construir a árvore.  

---

### 🏷️ Teste Extra: Validação de Palavras
**📝 Estrutura:** Tabela Hash  
- Valida se uma palavra pertence ao dicionário do Guardião.  
- Utiliza função de hash simples com resolução por encadeamento.  
- **Complexidade:** `O(1)` busca média, `O(n)` pior caso (colisões).  

---

## 🏗️ Arquitetura do Código

| Classe               | Função                                                    |
|----------------------|------------------------------------------------------------|
| `SearchModule`       | Contém Busca Sequencial, Busca Binária e Rabin-Karp        |
| `HuffmanCompressor`  | Comprime e descomprime textos com algoritmo de Huffman     |
| `WordValidator`      | Valida palavras com hash table                             |
| `main_menu()`        | Interface principal do jogo                                |
| `desafio1(), desafio2(), desafio3()` | Mini-jogos temáticos com narrativa integrada |

---

## 🚀 Como Executar

### ✅ Requisitos
- Python 3.x  
- (Opcional) Terminal que suporte UTF-8 para exibir os caracteres especiais.

### ▶️ Rodando o jogo
```bash
python3 arquivista_desesperado.py
```

Siga o menu interativo para jogar os desafios ou testar os algoritmos.

---

## 📊 Análise de Complexidade

| Algoritmo             | Complexidade (Big O) |
|-----------------------|-----------------------|
| Busca Sequencial      | `O(n)`               |
| Busca Binária         | `O(log n)`           |
| Rabin-Karp Matcher    | `O(n + m)`           |
| Compressão Huffman    | `O(n log n)`         |
| Validação com Hashing | `O(1)` média, `O(n)` pior caso |

---

## 🌟 Destaques
- Narrativa integrada ao aprendizado (RPG com algoritmos)
- Métricas exibidas em tempo real (comparações, tempo)
- Modularidade permite uso dos algoritmos isoladamente

---

## 📁 Estrutura do Projeto
```
DungeonOfWords/
├── arquivista_desesperado.py   # Código principal
├── README.md                   # Este arquivo
```

---



