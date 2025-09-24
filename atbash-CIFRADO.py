import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class CifradorAtbash:
    def __init__(self):
        self.alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"
    
    def preprocesar_texto(self, texto):
        texto_limpio = ""
        for caracter in texto:
            if caracter == 'ñ' or caracter == 'Ñ':
                continue
            elif caracter.isalpha() or caracter.isdigit():
                texto_limpio += caracter
        return texto_limpio
    
    def cifrar(self, texto_plano):
        texto_procesado = self.preprocesar_texto(texto_plano)
        texto_cifrado = ""
        
        for caracter in texto_procesado:
            if caracter in self.alfabeto_mayusculas:
                posicion = self.alfabeto_mayusculas.index(caracter)
                opuesto = self.alfabeto_mayusculas[25 - posicion]
                texto_cifrado += opuesto
            elif caracter in self.alfabeto_minusculas:
                posicion = self.alfabeto_minusculas.index(caracter)
                opuesto = self.alfabeto_minusculas[25 - posicion]
                texto_cifrado += opuesto
            elif caracter.isdigit():
                texto_cifrado += caracter
        
        return texto_cifrado

class InterfazCifrador:
    def __init__(self, root):
        self.root = root
        self.cifrador = CifradorAtbash()
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.root.title("🔐 Cifrador Atbash")
        self.root.geometry("850x600")

        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        estilo.configure("TLabel", font=("Arial", 11))
        estilo.configure("Title.TLabel", font=("Arial", 16, "bold"))

        # Contenedor principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Pestaña Entrada / Salida -----
        tab_main = ttk.Frame(notebook)
        notebook.add(tab_main, text="Cifrado")

        ttk.Label(tab_main, text="Texto a cifrar:", style="Title.TLabel").pack(anchor="w", pady=(5,2))
        self.texto_entrada = scrolledtext.ScrolledText(tab_main, width=90, height=5, font=("Consolas", 11))
        self.texto_entrada.pack(pady=5, fill="x")

        frame_botones = ttk.Frame(tab_main)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="🔒 Cifrar", command=self.cifrar_texto).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="🧹 Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="📋 Copiar resultado", command=self.copiar_resultado).pack(side="left", padx=5)

        ttk.Label(tab_main, text="Texto procesado:", style="Title.TLabel").pack(anchor="w", pady=(10,2))
        self.texto_procesado = scrolledtext.ScrolledText(tab_main, width=90, height=3, font=("Consolas", 11))
        self.texto_procesado.pack(pady=5, fill="x")

        ttk.Label(tab_main, text="Texto cifrado:", style="Title.TLabel").pack(anchor="w", pady=(10,2))
        self.texto_cifrado = scrolledtext.ScrolledText(tab_main, width=90, height=4, font=("Consolas", 11))
        self.texto_cifrado.pack(pady=5, fill="x")

        # ----- Pestaña Transformación -----
        tab_trans = ttk.Frame(notebook)
        notebook.add(tab_trans, text="Transformación paso a paso")

        self.texto_ejemplo = scrolledtext.ScrolledText(tab_trans, width=95, height=25, font=("Consolas", 10))
        self.texto_ejemplo.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Pestaña Información -----
        tab_info = ttk.Frame(notebook)
        notebook.add(tab_info, text="ℹ️ Información")

        info_label = tk.Label(tab_info, text=self.info_texto(), justify="left", font=("Arial", 11), anchor="nw")
        info_label.pack(fill="both", expand=True, padx=10, pady=10)

    def cifrar_texto(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingresa texto para cifrar.")
            return
        texto_procesado = self.cifrador.preprocesar_texto(texto)
        texto_cifrado = self.cifrador.cifrar(texto)
        self.texto_procesado.delete("1.0", tk.END)
        self.texto_procesado.insert("1.0", texto_procesado)
        self.texto_cifrado.delete("1.0", tk.END)
        self.texto_cifrado.insert("1.0", texto_cifrado)
        self.mostrar_transformacion_completa(texto_procesado, texto_cifrado)

    def mostrar_transformacion_completa(self, texto_procesado, texto_cifrado):
        if not texto_procesado:
            self.texto_ejemplo.insert("1.0", "No hay texto para mostrar.")
            return
        ejemplo_texto = "POS | ORIGINAL | CIFRADO | TIPO\n" + "-"*40 + "\n"
        for i, (orig, cif) in enumerate(zip(texto_procesado, texto_cifrado), 1):
            tipo = "MAYÚSCULA" if orig.isupper() else "minúscula" if orig.islower() else "NÚMERO"
            ejemplo_texto += f"{i:>3} |    {orig:^6} |   {cif:^6} | {tipo}\n"
        self.texto_ejemplo.delete("1.0", tk.END)
        self.texto_ejemplo.insert("1.0", ejemplo_texto)

    def limpiar_campos(self):
        for campo in [self.texto_entrada, self.texto_procesado, self.texto_cifrado, self.texto_ejemplo]:
            campo.delete("1.0", tk.END)

    def copiar_resultado(self):
        texto = self.texto_cifrado.get("1.0", tk.END).strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            messagebox.showinfo("Copiado", "El texto cifrado se copió al portapapeles.")

    def info_texto(self):
        return (
            "🔐 CIFRADO ATBASH\n\n"
            "El Atbash es un cifrado de sustitución simple:\n"
            "• A ↔ Z, B ↔ Y, C ↔ X, ...\n"
            "• a ↔ z, b ↔ y, c ↔ x, ...\n\n"
            "Características:\n"
            "✓ Mantiene mayúsculas y minúsculas\n"
            "✓ Los números no cambian\n"
            "✓ Espacios y signos se eliminan\n"
        )

def main():
    root = tk.Tk()
    InterfazCifrador(root)
    root.mainloop()

if __name__ == "__main__":
    main()
