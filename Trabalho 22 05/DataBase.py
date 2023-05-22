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

class Times:
    def __init__(self, ID, Nome):
        self._ID = ID
        self._Nome = Nome

    def verListaDeTimes(self):

        listaTimes = conexaoBanco.consultarBanco('''
        SELECT * FROM "Times"
        ORDER BY "ID" ASC
        ''')

        if listaTimes:
            for Time in listaTimes:
                return f"{Time[0]} | {Time[1]}"

    def cadastrarNovoTime(self):
            sqlInserir = f'''
            INSERT INTO "Times"
            Values(default, '{self._Nome}')
            '''
            
            if conexaoBanco.manipularBanco(sqlInserir):

                return f"O time {self._Nome} foi inserido com sucesso."

    def atualizarTime(self):      
        Times.verListaDeTimes()

        conexaoBanco.manipularBanco(f'''
        UPDATE "Times"
        SET "Nome" = '{self._Nome}'
        WHERE "ID" = {self._ID}
        ''')

        return f"O nome foi alterado para '{self._Nome}'."

    def verTimeEspecifico(self, idTime):
        Time = conexaoBanco.consultarBanco(f'''SELECT * FROM "Times"
        WHERE "ID" = {idTime}
        ''')

        if Time:
            Time = Time[0]

            listaPartidas = conexaoBanco.consultarBanco(f'''
            SELECT * FROM "Partidas"
            WHERE "Time1" = '{Time[0]}' or "Time2" = '{Time[0]}'
            ''')

            if listaPartidas:
                for Partida in listaPartidas:
                    
                    Time1daPartida = conexaoBanco.consultarBanco(f'''
                        SELECT * FROM "Times"
                        WHERE "ID" = '{Partida[1]}'
                        ''')[0]
                    
                    Time2daPartida = conexaoBanco.consultarBanco(f'''
                        SELECT * FROM "Times"
                        WHERE "ID" = '{Partida[4]}'
                        ''')[0]
                    
                    return "{:^9} | {:^3}/{:^3} | {:^9} ".format((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1]))

        if Time:
            Time = Time

            listaTabelas = conexaoBanco.consultarBanco(f'''
            SELECT * FROM "Tabela"
            WHERE "ID_Time" = '{Time[0]}'
            ''')

            if listaTabelas:
                # print("\n{:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format("Time", "P", "V", "E" , "D" , "GP" , "GC" , "SG"))
                for Tabela in listaTabelas:
                    
                    TimedaTabela = conexaoBanco.consultarBanco(f'''
                        SELECT * FROM "Times"
                        WHERE "ID" = '{Tabela[1]}'
                        ''')[0]

                    return("{:^9} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6} | {:^6}".format((TimedaTabela[1]), (Tabela[2]), (Tabela[3]), (Tabela[4]), (Tabela[5]), (Tabela[6]), (Tabela[7]), (Tabela[8])))
        
        #     else:
        #         print("O time não está na tabela.")

        # else:
        #     print("O time não foi encontrado!")

    def removerTime(self, timeEscolhido):
        
        listaTimes = conexaoBanco.consultarBanco('''
        SELECT * FROM "Times"
        ORDER BY "ID" ASC
        ''')

        if listaTimes:
            for Time in listaTimes:
                return f"{Time[0]} | {Time[1]}"

        Times.verTimeEspecifico(timeEscolhido)

        resultadoRemocao = conexaoBanco.manipularBanco(f'''
        DELETE FROM "Times"
        WHERE "ID" = '{timeEscolhido}'
        ''')
            
        if resultadoRemocao:
            return "Time removido com sucesso."

#----------------------------------------------------------------------------------------------------------------------#

class Partida:
    def __init__(self, ID, Time1, Gols1, Gols2, Time2):
        self._ID = ID
        self._Time1 = Time1
        self._Gols1 = Gols1
        self._Gols2 = Gols2
        self._Time2 = Time2

    def verListaDePartidas():

        listaPartidas = conexaoBanco.consultarBanco('''
        SELECT * FROM "Partidas"
        ORDER BY "ID" ASC
        ''')

        lista=[]

        for Partida in listaPartidas:
            
            Time1daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[1]}'
                ''')[0]
            
            Time2daPartida = conexaoBanco.consultarBanco(f'''
                SELECT * FROM "Times"
                WHERE "ID" = '{Partida[4]}'
                ''')[0]

            lista.append((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1]))
                
        return lista

    def gerarCampeonato(self):

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
                        return "Campeonato gerado com sucesso."

    def criarPartida(self):

        listaTimes = conexaoBanco.consultarBanco('''
        SELECT * FROM "Times"
        ORDER BY "ID" ASC
        ''')

        if listaTimes:
            for Time in listaTimes:
                return f"{Time[0]} | {Time[1]}"

        sqlInserir = f'''
        INSERT INTO "Partidas"
        Values(default, {self._Time1},{self._Gols1},{self._Gols2},{self._Time2})
        '''
                    
        if conexaoBanco.manipularBanco(sqlInserir):
            return "Partida gerada com sucesso."

    def atualizarPartida(self, PartidaEscolhido):
        
        Partida.verListaDePartidas()
        Partida.verPartidaEspecifico(PartidaEscolhido)

        sqlInserir = f'''
        UPDATE "Partidas"
        SET "Time1" = {self._Time1}, "Gols1" = {self._Gols1}, "Gols2" = {self._Gols2}, "Time2" = {self._Time2}
        WHERE "ID" = {PartidaEscolhido[0]}
        '''
                                    
        if conexaoBanco.manipularBanco(sqlInserir):
            return "Partida alterada com sucesso."

    def verPartidaEspecifico(self, idPartida):

        listaPartidas = conexaoBanco.consultarBanco(f'''
        SELECT * FROM "Partidas"
        WHERE "ID" = {idPartida[0]}
        ''')

        if listaPartidas:
            for Partida in listaPartidas:
                
                Time1daPartida = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Partida[1]}'
                    ''')[0]
                
                Time2daPartida = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Partida[4]}'
                    ''')[0]
                
                return "{:^9} | {:^3}/{:^3} | {:^9} ".format((Time1daPartida[1]), (Partida[2]), (Partida[3]), (Time2daPartida[1]))

    def removerPartida(self, partidaEscolhido):

        Partida.verListaDePartidas()
        Partida.verPartidaEspecifico(partidaEscolhido)

        resultadoRemocao = conexaoBanco.manipularBanco(f'''
        DELETE FROM "Partidas"
        WHERE "ID" = '{partidaEscolhido}'
        ''')
        
        if resultadoRemocao:
            return "Partida removida com sucesso."

    def zerarPartidas(self):
        
        Partida.verListaDePartidas()

        listaPartidas = conexaoBanco.consultarBanco('''
        SELECT * FROM "Partidas"
        ORDER BY "ID" ASC
        ''')
            
        for idPartida in  listaPartidas:
            sqlRemocao = f'''
            DELETE FROM "Partidas"
            WHERE "ID" = '{idPartida[0]}'
            '''
            
            if conexaoBanco.manipularBanco(sqlRemocao):
                return "Campeonato zerada com sucesso."

#----------------------------------------------------------------------------------------------------------------------#

class Tabela:
    def __init__(self, ID, ID_Time, Pontos, Vitorias, Empates, Derrotas, GolsPró, GolsContra, SaldodeGols):
        self._ID = ID
        self._ID_Time = ID_Time
        self._Pontos = Pontos
        self._Vitorias = Vitorias
        self._Empates = Empates
        self._Derrotas = Derrotas
        self._GolsPró = GolsPró
        self._GolsContra = GolsContra
        self._SaldodeGols = SaldodeGols

    def verListaDeTabela(self):

        i = 0
        lista = []

        listaTabelas = conexaoBanco.consultarBanco('''
        SELECT * FROM "Tabela"
        ORDER BY "Pontos" DESC
        ''')

        if listaTabelas:
            for Tabela in listaTabelas:

                i = i + 1
                
                TimedaTabela = conexaoBanco.consultarBanco(f'''
                    SELECT * FROM "Times"
                    WHERE "ID" = '{Tabela[1]}'
                    ''')[0]

                lista.append((TimedaTabela[1]), (Tabela[2]), (Tabela[3]), (Tabela[4]), (Tabela[5]), (Tabela[6]), (Tabela[7]), (Tabela[8]))

        return lista

    def atualizarTabela(self):

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
                    pontosTorais = pontosV + pontosE + pontosVF + pontosEF

                golsProsTotal = golsProsTotal +(golsPros + golsProsF)
                golsContrasTotal = golsContrasTotal + (golsContras + golsContrasF)
                    
                saldodeGolsTotais = saldodeGolsTotais + (golsProsTotal - golsContrasTotal)

            sqlInserir = f'''
            INSERT INTO "Tabela"
            Values(default, {idTime},{pontosTorais},{vitoriasTotais},{empatesTotais},{derrotasTotais},{golsProsTotal},{golsContrasTotal},{saldodeGolsTotais})
            '''
        
        return f"A Tabela foi atualizada com sucesso."
        
    def zerarTabela(self):
        
        Tabela.verListaDeTabela()

        listaTabela = conexaoBanco.consultarBanco('''
        SELECT * FROM "Tabela"
        ORDER BY "ID" ASC
        ''')
            
        for idTabela in  listaTabela:
            sqlRemocao = f'''
            DELETE FROM "Tabela"
            WHERE "ID" = '{idTabela[0]}'
            '''
            
            if conexaoBanco.manipularBanco(sqlRemocao):
                return "Tabela zerada com sucesso."

while True:

    print('''
    Bem vindo ao Campeonato
    1. ver de partidas

    0. Sair
    ''')

    op = input("Escolha o menu que deseja acessar:")

    match op:
        case "1":
            Partida.verListaDePartidas()

        case "0":
            print("Saindo da programa...")
            break
        case _:
            print("Escolha uma opção válida.")