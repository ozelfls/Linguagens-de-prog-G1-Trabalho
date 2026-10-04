import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data import monthly_series


sns.set_theme(style="whitegrid", palette="crest")


def timeline(frame: pd.DataFrame):
    monthly = monthly_series(frame)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly["data"], monthly["consumo_milhoes_litros"], label="Consumo mensal")
    ax.plot(monthly["data"], monthly["media_movel_12m"], label="Média móvel (12 meses)")
    ax.set(ylabel="Milhões de litros", xlabel="Mês")
    ax.legend()
    fig.tight_layout()
    return fig


def ranking(frame: pd.DataFrame, column: str, title: str):
    totals = (
        frame.groupby(column, as_index=False)["consumo_milhoes_litros"]
        .sum()
        .sort_values("consumo_milhoes_litros", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, max(3.5, len(totals) * 0.34)))
    sns.barplot(data=totals, y=column, x="consumo_milhoes_litros", ax=ax, color="#147d87")
    ax.set(title=title, xlabel="Milhões de litros", ylabel="")
    fig.tight_layout()
    return fig


def rain_scatter(frame: pd.DataFrame):
    monthly = frame.groupby("data", as_index=False).agg(
        consumo=("consumo_milhoes_litros", "sum"),
        chuva=("chuva_mm", "mean"),
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=monthly, x="chuva", y="consumo", ax=ax, color="#147d87")
    ax.set(xlabel="Chuva média mensal (mm)", ylabel="Consumo mensal (milhões de litros)")
    fig.tight_layout()
    return fig


def loss_ranking(frame: pd.DataFrame):
    losses = (
        frame.groupby("uf", as_index=False)["desperdicio_percentual"]
        .mean()
        .sort_values("desperdicio_percentual", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, max(3.5, len(losses) * 0.34)))
    sns.barplot(data=losses, y="uf", x="desperdicio_percentual", ax=ax, color="#147d87")
    ax.set(title="Desperdício médio por estado", xlabel="Percentual médio", ylabel="")
    fig.tight_layout()
    return fig


def seasonality(frame: pd.DataFrame):
    monthly = frame.groupby(["ano", "mes"], as_index=False)["consumo_milhoes_litros"].sum()
    table = monthly.pivot(index="ano", columns="mes", values="consumo_milhoes_litros")
    fig, ax = plt.subplots(figsize=(10, max(3.5, len(table) * 0.35)))
    sns.heatmap(table, cmap="YlGnBu", ax=ax, cbar_kws={"label": "Milhões de litros"})
    ax.set(xlabel="Mês", ylabel="Ano")
    fig.tight_layout()
    return fig
