from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np


def calculate_k(i, j):
    """k 值计算函数"""
    x1, y1 = df_x.iloc[i-3, j-3], df_y.iloc[i-3, j-3]
    x2, y2 = df_x.iloc[i+3, j-3], df_y.iloc[i+3, j-3]
    x3, y3 = df_x.iloc[i+3, j+3], df_y.iloc[i+3, j+3]
    x4, y4 = df_x.iloc[i-3, j+3], df_y.iloc[i-3, j+3]
    k = np.max([np.sqrt(np.square(x4-x2) + np.square(y4-y2)),
                np.sqrt(np.square(x3-x1) + np.square(y3-y1))])
    return k


if __name__ == "__main__":
    # 读取原始数据矩阵
    df_x_ = pd.read_excel("x-displacement.xlsx", header=None)
    df_y_ = pd.read_excel("y-displacement.xlsx", header=None)
    # 检查文件尺寸
    try:
        df_x_.shape == df_y_.shape
        print(f"读取到形状为 {df_x_.shape} 的数据矩阵")
    except:
        print("位移数据尺寸不匹配")
    # 方便计算将原始矩阵向 4 个方向拓展 3 个 0 单位
    df_x = pd.DataFrame(np.pad(df_x_, ((3, 3), (3, 3)), 'constant'))
    df_y = pd.DataFrame(np.pad(df_y_, ((3, 3), (3, 3)), 'constant'))

    df_k_ = df_x.copy()
    # 遍历原始数据坐标
    for i in range(len(df_x_.index)):
        for j in range(len(df_x_.columns)):
            # 计算 k 并赋值于拓展矩阵
            df_k_.iloc[i, j] = calculate_k(i, j)
    # 切割拓展矩阵为原始矩阵大小
    df_k = df_k_.iloc[3:-3, 3:-3]
    # 保存 K 值数据文件
    df_k.to_csv("k_values.csv", index=None)

    # 绘制 k 值分布图
    X, Y = np.meshgrid([x for x in range(len(df_k.columns))], [y for y in range(len(df_k))])
    Z = df_k.values
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='winter')
    plt.savefig("Figure.svg")
    plt.show()