import streamlit as st

def obter_texto(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade):
    filtros_selecionados = []

    if anos:
        filtros_selecionados.append(f"<b>Ano(s)</b>: {', '.join(map(str, anos))}")
    if site:
        filtros_selecionados.append(f"<b>Site(s)</b>: {', '.join(map(str, site))}")
    if nick:
        filtros_selecionados.append(f"<b>Nickname(s)</b>: {', '.join(map(str, nick))}")
    if tamanho_field:
        filtros_selecionados.append(f"<b>Tamanho(s) de Field</b>: {', '.join(map(str, tamanho_field))}")
    if intervalo_buyin:
        filtros_selecionados.append(f"<b>Intervalo(s) de Buy-in</b>: {', '.join(map(str, intervalo_buyin))}")
    if dia_semana:
        filtros_selecionados.append(f"<b>Dia(s) da Semana</b>: {', '.join(map(str, dia_semana))}")
    if mes:
        filtros_selecionados.append(f"<b>Mês(es)</b>: {', '.join(map(str, mes))}")
    if tipo_de_torneio:
        filtros_selecionados.append(f"<b>Tipo(s) de Torneio(s)</b>: {', '.join(map(str, tipo_de_torneio))}")
    if tipo_de_duraçao:
        filtros_selecionados.append(f"<b>Duração(ões)</b>: {', '.join(map(str, tipo_de_duraçao))}")
    if tipo_de_intervalo:
        filtros_selecionados.append(f"<b>Intervalo(s) de Horário(s)</b>: {', '.join(map(str, tipo_de_intervalo))}")
    if moeda:
        filtros_selecionados.append(f"<b>Moeda(s)</b>: {', '.join(map(str, moeda))}")
    if rebuy:
        filtros_selecionados.append(f"<b>Rebuy(s)</b>: {', '.join(map(str, rebuy))}")
    if velocidade:
        filtros_selecionados.append(f"<b>Velocidade(s)</b>: {', '.join(map(str, velocidade))}")

    texto_informativo = "<br>".join(filtros_selecionados)

    return f"<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>{texto_informativo}" if texto_informativo else "<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>"
