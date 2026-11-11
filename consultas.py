from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017")

db = client["campusflow_a12"]

solicitacoes = db["solicitacoes"]


print("\n-- MISSÃO 1 — FILA CRÍTICA --\n")

filtro = {
    "situacao": {
        "$in": ["ABERTA", "EM_ANALISE"]
    },
    "prioridade": {
        "$gte": 4
    }
}

projecao = {
    "_id": 0,
    "protocolo": 1,
    "estudante.nome": 1,
    "categoria.nome": 1,
    "situacao": 1,
    "prioridade": 1
}

resultado = solicitacoes.find(
    filtro,
    projecao
).sort([
    ("prioridade", -1),
    ("criadoEm", 1)
])

for documento in resultado:
    pprint(documento)


print("\n-- MISSÃO 2 — BACKLOG POR CATEGORIA --\n")

pipeline_backlog = [
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
    }
]

resultado_backlog = solicitacoes.aggregate(pipeline_backlog)

for documento in resultado_backlog:
    pprint(documento)


print("\n-- MISSÃO 3 — CARGA POR SETOR --\n")

pipeline_setores = [
    {
        "$unwind": "$atendimentos"
    },
    {
        "$group": {
            "_id": "$atendimentos.setor",
            "interacoes": {
                "$sum": 1
            },
            "tempoMedio": {
                "$avg": "$atendimentos.duracaoMin"
            },
            "maiorDuracao": {
                "$max": "$atendimentos.duracaoMin"
            }
        }
    },
    {
        "$sort": {
            "interacoes": -1
        }
    }
]

resultado_setores = solicitacoes.aggregate(pipeline_setores)

for documento in resultado_setores:
    pprint(documento)


print("\n-- MISSÃO 4 — ESTUDANTES RECORRENTES --\n")

pipeline_estudantes = [
    {
        "$group": {
            "_id": "$estudante.id",
            "nome": {
                "$first": "$estudante.nome"
            },
            "quantidade": {
                "$sum": 1
            },
            "protocolos": {
                "$push": "$protocolo"
            }
        }
    },
    {
        "$match": {
            "quantidade": {
                "$gt": 1
            }
        }
    },
    {
        "$sort": {
            "quantidade": -1
        }
    }
]

resultado_estudantes = solicitacoes.aggregate(pipeline_estudantes)

for documento in resultado_estudantes:
    pprint(documento)


client.close()
