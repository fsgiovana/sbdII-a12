from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["campusflow_a12"]

solicitacoes = db["solicitacoes"]


print("\n-- RELATÓRIO EXECUTIVO — CAMPUSFLOW --")


print("\n1. CATEGORIA COM MAIOR DEMANDA")

pipeline_demanda = [
    {
        "$match": {
            "situacao": {
                "$ne": "CONCLUIDA"
            }
        }
    },
    {
        "$group": {
            "_id": "$categoria.nome",
            "quantidade": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "quantidade": -1
        }
    },
    {
        "$limit": 1
    }
]

demanda = list(solicitacoes.aggregate(pipeline_demanda))

for item in demanda:
    print(f"A categoria {item['_id']} possui {item['quantidade']} solicitações pendentes.")
    print("Conclusão: é importante acompanhar essa categoria para evitar acúmulo de solicitações.")


print("\n2. SETOR COM MAIOR TEMPO MÉDIO")

pipeline_setores = [
    {
        "$unwind": "$atendimentos"
    },
    {
        "$group": {
            "_id": "$atendimentos.setor",
            "tempoMedio": {
                "$avg": "$atendimentos.duracaoMin"
            }
        }
    },
    {
        "$sort": {
            "tempoMedio": -1
        }
    },
    {
        "$limit": 1
    }
]

setores = list(solicitacoes.aggregate(pipeline_setores))

for item in setores:
    print(f"O setor {item['_id']} apresenta tempo médio de {item['tempoMedio']:.2f} minutos.")
    print("Conclusão: esse setor merece atenção para identificar oportunidades de melhorar o tempo de atendimento.")


print("\n3. ESTUDANTE COM MAIOR RECORRÊNCIA")

pipeline_estudantes = [
    {
        "$group": {
            "_id": "$estudante.id",
            "nome": {
                "$first": "$estudante.nome"
            },
            "quantidade": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "quantidade": -1
        }
    },
    {
        "$limit": 1
    }
]

estudantes = list(solicitacoes.aggregate(pipeline_estudantes))

for item in estudantes:
    print(f"{item['nome']} possui {item['quantidade']} solicitações registradas.")
    print("Conclusão: acompanhar estudantes com solicitações recorrentes pode ajudar a identificar dificuldades frequentes nos serviços acadêmicos.")


print("\n---------------------------")

client.close()