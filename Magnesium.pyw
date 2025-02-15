import tkinter as tk
from tkinter import messagebox
import random
import time
import win32gui
import win32api
import win32con
import win32ui
import ctypes
from ctypes import windll
import threading

# Função de BitBlt para o primeiro efeito GDI
def BitBlt(hdcDest, xDest, yDest, width, height, hdcSrc, xSrc, ySrc, rop):
    ctypes.windll.gdi32.BitBlt(hdcDest, xDest, yDest, width, height, hdcSrc, xSrc, ySrc, rop)

# Função para exibir o aviso
def exibir_aviso():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    messagebox.showinfo("error", "DONT GO LITTLE GOD")

# Função para o primeiro efeito GDI que pisca por 10 segundos
def efeito_piscante():
    start_time = time.time()
    screen_width = win32api.GetSystemMetrics(0)  # Largura da tela
    screen_height = win32api.GetSystemMetrics(1)  # Altura da tela

    while True:
        # Obtém o contexto de dispositivo (DC) da tela
        hdc = win32gui.GetDC(0)
        
        # Realiza o efeito de inversão utilizando PatBlt (PATINVERT)
        win32gui.PatBlt(hdc, 0, 0, screen_width, screen_height, win32con.PATINVERT)
        
        # Verifica se 10 segundos se passaram
        if time.time() - start_time >= 10:
            win32gui.ReleaseDC(0, hdc)  # Libera o contexto de dispositivo
            break  # Sai do loop após 10 segundos
        
        # Aguarda 100ms antes de realizar a próxima inversão
        time.sleep(0.1)
        
        # Libera o contexto de dispositivo (DC)
        win32gui.ReleaseDC(0, hdc)

# Função para desenhar a bola por 10 segundos
def draw_circle():
    # Inicializando variáveis de movimento
    x, y = 10, 10
    signX, signY = 1, 1
    incrementor = 10
    start_time = time.time()  # Marca o tempo de início da animação da bola

    while True:
        # Obtendo o contexto de dispositivo (DC) para a tela inteira
        hdc = win32gui.GetDC(0)  # 0 refere-se à tela inteira

        # Movendo o círculo
        x += incrementor * signX
        y += incrementor * signY

        # Definindo as coordenadas para a elipse
        top_x, top_y = x, y
        bottom_x, bottom_y = x + 100, y + 100

        # Criando uma cor aleatória para o círculo
        brush = win32gui.CreateSolidBrush(win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        win32gui.SelectObject(hdc, brush)

        # Desenhando a elipse (círculo) na tela
        win32gui.Ellipse(hdc, top_x, top_y, bottom_x, bottom_y)

        # Detecção de bordas para mover o círculo
        if y >= win32api.GetSystemMetrics(1):  # Altura da tela
            signY = -1  # Inverte o movimento no eixo Y
        if x >= win32api.GetSystemMetrics(0):  # Largura da tela
            signX = -1  # Inverte o movimento no eixo X
        if y <= 0:
            signY = 1  # Inverte o movimento no eixo Y
        if x <= 0:
            signX = 1  # Inverte o movimento no eixo X

        # Espera de 10 milissegundos antes de atualizar a tela
        time.sleep(0.01)

        # Limpeza do contexto de dispositivo (para evitar borrões de desenho)
        win32gui.DeleteObject(brush)
        win32gui.ReleaseDC(0, hdc)

        # Se o tempo de animação da bola for superior a 10 segundos, sai do loop
        if time.time() - start_time >= 10:
            break

# Função para desenhar um "pie" (parte de elipse) de cor aleatória
def draw_random_pie():
    # Obtém o HDC da tela
    hdc = win32gui.GetDC(0)

    # Obtém as dimensões da tela
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    # Cria uma cor aleatória
    color = random_color()
    brush = win32gui.CreateSolidBrush(win32api.RGB(*color))

    # Seleciona o pincel (brush)
    win32gui.SelectObject(hdc, brush)

    # Desenha um "pie" (parte de elipse) com coordenadas aleatórias
    x1 = random.randint(0, screen_width)
    y1 = random.randint(0, screen_height)
    x2 = random.randint(0, screen_width)
    y2 = random.randint(0, screen_height)
    x3 = random.randint(0, screen_width)
    y3 = random.randint(0, screen_height)
    x4 = random.randint(0, screen_width)
    y4 = random.randint(0, screen_height)

    # Desenha o "pie"
    win32gui.Pie(hdc, x1, y1, x2, y2, x3, y3, x4, y4)

    # Libera os recursos
    win32gui.DeleteObject(brush)
    win32gui.ReleaseDC(0, hdc)

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Função para desenhar o BitBlt com círculos progressivos
def ci(x, y, w, h):
    # Obter o contexto do dispositivo da tela
    hdc = win32gui.GetDC(0)
    # Criar uma região elíptica (máscara)
    hrgn = windll.gdi32.CreateEllipticRgn(x, y, w + x, h + y)
    # Selecionar a região na área de clip do hdc
    windll.gdi32.SelectClipRgn(hdc, hrgn)
    # Realizar o BitBlt (operar a cópia de pixels com a operação NOTSRCCOPY)
    windll.gdi32.BitBlt(hdc, x, y, w, h, hdc, x, y, win32con.NOTSRCCOPY)
    # Deletar o objeto de região (para liberar a memória)
    windll.gdi32.DeleteObject(hrgn)
    # Liberar o contexto de dispositivo
    win32gui.ReleaseDC(0, hdc)

def efeito_bitblt():
    # Obter as dimensões da tela
    hwnd = win32gui.GetDesktopWindow()
    rect = win32gui.GetWindowRect(hwnd)
    w = rect[2] - rect[0] - 500  # Largura da tela menos um offset
    h = rect[3] - rect[1] - 500  # Altura da tela menos um offset

    start_time = time.time()

    while True:
        # Gerar coordenadas x e y aleatórias
        size = 1000
        x = random.randint(-size // 2, w + size // 2)
        y = random.randint(-size // 2, h + size // 2)

        # Criar círculos com tamanhos progressivamente maiores
        for i in range(0, size, 100):
            ci(x - i // 2, y - i // 2, i, i)
            time.sleep(0.025)  # Pausar por 25ms

        # Verifica se 10 segundos se passaram
        if time.time() - start_time >= 10:
            break  # Sai do loop após 10 segundos

def start_thread_thing6():
    import threading
    thread = threading.Thread(target=thing6)
    thread.daemon = True  # Para que a thread termine com o programa
    thread.start()
    thread.join()  # Manter o script em execução enquanto a thread está ativa

def thing6():
    while True:
        # Obter contexto de dispositivo para a tela
        hdc = win32gui.GetDC(0)
        hdc_mem = win32gui.CreateCompatibleDC(hdc)
        
        # Obter a resolução da tela
        sw = get_system_metrics(0)  # Largura da tela
        sh = get_system_metrics(1)  # Altura da tela
        
        # Criar uma bitmap compatível
        bm = win32gui.CreateCompatibleBitmap(hdc, sw, sh)
        win32gui.SelectObject(hdc_mem, bm)
        
        # Obter a posição da área de trabalho
        rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        
        # Gerar pontos para o polígono
        inc3 = random.randint(0, 700)
        v = random.randint(0, 1)
        if v == 1:
            inc3 = -700
        inc3 += 1
        
        pt = [
            (rect[0] - inc3, rect[1] + inc3),
            (rect[2] - inc3, rect[1] - inc3),
            (rect[0] + inc3, rect[3] - inc3)
        ]
        
        # Realizar uma transferência de imagem usando um polígono
        win32gui.PlgBlt(hdc_mem, pt, hdc, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], 0, 0, 0)
        
        # Criar uma cor aleatória para o pincel
        brush = win32gui.CreateSolidBrush(win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        win32gui.SelectObject(hdc, brush)
        
        # Copiar o conteúdo da memória para a tela
        win32gui.BitBlt(hdc, random.randint(0, 20), random.randint(0, 20), sw, sh, hdc_mem, random.randint(0, 20), random.randint(0, 20), 0x123456)
        
        # Limpeza dos objetos criados
        win32gui.DeleteObject(brush)
        win32gui.DeleteObject(hdc_mem)
        win32gui.DeleteObject(bm)
        win32gui.ReleaseDC(0, hdc)
        
        sleep(1)  # Atraso de 1 milissegundo

# Função equivalente a GetSystemMetrics
def get_system_metrics(index):
    return ctypes.windll.user32.GetSystemMetrics(index)

# Função equivalente a Sleep (em milissegundos)
def sleep(ms):
    time.sleep(ms / 1000.0)

# Função principal
def main():
    # Exibe o aviso
    exibir_aviso()

    # Efeito piscante
    efeito_piscante()

    # Desenha a bola
    draw_circle()

    # Desenha "pies"
    start_time = time.time()
    while True:
        draw_random_pie()
        if time.time() - start_time >= 10:
            break  # Sai após 10 segundos

    # Efeito BitBlt
    efeito_bitblt()

    # Inicia a thread para o código thing6 após os 10 segundos de efeito
    start_thread_thing6()

    # Aguarda 10 segundos antes de reexecutar a onda senoide
    time.sleep(10)
    # Chama novamente o efeito da onda senoide
    efeito_piscante()

if __name__ == "__main__":
    main()
