from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "dados" / "simulacao_consumo_agua_brasil.csv"
NUMERIC_COLUMNS = [
    "consumo_milhoes_litros",
    "desperdicio_percentual",
    "reservatorios_percentual",
    "chuva_mm",
    "temperatura_media",
    "populacao",
    "consumo_per_capita",
]
REQUIRED_COLUMNS = [
    "ano", "mes", "data", "regiao", "uf", "setor_consumo",
    *NUMERIC_COLUMNS, "nivel_alerta",
]


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {', '.join(sorted(missing))}")

    frame = frame[REQUIRED_COLUMNS].copy()
    frame["data"] = pd.to_datetime(frame["data"], errors="coerce")
    for column in ["ano", "mes", *NUMERIC_COLUMNS]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    for column in ["regiao", "uf", "setor_consumo", "nivel_alerta"]:
        frame[column] = frame[column].astype("string").str.strip()

    frame = frame.dropna(subset=REQUIRED_COLUMNS).drop_duplicates()
    frame = frame.loc[
        frame["ano"].eq(frame["data"].dt.year)
        & frame["mes"].eq(frame["data"].dt.month)
        & frame["mes"].between(1, 12)
        & frame["consumo_milhoes_litros"].ge(0)
        & frame["desperdicio_percentual"].between(0, 100)
        & frame["reservatorios_percentual"].between(0, 100)
    ].copy()
    frame[["ano", "mes"]] = frame[["ano", "mes"]].astype(int)
    return frame.sort_values(["data", "regiao", "uf"]).reset_index(drop=True)


def monthly_series(frame: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        frame.groupby("data", as_index=False)["consumo_milhoes_litros"]
        .sum()
        .sort_values("data")
    )
    monthly["media_movel_12m"] = (
        monthly["consumo_milhoes_litros"]
        .rolling(window=12, min_periods=3)
        .mean()
    )
    return monthly


def rain_correlation(frame: pd.DataFrame) -> float:
    monthly = frame.groupby("data", as_index=False).agg(
        consumo=("consumo_milhoes_litros", "sum"),
        chuva=("chuva_mm", "mean"),
    )
    return float(monthly["chuva"].corr(monthly["consumo"]))
