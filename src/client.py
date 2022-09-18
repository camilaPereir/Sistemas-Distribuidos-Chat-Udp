import socket
import sys
import _thread
import json
import time

HOST = ""  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
IP_SERVER = "10.0.1.10"
NICKNAME = None
GROUP_ID = None
MSG_ID = 1
ENTRIED_GROUP = False
SEND_MESSAGE = False


def server(udp):
    global ENTRIED_GROUP
    global MSG_ID
    global SEND_MESSAGE

    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, cliente = udp.recvfrom(1024)
        msg_decoded = msg.decode('utf-8')
        string_dict = json.loads(msg_decoded)
        if 'action' not in string_dict:
            if string_dict["group_id"] == GROUP_ID:
                print(
                    f'\r{string_dict["name"]}:\n   {string_dict["msg"]}', end="")
                print("\n(Voce)-> ", end="")
        else:
            if string_dict["action"] == 0:
                menu()
            elif string_dict["action"] == 1:
                if string_dict["group_id"] == GROUP_ID:
                    if string_dict["status"] == 1:
                        ENTRIED_GROUP = True
            elif string_dict["action"] == 2:
                udp.close()
                sys.exit(0)
            elif string_dict["action"] == 3:
                if string_dict["group_id"] == GROUP_ID:
                    if string_dict["status"] == 1:
                        SEND_MESSAGE = True


def client():
    global ENTRIED_GROUP
    global MSG_ID
    global GROUP_ID
    print(f"Starting UDP Server on port {PORT}")
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _thread.start_new_thread(server, (udp,))
    print("Type q to exit")
    message = None
    dest = (IP_SERVER, PORT)
    menu()
    name = input("Informe o seu nome/apelido -> ")
    try:
        groupId = int(input("Informe o ID do grup que deseja entrar -> "))
        GROUP_ID = groupId
        entryGroup = {
            "action": 1,
            "name": name,
            "group_id": groupId
        }
        stringJson = json.dumps(entryGroup)
        udp.sendto(stringJson.encode('utf-8'), dest)
    except Exception as ex:
        sys.exit(0)

    count = 0
    print("Aguardando confirmacao.")
    while True:
        if not ENTRIED_GROUP:
            count += 1
        else:
            break
        if count == 10:
            sys.exit(0)
        time.sleep(1)

    while message != "!sair":
        message = input("-> ")
        msg = {
            "acao": 3,
            "name": name,
            "group_id": GROUP_ID,
            "msg_id": MSG_ID,
            "msg": message
        }
        stringJson = json.dumps(msg)
        udp.sendto(stringJson.encode('utf-8'), dest)
        MSG_ID += 1
    menu()


def menu():
    OPTION = 0

    print("-------------------------------")
    print("-- 1 - Entrar em um chat     --")
    print("-- 2 - Sair                  --")
    print("-- 0 - Voltar ao menu        --")
    print("-------------------------------")

    OPTION = int(input("Escolha uma opcao:\n "))


if __name__ == "__main__":
    client()
