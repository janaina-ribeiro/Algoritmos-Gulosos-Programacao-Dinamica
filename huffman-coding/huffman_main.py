"""

Implementação do Algoritmo de Huffman Coding (Algoritmo Guloso)
================================================================
Nome: Janaína Ribeiro 
Disciplina: Projeto e Análise de Algoritmos
Algoritmo Guloso: Huffman Coding

"""

import heapq          
from collections import Counter  
import time  
from huffman_node import HuffmanNode    
import random
import string     


def construir_arvore_huffman(text):

    """

    construir_arvore_huffman
    -------------------------------
    Constrói a árvore de Huffman a partir de um texto de entrada.

    Escolha Gulosa:
        A cada iteração, os dois nós de MENOR frequência são fundidos.
        Essa escolha local ótima garante o código ótimo globalmente.
        Primeiro, cria-se uma folha para cada caractere com sua frequência. 
        Depois, repetidamente fundem-se os dois nós de menor frequência até restar apenas um nó: 
        a raiz da árvore de Huffman.

    Parâmetro:
        text (str): texto a ser codificado

    Retorna:
        HuffmanNode: raiz da árvore de Huffman construída

    """

    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]

    heapq.heapify(heap)

    while len(heap) > 1:
        left  = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged       = HuffmanNode(None, left.freq + right.freq)
        merged.left  = left   
        merged.right = right   

        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def gerar_codigos(node, prefix="", codes=None):

    """

    Gerar_codigos
    -------------------------------
    Percorre a árvore recursivamente e gera o código binário de cada folha.

    Convenção:
        - Ramo esquerdo  →  acrescenta '0' ao prefixo
        - Ramo direito   →  acrescenta '1' ao prefixo

    Parâmetros:
        node   (HuffmanNode): nó atual da recursão
        prefix (str)         : código acumulado até este nó
        codes  (dict)        : dicionário que será preenchido

    Retorna:
        dict: mapeamento {char: código binário (str)}

    """

    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = prefix if prefix else "0"
        return codes

    gerar_codigos(node.left,  prefix + "0", codes)
    gerar_codigos(node.right, prefix + "1", codes)

    return codes



def codificar(text, codes):

    """
    Codificar
    ------------------------------------------------------------
    Substitui cada caractere do texto pelo seu código de Huffman.

    Parâmetros:
        text  (str) : texto original
        codes (dict): tabela de códigos 

    Retorna:
        str: sequência de bits (string de '0' e '1')
    """
    return ''.join(codes[char] for char in text)



def decodificar(encoded, root):

    """
    Decodificar
    ------------------------------------------------------------
    Reconstrói o texto original a partir da sequência de bits e da árvore.

    Estratégia:
        Percorre bit a bit; quando atinge uma folha, registra o caractere
        e retorna à raiz para continuar.

    Parâmetros:
        encoded (str)        : sequência de bits gerada na codificação
        root    (HuffmanNode): raiz da árvore de Huffman

    Retorna:
        str: texto original decodificado
    """
    decoded = []       
    current = root     

    if root.char is not None:
        return root.char * len(encoded)

    for bit in encoded:
        current = current.left if bit == '0' else current.right

        if current.char is not None:
            decoded.append(current.char)  
            current = root                

    return ''.join(decoded)



def huffman_coding(text):

    """
    Huffman coding
    ------------------------------------------------------------
    Executa o pipeline completo de Huffman: build, codes , encode e decode.

    Retorna:
        tuple: (codes, encoded, decoded, root)
            codes   : tabela de códigos 
            encoded : texto codificado 
            decoded : texto reconstruído
            root    : raiz da árvore 
    """
    root    = construir_arvore_huffman(text)         
    codes   = gerar_codigos(root)              
    encoded = codificar(text, codes)              
    decoded = decodificar(encoded, root)            
    return codes, encoded, decoded, root



def compressao_stats(text, encoded):

    """

    Compressão_stats
    ------------------------------------------------------------
    Calcula taxa de compressão comparando bits originais (ASCII 8-bit) com
    bits Huffman.
    Parâmetros:
        text    (str): texto original
        encoded (str): texto codificado (bits)
    Retorna:
        tuple: (original_bits, compressed_bits, ratio)
        original_bits   : bits originais  
        compressed_bits : bits comprimidos 
        ratio           : taxa de compressão 

    """
    original_bits = len(text) * 8           
    compressed_bits = len(encoded)          
    ratio = (1 - compressed_bits / original_bits) * 100 if original_bits else 0
    return original_bits, compressed_bits, ratio



def run_test(instance_name, text, counter, output_file):

    """
    testes
    ----------------------------------------------------------------------
    Executa o algoritmo para uma instância de teste e escreve os resultados em arquivo txt.
    Utiliza um contador mutável para numerar as instâncias.

    Parâmetros:
        instance_name (str): nome descritivo da instância
        text          (str): texto de entrada
        counter       (list): contador mutável 
        output_file   (file): arquivo aberto para escrita
    """
    counter[0] += 1  

    output_file.write(f"  INSTÂNCIA {counter[0]:02d}: {instance_name}\n")
    output_file.write(f"\n  Entrada: {repr(text)}\n")
    output_file.write(f"  Tamanho: {len(text)} caracteres\n\n")

    start = time.perf_counter()
    codes, encoded, decoded, _ = huffman_coding(text)
    elapsed = time.perf_counter() - start

    freq = Counter(text)
    output_file.write(f"  {'Char':<8} {'Freq':<8} {'Código'}\n")
    for char in sorted(codes, key=lambda c: freq[c], reverse=True):
        display = repr(char) if char in (' ', '\n', '\t') else char
        output_file.write(f"  {display:<8} {freq[char]:<8} {codes[char]}\n")

    orig_bits, comp_bits, ratio = compressao_stats(text, encoded)
    output_file.write(f"\n Texto codificado: {encoded[:80]}{'...' if len(encoded) > 80 else ''}\n")
    output_file.write(f"\n Bits originais : {orig_bits}\n")
    output_file.write(f"  Bits comprimidos - Huffman   : {comp_bits}\n")
    output_file.write(f"  Taxa de compressão           : {ratio:.2f}%\n")

    correto = "CORRETO" if decoded == text else "ERRO!"
    output_file.write(f"\n  Verificação: {correto}\n")

    output_file.write(f"\n  Tempo de execução: {elapsed * 1_000_000:.3f} µs  ({elapsed:.8f} s)\n")
    output_file.write("\n")



if __name__ == "__main__":

    counter = [0]

    """
        Casos de teste
        --------------------------------------------------------------
        1. Exemplo clássico didático: "ABRACADABRA"
        2. Texto com espaços: "huffman coding is a greedy algorithm"
        3. Caractere único repetido: "aaaaaaaaaa"
        4. Texto aleatório grande (50 000 caracteres)
        5. Sequência de DNA (1 000 bases, bias A/T)
    
    """

    with open("huffman_output.txt", "w", encoding="utf-8") as output_file:
        
        run_test(
            "Exemplo simples: 'ABRACADABRA'",
            "ABRACADABRA",
            counter,
            output_file=output_file
        )

        output_file.write("-" * 80 + "\n\n")

        run_test(
            "Texto com espaços",
            "huffman coding is a greedy algorithm",
            counter,
            output_file=output_file
        )

        output_file.write("-" * 80 + "\n\n")

        run_test(
            "Caractere único repetido",
            "aaaaaaaaaa",
            counter,
            output_file=output_file
        )

        output_file.write("-" * 80 + "\n\n")

        random.seed(42)
        large_text = ''.join(random.choices(string.ascii_lowercase + ' ', k=50_000))
        run_test(
            "Texto aleatório grande - 50000 caracteres",
            large_text,
            counter,
            output_file=output_file
        )

