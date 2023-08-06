import os


def divide(x, y, r=None, percent=None):
    """
    :param x: 除数
    :param y: 被除数
    :param r: default None, 保留小数位
    :param percent: default None, 百分比类型，可选：ratio（占比）、compare（增减百分比）
    """
    if not percent:
        if y == 0:
            return 0
        else:
            if r:
                return round(x / y, r)
            else:
                return x / y
    elif percent == "ratio":
        if y == 0:
            return "0.00%"
        else:
            return "{:.2%}".format(x / y)
    elif percent == "compare":
        if y == 0:
            return "-"
        else:
            return "{:.2%}".format(x / y - 1)


def print_df(df):
    print("\t", "\t".join(df.columns.astype(str)))
    for idx, row in df.iterrows():
        print(idx, "\t", "\t".join(row.astype(str).values))


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
