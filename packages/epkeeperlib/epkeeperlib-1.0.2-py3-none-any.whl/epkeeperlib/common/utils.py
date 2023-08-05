import pandas as pd


def get_ele_use(epi: pd.Series, freq="H", negative_trend_check=True):
    if not isinstance(epi, pd.Series):
        raise TypeError("INPUT EPI NOT pandas.Series TYPE!")
    if not isinstance(epi.index, pd.DatetimeIndex):
        raise TypeError("INPUT EPI INDEX NOT datetime TYPE!")
    epi_dif = epi.sort_index().diff().fillna(0)
    if negative_trend_check:
        if (epi_dif < 0).any():
            raise ValueError("EPI DATA HAS NEGATIVE TREND!")
    epi.sort_index(inplace=True)
    epi_mark = epi.resample(freq).first().interpolate("linear").append(epi.iloc[[-1]])
    ele = -epi_mark.diff(periods=-1).dropna()
    return ele


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

