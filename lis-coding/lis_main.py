"""

Implementação do Algoritmo Longest Increasing Subsequence (LIS)
================================================================
Nome: Janaína Ribeiro
Disciplina: Projeto e Análise de Algoritmos
Programação Dinâmica — Abordagem Bottom-Up

"""

import time
import random


def lis_dp(arr):

    """

    lis_dp
    -------------------------------
    Calcula o comprimento e a subsequência crescente mais longa 
    usando Programação Dinâmica bottom-up em O(n²).

    Estratégia:
        Para cada posição i, percorre todos os índices j < i.
        Se arr[j] < arr[i], a subsequência ótima que termina em j
        pode ser estendida com arr[i]. Registra o predecessor em
        parent[i] para permitir a reconstrução da solução.

    Parâmetros:
        arr (list[int]): sequência de entrada

    Retorna:
        length      (int)       : comprimento da LIS
        subsequence (list[int]) : a subsequência reconstruída
        comparisons (int)       : contador de comparações realizadas

    """

    n = len(arr)
    if n == 0:
        return 0, [], 0

    L = [1] * n      
    parent = [-1] * n 

    comparisons = 0

    for i in range(1, n):
        for j in range(i):
            comparisons += 1
            if arr[j] < arr[i]:
                comparisons += 1
                if L[j] + 1 > L[i]:
                    L[i] = L[j] + 1
                    parent[i] = j

    max_len = max(L)
    max_idx = L.index(max_len)

    subsequence = []
    idx = max_idx
    while idx != -1:
        subsequence.append(arr[idx])
        idx = parent[idx]
    subsequence.reverse()

    return max_len, subsequence, comparisons


def is_increasing(subseq):

    """

    is_increasing
    -------------------------------
    Verifica se uma sequência é estritamente crescente.

    Parâmetros:
        subseq (list): sequência a verificar

    Retorna:
        bool: True se estritamente crescente, False caso contrário

    """

    return all(subseq[i] < subseq[i + 1] for i in range(len(subseq) - 1))


def lis_brute_force(arr):

    """

    lis_brute_force
    -------------------------------
    Força bruta: gera todas as 2ⁿ subsequências e retorna a mais longa
    que é estritamente crescente. Complexidade O(2ⁿ · n).
    Utilizada apenas para verificação de correção em entradas pequenas (n ≤ 20).

    Parâmetros:
        arr (list[int]): sequência de entrada

    Retorna:
        length (int)      : comprimento da maior subsequência crescente
        best   (list[int]): a subsequência encontrada
        calls  (int)      : contador de operações realizadas

    """

    n = len(arr)
    best = []
    calls = [0]  

    for mask in range(1, 1 << n):   
        subseq = []
        for bit in range(n):
            calls[0] += 1
            if mask & (1 << bit):
                subseq.append(arr[bit])
        if is_increasing(subseq) and len(subseq) > len(best):
            best = subseq

    return len(best), best, calls[0]


def run_test(instance_name, arr, counter, output_file, run_brute=False):

    """

    run_test
    -------------------------------
    Executa o algoritmo para uma instância de teste e escreve os
    resultados em um arquivo de saída. Utiliza um contador mutável
    para numerar as instâncias. Na saída DP significa "Dynamic Programming" e o BF "Brute Force".

    Parâmetros:
        instance_name (str)  : nome descritivo da instância
        arr           (list) : sequência de entrada
        counter       (list) : contador mutável [int]
        output_file   (file) : arquivo aberto para escrita
        run_brute     (bool) : se True, executa também a força bruta

    """

    counter[0] += 1

    output_file.write(f"  INSTÂNCIA {counter[0]:02d}: {instance_name}\n")
    output_file.write(f"\n  Entrada ({len(arr)} elementos): {arr}\n\n")

    t0 = time.perf_counter()
    length, subseq, cmp_dp = lis_dp(arr)
    t1 = time.perf_counter()
    elapsed_dp = t1 - t0

    output_file.write(f"  DP  Comprimento da LIS : {length}\n")
    output_file.write(f"  DP  Subsequência       : {subseq}\n")
    output_file.write(f"  DP  Comparações        : {cmp_dp}\n")
    output_file.write(f"  DP  Tempo de execução  : {elapsed_dp * 1_000_000:.3f} µs  ({elapsed_dp:.8f} s)\n")

    if run_brute:
        t2 = time.perf_counter()
        bf_len, bf_subseq, cmp_bf = lis_brute_force(arr)
        t3 = time.perf_counter()
        elapsed_bf = t3 - t2

        output_file.write(f"\n  BF  Comprimento da LIS : {bf_len}\n")
        output_file.write(f"  BF  Subsequência       : {bf_subseq}\n")
        output_file.write(f"  BF  Operações          : {cmp_bf}\n")
        output_file.write(f"  BF Tempo de execução  : {elapsed_bf * 1_000_000:.3f} µs  ({elapsed_bf:.8f} s)\n")

        ok = "CORRETO" if bf_len == length else "DIVERGÊNCIA!"
        output_file.write(f"\n  Verificação DP x BF      : {ok}\n")

    output_file.write("\n")



if __name__ == "__main__":

    counter = [0]

    with open("lis_output.txt", "w", encoding="utf-8") as output_file:


        run_test(
            "Exemplo clássico",
            [10, 9, 2, 5, 3, 7, 101, 18],
            counter,
            output_file,
            run_brute=True
        )

        output_file.write("-" * 65 + "\n\n")

        run_test(
            "Sequência já crescente",
            [1, 2, 3, 4, 5, 6, 7, 8],
            counter,
            output_file,
            run_brute=True
        )

        output_file.write("-" * 65 + "\n\n")


        run_test(
            "Sequência decrescente",
            [8, 7, 6, 5, 4, 3, 2, 1],
            counter,
            output_file,
            run_brute=True
        )

        output_file.write("-" * 65 + "\n\n")

        run_test(
            "Elementos repetidos",
            [5, 5, 5, 5, 5],
            counter,
            output_file,
            run_brute=True
        )

        output_file.write("-" * 65 + "\n\n")

        run_test(
            "Um único elemento",
            [42],
            counter,
            output_file,
            run_brute=True
        )

        output_file.write("-" * 65 + "\n\n")


    print("Saída gravada em lis_output.txt")
