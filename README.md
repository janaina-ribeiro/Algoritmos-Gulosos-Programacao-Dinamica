# Algoritmos — PAA: Guloso e Programação Dinâmica
Implementação e análise de dois algoritmos clássicos:

| Algoritmo | Paradigma | Arquivo |
|---|---|---|
| **Huffman Coding** | Algoritmo Guloso | `huffman-coding/huffman_main.py` |
| **Longest Increasing Subsequence** | Programação Dinâmica | |

---

## Estrutura do Projeto

```
Algoritmo-PAA/
├── huffman-coding/
│   ├── huffman_main.py      # pipeline completo: build → encode → decode
│   └── huffman_node.py      # nó da árvore binária de Huffman
├── huffman_output.txt        # saída gerada pelas instâncias de teste
├── EXPLICACAO.md             # documentação matemática detalhada
└── README.md
```

---

## Como Executar

1 - Huffman Coding:
```bash
cd huffman-coding
python huffman_main.py

```
A saída detalhada de cada instância de teste, incluindo tabelas de frequência, códigos gerados, texto codificado e estatísticas de compressão, será salva em `huffman_output.txt`.

2 - Longest Increasing Subsequence:


## 1. Huffman Coding — Algoritmo Guloso

### 1.1 O que é?

**Huffman Coding** é um algoritmo de compressão sem perda (*lossless*), proposto por **David A. Huffman** em 1952. Ele gera um **código de prefixo livre ótimo**: símbolos mais frequentes recebem códigos mais curtos, e nenhum código é prefixo de outro, garantindo decodificação unívoca.

É amplamente utilizado em ZIP, PNG, JPEG, MP3 e na maioria dos compressores modernos.

### 1.2 Por que é Guloso?

A **escolha gulosa** consiste em, a cada passo, fundir os **dois nós de menor frequência** da fila de prioridade. Essa decisão local ótima — comprovada por um argumento de troca formal (CLRS, Cap. 16) — leva à solução globalmente ótima: a árvore de menor comprimento médio ponderado.

```
Força Bruta  →  explora TODAS as árvores possíveis       (exponencial)
Guloso       →  decide localmente, nunca volta atrás     (O(n log n))
```

### 1.3 O Algoritmo — Pseudocódigo

```
HUFFMAN(C):
  Q ← min-heap com um nó-folha por símbolo (ordenado por frequência)

  enquanto |Q| > 1:
    x ← EXTRACT-MIN(Q)          ← escolha gulosa 1
    y ← EXTRACT-MIN(Q)          ← escolha gulosa 2
    z ← novo nó interno
    z.freq  ← x.freq + y.freq
    z.left  ← x
    z.right ← y
    INSERT(Q, z)

  retorna EXTRACT-MIN(Q)         ← raiz da árvore
```

### 1.4 Exemplo Passo a Passo — `"ABRACADABRA"`

**Frequências:**

| Símbolo | A | B | R | C | D |
|---|---|---|---|---|---|
| Frequência | 5 | 2 | 2 | 1 | 1 |

**Construção da árvore (heap):**

```
Inicial  : [C:1, D:1, B:2, R:2, A:5]

Iter 1   : funde C(1) + D(1) → CD:2
           heap: [B:2, R:2, CD:2, A:5]

Iter 2   : funde B(2) + R(2) → BR:4
           heap: [CD:2, A:5, BR:4]

Iter 3   : funde CD(2) + BR(4) → CDBR:6
           heap: [A:5, CDBR:6]

Iter 4   : funde A(5) + CDBR(6) → Raiz:11
```

**Árvore resultante:**

```
           [11]
          /    \
       [A:5]  [CDBR:6]
              /       \
           [BR:4]   [CD:2]
           /    \   /    \
         [B:2][R:2][C:1][D:1]
```

**Tabela de códigos gerada:**

| Símbolo | Freq | Código | Bits |
|---|---|---|---|
| A | 5 | `0`   | 1 |
| B | 2 | `100` | 3 |
| R | 2 | `101` | 3 |
| C | 1 | `110` | 3 |
| D | 1 | `111` | 3 |

**Compressão:**
$$5{\times}1 + 2{\times}3 + 2{\times}3 + 1{\times}3 + 1{\times}3 = 23 \text{ bits}$$
versus ASCII: $11 \times 8 = 88$ bits → **73,86% de compressão**.

### 1.5 Implementação

#### `huffman_node.py` — Nó da Árvore

```python
class HuffmanNode:
    def __init__(self, char, freq):
        self.char  = char    
        self.freq  = freq    
        self.left  = None    
        self.right = None    

    def __lt__(self, other):
        return self.freq < other.freq   
```

#### `huffman_main.py` — Pipeline Completo

| Função | Responsabilidade |
|---|---|
| `construir_arvore_huffman(text)` | Conta frequências com `Counter`, monta min-heap, executa as fusões gulosas e retorna a raiz |
| `gerar_codigos(node, prefix, codes)` | DFS recursiva na árvore: `'0'` para esquerda, `'1'` para direita; grava código ao atingir folha |
| `codificar(text, codes)` | Substitui cada caractere pelo seu código Huffman; retorna string de bits |
| `decodificar(encoded, root)` | Percorre os bits navegando na árvore; ao atingir folha, registra o caractere e volta à raiz |
| `compressao_stats(text, encoded)` | Calcula bits originais (8×n), bits comprimidos e taxa de compressão |
| `run_test(...)` | Executa o pipeline em uma instância, mede tempo com `perf_counter` e escreve em arquivo |

**Decodificação — funcionamento:**

```python
for bit in encoded:
    current = current.left if bit == '0' else current.right
    if current.char is not None:   
        decoded.append(current.char)
        current = root            
```

A propriedade de prefixo livre garante que nunca há ambiguidade: ao atingir uma folha, sabemos exatamente qual símbolo foi decodificado.

### 1.6 Complexidade

| Etapa | Custo |
|---|---|
| Contagem de frequências (`Counter`) | $O(N)$ |
| Construção do heap (`heapify`) | $O(n)$ |
| Loop de fusões ($n-1$ iterações × 2 `EXTRACT-MIN` + 1 `INSERT`) | $O(n \log n)$ |
| Geração de códigos (DFS) | $O(n)$ |
| Codificação / Decodificação | $O(N)$ |
| **Total** | $\boldsymbol{O(N + n \log n)}$ |

onde $N$ = tamanho do texto e $n$ = número de símbolos distintos.  
Como $n \ll N$ na prática, o gargalo é $O(N)$.

**Otimalidade:** o comprimento médio $L$ satisfaz $H \leq L < H + 1$, onde $H = -\sum p_i \log_2 p_i$ é a entropia de Shannon. Huffman nunca desperdiça mais de 1 bit por símbolo em relação ao limite teórico.

### 1.7 Instâncias de Teste

| # | Descrição | Chars | Compressão | Tempo |
|---|---|---|---|---|
| 01 | `"ABRACADABRA"` — clássico didático | 11 | 73,86% | ~132 µs |
| 02 | Frase com espaços | 36 | 49,65% | ~140 µs |
| 03 | Caractere único `"aaaaaaaaaa"` | 10 | 87,50% | ~60 µs |
| 04 | Texto aleatório — 50 000 chars | 50 000 | 39,89% | ~33 ms |

Os resultados completos com tabelas de frequência, bits e verificação de corretude são salvos em [`huffman_output.txt`](huffman_output.txt).

---

## 2. Longest Increasing Subsequence (LIS) — Programação Dinâmica

> **Esta seção será preenchida com a implementação do algoritmo LIS.**

### 2.1 O que é?

<!-- Descrever o problema: dado um array de inteiros, encontrar o comprimento da maior subsequência estritamente crescente. -->

### 2.2 Por que é Programação Dinâmica?

<!-- Explicar a subestrutura ótima e a sobreposição de subproblemas que justificam o uso de PD. -->

### 2.3 O Algoritmo — Pseudocódigo

```
LIS(A, n):
  ...
```

### 2.4 Exemplo Passo a Passo

<!-- Inserir exemplo visual da tabela de PD sendo preenchida. -->

### 2.5 Implementação

<!-- Descrever as funções do arquivo de implementação. -->

### 2.6 Complexidade

| Versão | Tempo | Espaço |
|---|---|---|
| DP clássica ($O(n^2)$) | — | — |
| DP + busca binária ($O(n \log n)$) | — | — |

### 2.7 Instâncias de Teste

<!-- Tabela com instâncias, entrada, LIS encontrada e tempo de execução. -->

---

## Referências

- **Huffman, D. A.** (1952). *A Method for the Construction of Minimum-Redundancy Codes*. Proceedings of the IRE, 40(9), 1098–1101.
- **Cormen, T. H. et al.** (2022). *Introduction to Algorithms*, 4ª ed. MIT Press. Cap. 15 — Greedy Algorithms.
- **Kleinberg, J.; Tardos, É.** (2005). *Algorithm Design*. Pearson. Cap. 4 — Greedy Algorithms.
- **Shannon, C. E.** (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.

