# Dungeon of Words - Módulo 2: Otimização de Recursos - Espaço é Poder

Este módulo faz parte do projeto Dungeon of Words e traz implementações para otimização de armazenamento e acesso a dados. 

Ele contempla:

- **Compressão de Dados** usando os algoritmos Run-Length Encoding (RLE) e Huffman.
- **Tabela Hash** com múltiplas funções de hash (multiplicação, meio-quadrado, extração, transformação da raiz), com tratamento de colisões via encadeamento.

---

## Funcionalidades principais

### Compressão de Dados

- **RLE (Run-Length Encoding):** compacta sequências repetidas de caracteres em formato `<caractere><quantidade>`.
- **Huffman:** cria códigos binários baseados na frequência de caracteres, gerando compressão eficiente para textos variados.

### Tabela Hash

- Suporta quatro funções de hash configuráveis:
  - Multiplicação
  - Meio-Quadrado
  - Extração
  - Transformação da Raiz
- Implementa encadeamento para resolver colisões.
- Permite inserir e buscar fragmentos através de uma chave.

---
