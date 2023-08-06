# -*- coding: utf-8 -*-
# @Time    : 2022-11-15 11:29
# @Author  : zbmain


def view_df(df, head_num: int = 5, tail_num: int = 5, comment: str = 'DataFrame'):
    print('%s row_size:%d' % (comment, df.shape[0]))
    return None if -1 in (head_num, tail_num) else df.head(head_num).append(df.tail(tail_num))


def check_null(x, null_values: list = []):
    """
    检测空值

    @param x: 检测值
    @param null_values: list 检测值黑名单表,都作为None.
    """
    import pandas as pd
    return None if x and str(x).lower() in map(lambda z: z.lower(), null_values) or pd.isna(x) or pd.isnull(x) \
        else x


if __name__ == '__main__':
    import numpy as np

    print(check_null(np.nan))
