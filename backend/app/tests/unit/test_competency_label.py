from app.services.competency_label import competency_name


def test_nome_traz_os_dois_meses_da_janela():
    assert competency_name(8) == "Agosto/Setembro"
    assert competency_name(9) == "Setembro/Outubro"


def test_virada_de_ano_volta_para_janeiro():
    assert competency_name(12) == "Dezembro/Janeiro"


def test_mes_invalido_nao_explode():
    assert competency_name(0) == ""
    assert competency_name(13) == ""
