import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class CifradorAtbash:
    def __init__(self):
        self.alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"
        self.mapa_normalizacion = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U',
            'ñ': 'n', 'Ñ': 'N'
        }
    
    def normalizar_caracter(self, caracter):
        return self.mapa_normalizacion.get(caracter, caracter)
    
    def preprocesar_texto(self, texto):
        texto_limpio = ""
        for caracter in texto:
            caracter_normalizado = self.normalizar_caracter(caracter)
            
            if (caracter_normalizado in self.alfabeto_mayusculas or 
                caracter_normalizado in self.alfabeto_minusculas or 
                caracter_normalizado.isdigit()):
                texto_limpio += caracter_normalizado
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

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

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

        tab_trans = ttk.Frame(notebook)
        notebook.add(tab_trans, text="Transformación paso a paso")

        self.texto_ejemplo = scrolledtext.ScrolledText(tab_trans, width=95, height=25, font=("Consolas", 10))
        self.texto_ejemplo.pack(fill="both", expand=True, padx=10, pady=10)

        tab_info = ttk.Frame(notebook)
        notebook.add(tab_info, text="ℹ️ Información")

        info_label = tk.Label(tab_info, text=self.info_texto(), justify="left", font=("Arial", 11), anchor="nw")
        info_label.pack(fill="both", expand=True, padx=10, pady=10)

    def cifrar_texto(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingresa texto para cifrar.")
            return
        
        caracteres_normalizados = []
        for caracter in texto:
            if caracter in self.cifrador.mapa_normalizacion:
                normalizacion = f"{caracter}→{self.cifrador.mapa_normalizacion[caracter]}"
                if normalizacion not in caracteres_normalizados:
                    caracteres_normalizados.append(normalizacion)
        
        texto_procesado = self.cifrador.preprocesar_texto(texto)
        
        if not texto_procesado:
            messagebox.showwarning("Sin texto válido", 
                                 "No quedó texto válido después del procesamiento.")
            return
        
        texto_cifrado = self.cifrador.cifrar(texto)
        
        self.texto_procesado.delete("1.0", tk.END)
        self.texto_procesado.insert("1.0", texto_procesado)
        
        self.texto_cifrado.delete("1.0", tk.END)
        self.texto_cifrado.insert("1.0", texto_cifrado)
        
        self.mostrar_transformacion_completa(texto_procesado, texto_cifrado)

        if caracteres_normalizados:
            info_msg = f"✅ Cifrado completado con normalización\n\n"
            info_msg += f"Caracteres normalizados (tildes eliminadas):\n"
            info_msg += f"• {', '.join(caracteres_normalizados)}\n\n"
            info_msg += f"Texto original: {len(texto)} caracteres\n"
            info_msg += f"Texto procesado: {len(texto_procesado)} caracteres válidos"
            messagebox.showinfo("Información del cifrado", info_msg)

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
            "CIFRADO ATBASH - ALFABETO INGLÉS\n\n"
            "El Atbash es un cifrado de sustitución simple:\n"
            "• A ↔ Z, B ↔ Y, C ↔ X, ...\n"
            "• a ↔ z, b ↔ y, c ↔ x, ...\n\n"
            "ALFABETO INGLÉS (26 letras):\n"
            "• MAYÚSCULAS: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n"
            "• minúsculas: a b c d e f g h i j k l m n o p q r s t u v w x y z\n\n"
            "MANEJO DE CARACTERES ESPAÑOLES:\n"
            "✓ TILDES se ELIMINAN automáticamente:\n"
            "  • á,é,í,ó,ú → a,e,i,o,u\n"
            "  • Á,É,Í,Ó,Ú → A,E,I,O,U\n"
            "  • ü,Ü → u,U\n"
            "  • ñ,Ñ → n,N\n\n"
            "Características:\n"
            "✓ Mantiene mayúsculas y minúsculas\n"
            "✓ Los números no cambian (0-9)\n"
            "✓ Espacios y signos de puntuación se eliminan\n"
            "✓ TILDES se eliminan automáticamente\n\n"
            "EJEMPLOS:\n"
            "• 'NIÑO' → 'NINO' → 'MRML'\n"
            "• 'María' → 'Maria' → 'Nzirz'\n"
            "• 'Jesús' → 'Jesus' → 'Qvhfh'\n\n"
            "MAPEO COMPLETO:\n"
            "A→Z  B→Y  C→X  D→W  E→V  F→U  G→T  H→S  I→R  J→Q  K→P  L→O  M→N\n"
            "N→M  O→L  P→K  Q→J  R→I  S→H  T→G  U→F  V→E  W→D  X→C  Y→B  Z→A\n"
        )

def main():
    root = tk.Tk()
    InterfazCifrador(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    