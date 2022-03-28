#
# https://pandas.pydata.org/docs/user_guide/10min.html
#

# %%
import numpy as np
import pandas as pd

#%%
s = pd.Series([1, 2, 5, np.nan, 6, 8])
print(s)


#%%
# 4 dais sta
dates = pd.date_range("20130101", periods=6)

# %% 6 x 4 datafrane
df = pd.DataFrame(np.random.randn(6, 4), columns=list("ABCD"))
df
# %%
print(df.describe())
print(df.head())
print(df.tail())

# %%
df.sort_values(by="D")


# %%
df2 = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)
df2
# %%
df2.loc[:, ["A", "E"]]

# %%
