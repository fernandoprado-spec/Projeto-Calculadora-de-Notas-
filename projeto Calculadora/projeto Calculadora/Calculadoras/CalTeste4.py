import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib
import joblib
import os

# ==========================
# Carregar modelo treinado
# ==========================

MODELO_ARQUIVO = "modelo_notas.pkl"

modelo = None

if os.path.exists(MODELO_ARQUIVO):
    try:
        modelo = joblib.load(MODELO_ARQUIVO)
    except Exception as erro:
        print("Erro ao carregar modelo:", erro)

# ==========================
# Idiomas
# ==========================

idioma = "pt"

textos = {

    "pt": {
        "titulo": "Calculadora Inteligente de Notas",
        "nome": "Nome do aluno",
        "materia": "Nome da matéria",
        "nota1": "Nota de Leitura",
        "nota2": "Nota de Escrita",
        "nota3": "Nota de Matemática",
        "calcular": "Calcular Resultado",
        "trocar": "Mudar Idioma",
        "resultado": "Resultado aparecerá aqui",
        "aprovado": "APROVADO ✅",
        "reprovado": "REPROVADO ❌",
        "aluno": "Aluno",
        "materiaTxt": "Matéria",
        "media": "Média",
        "status": "Status",
        "predicao": "Previsão do Modelo"
    },

    "en": {
        "titulo": "Smart Grade Calculator",
        "nome": "Student Name",
        "materia": "Subject",
        "nota1": "Reading Grade",
        "nota2": "Writing Grade",
        "nota3": "Math Grade",
        "calcular": "Calculate",
        "trocar": "Change Language",
        "resultado": "Result will appear here",
        "aprovado": "APPROVED ✅",
        "reprovado": "FAILED ❌",
        "aluno": "Student",
        "materiaTxt": "Subject",
        "media": "Average",
        "status": "Status",
        "predicao": "Model Prediction"
    },

    "es": {
        "titulo": "Calculadora Inteligente",
        "nome": "Nombre del alumno",
        "materia": "Materia",
        "nota1": "Nota de Lectura",
        "nota2": "Nota de Escritura",
        "nota3": "Nota de Matemáticas",
        "calcular": "Calcular",
        "trocar": "Cambiar Idioma",
        "resultado": "El resultado aparecerá aquí",
        "aprovado": "APROBADO ✅",
        "reprovado": "REPROBADO ❌",
        "aluno": "Alumno",
        "materiaTxt": "Materia",
        "media": "Promedio",
        "status": "Estado",
        "predicao": "Predicción"
    }
}


# ==========================
# Atualizar idioma
# ==========================

def atualizar_tela():

    titulo.config(text=textos[idioma]["titulo"])

    btn_idioma.config(
        text=textos[idioma]["trocar"]
    )

    btn_calcular.config(
        text=textos[idioma]["calcular"]
    )


def trocar_idioma():

    global idioma

    if idioma == "pt":
        idioma = "en"

    elif idioma == "en":
        idioma = "es"

    else:
        idioma = "pt"

    atualizar_tela()


# ==========================
# Calcular
# ==========================

def calcular_nota():

    try:

        nome = entrada_nome.get()
        materia = entrada_materia.get()

        leitura = float(entrada_nota1.get())
        escrita = float(entrada_nota2.get())
        matematica = float(entrada_nota3.get())

        media = (
            leitura +
            escrita +
            matematica
        ) / 3

        # -----------------------
        # Predição Machine Learning
        # -----------------------

        if modelo is not None:

            entrada = pd.DataFrame({
                "escrita": [escrita],
                "leitura": [leitura],
                "matematica": [matematica],
                "media": [media]
            })

            previsao = float(
                modelo.predict(entrada)[0]
            )

            aprovado = previsao >= 0.5

        else:
            previsao = media / 100
            aprovado = media >= 70

        if aprovado:
            status = textos[idioma]["aprovado"]
        else:
            status = textos[idioma]["reprovado"]

        resultado.config(
            text=
            f"{textos[idioma]['aluno']}: {nome}\n\n"
            f"{textos[idioma]['materiaTxt']}: {materia}\n\n"
            f"{textos[idioma]['media']}: {media:.2f}\n\n"
            f"{textos[idioma]['predicao']}: {previsao:.3f}\n\n"
            f"{textos[idioma]['status']}: {status}"
        )

    except ValueError:

        messagebox.showerror(
            "Erro",
            "Digite apenas números válidos."
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


# ==========================
# Interface Tkinter
# ==========================

janela = tk.Tk()
janela.title("CalTeste4 - Machine Learning")
janela.geometry("600x650")

titulo = tk.Label(
    janela,
    text=textos["pt"]["titulo"],
    font=("Arial", 18, "bold")
)

titulo.pack(pady=10)

btn_idioma = tk.Button(
    janela,
    text=textos["pt"]["trocar"],
    command=trocar_idioma
)

btn_idioma.pack(pady=5)

entrada_nome = tk.Entry(
    janela,
    width=50
)

entrada_nome.pack(pady=5)
entrada_nome.insert(0, "Nome do aluno")

entrada_materia = tk.Entry(
    janela,
    width=50
)

entrada_materia.pack(pady=5)
entrada_materia.insert(0, "Nome da matéria")

tk.Label(
    janela,
    text="Leitura"
).pack()

entrada_nota1 = tk.Entry(
    janela,
    width=20
)

entrada_nota1.pack(pady=5)

tk.Label(
    janela,
    text="Escrita"
).pack()

entrada_nota2 = tk.Entry(
    janela,
    width=20
)

entrada_nota2.pack(pady=5)

tk.Label(
    janela,
    text="Matemática"
).pack()

entrada_nota3 = tk.Entry(
    janela,
    width=20
)

entrada_nota3.pack(pady=5)

btn_calcular = tk.Button(
    janela,
    text=textos["pt"]["calcular"],
    command=calcular_nota,
    bg="#00aa44",
    fg="white"
)

btn_calcular.pack(pady=15)

resultado = tk.Label(
    janela,
    text=textos["pt"]["resultado"],
    justify="left",
    font=("Arial", 12)
)

resultado.pack(pady=20)

if modelo is not None:
    print("✓ Modelo carregado com sucesso")
else:
    print("⚠ Modelo não encontrado. Usando regra baseada na média.")

janela.mainloop()