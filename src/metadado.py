from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    metadado.nao_requer_login = True
    metadado.nao_requer_captcha = True
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO
    metadado.extensao = Coleta.Metadados.Extensao.XLS
    metadado.estritamente_tabular = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    if month in [6, 7] and year == 2019:
        metadado.formato_consistente = False
    else:
        metadado.formato_consistente = True

    return metadado
