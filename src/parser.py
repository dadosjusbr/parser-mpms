# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import *
import number


def parse_employees(fn, chave_coleta, categoria):
    employees = {}
    counter = 1
    for row in fn:
        if not number.is_nan(row[0]):
            if row[0] == "TOTAL GERAL" or row[0] == "Total":
                break
            else:
                matricula = row[0]
                name = row[1]
                function = row[2]
                location = row[3]
                if not number.is_nan(matricula) and matricula != "Matrícula" and matricula != "MATRÍCULA":
                    membro = Coleta.ContraCheque()
                    membro.id_contra_cheque = chave_coleta + "/" + str(counter)
                    membro.chave_coleta = chave_coleta
                    membro.matricula = str(matricula)
                    membro.nome = name
                    membro.funcao = function
                    membro.local_trabalho = location
                    membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
                    membro.ativo = True

                    membro.remuneracoes.CopyFrom(
                        cria_remuneracao(row, categoria)
                    )

                    employees[str(matricula)] = membro
                    counter += 1

    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneracao.valor = float(abs(number.format_value(row[value])))

        if (categoria == CONTRACHEQUE or categoria == CONTRACHEQUE_2018) and value in [13, 14, 15]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        elif (categoria == CONTRACHEQUE_2022) and value in [11, 12, 13]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        else:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value(
                "O")

        if (
            categoria == CONTRACHEQUE or categoria == CONTRACHEQUE_2018 or categoria == CONTRACHEQUE_2022
        ) and value in [4]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value(
                "B")

        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        matricula = str(row[0])
        if matricula in employees.keys():
            emp = employees[matricula]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[matricula] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    if(int(year) == 2018 or (int(year) == 2019 and int(month) <= 6)):
        # Puts all parsed employees in the big map
        employees.update(parse_employees(data.contracheque,
                         chave_coleta, CONTRACHEQUE_2018))
    elif(int(year) >= 2022):
        employees.update(parse_employees(data.contracheque,
                         chave_coleta, CONTRACHEQUE_2022))
        update_employees(data.indenizatorias, employees, INDENIZACOES_2022)
    else:
        employees.update(parse_employees(
            data.contracheque, chave_coleta, CONTRACHEQUE))
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
