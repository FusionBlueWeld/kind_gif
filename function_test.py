import math
import numpy as np
import matplotlib.pyplot as plt

def define_variables():
    return {
        "x1": np.linspace(0, 800, 200),
        "x2": np.linspace(-6, 6, 200),
        "x3": np.linspace(0, 7, 200),
        "x4": np.linspace(0, 2000, 200)
    }

def define_labels():
    variable_labels = {
        "x1": "welding speed",
        "x2": "head position",
        "x3": "material thickness",
        "x4": "laser power"
    }

    unit_labels = {
        "x1": "mm/sec",
        "x2": "mm",
        "x3": "mm",
        "x4": "W"
    }

    return variable_labels, unit_labels

def h(x1, x2, x3, x4):
    # welding_speedの関数
    lambda_1 = 0.0045
    g_x1 =  np.exp(-lambda_1 * abs(x1))

    # head_positionの関数
    mu = 0
    sigma = 2
    f_x2 = (1 / math.sqrt(2 * math.pi * sigma**2)) * np.exp(-((x2 - mu)**2) / (2 * sigma**2))

    # material_thicknessの関数
    lambda_3 = 1.0
    C = 0.5
    s_x3 = C + (1 - C) * np.exp(-lambda_3 * x3)

    # laser_powerの関数
    alpha = 1.0
    l_x4 = 1 + alpha * (x4 / 100)

    return f_x2 * g_x1 * s_x3 * l_x4

def initialize_h_dict(trigger, variable_values):
    # h_dict を初期化
    h_dict = {}
    
    # トリガーのキーを反復処理
    for key in trigger.keys():
        # x_var が指定された場合、x_axis と h_dict を設定
        if trigger[key] == "x_var":
            x_axis = (key, variable_values[key])
            h_dict[key] = variable_values[key]
        # y_var が指定された場合、y_axis と h_dict を設定
        elif trigger[key] == "y_var":
            y_axis = (key, variable_values[key])
            h_dict[key] = variable_values[key]
        # それ以外の場合、h_dict にトリガーの値を設定
        else:
            h_dict[key] = trigger[key]
    
    # h_dict, x_axis, y_axis を返す
    return h_dict, x_axis, y_axis


def create_grid(x_axis, y_axis):
    X, Y = np.meshgrid(x_axis[1], y_axis[1])
    return X, Y

def assign_variable_values(x_axis, y_axis, X, Y, h_dict, trigger):
    # 変数を初期化
    x1 = x2 = x3 = x4 = None

    # x_axisに対応する変数にXの値を割り当てる
    if x_axis[0] == "x1":
        x1 = X
    elif x_axis[0] == "x2":
        x2 = X
    elif x_axis[0] == "x3":
        x3 = X
    else:
        x4 = X

    # y_axisに対応する変数にYの値を割り当てる
    if y_axis[0] == "x1":
        x1 = Y
    elif y_axis[0] == "x2":
        x2 = Y
    elif y_axis[0] == "x3":
        x3 = Y
    else:
        x4 = Y

    # 割り当てられていない変数にtriggerの値を割り当てる
    if x1 is None:
        x1 = trigger["x1"]
    elif x2 is None:
        x2 = trigger["x2"]
    elif x3 is None:
        x3 = trigger["x3"]
    else:
        x4 = trigger["x4"]

    # 再度、割り当てられていない変数にtriggerの値を割り当てる
    if x1 is None:
        x1 = trigger["x1"]
    elif x2 is None:
        x2 = trigger["x2"]
    elif x3 is None:
        x3 = trigger["x3"]
    else:
        x4 = trigger["x4"]

    # h関数に渡す変数のリストを作成
    h_values = [x1, x2, x3, x4]
    return h_values


def plot_graph(X, Y, Z, trigger, variable_labels, unit_labels):
    # グラフのフィギュアを作成
    plt.figure()
    # X, Y, Z のデータを使ってカラーメッシュを描画
    plt.pcolormesh(X, Y, Z, cmap='jet')
    # カラーバーを追加し、ラベルを設定
    plt.colorbar(label='Amplitude')
    # グリッドを表示
    plt.grid()

    # x軸とy軸の変数名を取得
    keys_with_x_var = [key for key, value in trigger.items() if value == "x_var"][0]
    keys_with_y_var = [key for key, value in trigger.items() if value == "y_var"][0]
    # x軸とy軸以外の変数名を取得
    keys_with_not_xy_var = [key for key, value in trigger.items() if value not in ["x_var", "y_var"]]

    # x軸のラベルを設定
    plt.xlabel(f"{variable_labels[keys_with_x_var]} [{unit_labels[keys_with_x_var]}]")
    # y軸のラベルを設定
    plt.ylabel(f"{variable_labels[keys_with_y_var]} [{unit_labels[keys_with_y_var]}]")

    # グラフのタイトルを設定
    plt.title(f"{variable_labels[keys_with_not_xy_var[0]]}: {trigger[keys_with_not_xy_var[0]]} [{unit_labels[keys_with_not_xy_var[0]]}], {variable_labels[keys_with_not_xy_var[1]]}: {trigger[keys_with_not_xy_var[1]]} [{unit_labels[keys_with_not_xy_var[1]]}]")

    # グラフを表示
    plt.show()

def main(trigger):
    # 変数の定義
    variable_values = define_variables()
    # ラベルの定義
    variable_labels, unit_labels = define_labels()
    # h_dict, x_axis, y_axis の初期化
    h_dict, x_axis, y_axis = initialize_h_dict(trigger, variable_values)
    # グリッドの作成
    X, Y = create_grid(x_axis, y_axis)
    # 変数の値を割り当て
    h_values = assign_variable_values(x_axis, y_axis, X, Y, h_dict, trigger)
    # h(x1, x2, x3, x4) の計算
    Z = h(h_values[0], h_values[1], h_values[2], h_values[3])
    # グラフの描画
    plot_graph(X, Y, Z, trigger, variable_labels, unit_labels)

# main関数を実行
if __name__ == "__main__":
    # トリガー1の定義
    trigger1 = {
        "x1": 500,
        "x2": "y_var",
        "x3": 1.0,
        "x4": "x_var"
    }

    # トリガー1を使ってmain関数を実行
    main(trigger1)
