class HuffmanNode:

    """

    Representa um nó da árvore binária de Huffman
    ------------------------------------------------
    Atributos:
        char  (str | None): caractere armazenado 
        freq  (int)        : frequência / peso do nó
        left  (HuffmanNode): filho esquerdo
        right (HuffmanNode): filho direito

    """

    def __init__(self, char, freq):
        self.char  = char
        self.freq  = freq
        self.left  = None
        self.right = None


    def __lt__(self, other):
        return self.freq < other.freq

