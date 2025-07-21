# Dungeon of Words – Módulo 2: Espaço é Poder

## 📦 Descrição do Projeto
Este projeto é parte da Fase 2 do *Dungeon of Words*, com foco na otimização de espaço e desempenho usando algoritmos de **compressão** e **hashing**. Ele inclui também buscas eficientes em grandes conjuntos de dados.

O código permite testar e visualizar os seguintes algoritmos:
- **Busca Sequencial, Binária e Rabin-Karp**
- **Compressão e Descompressão (Huffman e RLE)**
- **Hashing com funções Extração e Transformação da Raiz**

## 📂 Estrutura do Projeto
```
📁 dungeon_of_words/
├── main.py          # Código-fonte principal com todos os módulos
├── README.md        # Documentação do projeto
```

## 🚀 Como Executar
1. Clone o repositório ou copie os arquivos.
2. Execute o arquivo `main.py` com Python 3:
   ```bash
   python main.py
   ```
3. Siga o menu interativo para explorar cada módulo.

## 🧠 Algoritmos Implementados
### 🔍 Módulo de Busca
| Algoritmo         | Complexidade     |
|-------------------|------------------|
| Busca Sequencial  | O(n)             |
| Busca Binária     | O(log n)         |
| Rabin-Karp        | O(n + m)         |

### 📦 Módulo de Compressão
| Algoritmo           | Complexidade   |
|---------------------|----------------|
| Huffman (compressão)| O(n log n)     |
| Huffman (decompress)| O(n)           |
| RLE (compressão)    | O(n)           |
| RLE (decompressão)  | O(n)           |

### 🗄️ Módulo de Hashing
| Função Hash               | Complexidade Inserção/Busca |
|---------------------------|-----------------------------|
| Extração                  | O(1) média / O(n) pior caso |
| Transformação da Raiz     | O(1) média / O(n) pior caso |

**Tratamento de colisão:** Encadeamento (listas ligadas)

## 🖥️ Funcionalidades Interativas
- **Busca**:
  - Teste os algoritmos com dados gerados aleatoriamente.
- **Compressão**:
  - Insira um texto e veja a redução de tamanho com Huffman e RLE.
- **Hashing**:
  - Insira ou busque pares chave-valor.
  - Simule a inserção de 1000+ elementos e veja estatísticas de colisões.

## 📊 Exemplo de Saída
```
DESAFIO 1: Busca Sequencial
Fragmento encontrado em 5432 após 102 comparações.
Tempo gasto: 0.000234 segundos
Complexidade teórica (sequencial): O(n)
```

## 🔗 Dependências
- Python 3.x
- Bibliotecas padrão (`random`, `time`, `heapq`, `collections`)

## 👨‍💻 Autoria
Projeto desenvolvido para a disciplina **Estruturas de Dados II**.

---
⚡ **Dungeon of Words – sua jornada de otimização começa aqui!**
