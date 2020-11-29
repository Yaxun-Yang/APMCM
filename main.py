import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
import numpy as np


color = ['#BF242A', '#FF461F', '#845A33', '#16A951', '#003472', '#FFC64B', '#FF4777', '#50616D', '#FFF2DF', '#1685A9', '#FFB61E']


def csv_read(file_path):
    csv_data = pd.read_csv(file_path, header=0)

    return csv_data





def devision(data, min_y):

    # 以最小值为起点重排序数据集
    new_data = np.vstack((data[min_y:], data[:min_y]))

    # 记录极值点
    ex_value = []
    # 记录从顺时针方向看是否是上升趋势
    up_tend = True

    for i in range(len(new_data) - 1):
        if not up_tend and new_data[i + 1][1] > new_data[i][1]:
            ex_value.append(i)
            up_tend = not up_tend
        elif up_tend and new_data[i + 1][1] < new_data[i][1]:
            ex_value.append(i)
            up_tend = not up_tend
    ex_value.append(len(new_data) - 1)

    # 为方便接下来的计算重新划分数据集, 将最小值点下一个极值点作为全部数据的起点
    temp = ex_value[0]
    ex_value[:] = [x - temp for x in ex_value]
    new_data = np.vstack((new_data[temp:], new_data[:temp]))

    ex_value.append(len(new_data)-1)

    # 每一段分别求function
    function = []
    for i in range(len(ex_value)-1):
        temp_data = np.transpose(new_data[ex_value[i]:ex_value[i+1]])
        function.append(interpolate.interp1d(temp_data[1], temp_data[0], kind=1, fill_value='extrapolate'))

    # 做区域的划分工作
    record = []
    # 记录每组相对应的线段
    func_record = []
    # 记录每组y值的取值范围
    y_record = []
    now_data = new_data[ex_value[0]]
    up_tend = False
    record_tend = False
    flag = False
    for i in range(len(ex_value) - 2):
        if flag:
            flag = False
            continue
        if not up_tend:
            temp = min(new_data[ex_value[i+2]][1], now_data[1])
        else:
            temp = max(new_data[ex_value[i+2]][1], now_data[1])

        y_record.append([min(new_data[ex_value[i+1]][1], temp), max(new_data[ex_value[i+1]][1], temp)])
        func_record.append([i, i+1])
        if temp == now_data[1] and temp != new_data[ex_value[i+1]][1]:
            now_data[0] = function[i + 1](now_data[1])
            up_tend = not up_tend
            while up_tend is not record_tend and record:
                func_record.append([record[-1][0], i+1])
                if up_tend:
                    now_y = min(new_data[ex_value[i+2]][1], record[-1][1])
                else:
                    now_y = max(new_data[ex_value[i+2]][1], record[-1][1])
                y_record.append([min(now_data[1], now_y), max(now_data[1], now_y)])
                now_data = [function[i + 1](now_y), now_y]
                if new_data[ex_value[i+2]][1] == now_y:
                    up_tend = not up_tend
                    flag = True
                    break
                else:
                    record.pop(-1)

        elif temp == new_data[ex_value[i+2]][1] and temp != now_data[1]:
            record.append([i, now_data[1]])
            now_data = new_data[ex_value[i+2]]
            record_tend = up_tend
            flag = True
        else:
            now_data = new_data[ex_value[i+2]]
            flag = True
    return y_record, func_record, function


def color_draw(y_record, func_record, function, color_num):

    for i in range(len(y_record)):

        temp_data = np.arange(y_record[i][0], y_record[i][1], 0.001)
        # print(func_record[i], function[func_record[i][0]](y_record[i]), function[func_record[i][1]](y_record[i]), y_record[i])
        plt.plot(function[func_record[i][0]](temp_data), temp_data, color[color_num[str(func_record[i])]])
        plt.plot(function[func_record[i][1]](temp_data), temp_data, color[color_num[str(func_record[i])]])
    plt.show()


def line_connection(y_record, func_record, function, range_y, color_num):
    interval = 0.1
    x_set = np.arange(range_y[0], range_y[1], interval)
    new_y_record = y_record
    new_func_record = func_record

    for i in range(len(func_record)):
        for j in range(i+1, len(func_record)):
            if new_y_record[j][0] < new_y_record[i][0] or new_y_record[j][0] == new_y_record[i][0] \
                    and new_y_record[j][1] < new_y_record[i][1]:
                temp = new_y_record[i]
                new_y_record[i] = new_y_record[j]
                new_y_record[j] = temp
                temp = new_func_record[i]
                new_func_record[i] = new_func_record[j]
                new_func_record[j] = temp

    scan_list = []
    roof_iter = 0
    total = 0
    num = 0
    # plt.figure(figsize=(20, 20))
    for i in x_set:
        while roof_iter < len(new_y_record) and new_y_record[roof_iter][0] <= i:
            scan_list.append(roof_iter)
            roof_iter += 1
        for j in range(len(scan_list))[::-1]:
            if new_y_record[scan_list[j]][1] < i:
                scan_list.pop(j)
        print(i)
        for x in scan_list:
            print(new_func_record[x], end=' ')
        print('')
        for j in range(len(scan_list)):
            if abs(function[new_func_record[scan_list[j]][1]](i) - function[new_func_record[scan_list[j]][0]](i)) > 2*interval:
                num += 1
                total += abs(function[new_func_record[scan_list[j]][1]](i) - function[new_func_record[scan_list[j]][0]](i)) - 2*interval
                if function[new_func_record[scan_list[j]][1]](i) < - 30:
                    print(function[new_func_record[scan_list[j]][1]](i), new_func_record[scan_list[j]])
                    print(new_y_record[scan_list[j]], i, "!!!!!!!!!!!!!!!")
                plt.plot([min(function[new_func_record[scan_list[j]][0]](i),
                              function[new_func_record[scan_list[j]][1]](i)) + interval,
                          max(function[new_func_record[scan_list[j]][0]](i),
                              function[new_func_record[scan_list[j]][1]](i)) - interval],
                         [i, i], color=color[color_num[str(new_func_record[scan_list[j]])]], linewidth=1)
    color_draw(y_record, func_record, function, color_num)
    return total, num


def main():
    plt.figure(figsize=[8, 5])
    data = csv_read('Attachment 1/graph1.csv').to_numpy()

    # 2*n to n*2

    # 求y轴上的极值
    range_y = [data[np.argmin(data.transpose()[1])][1], data[np.argmax(data.transpose()[1])][1]]
    # range_x = [data[np.argmin(data.transpose()[0])][0], data[np.argmax(data.transpose()[0])][0]]
    y_record, func_record, function = devision(data, np.argmin(data.transpose()[1]))
    color_num = {}
    for i in range(len(func_record)):
        color_num[str(func_record[i])] = i

    # color_draw(y_record, func_record, function)

    total, num = line_connection(y_record, func_record, function, range_y, color_num)
    print(total, num)


if __name__ == '__main__':
    main()


