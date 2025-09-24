import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import itertools
import os

def descifrar(texto, grupo, perm):
    inv_permutacion = [0] * grupo
    for i, p in enumerate(perm):
        inv_permutacion[p - 1] = i + 1

    resultado = []
    for i in range(0, len(texto), grupo):
        bloque = texto[i:i+grupo]
        if len(bloque) < grupo:
            return None
        nuevo = "".join(bloque[inv_permutacion[j]-1] for j in range(grupo))
        resultado.append(nuevo)

    while resultado and resultado[-1].endswith('X'):
        resultado[-1] = resultado[-1].rstrip('X')
        if not resultado[-1]:
            resultado.pop()

    return "".join(resultado)

class DescifradorPermutacion:
    def __init__(self, root):
        self.root = root
        self.resultados = []
        self.configurar_interfaz()

    def configurar_interfaz(self):
        self.root.title("🔓 Descifrado por Permutación de Grupos")
        self.root.geometry("900x600")

        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        estilo.configure("TLabel", font=("Arial", 11))
        estilo.configure("Title.TLabel", font=("Arial", 14, "bold"))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_main = ttk.Frame(notebook)
        notebook.add(tab_main, text="Descifrar")

        ttk.Label(tab_main, text="Texto cifrado:", style="Title.TLabel").pack(anchor="w")
        self.entrada_texto = tk.Text(tab_main, height=6, width=90)
        self.entrada_texto.pack(pady=5)

        ttk.Button(tab_main, text="📂 Cargar archivo .txt", command=self.cargar_archivo).pack(pady=5)

        frame_opts = ttk.Frame(tab_main)
        frame_opts.pack(pady=10, fill="x")

        ttk.Label(frame_opts, text="Tamaño del grupo:").grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_grupo = ttk.Entry(frame_opts, width=10)
        self.entrada_grupo.grid(row=0, column=1, padx=5)

        ttk.Label(frame_opts, text="Permutación (ejemplo: 3 1 4 2):").grid(row=0, column=2, sticky="w", padx=5)
        self.entrada_perm = ttk.Entry(frame_opts, width=20)
        self.entrada_perm.grid(row=0, column=3, padx=5)

        frame_btns = ttk.Frame(tab_main)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="🔎 Descifrar", command=self.ejecutar_descifrado).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="🧹 Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="📋 Copiar resultado", command=self.copiar_resultado).pack(side="left", padx=5)

        ttk.Label(tab_main, text="Resultados:", style="Title.TLabel").pack(anchor="w", pady=5)
        self.salida_texto = tk.Text(tab_main, wrap="word", height=18, width=100, state="disabled")
        self.salida_texto.pack(padx=5, pady=5, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tab_main, command=self.salida_texto.yview)
        scrollbar.pack(side="right", fill="y")
        self.salida_texto.config(yscrollcommand=scrollbar.set)

        tab_info = ttk.Frame(notebook)
        notebook.add(tab_info, text="ℹ️ Información")
        info = (
            "📖 DESCIFRADO POR PERMUTACIÓN DE GRUPOS\n\n"
            "Este método consiste en dividir el texto en bloques de tamaño fijo (grupos) y luego\n"
            "reordenar las letras dentro de cada grupo según una permutación.\n\n"
            "Ejemplo (grupo=4, permutación=2 4 1 3):\n"
            "Texto:  HOLA MUNDO\n"
            "Bloques: HOLA | MUND | O\n"
            "Permutación: 2 4 1 3 → OAHL\n"
            "Resultado: OAHL UDMN XXOX\n\n"
            "👉 Para descifrar, se aplica la permutación inversa."
        )
        tk.Label(tab_info, text=info, justify="left", font=("Arial", 11), anchor="nw").pack(fill="both", expand=True, padx=10, pady=10)

    def ejecutar_descifrado(self):
        texto = self.entrada_texto.get("1.0", tk.END).strip()
        texto = re.sub(r'[^A-Za-z]', '', texto).upper()
        if not texto:
            messagebox.showerror("Error", "El texto cifrado no puede estar vacío y debe contener solo letras.")
            return

        entrada_grupo_val = self.entrada_grupo.get().strip()
        entrada_perm_val = self.entrada_perm.get().strip()

        self.resultados = []
        texto_descifrado = None

        if entrada_grupo_val and entrada_perm_val:
            try:
                grupo = int(entrada_grupo_val)
                perm = list(map(int, entrada_perm_val.split()))
                if sorted(perm) != list(range(1, grupo + 1)):
                    raise ValueError
                texto_descifrado = descifrar(texto, grupo, perm)
            except ValueError:
                messagebox.showerror("Error", "Revise el tamaño de grupo y la permutación ingresada.")
                return
        else:
            # búsqueda exhaustiva
            for grupo in range(2, min(9, len(texto) + 1)):
                for perm in itertools.permutations(range(1, grupo + 1)):
                    cand = descifrar(texto, grupo, perm)
                    if cand:
                        self.resultados.append((grupo, perm, cand))

        self.salida_texto.config(state="normal")
        self.salida_texto.delete("1.0", tk.END)

        if self.resultados:
            self.salida_texto.insert(tk.END, "Resultados de búsqueda exhaustiva:\n\n")
            for grupo, perm, cand in self.resultados:
                self.salida_texto.insert(tk.END, f"Grupo {grupo}, Permutación {perm}:\n{cand}\n\n")
        elif texto_descifrado:
            self.salida_texto.insert(tk.END, texto_descifrado)
            self.resultados.append(texto_descifrado)
        else:
            self.salida_texto.insert(tk.END, "No se encontraron resultados válidos.")

        self.salida_texto.config(state="disabled")

    def limpiar(self):
        self.entrada_texto.delete("1.0", tk.END)
        self.entrada_grupo.delete(0, tk.END)
        self.entrada_perm.delete(0, tk.END)
        self.salida_texto.config(state="normal")
        self.salida_texto.delete("1.0", tk.END)
        self.salida_texto.config(state="disabled")
        self.resultados = []

    def copiar_resultado(self):
        if not self.resultados:
            messagebox.showerror("Error", "No hay texto descifrado para copiar.")
            return
        texto = ""
        for r in self.resultados:
            if isinstance(r, tuple):
                texto += f"Grupo {r[0]}, Permutación {r[1]}:\n{r[2]}\n\n"
            else:
                texto += r + "\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        messagebox.showinfo("Copiado", "El resultado se copió al portapapeles.")

    def cargar_archivo(self):
        archivo = filedialog.askopenfile(title="Seleccionar archivo", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            try:
                with open(archivo.name, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.entrada_texto.delete("1.0", tk.END)
                self.entrada_texto.insert(tk.END, contenido)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

def main():
    root = tk.Tk()
    DescifradorPermutacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
