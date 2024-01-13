import pandas as pd
from classes.bid import Bid


def inteception_asks_with_bids(bids: list[Bid], asks: list[Bid]):
    df_b = pd.DataFrame(b.__dict__ for b in bids)
    df_a = pd.DataFrame(a.__dict__ for a in asks)
    df_ask_x = df_a["energy"].cumsum().abs().repeat(2)
    df_bid_x = df_b["energy"].cumsum().abs().repeat(2)
    df_ask_x = pd.concat([pd.Series([0]), df_ask_x])
    df_bid_x = pd.concat([pd.Series([0]), df_bid_x])
    df_bid_x = df_bid_x.iloc[:-1]
    df_ask_x = df_ask_x.iloc[:-1]
    df_ask_y = df_a["buy_price"].repeat(2)
    df_bid_y = df_b["sell_price"].repeat(2)

    if len(df_ask_x) == 2 or len(df_bid_x) == 2:
        if df_ask_y.iloc[0] == df_bid_y.iloc[0]:
            return df_ask_x[1], df_ask_y[1]
        return None, None

    for i in range(0, len(df_ask_x) - 1):
        for k in range(1, len(df_bid_x) - 1):
            if (df_ask_x.iloc[i] == df_ask_x.iloc[i + 1] and df_bid_x.iloc[k] <= df_ask_x.iloc[i] <= df_bid_x.iloc[k + 1] and df_ask_y.iloc[i + 1] <= df_bid_y.iloc[k] <= df_ask_y.iloc[i]):
                return df_ask_x.iloc[i], df_bid_y.iloc[k]

            elif (df_ask_x.iloc[i] <= df_bid_x.iloc[k] <= df_ask_x.iloc[i + 1] and df_bid_y.iloc[k] <= df_ask_y.iloc[i] <= df_bid_y.iloc[k + 1]):
                if df_bid_x.iloc[k] == df_bid_x.iloc[k + 1] == df_ask_x.iloc[i + 1]:
                    return df_ask_x.iloc[k], (df_bid_y.iloc[k] + df_ask_y.iloc[i]) / 2
                return df_bid_x.iloc[k], df_ask_y.iloc[i]

    if (df_bid_x.iloc[-1] < df_ask_x.iloc[-1] and df_bid_y.iloc[-1] <= df_ask_y.loc[df_ask_x.ge(df_bid_x.iloc[-1]).idxmax()].iat[0]):
        y = (df_ask_y.loc[df_ask_x.ge(df_bid_x.iloc[-1]).idxmax()].iat[0] + df_bid_y.iloc[-1]) / 2
        return df_bid_x.iloc[-1], y

    if (df_ask_x.iloc[-1] < df_bid_x.iloc[-1] and df_ask_y.iloc[-1] >= df_bid_y.loc[df_bid_x.ge(df_ask_x.iloc[-1]).idxmax()].iat[0]):
        y = (df_bid_y.loc[df_bid_x.ge(df_ask_x.iloc[-1]).idxmax()].iat[0] + df_ask_y.iloc[-1]) / 2
        return df_ask_x.iloc[-1], y
    return None, None
