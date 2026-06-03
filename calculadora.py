import ast
import operator
import tkinter as tk
from tkinter import messagebox


OPERADORES_PERMITIDOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)

        self.entrada = tk.Entry(
            self,
            width=16,
            font=("Arial", 24),
            borderwidth=6,
            relief="sunken",
            justify="right",
        )
        self.entrada.grid(row=0, column=0, columnspan=4, padx=4, pady=(0, 8))

        botoes = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for texto, linha, coluna in botoes:
            tk.Button(
                self,
                text=texto,
                width=5,
                height=2,
                font=("Arial", 14),
                command=lambda valor=texto: self.clicar_botao(valor),
            ).grid(row=linha, column=coluna, padx=3, pady=3)

        self.bind_all("<Key>", self.lidar_com_teclado)

    def lidar_com_teclado(self, evento):
        tecla = evento.keysym
        caractere = evento.char

        if tecla == "Return":
            self.calcular()
            return "break"

        if tecla == "Escape":
            self.limpar()
            return "break"

        if tecla == "BackSpace":
            if self.entrada.get():
                posicao_final = len(self.entrada.get()) - 1
                self.entrada.delete(posicao_final, tk.END)
            return "break"

        if caractere in "0123456789+-*/()":
            self.entrada.insert(tk.END, caractere)
            return "break"

        if caractere in ".,":
            self.entrada.insert(tk.END, ".")
            return "break"

        return None

    def clicar_botao(self, valor):
        if valor == "C":
            self.limpar()
        elif valor == "=":
            self.calcular()
        else:
            self.entrada.insert(tk.END, valor)

    def limpar(self):
        self.entrada.delete(0, tk.END)

    def calcular(self):
        expressao = self.entrada.get().strip()

        if not expressao:
            return

        try:
            resultado = avaliar_expressao(expressao)
        except (ValueError, ZeroDivisionError):
            messagebox.showerror("Erro", "Cálculo inválido")
            return

        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, formatar_resultado(resultado))


def avaliar_expressao(expressao):
    try:
        arvore = ast.parse(expressao, mode="eval")
    except SyntaxError as erro:
        raise ValueError("Expressão inválida") from erro

    return avaliar_item(arvore.body)


def avaliar_item(item):
    if isinstance(item, ast.Constant) and isinstance(item.value, (int, float)):
        return item.value

    if isinstance(item, ast.BinOp) and type(item.op) in OPERADORES_PERMITIDOS:
        esquerda = avaliar_item(item.left)
        direita = avaliar_item(item.right)
        return OPERADORES_PERMITIDOS[type(item.op)](esquerda, direita)

    if isinstance(item, ast.UnaryOp) and type(item.op) in OPERADORES_PERMITIDOS:
        return OPERADORES_PERMITIDOS[type(item.op)](avaliar_item(item.operand))

    raise ValueError("Expressão inválida")


def formatar_resultado(resultado):
    if isinstance(resultado, float) and resultado.is_integer():
        return str(int(resultado))

    return str(resultado)


if __name__ == "__main__":
    aplicativo = Calculadora()
    aplicativo.mainloop()
