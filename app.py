import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from charts import loss_ranking, rain_scatter, ranking, seasonality, timeline
from data import DATA_PATH, load_data, rain_correlation


st.set_page_config(page_title="Consumo de Água no Brasil", layout="wide")


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data(DATA_PATH)


def show_chart(fig) -> None:
    st.pyplot(fig)
    plt.close(fig)


def main() -> None:
    st.title("Consumo de Água no Brasil")
    st.caption(
        "Aluno: Daniel de Oliveira Teixeira Silva · "
        "Disciplina: Linguagens de Programação · "
        "Professor: Alexandre Neves Louzada"
    )
    st.markdown("[Repositório no GitHub](https://github.com/ozelfls/Linguagens-de-prog-G1-Trabalho)")
    st.caption("Consumo, perdas e clima em uma base simulada de 2015 a 2024.")

    try:
        data = get_data()
    except (OSError, ValueError) as error:
        st.error(f"Não foi possível carregar a base: {error}")
        st.stop()

    all_option = "Todos"
    st.sidebar.header("Filtros")
    years = st.sidebar.slider(
        "Período",
        min_value=int(data["ano"].min()),
        max_value=int(data["ano"].max()),
        value=(int(data["ano"].min()), int(data["ano"].max())),
    )
    region = st.sidebar.selectbox("Região", [all_option, *sorted(data["regiao"].unique())])
    sector = st.sidebar.selectbox("Setor", [all_option, *sorted(data["setor_consumo"].unique())])
    state_options = data if region == all_option else data.loc[data["regiao"].eq(region)]
    with st.sidebar.expander("Mais filtros"):
        month = st.selectbox("Mês", [all_option, *range(1, 13)])
        state = st.selectbox("Estado", [all_option, *sorted(state_options["uf"].unique())])
        alert = st.selectbox("Nível de alerta", [all_option, *sorted(data["nivel_alerta"].unique())])

    filtered = data.loc[data["ano"].between(*years)]
    for column, value in (
        ("regiao", region),
        ("setor_consumo", sector),
        ("mes", month),
        ("uf", state),
        ("nivel_alerta", alert),
    ):
        if value != all_option:
            filtered = filtered.loc[filtered[column].eq(value)]
    st.sidebar.caption(f"{len(filtered):,} registros na seleção")
    if filtered.empty:
        st.warning("Nenhum registro corresponde aos filtros selecionados.")
        st.stop()

    state_totals = filtered.groupby("uf")["consumo_milhoes_litros"].sum()
    sector_totals = filtered.groupby("setor_consumo")["consumo_milhoes_litros"].sum()
    metrics = [
        ("Consumo total", f"{filtered['consumo_milhoes_litros'].sum():,.1f} milhões L"),
        ("Estado líder", state_totals.idxmax()),
        ("Setor líder", sector_totals.idxmax()),
    ]
    for column, (label, value) in zip(st.columns(3), metrics):
        column.metric(label, value)

    evolution, comparisons, environment, table = st.tabs(
        ["Evolução", "Comparar", "Ambiente", "Dados"]
    )
    with evolution:
        show_chart(timeline(filtered))
        st.caption("A média móvel usa até 12 meses disponíveis na seleção.")
        with st.expander("Ver sazonalidade por mês"):
            show_chart(seasonality(filtered))

    with comparisons:
        left, right = st.columns(2)
        with left:
            show_chart(ranking(filtered, "uf", "Consumo por estado"))
        with right:
            show_chart(ranking(filtered, "setor_consumo", "Consumo por setor"))
        with st.expander("Ver comparação entre regiões"):
            show_chart(ranking(filtered, "regiao", "Consumo por região"))
        st.caption(
            "Os totais somam os registros da amostra. Há quantidades diferentes de registros "
            "por estado; portanto, o ranking não representa o consumo real de cada UF."
        )

    with environment:
        environmental_metrics = [
            ("Per capita médio", f"{filtered['consumo_per_capita'].mean():,.1f}"),
            ("Desperdício médio", f"{filtered['desperdicio_percentual'].mean():,.1f}%"),
            ("Reservatórios médios", f"{filtered['reservatorios_percentual'].mean():,.1f}%"),
        ]
        for column, (label, value) in zip(st.columns(3), environmental_metrics):
            column.metric(label, value)
        st.caption(
            f"Chuva média: {filtered['chuva_mm'].mean():.1f} mm · "
            f"Alertas altos ou críticos: {filtered['nivel_alerta'].isin(['Alto', 'Crítico']).sum()} registros"
        )
        show_chart(rain_scatter(filtered))
        correlation = rain_correlation(filtered)
        if pd.notna(correlation):
            st.write(f"Correlação de Pearson entre chuva média e consumo mensal: **{correlation:.2f}**.")
        else:
            st.write("Não há meses suficientes para calcular a correlação.")
        st.caption("A correlação descreve associação na base simulada; não indica causa.")
        with st.expander("Ver desperdício por estado"):
            show_chart(loss_ranking(filtered))
            st.caption("Média simples do percentual de desperdício registrado para cada UF.")

    with table:
        st.dataframe(filtered, width="stretch", hide_index=True)
        st.download_button(
            "Baixar dados filtrados",
            filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="consumo_agua_filtrado.csv",
            mime="text/csv",
        )

    with st.expander("Conclusão executiva"):
        st.write(
            f"Nos {len(filtered):,} registros selecionados, {state_totals.idxmax()} lidera a soma "
            f"de consumo e o setor {sector_totals.idxmax()} tem o maior total. "
            f"O desperdício médio é {filtered['desperdicio_percentual'].mean():.1f}% e o nível "
            f"médio dos reservatórios é {filtered['reservatorios_percentual'].mean():.1f}%. "
            "Os dados simulados não permitem conclusões sobre a situação hídrica real do Brasil."
        )


if __name__ == "__main__":
    main()
