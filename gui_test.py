import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 2次元ガウシアン関数の定義
def gaussian_2d(x, y, a=1, x0=0, y0=0, sigma_x=1, sigma_y=1):
    exp_x = -((x - x0) ** 2) / (2 * sigma_x ** 2)
    exp_y = -((y - y0) ** 2) / (2 * sigma_y ** 2)
    return a * np.exp(exp_x + exp_y)

# 2次元ガウシアン分布をプロットする関数
def plot_gaussian_2d():
    global colorbar

    amplitude = float(entry_box_a.get())
    x0 = float(entry_box_x0.get())
    y0 = float(entry_box_y0.get())
    sigma_x = float(entry_box_sigma_x.get())
    sigma_y = float(entry_box_sigma_y.get())

    X, Y = np.meshgrid(x, y)
    Z = gaussian_2d(X, Y, a=amplitude, x0=x0, y0=y0, sigma_x=sigma_x, sigma_y=sigma_y)
    ax.clear()

    if 'colorbar' in globals():
        colorbar.remove()

    c = ax.pcolormesh(X, Y, Z, cmap='jet', shading='auto')
    colorbar = fig.colorbar(c, ax=ax)

    ax.grid(True)

    canvas.draw()

def main():
    # 1. グローバル変数の設定
    global entry_box_a, entry_box_x0, entry_box_y0, entry_box_sigma_x, entry_box_sigma_y, canvas, ax, x, y, fig, colorbar

    # 2. ウィンドウの作成
    window = tk.Tk()
    window.title("2D Gaussian colormap")

    # 3. 描画範囲の設定
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)

    # 4. グラフの初期化
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # 5. ラベルと入力ボックスの作成
    label_a = tk.Label(window, text="Amplitude:")
    label_a.pack(side=tk.LEFT)
    entry_box_a = tk.Entry(window)
    entry_box_a.insert(0, '1')
    entry_box_a.pack(side=tk.LEFT)

    label_x0 = tk.Label(window, text="x0:")
    label_x0.pack(side=tk.LEFT)
    entry_box_x0 = tk.Entry(window)
    entry_box_x0.insert(0, '0')
    entry_box_x0.pack(side=tk.LEFT)

    label_y0 = tk.Label(window, text="y0:")
    label_y0.pack(side=tk.LEFT)
    entry_box_y0 = tk.Entry(window)
    entry_box_y0.insert(0, '0')
    entry_box_y0.pack(side=tk.LEFT)

    label_sigma_x = tk.Label(window, text="sigma_x:")
    label_sigma_x.pack(side=tk.LEFT)
    entry_box_sigma_x = tk.Entry(window)
    entry_box_sigma_x.insert(0, '1')
    entry_box_sigma_x.pack(side=tk.LEFT)

    label_sigma_y = tk.Label(window, text="sigma_y:")
    label_sigma_y.pack(side=tk.LEFT)
    entry_box_sigma_y = tk.Entry(window)
    entry_box_sigma_y.insert(0, '1')
    entry_box_sigma_y.pack(side=tk.LEFT)

    # 6. ボタンの作成
    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.TOP)

    calculate_button = tk.Button(button_frame, text="Calculate", command=plot_gaussian_2d)
    calculate_button.pack(side=tk.LEFT)

    exit_button = tk.Button(button_frame, text="EXIT", command=window.quit)
    exit_button.pack(side=tk.LEFT)

    # 7. 2次元ガウシアン分布のプロット
    plot_gaussian_2d()

    # 8. イベントループの開始
    window.mainloop()


if __name__ == "__main__":
    main()





def depth_function(x1, x2, x3, x4, x2_mu, x2_sigma, x1_decay_param, x3_decay_param, x3_saturation_param):
    amplitude_scale = 1 + (x4 / 100)
    x3_effect = x3_saturation_param * (1 - np.exp(-x3_decay_param * x3))
    Y = amplitude_scale * ((1 / (np.sqrt(2 * np.pi * x2_sigma**2))) * np.exp(- (x2 - x2_mu)**2 / (2 * x2_sigma**2))) * np.exp(-x1_decay_param * np.abs(x1)) * x3_effect
    return Y

x1_values = np.linspace(-6, 6, 100)
x2_values = np.linspace(0, 800, 100)
x3_values = np.arange(0, 7, 0.1)
x4_values = np.arange(0, 2000, 500)

x1_decay_param = 0.0045
x2_mu = 0
x2_sigma = 2
x3_decay_param = 1.0
x3_saturation_param = 0.5