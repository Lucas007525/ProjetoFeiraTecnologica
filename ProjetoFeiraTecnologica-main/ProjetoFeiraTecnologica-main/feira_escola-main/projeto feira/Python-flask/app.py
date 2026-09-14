# ============================================================
# IMPORTS
# ============================================================
# O Flask cria a aplicação, o render_template permite carregar
# nossas páginas HTML e o request permite receber informações
# enviadas pelo usuário.
from flask import Flask, render_template, request


# ============================================================
# CRIAÇÃO DA APLICAÇÃO
# ============================================================
# Aqui estamos criando a aplicação Flask e armazenando ela na
# variável app. O __name__ ajuda o Flask a identificar onde a
# aplicação está localizada.
app = Flask(__name__)


# ============================================================
# DADOS TEMPORÁRIOS DOS SEBOS
# ============================================================
# Dados simples e fictícios para testar a funcionalidade da
# página. Serão substituídos pelos dados reais do banco de dados.
#
# Lista chamada "sebos", contendo dicionários. Cada dicionário
# representa um sebo e guarda informações como nome, endereço,
# avaliação e telefone.
sebos = [
    {
        "id": 1,
        "nome": "Sebo Exemplo",
        "local": "Centro, Londrina - PR",
        "avaliacao": 4.8,
        "descricao": "Livros usados, raridades e literatura.",
        "telefone": "(43) 3333-3333",
        "horario": "Segunda a sábado, 09h às 18h",
        "endereco": "Rua Exemplo, 100 - Centro"
    },
    {
        "id": 2,
        "nome": "Livraria Exemplo",
        "local": "Zona Oeste, Londrina - PR",
        "avaliacao": 4.5,
        "descricao": "Grande variedade de livros e coleções.",
        "telefone": "(43) 3444-4444",
        "horario": "Segunda a sexta, 09h às 18h",
        "endereco": "Avenida Exemplo, 200 - Zona Oeste"
    },
    {
        "id": 3,
        "nome": "Sebo do Leitor",
        "local": "Londrina - PR",
        "avaliacao": 4.3,
        "descricao": "Literatura, quadrinhos e livros acadêmicos.",
        "telefone": "(43) 3555-5555",
        "horario": "Segunda a sábado, 10h às 19h",
        "endereco": "Rua dos Livros, 300 - Londrina"
    }
]


# ============================================================
# ACESSO AOS DADOS 
# ============================================================
# Função única de acesso aos dados dos sebos. Hoje devolve a
# lista fixa acima; quando o banco MySQL estiver pronto, só
# precisamos trocar o CONTEÚDO desta função por uma consulta —
# o resto do código continua chamando buscar_sebos() sem mudar
# nada.
def buscar_sebos():
    return sebos


# ============================================================
# PÁGINA INICIAL
# ============================================================
@app.route("/")
def inicio():
    # Manda o HTML da página inicial para o navegador.
    return render_template("index.html")


# ============================================================
# SOBRE O PROJETO 
# ============================================================
# Página "Sobre" explicando o projeto. Não usa dados de sebo,
# então não depende do banco de dados — é só um render_template
# puro, igual à página inicial.
#
# OBS: precisa existir "sobre.html" na pasta templates.
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# ============================================================
# PESQUISA
# ============================================================
@app.route("/pesquisar")
def pesquisar():

    termo = request.args.get("busca", "")

    # --- VALIDAÇÃO BÁSICA DE ENTRADA ---
    # Limitamos o tamanho máximo do termo pesquisado (100
    # caracteres é mais que suficiente para nome ou endereço de
    # sebo) e removemos espaços extras no início/fim, evitando
    # que um texto absurdamente longo ou cheio de espaços cause
    # problemas.
    LIMITE_CARACTERES_BUSCA = 100
    termo = termo.strip()[:LIMITE_CARACTERES_BUSCA]

    todos_os_sebos = buscar_sebos()

    # --- FILTRO DE PESQUISA ---
    # Só entram em "resultados" os sebos cujo nome OU local
    # contenha o termo pesquisado. O .lower() nos dois lados
    # evita diferenciar maiúsculas de minúsculas.
    resultados = []
    for sebo in todos_os_sebos:
        if termo.lower() in sebo["nome"].lower() or termo.lower() in sebo["local"].lower():
            resultados.append(sebo)

    # --- TRATAMENTO DE PESQUISA VAZIA E SEM RESULTADO ---
    # 1) Campo vazio -> pedimos para digitar algo, "resultados"
    #    fica vazio (não mostramos tudo à toa).
    # 2) Termo preenchido mas sem sebo encontrado -> avisamos que
    #    nada foi encontrado.
    # 3) Encontrou resultados -> "mensagem" fica None.
    mensagem = None

    if termo == "":
        resultados = []
        mensagem = "Digite um termo para pesquisar."
    elif len(resultados) == 0:
        mensagem = f"Nenhum sebo encontrado para \"{termo}\"."

    return render_template(
        "resultado.html",
        termo=termo,
        sebos=resultados,
        mensagem=mensagem  # O template pode usar essa variável para
                            # exibir o aviso, ex: {% if mensagem %}...{% endif %}
    )


# ============================================================
# PÁGINA INDIVIDUAL DO SEBO
# ============================================================
# O <int:id> recebe o ID do sebo pela URL. O conversor "int" do
# Flask já garante que só números inteiros cheguem até aqui — se
# alguém digitar letras na URL, o Flask já devolve 404 sozinho.
@app.route("/sebo/<int:id>")
def detalhes_sebo(id):

    # --- VALIDAÇÃO BÁSICA DE ENTRADA ---
    # IDs negativos ou zero nunca são válidos no nosso sistema,
    # então nem perdemos tempo procurando.
    if id <= 0:
        return "ID inválido", 404

    todos_os_sebos = buscar_sebos()

    sebo_encontrado = None
    for sebo in todos_os_sebos:
        if sebo["id"] == id:
            sebo_encontrado = sebo
            break

    if sebo_encontrado is None:
        return "Sebo não encontrado", 404

    return render_template("sebo.html", sebo=sebo_encontrado)


# ============================================================
# PONTOS DE INTEGRAÇÃO COM O BANCO:
# ============================================================
# Resumo dos lugares exatos onde o MySQL vai "entrar" no código,
# para facilitar a vida de quem for integrar depois:
#
# 1) buscar_sebos() — hoje devolve a lista fixa "sebos".
#    Depois deve fazer algo como "SELECT * FROM sebos" e devolver
#    o resultado no mesmo formato (lista de dicionários com as
#    mesmas chaves), para que o resto do código não precise mudar.
#
# 2) detalhes_sebo() — hoje percorre a lista inteira procurando
#    o id. Depois, o ideal é buscar direto no MySQL
#    ("SELECT * FROM sebos WHERE id = %s"), sem trazer tudo.
#
# 3) pesquisar() — hoje filtra em Python com "in". Depois pode
#    virar "WHERE nome LIKE %s OR local LIKE %s", deixando o
#    próprio banco fazer o filtro.
#
# Import provavelmente necessário quando isso acontecer:
# from flask_mysqldb import MySQL (ou lib equivalente, a definir
# com a equipe).


# ============================================================
# INICIAR SERVIDOR
# ============================================================
# Verifica se o arquivo está sendo executado diretamente; se
# estiver, app.run() inicia o servidor Flask. debug=True ativa o
# modo de desenvolvimento para facilitar testes e identificar erros.
if __name__ == "__main__":
    app.run(debug=True)


# ============================================================
# GUIA / CHECKLIST PARA CONTINUARMOS O BACK-END DO PROJETO
# ============================================================

# Pessoal, é o nosso código mais atualizado e preparado por mim até então na parte do app.py
# O restante do código vai ser mais com vocês, mas estarei sempre disposto a ajudar e ouvir.
# Juntos vamos finalizar esse projeto juntos. 
#
# Os dados dos sebos que estão neste arquivo são apenas dados
# temporários e fictícios que usamos para testar o funcionamento.
# Eles serão substituídos pelos dados reais do banco de dados.


# 1 - CONECTAR O PYTHON AO MYSQL
# (Não resolvido, equipe dev Maycon e Miguel)
#
# Precisamos fazer a conexão entre o Flask e o banco de dados
# MySQL que a equipe está desenvolvendo.


# 2 - CRIAR E ORGANIZAR AS TABELAS DO BANCO
# (Não resolvido, equipe dev Maycon e Miguel)
#
# Definir quais informações serão armazenadas: Sebos, Usuários,
# Avaliações, Livros, Categorias.


# 3 - BUSCAR OS SEBOS NO BANCO DE DADOS
# (Parcialmente feito por Lucas)
#
# A função buscar_sebos() já existe e centraliza o acesso aos
# dados — falta só trocar seu conteúdo por uma consulta real ao
# MySQL quando o banco estiver pronto.


# 4 - MELHORAR A PESQUISA
# (Parcialmente feito por Lucas)
#
# A rota /pesquisar já filtra corretamente, trata pesquisa vazia
# e sem resultado, e valida o tamanho da entrada — mas ainda
# busca na lista fictícia, não no banco.


# 5 - CADASTRO E LOGIN
# (Não resolvido, equipe dev Maycon e Miguel)
#
# Lógica de criação de conta e login, com dados armazenados no
# banco de dados.


# 6 - ÁREA DO USUÁRIO
# (Não resolvido, equipe dev Maycon e Miguel)
#
# Depende do login estar pronto.


# 7 - AVALIAÇÕES DOS SEBOS
# (Não resolvido, equipe dev Maycon e Miguel)
#
# Receber, identificar usuário/sebo, salvar e mostrar avaliações.


# 8 - DETALHES DOS SEBOS
# (Feito por Lucas)
#
# A rota /sebo/<int:id> já funciona, com validação de ID e
# tratamento de "não encontrado" — usando os dados fictícios.
# Só precisará trocar a fonte de dados quando o MySQL entrar.


# 9 - VALIDAR OS DADOS
# (Parcialmente feito por Lucas)
#
# Validação básica já existe na pesquisa (tamanho do termo) e no
# ID do sebo. Falta validar os dados que virão do cadastro/login
# e das avaliações, que ainda não existem.


# 10 - TESTAR TODAS AS FUNCIONALIDADES
# (Não resolvido, equipe dev Maycon e Miguel)
#
# As partes que dependem do banco (cadastro, login, avaliações)
# ainda não existem para serem testadas.


# 11 - ORGANIZAR E CORRIGIR O CÓDIGO
# (Feito por Lucas)
#
# Código revisado, comentários organizados, espaçamento e
# indentação padronizados nesta versão.


# 12 - INTEGRAR TUDO
# (Não resolvido, equipe dev Maycon e Miguel)
#
# HTML/CSS -> Flask/Python -> MySQL, tudo funcionando junto.

# ============================================================