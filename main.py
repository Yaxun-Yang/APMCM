import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
import numpy as np


def csv_read(file_path):
    csv_data = pd.read_csv(file_path, header=0)

    return csv_data


def draw(data):
    # 2*n to n*2
    data2 = data.transpose()

    # 求y轴上的极值
    max_y = np.argmax(data2[1])
    min_y = np.argmin(data2[1])
    
    # 分别构造左右数据集
    left_data = np.transpose(data[max_y:min_y])
    right_data = np.transpose(np.vstack((data[min_y:-1], data[0:max_y])))

    # 原始数据点集
    # plt.scatter(left_data[0], left_data[1], marker='o', color='green', s=1)
    # plt.scatter(right_data[0], right_data[1], marker="o", color='blue', s=1)

    # 作插值
    left_function = interpolate.interp1d(left_data[1], left_data[0], kind="cubic")
    right_function = interpolate.interp1d(right_data[1], right_data[0], kind="cubic")
    # 插值后图像
    plt.plot(left_function(left_data[1]), left_data[1])
    plt.plot(right_function(right_data[1]), right_data[1])

    plt.show()


def main():
    data = csv_read('Attachment 1/graph1.csv').to_numpy()
    draw(data)


if __name__ == '__main__':
    main()


