import multiprocessing
import threading

def processo_filho(processo_id, shm, num_processos, barreira):
    print(f"processo filho {processo_id} iniciado")
    barreira.wait()  # Aguarda a barreira para sincronizar a inicialização dos processos filhos

    for i in range(num_processos):
        mensagem = shm.get()
        if mensagem:
            print(f"processo filho {processo_id} recebeu a mensagem: {mensagem}")
            shm.task_done()
            if shm.qsize() == 0:
                print("a mensagem foi lida por todos os processos")
                break

def main():
    num_processos = int(input("numero de processos a serem gerados? "))
    if num_processos <= 2:
        print("digite um numero maior que 2 seu btl")
        return
    
    # Cria a fila compartilhada para a troca de mensagens
    shm = multiprocessing.JoinableQueue()

    # Cria a barreira para sincronizar a inicialização dos processos filhos
    barreira = threading.Barrier(num_processos)

    # Cria os processos filhos
    processos = []
    for i in range(num_processos):
        p = multiprocessing.Process(target=processo_filho, args=(i, shm, num_processos, barreira))
        p.start()
        processos.append(p)
    print("processo pai iniciado")
    mensagem = input("qual a mensagem que vc quer enviar ")
    for i in range(num_processos):
        shm.put(mensagem)
    shm.join()
    print("processo pai finalizado.")
# Chamando a função main
main()
