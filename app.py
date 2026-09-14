# Essa linha importa algumas ferramentas do Flask que vamos usar no nosso projeto.
# O Flask cria a aplicação, o render_template
# permite carregar nossas páginas HTML e o request permite receber informações enviadas pelo usuário.

from flask import Flask, render_template, request



# Aqui estamos criando a aplicação Flask e armazenando ela na variável app.
# O __name__ ajuda o Flask a identificar onde a aplicação está localizada.
app = Flask(__name__)


# ==========================================
# DADOS TEMPORÁRIOS DOS SEBOS
# ==========================================


# Aqui eu criei dados simples e fictícios para testar a funcionalidade da página.
# Vamos mudar depois para os dados do banco de dados.

# Criei uma lista chamada sebos, que contém dicionários. 
# Cada dicionário representa um sebo e guarda informações como nome, endereço, avaliação e telefone.
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


# ==========================================
# PÁGINA INICIAL
# ==========================================
# Essa linha cria uma rota para a página inicial. O / representa o endereço principal
# do nosso site e indica ao Flask qual função deve ser executada quando essa página for acessada.
@app.route("/")

# Aqui eu estou
# criando uma função chamada inicio. Ela será executada quando a rota da página inicial for acessada.
def inicio():

# Essa é a parte que efetivamente manda o HTML para o navegador.
    return render_template(
        "index.html"
    )


# ==========================================
# PESQUISA
# ==========================================

# Essa rota é responsável pela pesquisa. Quando o usuário acessa /pesquisar,
# o Flask chama a função pesquisar, que vai tratar o que foi pesquisado e mostrar os resultados.
@app.route("/pesquisar")

# Essa função recebe o que o usuário pesquisou através do request, guarda o termo na variável termo
# e depois filtra a lista de sebos, mostrando só os resultados que combinam com a pesquisa.
def pesquisar():

    termo = request.args.get(
        "busca",
        ""
    )

    # DEGRAU 1 - FILTRO DE PESQUISA
    # Antes, essa rota simplesmente devolvia a lista "sebos" inteira, sem
    # considerar o termo pesquisado. Agora criamos a lista "resultados",
    # que só recebe os sebos cujo nome OU local contenha o termo pesquisado.
    #
    # O .lower() nos dois lados da comparação serve para a busca não
    # diferenciar maiúsculas de minúsculas (ex: "sebo" e "Sebo" encontram
    # o mesmo resultado).
    #
    # OBS: se o termo pesquisado vier vazio (""), a condição é verdadeira
    # para todos os sebos, então a busca em branco mostra a lista toda.
    # Isso será tratado com mais cuidado no Degrau 2.
    resultados = []

    for sebo in sebos:
        if termo.lower() in sebo["nome"].lower() or termo.lower() in sebo["local"].lower():
            resultados.append(sebo)

    return render_template(
        "resultado.html",
        termo=termo,
        sebos=resultados
    )


# ==========================================
# PÁGINA INDIVIDUAL DO SEBO
# ==========================================


# Essa rota mostra os detalhes de um sebo específico. 
# O <int:id> recebe o ID do sebo pela URL, permitindo que o sistema saiba qual sebo deve ser mostrado.
@app.route("/sebo/<int:id>")


# Aqui eu crio a função que vai procurar e mostrar os detalhes do sebo.
#  Ela recebe o ID que veio pela URL.
def detalhes_sebo(id):

    sebo_encontrado = None

    # Procura o sebo pelo ID
    for sebo in sebos:

        if sebo["id"] == id:

            sebo_encontrado = sebo

            break


    # Se o sebo não existir
    if sebo_encontrado is None:

        return "Sebo não encontrado", 404


    # Envia os dados para o HTML
    return render_template(
        "sebo.html",
        sebo=sebo_encontrado
    )


# ==========================================
# INICIAR SERVIDOR
# ==========================================


# Essa parte verifica se o arquivo está sendo executado diretamente. Se estiver, o app.run() 
# inicia o servidor Flask.
#  O debug=True ativa o modo de desenvolvimento para facilitar os testes e identificar erros.

if __name__ == "__main__":

    app.run(
        debug=True
    )
# ============================================================
# GUIA PARA CONTINUARMOS O BACK-END DO PROJETO
# ============================================================

# Pessoal, até aqui nós já fizemos a estrutura inicial do nosso
# back-end utilizando Flask e já conseguimos conectar o Python
# com as páginas HTML do nosso projeto.
#
# Os dados dos sebos que estão neste arquivo são apenas dados
# temporários e fictícios que usamos para testar o funcionamento.
# Eles serão substituídos pelos dados reais do banco de dados.
#
# A partir daqui, precisamos continuar o desenvolvimento juntos
# e dividir as próximas etapas entre a equipe.
#
#
# PRÓXIMOS PASSOS DO BACK-END:
#
# 1 - CONECTAR O PYTHON AO MYSQL
#
# Primeiro precisamos fazer a conexão entre o Flask e o banco
# de dados MySQL que a equipe está desenvolvendo.
#
# Depois da conexão, não vamos mais precisar deixar todos os
# dados dos sebos escritos diretamente nesta lista do Python.
#
#
# 2 - CRIAR E ORGANIZAR AS TABELAS DO BANCO
#
# Precisamos definir junto com a equipe quais informações serão
# armazenadas no banco de dados.
#
# Por exemplo:
# - Sebos
# - Usuários
# - Avaliações
# - Livros
# - Categorias
#
# A estrutura final deve ser decidida junto com a modelagem
# do banco de dados que a equipe está fazendo.
#
#
# 3 - BUSCAR OS SEBOS NO BANCO DE DADOS
#
# Depois de conectar o MySQL, precisamos substituir os dados
# fictícios da variável "sebos" por dados vindos do banco.
#
# Assim, quando o usuário pesquisar, o Python poderá consultar
# o banco e mostrar os sebos cadastrados de verdade.
#
#
# 4 - MELHORAR A PESQUISA
#
# Atualmente a rota "/pesquisar" recebe o termo pesquisado,
# mas ainda estamos mostrando nossa lista temporária.
#
# Precisamos fazer a pesquisa realmente verificar os dados
# cadastrados no banco.
#
# Também podemos pensar em filtros, como localização, avaliação,
# tipo de livro ou outras informações que decidirmos colocar
# no projeto.
#
#
# 5 - CADASTRO E LOGIN
#
# Precisamos desenvolver a parte lógica do cadastro e do login.
#
# O usuário deverá poder criar uma conta e depois entrar no
# sistema utilizando seus dados.
#
# Essas informações deverão ser armazenadas no banco de dados.
#
#
# 6 - ÁREA DO USUÁRIO
#
# Depois do login, precisamos criar a lógica da área do usuário.
#
# Nela poderemos mostrar informações do usuário e, dependendo
# do que decidirmos para o projeto, permitir que ele veja ou
# altere seus dados e suas avaliações.
#
#
# 7 - AVALIAÇÕES DOS SEBOS
#
# Uma das principais funcionalidades do nosso projeto será
# permitir que os usuários avaliem os sebos.
#
# Precisamos criar a lógica para:
# - receber a avaliação;
# - identificar o usuário;
# - identificar o sebo;
# - salvar a avaliação no banco;
# - mostrar as avaliações na página do sebo.
#
#
# 8 - DETALHES DOS SEBOS
#
# A rota "/sebo/<int:id>" já foi criada e atualmente funciona
# utilizando nossos dados temporários.
#
# Depois da integração com o banco, essa rota deverá buscar
# o sebo pelo ID diretamente no MySQL.
#
#
# 9 - VALIDAR OS DADOS
#
# Precisamos verificar os dados enviados pelos usuários antes
# de salvar qualquer informação no banco.
#
# Por exemplo, verificar se os campos obrigatórios foram
# preenchidos corretamente.
#
#
# 10 - TESTAR TODAS AS FUNCIONALIDADES
#
# Depois que as funcionalidades forem desenvolvidas, precisamos
# testar cada uma delas individualmente.
#
# Vamos verificar principalmente:
# - cadastro;
# - login;
# - pesquisa;
# - detalhes do sebo;
# - avaliações;
# - navegação entre as páginas;
# - possíveis erros.
#
#
# 11 - ORGANIZAR E CORRIGIR O CÓDIGO
#
# Depois que tudo estiver funcionando, precisamos revisar o
# código, organizar os arquivos e corrigir possíveis problemas.
#
# Também devemos manter os comentários importantes para que
# todos da equipe consigam entender o que foi feito.
#
#
# 12 - INTEGRAR TUDO
#
# No final, precisamos garantir que:
#
# HTML/CSS
#     ↓
# Flask / Python
#     ↓
# MySQL
#
# estejam funcionando juntos.
#
# O usuário deverá conseguir utilizar o site normalmente,
# enquanto o Python ficará responsável pela lógica e o MySQL
# pelo armazenamento dos dados.
#
#
# OBJETIVO FINAL
#
# Nosso objetivo é entregar um site funcional sobre os sebos
# de Londrina, permitindo que o usuário encontre sebos e veja
# qual deles atende melhor às suas necessidades.
#
# O front-end já está estruturado.
# O Flask já está funcionando.
# Agora precisamos construir o restante do back-end juntos,
# integrar o banco de dados e testar o produto final.
#
# Vamos fazendo cada etapa juntos para que todo mundo da equipe
# entenda uma parte do projeto e consiga ajudar no desenvolvimento.
# ============================================================