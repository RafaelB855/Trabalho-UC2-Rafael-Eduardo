from conexao import Conexao
import random

def criarTabela(con):
    listaSql=['''
    CREATE TABLE "Times"(
    "ID" int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Nome" varchar(255) NOT NULL
    )
    ''',
    
    '''
    CREATE TABLE "Partidas"(
    "ID" int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Time1" int NOT NULL,
    "Gols1" int NOT NULL,
    "Gols2" int NOT NULL,
    "Time2" int NOT NULL,
    CONSTRAINT fk_Time1
        FOREIGN KEY("Time1")
        REFERENCES "Times"("ID"),
    CONSTRAINT fk_Time2
        FOREIGN KEY("Time2")
        REFERENCES "Times"("ID")
    )
    ''',

    '''
    CREATE TABLE "Tabela"(
    "ID" int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "ID_Time" int NOT NULL,
    "Pontos" int NOT NULL,
    "Vitorias" int NOT NULL,
    "Empates" int NOT NULL,
    "Derrotas" int NOT NULL,
    "GolsPró" int NOT NULL,
    "GolsContra" int NOT NULL,
    "SaldodeGols" int NOT NULL,
    CONSTRAINT fk_Time
        FOREIGN KEY("ID_Time")
        REFERENCES "Times"("ID")
    )
    ''']

    for sql in listaSql:
        if con.manipularBanco(sql):
            print("Tabela criada.")
        else:
            print("Falha ao criar.")

conexaoBanco = Conexao("Campeonato","localhost","5432","postgres","postgres")
#criarTabela(conexaoBanco) 

#----------------------------------------------------------------------------------------------------------------------#

def verMenuTimes():

    while True:
        print('''
        Opções menu Times:
        1. Ver Times
        2. Criar Time
        3. Atualizar Time
        4. Remover Time
        0. Voltar ao menu principal
        ''')
        op = input("Escolha uma das opções:")
        match op:
            case "1":
                verListaDeTimes()
            case "2":
                cadastrarNovoTime()
            case "3":
                atualizarTime()
            case "4":
                removerTime()
            case "0":
                print("Voltando ao menu principal...")
                break
            case _:
                print("Escolha uma opção válida.")

        input("Digite Enter para continuar...")

def verListaDeTimes():

    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ORDER BY "ID" ASC
    ''')

    if listaTimes:
        print("ID | NOME")
        for Time in listaTimes:
            print(f"{Time[0]} | {Time[1]}")

        confirmar = input("Deseja ver as informações de algum time? (S/N)").upper()

        match confirmar:
            case "S":
                timeEscolhido = input("Digite o id do time escolhido:")
                verTimeEspecifico(timeEscolhido)
            case "N":
                print("Ok voltando ao menu principal")
            case _:
                print("Você digitou um comando inválido. Voltando ao menu.")

    else:
        print("Ocorreu um erro na consulta, ou a lista é vazia.")

def cadastrarNovoTime():
    print("Cadastro de Time - Insira as informações pedidas")

    nome = input("Digite o nome do Time:")
    if nome == "":
        print("Inserira um nome valido!")
    
    else:
        sqlInserir = f'''
        INSERT INTO "Times"
        Values(default, '{nome}')
        '''
        
        if conexaoBanco.manipularBanco(sqlInserir):

            print(f"O time {nome} foi inserido com sucesso.")
        else:
            print("Falha ao inserir o time!")

def atualizarTime():
    print("Tela de atualização de time:")
    print("Lista de Times")
    
    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ORDER BY "ID" ASC
    ''')

    if listaTimes:
        print("ID | NOME")
        for Time in listaTimes:
            print(f"{Time[0]} | {Time[1]}")

    TimeEscolhido = input("Digite o id do time escolhido:")
    if TimeEscolhido.isdigit():
        verTimeEspecifico(TimeEscolhido)
        novoNome = input("Digite o novo nome (vazio para não alterar):")
    
        if novoNome:
            conexaoBanco.manipularBanco(f'''
            UPDATE "Times"
            SET "Nome" = '{novoNome}'
            WHERE "ID" = {TimeEscolhido}
            ''')

            print(f"O nome foi alterado para '{novoNome}'.")
        
        if novoNome == "":
            print("O nome não foi alterado.")

def verTimeEspecifico(idTime):
    Time = conexaoBanco.consultarBanco(f'''SELECT * FROM "Times"
    WHERE "ID" = {idTime}
    ''')

    if Time:
        Time = Time[0]
        print("Time Escolhido: ")
        print(f'''
        ID - {Time[0]}
        Nome - {Time[1]}
        ''')

        listaPartidas = conexaoBanco.consultarBanco(f'''
        SELECT * FROM "Partidas"
        WHERE "Time1" = '{Time[0]}' or "Time2" = '{Time[0]}'
        ''')

        if listaPartidas:
            print("{:^9} | {:^9} | {:^9} ".format("TIME" ,"PLACAR" ,"TIME"))
            for Partida in listaPartidas:
                
                Time1daPartida = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Partida[1]}'
                    ''')[0]
                
                Time2daPartida = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Partida[4]}'
                    ''')[0]
                
                print("{:^9} | {:^3}/{:^3} | {:^9} ".format((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1])))

        else:
            print("O time não possui partidas")

    if Time:
        Time = Time

        listaTabelas = conexaoBanco.consultarBanco(f'''
        SELECT * FROM "Tabela"
        WHERE "ID_Time" = '{Time[0]}'
        ''')

        if listaTabelas:
            print("\n{:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format("Time", "P", "V", "E" , "D" , "GP" , "GC" , "SG"))
            for Tabela in listaTabelas:
                
                TimedaTabela = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Tabela[1]}'
                    ''')[0]

                print("{:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format((TimedaTabela[1]), (Tabela[2]), (Tabela[3]), (Tabela[4]), (Tabela[5]), (Tabela[6]), (Tabela[7]), (Tabela[8])))
       
        else:
            print("O time não está na tabela.")

    else:
        print("O time não foi encontrado!")

def removerTime():
    print("Tela de remoção de time:")
    print("Lista de Times")
    
    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ORDER BY "ID" ASC
    ''')

    if listaTimes:
        print("ID | NOME")
        for Time in listaTimes:
            print(f"{Time[0]} | {Time[1]}")

    timeEscolhido = input("Digite o id do time escolhido:")
    verTimeEspecifico(timeEscolhido)
    confirmar = input("Deseja remover este time? (S/N)").upper()

    match confirmar:
        case "S":
           resultadoRemocao = conexaoBanco.manipularBanco(f'''
           DELETE FROM "Times"
           WHERE "ID" = '{timeEscolhido}'
           ''')
           
           if resultadoRemocao:
               print("Time removido com sucesso.")
           else:
               print("Time não existe ou não foi removido.")
        case "N":
            print("Ok voltando ao menu principal")
        case _:
            print("Você digitou um comando inválido. Voltando ao menu.")

#----------------------------------------------------------------------------------------------------------------------#

def verMenuPartidas():

    while True:
        print('''
        Opções menu Times:
        1. Ver Partidas
        2. Gerar Campeonato
        3. Criar Partida(Manualmente)
        4. Atualizar Partida
        5. Remover Partida
        6. zerar Partidas
        0. Voltar ao menu principal
        ''')
        op = input("Escolha uma das opções:")
        match op:
            case "1":
                verListaDePartidas()
            case "2":
                gerarCampeonato()
            case "3":
                criarPartida()
            case "4":
                atualizarPartida()
            case "5":
                removerPartida()
            case "6":
                zerarPartidas()
            case "0":
                print("Voltando ao menu principal...")
                break
            case _:
                print("Escolha uma opção válida.")

        input("Digite Enter para continuar...")

def verListaDePartidas():

    listaPartidas = conexaoBanco.consultarBanco('''
    SELECT * FROM "Partidas"
    ORDER BY "ID" ASC
    ''')

    if listaPartidas:
        print("{:^9} | {:^9} | {:^9} ".format("TIME" ,"PLACAR" ,"TIME"))
        for Partida in listaPartidas:
            
            Time1daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[1]}'
                ''')[0]
            
            Time2daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[4]}'
                ''')[0]

            print("{:^9} | {:^3}/{:^3} | {:^9} ".format((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1])))

    else:
        print("Ocorreu um erro na consulta, ou a lista é vazia.")

def gerarCampeonato():

    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ''')

    for Time1 in listaTimes:
        Time1 = Time1[0]
        for Time2 in listaTimes:
            Time2 = Time2[0]
            if Time1 != Time2:
                Gols1 = random.randrange(0,5)
                Gols2 = random.randrange(0,5)
                sqlInserir = f'''
                    INSERT INTO "Partidas"
                    Values(default,{Time1},{Gols1},{Gols2},{Time2})
                    '''
                    
                if conexaoBanco.manipularBanco(sqlInserir):
                    print("Campeonato gerado com sucesso.")
                else:
                    print("Falha ao gerar campeonato!")

def criarPartida():

    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ORDER BY "ID" ASC
    ''')

    if listaTimes:
        print("ID | NOME")
        for Time in listaTimes:
            print(f"{Time[0]} | {Time[1]}")

    else:
        print("Ocorreu um erro na consulta, ou a lista é vazia.")


    Time1 = input("Digite o id do time desejado:")
    if Time1.isdigit():
        Time2 = input(f"Digite o id do time que iria enfrentar o time {Time1}:")
        if Time1 != Time2 and Time2.isdigit():
            Gols1 = input("Digite a quantidade de gols do time escolhido:")
            if Gols1.isdigit():
                Gols2 = input("Digite a quantidade de gols do time adversário:")
                if Gols2.isdigit():
                    sqlInserir = f'''
                        INSERT INTO "Partidas"
                        Values(default, {Time1},{Gols1},{Gols2},{Time2})
                        '''
                                
                if conexaoBanco.manipularBanco(sqlInserir):
                    print("Partida gerada com sucesso.")
                else:
                    print("Falha ao gerar Partida!")
    else:
        print("Escolha uma opção válida.")

def atualizarPartida():
    print("Tela de atualização de Partida:")
    print("Lista de Partidas")
    
    verListaDePartidas()
    PartidaEscolhido = input("Digite o id do partida escolhida:")
    if PartidaEscolhido.isdigit():
        verPartidaEspecifico(PartidaEscolhido)
        Time1 = input("Digite o id do time desejado:")
        if Time1.isdigit():
            Time2 = input(f"Digite o id do time que iria enfrentar o time {Time1}:")
            if Time1 != Time2 and Time2.isdigit():
                Gols1 = input("Digite a quantidade de gols do time escolhido:")
                if Gols1.isdigit():
                    Gols2 = input("Digite a quantidade de gols do time adversário:")
                    if Gols2.isdigit():
                        sqlInserir = f'''
                           UPDATE "Partidas"
                            SET "Time1" = {Time1}, "Gols1" = {Gols1}, "Gols2" = {Gols2}, "Time2" = {Time2}
                            WHERE "ID" = {PartidaEscolhido[0]}
                            '''
                                    
                    if conexaoBanco.manipularBanco(sqlInserir):
                        print("Partida alterada com sucesso.")
                    else:
                        print("Falha ao gerar Partida!")
    else:
        print("Escolha uma opção válida.")

def verPartidaEspecifico(idPartida):

    listaPartidas = conexaoBanco.consultarBanco(f'''
    SELECT * FROM "Partidas"
    WHERE "ID" = {idPartida[0]}
    ''')

    if listaPartidas:
        print("{:^9} | {:^9} | {:^9} ".format("TIME" ,"PLACAR" ,"TIME"))
        for Partida in listaPartidas:
            
            Time1daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[1]}'
                ''')[0]
            
            Time2daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[4]}'
                ''')[0]
            
            print("{:^9} | {:^3}/{:^3} | {:^9} ".format((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1])))


    else:
        print("O Partidas não foi encontradas!")

def removerPartida():
    print("Tela de remoção de Partida:")
    print("Lista de Partidas")
    
    verListaDePartidas()
    partidaEscolhido = input("Digite o id do partida escolhida:")
    verPartidaEspecifico(partidaEscolhido)
    confirmar = input("Deseja remover esta partida? (S/N)").upper()

    match confirmar:
        case "S":
           resultadoRemocao = conexaoBanco.manipularBanco(f'''
           DELETE FROM "Partidas"
           WHERE "ID" = '{partidaEscolhido}'
           ''')
           
           if resultadoRemocao:
               print("Partida removida com sucesso.")
           else:
               print("Partida não existe ou não foi removido.")
        case "N":
            print("Ok voltando ao menu principal")
        case _:
            print("Você digitou um comando inválido. Voltando ao menu.")

def zerarPartidas():

    print("Tela de remoção de campeonato:")
    print("Lista de Partidas")
    
    verListaDePartidas()

    listaPartidas = conexaoBanco.consultarBanco('''
    SELECT * FROM "Partidas"
    ORDER BY "ID" ASC
    ''')

    confirmar = input("Deseja remover zerar tabela? (S/N)").upper()

    match confirmar:
        case "S":
           
           for idPartida in  listaPartidas:
            sqlRemocao = f'''
            DELETE FROM "Partidas"
            WHERE "ID" = '{idPartida[0]}'
            '''
            
            if conexaoBanco.manipularBanco(sqlRemocao):
                print("Campeonato zerada com sucesso.")
            else:
                print("Partida não existe ou não foi removido.")
        case "N":
            print("Ok voltando ao menu principal")
        case _:
            print("Você digitou um comando inválido. Voltando ao menu.")

#----------------------------------------------------------------------------------------------------------------------#

def verMenuTabela():

    while True:
        print('''
        Opções menu Tabela:
        1. Ver Tabela
        2. Atualizar Tabela
        3. Zerar Tabela
        0. Voltar ao menu principal
        ''')
        op = input("Escolha uma das opções:")
        match op:
            case "1":
                verListaDeTabela()
            case "2":
                atualizarTabela()
            case "3":
                zerarTabela()
            case "0":
                print("Voltando ao menu principal...")
                break
            case _:
                print("Escolha uma opção válida.")

        input("Digite Enter para continuar...")

def verListaDeTabela():

    i = 0

    listaTabelas = conexaoBanco.consultarBanco('''
    SELECT * FROM "Tabela"
    ORDER BY "Pontos" DESC
    ''')

    if listaTabelas:
        print("{:^6} | {:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format("Rank", "Time", "P", "V", "E" , "D" , "GP" , "GC" , "SG"))
        for Tabela in listaTabelas:

            i = i + 1
            
            TimedaTabela = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Tabela[1]}'
                ''')[0]

            print("{:^6} | {:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format((i), (TimedaTabela[1]), (Tabela[2]), (Tabela[3]), (Tabela[4]), (Tabela[5]), (Tabela[6]), (Tabela[7]), (Tabela[8])))
            
    else:
        print("Ocorreu um erro na consulta, ou a lista é vazia.")

def atualizarTabela():

    listaTimes = conexaoBanco.consultarBanco('''
    SELECT * FROM "Times"
    ORDER BY "ID" ASC
    ''')

    for idTime in listaTimes:
        idTime = idTime[0]

        vitoria = 0
        empate = 0
        derrota = 0
        pontosV = 0
        pontosE = 0
        pontosD = 0
        golsPros = 0
        golsContras = 0
        golsProsTotal = 0
        golsContrasTotal = 0
        saldodeGolsTotais = 0
        vitoriaF = 0
        empateF = 0
        derrotaF = 0
        pontosVF = 0
        pontosEF = 0
        pontosDF = 0
        golsProsF = 0
        golsContrasF = 0

        Time = conexaoBanco.consultarBanco(f'''SELECT * FROM "Times"
        WHERE "ID" = {idTime}
        ''')

        if Time:
            Time = Time[0]
            print("Time Escolhido: ")
            print(f'''
            ID - {Time[0]}
            Nome - {Time[1]}
            ''')

            listaPartidas = conexaoBanco.consultarBanco(f'''
            SELECT * FROM "Partidas"
            WHERE "Time1" = '{Time[0]}'
            ''')

            for partida in listaPartidas:

                if partida[2]<partida[3]:
                    vitoria = vitoria + 1
                    pontosV = pontosV + 3 
                if partida[2]==partida[3]:
                    empate = empate + 1
                    pontosE = pontosE + 1
                if partida[2]>partida[3]:
                    derrota = derrota + 1
                    pontosD = pontosD + 0

                golsPros = golsPros + partida[2]
                golsContras = golsContras + partida[3]

            listaPartidasFora = conexaoBanco.consultarBanco(f'''
            SELECT * FROM "Partidas"
            WHERE "Time2" = '{Time[0]}'
            ''')

            for partidaF in listaPartidasFora:

                if partidaF[2]<partidaF[3]:
                    vitoriaF = vitoriaF + 1
                    pontosVF = pontosVF + 3
                if partidaF[2]==partidaF[3]:
                    empateF = empateF + 1
                    pontosEF = pontosEF + 1
                if partidaF[2]>partidaF[3]:
                    derrotaF = derrotaF + 1
                    pontosDF = pontosDF + 0

                golsProsF = golsProsF + partidaF[3]
                golsContrasF = golsContrasF + partidaF[2]


                vitoriasTotais = vitoria + vitoriaF
                empatesTotais = empate + empateF
                derrotasTotais = derrota + derrotaF
                pontosTotais = pontosV + pontosE + pontosVF + pontosEF

            golsProsTotal = golsProsTotal +(golsPros + golsProsF)
            golsContrasTotal = golsContrasTotal + (golsContras + golsContrasF)
                
            saldodeGolsTotais = saldodeGolsTotais + (golsProsTotal - golsContrasTotal)

        sqlInserir = f'''
        INSERT INTO "Tabela"
        Values(default, {idTime},{pontosTotais},{vitoriasTotais},{empatesTotais},{derrotasTotais},{golsProsTotal},{golsContrasTotal},{saldodeGolsTotais})
        '''
    
        if conexaoBanco.manipularBanco(sqlInserir):

            print(f"A Tabela foi atualizada com sucesso.")
        else:
            print("Falha ao atualizar tabela!")

    else:
        print("O time não foi encontrado!")
    
def zerarTabela():

    print("Tela de remoção de tabela:")
    print("Lista de Tabela")
    
    verListaDeTabela()

    listaTabela = conexaoBanco.consultarBanco('''
    SELECT * FROM "Tabela"
    ORDER BY "ID" ASC
    ''')

    confirmar = input("Deseja remover zerar tabela? (S/N)").upper()

    match confirmar:
        case "S":
           
           for idTabela in  listaTabela:
            sqlRemocao = f'''
            DELETE FROM "Tabela"
            WHERE "ID" = '{idTabela[0]}'
            '''
            
            if conexaoBanco.manipularBanco(sqlRemocao):
                print("Tabela zerada com sucesso.")
            else:
                print("Tabela não existe ou não foi removido.")
        case "N":
            print("Ok voltando ao menu principal")
        case _:
            print("Você digitou um comando inválido. Voltando ao menu.")

#----------------------------------------------------------------------------------------------------------------------#

while True:

    print('''
    Bem vindo ao Campeonato
    1. Menu de Times
    2. Menu das Partidas
    3. Menu da Tabela
    0. Sair
    ''')

    op = input("Escolha o menu que deseja acessar:")

    match op:
        case "1":
            verMenuTimes()
        case "2":
            verMenuPartidas()
        case "3":
            verMenuTabela()
        case "0":
            print("Saindo da programa...")
            break
        case _:
            print("Escolha uma opção válida.")