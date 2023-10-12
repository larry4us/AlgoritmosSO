from Algoritmos import Algoritmos

class FIFO(Algoritmos):
    """Algoritmo de troca de página:
        Primeiro a entrar, primeiro a sair."""
    # Tamanho permitido na memória é definido na classe abstrata Algoritmos
    fila = []
    entrada = []
    cont_pagefault = 0

    def __init__(self, arquivo):
        self.memoria = []
        self.fila = []
        self.entrada = self.leitura(arquivo)

    def ler_string_de_referencia(self, string_referencia):
        """Lê os dados de entrada como uma string, e os separa em tuplas.
            O primeiro elemento representa o processo, o segundo a página"""

        if string_referencia.endswith(";"):
            # Remove o último caractere ";" da string
            string_referencia = string_referencia[:-1]

        sequencia_de_referencia = []  # Inicializa uma lista vazia para armazenar os pares de processos e páginas

        # Divide a string de referência nos pares de números usando o ponto e vírgula como separador
        pares = string_referencia.split(';')

        # Itera pelos pares de números e os converte em tuplas de inteiros
        for par in pares:
            processo, pagina = map(int, par.split(','))
            sequencia_de_referencia.append((processo, pagina))

        return sequencia_de_referencia
    
    def leitura(self, arquivo):
        try:
            with open(arquivo, 'r') as arquivo:
                conteudo = arquivo.read()
                conteudo = self.ler_string_de_referencia(conteudo)
            return conteudo
        except FileNotFoundError as e:
            print(f"Não foi possível ler o arquivo. Exceção: {e}")


    def page_fault(self, tupla):
        """Retorna 1 caso ocorra Page Fault e 0 caso contrário """
        
        for elemento in self.memoria:
            if tupla == elemento:
                return False
        return True
    
    def adiciona_memoria(self, tupla):
        """ Verifica na memória se existe espaço. Se sim, adiciona.
            Caso não, o algoritmo FIFO decide quem sai"""
        # Adiciona a fila
        self.fila.append(tupla)

        if len(self.memoria) < self.tamanho:
            self.memoria.append(tupla)
        else:
            mais_antigo = self.fila.pop(0)
            # Procura o mais antigo na memória
            for i,elemento in enumerate(self.memoria):
                if elemento == mais_antigo:
                    # Encontrou o mais_antigo na memória
                    self.memoria[i] = tupla

    def adiciona(self, tupla):
        """Adiciona as páginas do processo à minha memória física.
            Caso ocorra Page Fault, uma das páginas terá de sair! """
        # Só faz alguma coisa caso haja page fault
        if self.page_fault(tupla):
            self.cont_pagefault += 1
            self.adiciona_memoria(tupla)
    
    def executa(self):
        for entrada in self.entrada:
            # Verificando condição de parada da string de referência
            if entrada == (0,0):
                break
            self.adiciona(entrada)

    