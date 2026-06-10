# Algoritmos — PAA: Guloso e Programação Dinâmica
Implementação e análise de dois algoritmos clássicos:

| Algoritmo | Paradigma | Arquivo |
|---|---|---|
| **Huffman Coding** | Algoritmo Guloso | `huffman-coding/huffman_main.py` |
| **Longest Increasing Subsequence** | Programação Dinâmica | `lis-coding/lis_main.py` |

---

## Estrutura do Projeto

```
Algoritmo-PAA/
├── huffman-coding/
│   ├── huffman_main.py      # pipeline completo: build → encode → decode
│   └── huffman_node.py      # nó da árvore binária de Huffman
├── lis-coding/
│   ├── lis_main.py          # DP bottom-up + força bruta para verificação
│   ├── lis_output.txt       # saída gerada pelas instâncias de teste
│   └── LIS_explicacao.md   # documentação matemática detalhada
├── huffman_output.txt        # saída gerada pelas instâncias de teste
├── EXPLICACAO.md             # documentação matemática do Huffman
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
```bash
cd lis-coding
python lis_main.py
```
A saída detalhada de cada instância de teste, incluindo a sequência de entrada, a LIS encontrada, o número de comparações e o tempo de execução, será salva em `lis_output.txt`.

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

### 2.1 O que é?

O **Longest Increasing Subsequence (LIS)** — ou **Subsequência Crescente Mais Longa** — é um problema clássico de otimização combinatória. Dado um array de inteiros $A = \langle a_1, a_2, \ldots, a_n \rangle$, o objetivo é encontrar a maior subsequência **estritamente crescente** (respeitando a ordem original, mas podendo pular elementos).

**Exemplo:** para $A = \langle 10, 9, 2, 5, 3, 7, 101, 18 \rangle$, a LIS é $\langle 2, 5, 7, 101 \rangle$ com comprimento **4**.

Aplicações: alinhamento de DNA, algoritmo `diff`, análise de tendências em séries temporais.

### 2.2 Por que é Programação Dinâmica?

O problema exibe as duas propriedades que justificam o uso de PD:

**Subestrutura ótima:** qualquer prefixo de uma LIS também é uma LIS para o prefixo correspondente da sequência original. Isso permite definir:

> $L(i)$ = comprimento da LIS que termina **obrigatoriamente** no índice $i$

**Sobreposição de subproblemas:** $L(j)$ é consultado múltiplas vezes durante o cálculo de $L(i)$ para diferentes valores de $i > j$. A PD armazena cada $L(i)$ exatamente uma vez, eliminando recomputações.

```
Força Bruta  →  enumera todas as 2ⁿ subsequências      (O(2ⁿ · n))
P. Dinâmica  →  preenche tabela L[1..n] iterativamente  (O(n²))
```

### 2.3 O Algoritmo — Pseudocódigo

```
LIS-LENGTH(A, n):
  para i = 1 até n:
    L[i]      ← 1     // caso base: subsequência de tamanho 1
    parent[i] ← -1    // sem predecessor

  para i = 2 até n:
    para j = 1 até i-1:
      se A[j] < A[i] e L[j] + 1 > L[i]:
        L[i]      ← L[j] + 1
        parent[i] ← j          // registra predecessor para reconstrução

  L* ← max(L[1..n])
  retorna L*, parent


RECONSTRUCT-LIS(A, L, parent):
  max_idx ← índice do máximo em L
  subseq  ← lista vazia
  idx     ← max_idx

  enquanto idx ≠ -1:
    subseq.inserir_no_início(A[idx])
    idx ← parent[idx]

  retorna subseq
```

**Recorrência:**

$$L(i) = 1 + \max\{L(j) : 1 \leq j < i \text{ e } a_j < a_i\}$$

$$L^* = \max_{1 \leq i \leq n} L(i)$$

### 2.4 Exemplo Passo a Passo — $A = \langle 10, 9, 2, 5, 3, 7, 101, 18 \rangle$

**Preenchimento da tabela bottom-up:**

| $i$ | $a_i$ | $j$ que atualizou $L[i]$ | $L[i]$ | `parent[i]` |
|---|---|---|---|---|
| 1 | 10 | — (caso base) | **1** | -1 |
| 2 | 9  | — (nenhum $a_j < 9$) | **1** | -1 |
| 3 | 2  | — (nenhum $a_j < 2$) | **1** | -1 |
| 4 | 5  | $j=3$ ($a_3=2$, $L=1+1$) | **2** | 3 |
| 5 | 3  | $j=3$ ($a_3=2$, $L=1+1$) | **2** | 3 |
| 6 | 7  | $j=4$ ($a_4=5$, $L=2+1$) | **3** | 4 |
| 7 | 101 | $j=6$ ($a_6=7$, $L=3+1$) | **4** | 6 |
| 8 | 18 | $j=6$ ($a_6=7$, $L=3+1$) | **4** | 6 |

**Reconstrução** (percorre `parent[]` de trás para frente a partir do índice 7):

```
idx=7 (101) → idx=6 (7) → idx=4 (5) → idx=3 (2) → fim
Resultado: [2, 5, 7, 101]
```

### 2.5 Implementação

#### `lis_main.py` — Funções Principais

| Função | Responsabilidade |
|---|---|
| `lis_dp(arr)` | DP bottom-up $O(n^2)$: preenche `L[]` e `parent[]`, reconstrói e retorna a LIS com o contador de comparações |
| `lis_brute_force(arr)` | Força bruta $O(2^n \cdot n)$: enumera todos os subconjuntos e verifica se são crescentes; usada para verificação de corretude |
| `is_increasing(subseq)` | Verifica se uma sequência é estritamente crescente em $O(k)$ |
| `run_test(...)` | Executa ambas as versões em uma instância, mede tempo com `perf_counter` e escreve os resultados em arquivo |

**Trecho do núcleo da DP:**

```python
for i in range(1, n):
    for j in range(i):
        comparisons += 1
        if arr[j] < arr[i]:
            comparisons += 1
            if L[j] + 1 > L[i]:
                L[i] = L[j] + 1
                parent[i] = j
```

O contador `comparisons` registra cada verificação realizada, permitindo observar empiricamente o crescimento quadrático.

### 2.6 Complexidade

| Versão | Tempo | Espaço | Viável para $n = 10^4$? |
|---|---|---|---|
| Força Bruta | $O(2^n \cdot n)$ | $O(n)$ | Não |
| **DP clássica** | $\boldsymbol{O(n^2)}$ | $O(n)$ | **Sim** |
| DP + busca binária | $O(n \log n)$ | $O(n)$ | Sim (mais eficiente) |

A versão implementada é a DP $O(n^2)$, que deriva diretamente da recorrência e facilita a reconstrução da solução. O número de comparações satisfaz:

$$\sum_{i=2}^{n}(i-1) = \frac{n(n-1)}{2} = \Theta(n^2)$$

### 2.7 Instâncias de Teste

| # | Descrição | $n$ | LIS encontrada | Comparações | Verificação |
|---|---|---|---|---|---|
| 01 | Exemplo clássico `[10,9,2,5,3,7,101,18]` | 8 | `[2,5,7,101]` → len=4 | 45 | DP = BF ✓ |
| 02 | Sequência já crescente `[1..8]` | 8 | `[1,2,3,4,5,6,7,8]` → len=8 | 56 | DP = BF ✓ |
| 03 | Sequência decrescente `[8..1]` | 8 | `[8]` → len=1 | 28 | DP = BF ✓ |
| 04 | Elementos repetidos `[5,5,5,5,5]` | 5 | `[5]` → len=1 | 10 | DP = BF ✓ |
| 05 | Um único elemento `[42]` | 1 | `[42]` → len=1 | 0 | DP = BF ✓ |
| 06 | Sequência CLRS `[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]` | 16 | len=6 | 196 | — |

Os resultados completos com subsequências, comparações e tempos são salvos em [`lis-coding/lis_output.txt`](lis-coding/lis_output.txt).

---

## Referências

- **Huffman, D. A.** (1952). *A Method for the Construction of Minimum-Redundancy Codes*. Proceedings of the IRE, 40(9), 1098–1101.
- **Cormen, T. H. et al.** (2022). *Introduction to Algorithms*, 4ª ed. MIT Press. Cap. 15 — Greedy Algorithms; Cap. 14 — Dynamic Programming.
- **Kleinberg, J.; Tardos, É.** (2005). *Algorithm Design*. Pearson. Cap. 4 — Greedy Algorithms; Cap. 6 — Dynamic Programming.
- **Shannon, C. E.** (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.
- **CP-Algorithms — LIS.** Disponível em: https://cp-algorithms.com/sequences/longest_increasing_subsequence.html

