import multiprocessing

def processo_filho(processo_id, shm, num_processos):
    print(f"Processo filho {processo_id} iniciado")

    for i in range(num_processos): #ciclo for até o tamanho do número de processos
        mensagem = shm.get()
        if mensagem:
            print(f"Processo filho {processo_id} recebeu a mensagem: {mensagem}")
            shm.task_done()
            # verifica se todos os processos já leram a mensagem
            if shm.qsize() == 0:
                print("A mensagem foi lida por todos os processos")
                break

def main():
    num_processos = int(input("numero de processos a serem gerados? "))

    if num_processos <= 2:
        print("digite um numero maior que 2 seu btl.")
        main()
        return

    # cria a fila compartilhada para a troca de mensagens
    shm = multiprocessing.JoinableQueue()

    # cria os processos filhos
    processos = []
    for i in range(num_processos):
        p = multiprocessing.Process(target=processo_filho, args=(i, shm, num_processos))
        p.start()
        processos.append(p)

    print("Processo pai iniciado.")

    # pega a entrada do usuário e envia para os processos filhos
    mensagem = input("qual a mensagem que vc quer enviar ")
    for i in range(num_processos):
        shm.put(mensagem)

    # espera todos os processos filhos concluírem
    shm.join()
    print("processo pai finalizado.")