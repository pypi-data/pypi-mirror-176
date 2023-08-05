class Calculator:
    def __init__(self,n1,n2):
        self.n1 = n1
        self.n2 = n2
    def add(self):
        soma = self.n1 + self.n2
        return soma
    def sub(self):
        subtracao = self.n1 - self.n2
        return subtracao
    def mult(self):
        multiplicacao = self.n1 * self.n2
        return multiplicacao
    def div(self):
        divisao = self.n1 / self.n2
        return divisao
