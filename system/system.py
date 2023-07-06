### Atributos
import random
import os
import time
import random
import re #biblioteca utilizada para a verificação do cpf
import pygame #biblioteca para tocar a música de fundo, necessário instalação via terminal vscode: python -m pip install -U pygame --user
pygame.init() #inicialização da biblioteca

barra = "----------------------------------------------"
alunos = []
exercicios = []
alunosNomes = []
listasorteio = []
sorteado = False

class Participante:
    nome = None
    email = None

class Aluno: # definir classe com dados do aluno
    nome = None
    cpf = 0
    peso = 0
    altura = 0
    imc = 0
    status = None

class Atv:
    nomeExercicio = None
    numRepeticoes = 0
    pesoExercicio = 0 

def clear(): #função limpa a tela
    os.system('clear') #utilizar cls para windows e clear para linux
    
def verificaCPF(cpf):
    entrada = re.findall("\d", cpf) # remover caracteres NÃO numéricos
    if len(cpf) > 14 or len(entrada) < 11 or len(entrada) > 11: # validar quantidade de caracteres digitados
        print("CPF inválido, tente novamente realizar o cadastro.")
        time.sleep(2)
        clear()
        cadAluno()
    else: # verificar se todos os dígitos são iguais
        valid = 0
        for dig in range(0, 11):
            valid += int(entrada[dig])
            dig += 1
        if int(entrada[0]) == valid / 11:
            print("CPF inválido, tente novamente realizar o cadastro.")
            time.sleep(2)
            clear()
            cadAluno()
        # rotina de cálculos do dígito verificador do CPF
        else: # verificação do 10º dígito verificador
            soma = 0
            count = 10
            for i in range(0, len(entrada)-2):
                soma = soma + (int(entrada[i])*count)
                i+=1
                count-=1
            dg1 = 11-(soma%11)
            if dg1 >= 10:
                dg1 = 0
            soma = 0 # verificação do 11º dígito verificador
            count = 10
            for j in range(1, len(entrada)-1):
                soma = soma + (int(entrada[j])*count)
                j+=1
                count-=1
            dg2 = 11-(soma%11)
            if dg2 >= 10:
                dg2 = 0
            if int(entrada[9]) != dg1 or int(entrada[10]) != dg2:
                print("CPF inválido, tente novamente realizar o cadastro.")
                time.sleep(2)
                clear()
                cadAluno()

def music(): #função sorteia uma música para tocar
    numero_sorteado = random.randrange(1, 6)
    pygame.mixer.music.load('musica' + str(numero_sorteado) + '.mp3')
    pygame.mixer.music.play()
    pygame.event.wait()
    
def cadAluno(): #função para cadastrar alunos, chama validação cpf e calcula o imc
    print(barra)
    print("Cadastro de alunos")
    print(barra)
    a = Aluno()
    a.nome = input("Qual o nome do aluno? ")
    a.cpf = input("Qual o CPF do aluno? Não é possível alterar esse dado: ")
    verificaCPF(a.cpf)
    a.peso = float(input("Qual o peso do aluno? "))
    a.altura = float(input("Qual a altura do aluno, em centímetros? "))
    conta = a.peso / ((a.altura*a.altura)/10000)
    a.imc = conta
    a.status = False
    exercicios.append([])
    alunosNomes.append(a.nome)
    print("\nAluno cadastrado com sucesso.")
    return a

def cadExer(idAluno): #cadastramento de exercicio 
    clear()
    print(f"{barra}")
    if len(exercicios[idAluno]) == 10: #verifica a disponibilidade para adicionar outro treino
        print("Treino cheio. Exclua algum exercício e tente novamente. Redirecionando...")
        time.sleep(0.8)
        clear()
        treino(idAluno)
    else:
        exer = Atv()
        exer.id = idAluno
        exer.nome = input("Qual o nome do exercício? ")
        for i in range(len(exercicios[idAluno])):
            if exer.nome == exercicios[idAluno][i].nome:
                print(barra)
                print("Exercício já adicionado. Tente novamente.")
                time.sleep(0.8)
                clear()
                treino(idAluno)
        exer.reps = input("Quantas repetições do exercício serão feitas? ")
        exer.peso = float(input("Com que peso, em kgs, será feito o exercício? "))
        exercicios[idAluno].append(exer)
        if len(exercicios[idAluno][-1].nome) == 0:  ## se o tamanho do primeiro exercício for 0, ou seja, não houver um primeiro exercício, o status sera False.
            alunos[idAluno].status = False
        else:
            alunos[idAluno].status = True
        print("\nExercício cadastrado com sucesso. Redirecionando...")
        time.sleep(0.8) 
        clear()

def buscarAluno(): #busca aluno por nome cadastrado, gerencia o treino/dados
    os.system('clear')
    print(barra)
    busca = input("Qual o nome do aluno que deseja consultar? ")
    if busca not in alunosNomes:
        print("\nAluno não cadastrado. ")
        pergunta = int(input("\n1) Tentar novamente.\n2) Voltar ao início.\n\nInsira uma opção: "))
        if pergunta==1:
            clear()
            buscarAluno()
        elif pergunta==2:
            clear()
            inicio()
        else:
            print("Opção não disponível. Redirecionando...")
            time.sleep(0.8) 
            clear()
            buscarAluno()
        print(barra)
    idAluno = alunosNomes.index(busca)
    print(f"\nNome: {alunos[idAluno].nome};\nID do aluno: {idAluno+1};\nCPF: {alunos[idAluno].cpf};\nPeso: {alunos[idAluno].peso}kg;\nAltura: {alunos[idAluno].altura}cm;\nIMC: {alunos[idAluno].imc:.2f};\nStatus: {alunos[idAluno].status}\n")
    deseja = input("Deseja gerenciar seu treino (T), seus dados(D), ou voltar para o início (V)? ")
    if deseja == "T" or deseja == "t":
        clear()
        treino(idAluno)
    elif deseja == "D" or deseja == "d":
        clear()
        fazeroq = int(input(f"{barra}\nMENU:\n\n1) Editar o nome.\n2) Editar o peso.\n3) Editar a altura.\n4) Deletar o aluno e o treino.\n5) Voltar ao início.\n\nDigite sua opção: "))
        if fazeroq == 1:
            alunos[idAluno].nome = input("\nQual o novo nome? ")
            alunosNomes[idAluno] = alunos[idAluno].nome
            print(f"{alunos[idAluno].nome}; {alunos[idAluno].cpf}; {alunos[idAluno].peso}kg; {alunos[idAluno].altura}cm; IMC: {alunos[idAluno].imc:.2f}; Status:{alunos[idAluno].status}")
            print("Dado atualizado com sucesso. Redirecionando...")
            time.sleep(3)
            clear()
            inicio()
        elif fazeroq == 2:
            alunos[idAluno].peso = int(input("\nQual o novo peso? "))
            print(f"{alunos[idAluno].nome}; {alunos[idAluno].cpf}; {alunos[idAluno].peso}kg; {alunos[idAluno].altura}cm; IMC: {alunos[idAluno].imc:.2f}; Status:{alunos[idAluno].status}")
            print("Dado atualizado com sucesso. Redirecionando...")
            time.sleep(3)
            clear()
            inicio()
        elif fazeroq == 3:
            alunos[idAluno].altura = int(input("\nQual a nova altura? "))
            print(f"{alunos[idAluno].nome}; {alunos[idAluno].cpf}; {alunos[idAluno].peso}kg; {alunos[idAluno].altura}cm; IMC: {alunos[idAluno].imc:.2f}; Status:{alunos[idAluno].status}")
            print("Dado atualizado com sucesso. Redirecionando...")
            time.sleep(3)
            clear()
            inicio()
        elif fazeroq == 4:
                confirm = input("\nAtenção!⚠️\nTem certeza que deseja deletar o aluno e o treino?\nS = Sim\nN = Não\nInsira a opção (S/N): ")
                if confirm=='S' or confirm=="s":
                    alunos.pop(idAluno)
                    alunosNomes.pop(idAluno)
                    exercicios.pop(idAluno)
                    print("Aluno removido com sucesso. Redirecionando...")
                elif confirm=='N' or confirm=="n":
                    print("Aluno não removido. Redirecionando...")
                else:
                    print("Opção não disponível. Redirecionando...")
                time.sleep(0.8)
                clear()
                inicio()    
        elif fazeroq == 5:
            clear()
            inicio()
        else:
            print("Opção inválida. Redirecionando...")
            time.sleep(0.8)
            clear()
            inicio()
    elif deseja == "v" or deseja == "V":
        clear()
        inicio()

def treino(idAluno): #Mostra octreino do aluno e opções de alterar o treino: editar, excluir...
    print(barra)
    print(f"Aluno(a): {alunos[idAluno].nome}\n")
    for i in range(len(exercicios[idAluno])):
        print(f"{i}) Exercício: {exercicios[idAluno][i].nome}; Repetições: {exercicios[idAluno][i].reps}; Peso: {exercicios[idAluno][i].peso}")
    opcoes = int(input(f"\n1) Adicionar um exercício.\n2) Editar um exercício.\n3) Excluir um exercício.\n4) Excluir o treino.\n5) Voltar ao início.\n\nDigite sua opção: "))
    if opcoes == 1:
        cadExer(idAluno)
        treino(idAluno)
    elif opcoes == 2:
        qualexer = int(input(f"Qual exercício deseja editar? "))
        clear()
        fazeroq = int(input(f"{barra}\nMENU:\n\n1) Editar o nome do exercício.\n2) Editar o número de repetições.\n3) Editar o peso.\n\nDigite sua opção: "))
        if fazeroq == 1:
            exercicios[idAluno][qualexer].nome = input("Qual o novo nome? ")
            print(f"{i}) Exercício: {exercicios[idAluno][qualexer].nome}; Repetições: {exercicios[idAluno][qualexer].reps}; Peso: {exercicios[idAluno][qualexer].peso}")
            print("Execício atualizado com sucesso. Redirecionando...")
            time.sleep(0.8)
            clear()
            treino(idAluno)
        elif fazeroq == 2:
            exercicios[idAluno][qualexer].reps = int(input("Qual o novo número de repetições? "))
            print(f"{i}) Exercício: {exercicios[idAluno][qualexer].nome}; Repetições: {exercicios[idAluno][qualexer].reps}; Peso: {exercicios[idAluno][qualexer].peso}")
            print("Execício atualizado com sucesso. Redirecionando...")
            time.sleep(0.8)
            clear()
            treino(idAluno)
        elif fazeroq == 3:
            exercicios[idAluno][qualexer].peso = int(input("Qual o novo peso? "))
            print(f"{i}) Exercício: {exercicios[idAluno][qualexer].nome}; Repetições: {exercicios[idAluno][qualexer].reps}; Peso: {exercicios[idAluno][qualexer].peso}")
            print("Execício atualizado com sucesso. Redirecionando...")
            time.sleep(0.8)
            clear()
            treino(idAluno)
    elif opcoes == 3: #verifica se realmente deseja deletar
        qualexer = int(input("Qual exercício deseja apagar? "))
        confirm = input("\nAtenção!⚠️\nTem certeza que deseja deletar o exercício?\nS = Sim\nN = Não\nInsira a opção (S/N): ")
        if confirm=='S' or confirm=="s":
            if (len(exercicios[idAluno])) < 2:
                alunos[idAluno].status = False
                exercicios[idAluno] = []
            else:
                exercicios[idAluno].pop(qualexer)
                print("\nExercício removido com sucesso. Redirecionando...")
        elif confirm=='N' or confirm=="n":
            print("\nExercício não removido. Redirecionando...")
        else:
            print("\nOpção não disponível. Redirecionando...")
        clear()
        treino(idAluno)
    elif opcoes == 4: #verifica se realmente deseja deletar
        confirm = input("Atenção!⚠️\nTem certeza que deseja deletar o treino?\nS = Sim\nN = Não\nInsira a opção (S/N): ")
        if confirm=='S' or confirm=="s":
            exercicios[idAluno] = []
            alunos[idAluno].status = False
            print("\nTreino removido com sucesso. Redirecionando...")
        elif confirm=='N' or confirm=="n":
            print("\nTreino não removido. Redirecionando...")
        else:
            print("\nOpção não disponível. Redirecionando...")
        clear()
        treino(idAluno)
    elif opcoes == 5:
        clear()
        inicio()

def relatorio():
    print(barra, "\nMENU")
    deseja = int(input("\n1) Alunos ativos\n2) Alunos inativos\n3) Todos os alunos\n4) Voltar ao início\n\nInsira uma opção (1/2/3/4): "))
    if deseja == 1:
        clear()
        print(barra)
        for i in range(len(alunos)):
            if alunos[i].status == True:
                print((alunosNomes)[i])
        quer = input("\nAdicionar mais um aluno (A) ou voltar (V)? ")
        if quer == "A" or quer == "a":
            alunos.append(cadAluno())
            clear()
            relatorio()
        elif quer == "V" or quer == "v":
            clear()
            relatorio()
        else:
            print("Opção inválida. Redirecionando...")
            time.sleep(0.8)
            clear()
            relatorio()
    elif deseja == 2:
        clear()
        print(barra)
        for i in range(len(alunos)):
            if alunos[i].status == False:
                print((alunosNomes)[i])
        quer = input("\nAdicionar mais um aluno (A) ou voltar (V)? ")
        if quer == "A" or quer == "a":
            alunos.append(cadAluno())
            clear()
            relatorio()
        elif quer == "V" or quer == "v":
            clear()
            relatorio()
        else:
            print("Opção inválida. Redirecionando...")
            time.sleep(0.8)
            clear()
            relatorio()
    elif deseja == 3:
        clear()
        print(barra)
        for i in range(len(alunos)):
            print((alunosNomes)[i])
        quer = input("\nAdicionar mais um aluno (A) ou voltar (V)? ")
        if quer == "A" or quer == "a":
            alunos.append(cadAluno())
            clear()
            relatorio()
        elif quer == "V" or quer == "v":
            clear()
            relatorio()
        else:
            print("Opção inválida. Redirecionando...")
            time.sleep(0.8)
            clear()
            relatorio()
    elif deseja == 4:
        clear()
        inicio()
    else:
        print(barra,"Opção inválida")
        time.sleep(0.8)
        clear()
        relatorio()

def sorteio(): #sorteio da academia
    print(barra)
    print("Bem vindo ao sorteio anual da Academia Bem Estar!")
    menu = int(input("\nMENU\n\n1) Cadastrar participante\n2) Participantes\n3) Realizar o sorteio\n4) Voltar ao início\n\nInsira uma opção: "))
    clear()
    if menu == 1:
        for i in range(1):
            novo = Participante()
            novo.nome = input("Digite o nome do participante: ")
            if novo.nome not in alunosNomes: #verifica se a pessoa cadastrada é aluna da academia
                print("Aluno não matriculado. O sorteio é apenas para alunos da Academia Bem Estar.")
                time.sleep(2)
                clear()
                sorteio()
            novo.email = input("Digite seu e-mail: ")
            listasorteio.append(novo)
        print("Participante cadastrado com sucesso. Redirecionando...")
        time.sleep(1)
        clear()
        sorteio()
    elif menu == 2: #mostra os participantes
        print(barra)
        print("Participantes:\n")
        for i in range(len(listasorteio)):
            print(listasorteio[i].nome)
        clear()
        sorteio()
    elif menu == 3: #faz o sorteio utilizando random
        global x
        x = random.randint(0,len(listasorteio)-1)
        print(barra)
        time.sleep(0.8) 
        print("!!!!!!!!!!!!!PARABÉNS!!!!!!!!!!!!!")
        time.sleep(0.8) 
        print(barra)
        time.sleep(0.8)
        print(f"O ganhador do sorteio é {listasorteio[x].nome}. Confira sua caixa de entrada.")
        print(barra)
        time.sleep(2.5)
        global sorteado
        sorteado = True
        clear()
        inicio()
    elif menu == 4: #sai do sistema
        clear()
        inicio()
    else:
        print("Opção inválida. Redirecionando...")
        time.sleep(0.8)
        clear()
        sorteio()
    
def inicio(): #pagina inicial
    print(barra)
    print("Bem vindo ao sistema digital da Academia Bem Estar.")
    print("\n1) Cadastrar novo aluno\n2) Listar alunos cadastrados\n3) Buscar alunos\n4) Sair do sistema\n5) *** Sorteio *** ")
    if sorteado == False:
        print("\nSorteio de 12 meses de mensalidade gratuita até 30/06. Confira!")
    elif sorteado == True:
        print(f"\nO vencedor do sorteio foi {listasorteio[x].nome}. Parabéns!")
    a = int(input("\nInsira uma opção (1/2/3/4/5): "))
    cont = 0
    if a == 1:
        clear()
        alunos.append(cadAluno())
        clear()
        inicio()
    elif a == 2:
        clear()
        relatorio()
    elif a == 3:
        clear()
        buscarAluno()
    elif a ==4:
        exit()
    elif a == 5:
        clear()
        sorteio()
        inicio()
    else:
        print("\nOpção inválida. Redirecionando...")
        time.sleep(0.8)
        clear()
        inicio()

#sistema de segurança
senha = False
while senha != True:
    print(barra)
    print("         Sistema da Academia Bem Estar")
    print(barra)    
    senha = input("Digite a senha: ")
    if senha=="admin":
        senha = True
        time.sleep(1.2)
        clear()
        music()
        inicio()
    else:
        print("Senha incorreta, tente novamente.")
        time.sleep(1.2)
        clear()