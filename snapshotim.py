import getpass
from datetime import datetime
import win32gui
import mss
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox

# Títulos de janelas do sistema a ignorar na verificação fullscreen
TITULOS_IGNORADOS = {
    "Microsoft Text Input Application",
    "Program Manager",
    ""
}

def verificar_tela_cheia():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            largura_tela = monitor['width']
            altura_tela = monitor['height']

        tolerancia = 10
        resultados = []

        def enum_callback(hwnd, resultados):
            if not win32gui.IsWindowVisible(hwnd):
                return
            titulo = win32gui.GetWindowText(hwnd)
            if titulo in TITULOS_IGNORADOS:
                return  # ignora janelas do sistema

            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            largura = right - left
            altura = bottom - top

            pos_canto = abs(left) <= tolerancia and abs(top) <= tolerancia
            largura_igual = abs(largura - largura_tela) <= tolerancia
            altura_igual = abs(altura - altura_tela) <= tolerancia

            if pos_canto and largura_igual and altura_igual:
                print(f"❌ Janela fullscreen detectada: '{titulo}' (HWND: {hwnd})")
                resultados.append(hwnd)

        win32gui.EnumWindows(enum_callback, resultados)
        return len(resultados) > 0

    except Exception as e:
        print(f"⚠️ Erro na detecção com pywin32: {e}")
        return False

def capturar_todos_os_monitores():
    with mss.mss() as sct:
        monitor_virtual = sct.monitors[0]
        screenshot = sct.grab(monitor_virtual)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    return img

def adicionar_marca_dagua(imagem, texto):
    largura, altura = imagem.size
    marca = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))

    try:
        fonte = ImageFont.truetype("arial.ttf", 14)
    except:
        fonte = ImageFont.load_default()

    bbox = fonte.getbbox(texto)
    texto_largura = bbox[2] - bbox[0]
    texto_altura = bbox[3] - bbox[1]

    faixa_inicio = largura - 50
    faixa_espacamento = 60
    altura_espacamento = texto_largura + 8

    for x in range(faixa_inicio, -texto_altura, -faixa_espacamento):
        for y in range(altura - 10, -texto_altura, -altura_espacamento):
            layer = Image.new("RGBA", (texto_largura + 20, texto_altura + 20), (0, 0, 0, 0))
            draw_layer = ImageDraw.Draw(layer)
            draw_layer.text((6, 6), texto, font=fonte, fill=(0, 0, 0, 60))         # sombra
            draw_layer.text((5, 5), texto, font=fonte, fill=(255, 255, 255, 200))  # texto
            texto_rot = layer.rotate(90, expand=1)
            marca.paste(texto_rot, (x, y), texto_rot)

    imagem_alpha = imagem.convert("RGBA")
    imagem_final = Image.alpha_composite(imagem_alpha, marca)
    imagem.paste(imagem_final.convert("RGB"))

def salvar_imagem(imagem, usuario):
    data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    texto = f"{data_hora} | Usuário: {usuario}"
    adicionar_marca_dagua(imagem, texto)
    nome_arquivo = f"captura_monitores_{usuario}_{data_hora}.png".replace(":", "-")
    imagem.convert("RGB").save(nome_arquivo)
    print(f"✅ Captura salva: {nome_arquivo}")
    messagebox.showinfo("Captura feita", f"✅ Captura salva como:\n{nome_arquivo}")

def iniciar_captura(janela):
    if verificar_tela_cheia():
        messagebox.showwarning("Erro", "Feche janelas em tela cheia (F11) antes de continuar.")
        return
    janela.withdraw()
    janela.after(500, lambda: executar_captura(janela))

def executar_captura(janela):
    usuario = getpass.getuser()
    imagem = capturar_todos_os_monitores()
    salvar_imagem(imagem, usuario)
    janela.destroy()

def mostrar_janela():
    root = tk.Tk()
    root.title("Captura de Tela Antifraude")
    root.geometry("300x150")
    root.resizable(False, False)

    botao = tk.Button(root, text="📸 Capturar Tela", command=lambda: iniciar_captura(root),
                      font=("Arial", 16), bg="#4CAF50", fg="white")
    botao.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    mostrar_janela()
