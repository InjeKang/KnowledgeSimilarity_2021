import pandas as pd
from multiprocessing import Pool, cpu_count

x_list = [["a"], ["b"], ["c"], ["a", "b", "c"], ["x","y","z","k"]]
y_list = [1,2,3,4,5]

data = pd.DataFrame((zip(x_list, y_list)), columns = ["x", "y"])
data2 = pd.concat([data]*500000, ignore_index=True)

def x2y(df):
    x_ = []
    y_ = []
    for i in range(len(df)):
        if len(df["x"]) == 1:
            x_.append("".join(df["x"][i]))
            y_.append(int(df["y"][i]))
        else:
            for j in range(len(df["x"][i])):
                x_.append("".join(df["x"][i][j]))
                y_.append(int(df["y"][i]))
    output = pd.DataFrame((zip(x_, y_)), columns = ["x2", "y2"])
    return output

result = x2y(data2)

def multi_process(df, target_func):
    pool = Pool() # to define the number of process to be used..default = os.cpu_count()
    results = []
    ITERATION_COUNT = cpu_count() - 1
    count_per_iteration = len(df) / float(ITERATION_COUNT)
    for i in range(ITERATION_COUNT):
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        results.append(pool.apply_async(target_func, (df[list_start:list_end],)))
    pool.close()
    pool.join()
    results_val = [results[i].get() for i in range(len(results)) if results[i].successful()]
    return results_val

result2= pd.concat(multi_process(data, x2y), ignore_index=True)