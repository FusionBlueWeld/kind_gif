import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# x3の値
x3_values = np.arange(0, 7, 0.1)

# 平均と標準偏差
mu = 0
sigma = 2

# 減衰強度パラメータ
decay_param = 0.0045

# x3の影響を決めるパラメータ
x3_decay_param = 1.0
saturation_param = 0.5

# x4の値
x4_values = [0, 500, 1000, 1500, 2000]

# x1とx2の値
x1 = np.linspace(-6, 6, 100)
x2 = np.linspace(0, 800, 100)

# 画像を保存するフォルダ
output_folder = "png_files"

# フォルダが存在しない場合、作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for x4 in x4_values:
    # Amplitude scaling factor
    amplitude_scale = 1 + (x4 / 100)

    # GIFに保存する画像のリスト
    images = []

    n = 1
    for x3 in x3_values:
        # グリッドを作成
        X1, X2 = np.meshgrid(x2, x1)

        # x3の影響を計算
        x3_effect = saturation_param * (1 - np.exp(-x3_decay_param * x3))

        # ガウス関数
        Y = amplitude_scale * ((1 / (np.sqrt(2 * np.pi * sigma**2))) * np.exp(- (X2 - mu)**2 / (2 * sigma**2))) * np.exp(-decay_param * np.abs(X1)) * x3_effect

        # プロット
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(Y, interpolation='bilinear', origin='lower', cmap='jet', extent=(0, 800, -6, 6), aspect='auto', vmin=0, vmax=0.5)

        ax.set_title(f'2D Gaussian (x1, x2 variable) - x3 = {x3:.1f}, x4 = {x4}')
        ax.set_xlabel('x2')
        ax.set_ylabel('x1')
        plt.colorbar(ax.imshow(Y, interpolation='bilinear', origin='lower', cmap='jet', extent=(0, 800, -6, 6), aspect='auto', vmin=0, vmax=0.5), ax=ax, label='Amplitude')
        plt.grid(True)

        # 画像をフォルダに保存
        plt.savefig(os.path.join(output_folder, f'frame_x3_{x3:.1f}_x4_{x4}.png'))
        plt.close(fig)

        # 画像を読み込む
        images.append(imageio.imread(os.path.join(output_folder, f'frame_x3_{x3:.1f}_x4_{x4}.png')))

        print(f"n={n}")
        n += 1

    # GIFアニメーションを作成
    imageio.mimsave(f'output_x4_{x4}.gif', images, duration=100, loop=0)
