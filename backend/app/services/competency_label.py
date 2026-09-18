"""Rótulo da competência.

A competência não coincide com o mês civil: vai do dia 26 do mês inicial ao dia 25
do mês seguinte. Por isso o nome exibido traz os dois meses (ex.: Agosto/Setembro).
"""

MONTH_NAMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


def competency_name(month: int) -> str:
    """Nome da competência a partir do mês inicial: 8 -> 'Agosto/Setembro'."""
    start = MONTH_NAMES.get(month, "")
    end = MONTH_NAMES.get(month % 12 + 1, "")
    return f"{start}/{end}" if start and end else ""
