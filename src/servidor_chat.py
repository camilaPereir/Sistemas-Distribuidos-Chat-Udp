from distutils.debug import DEBUG
import socket
import json
import sys

HOST = ""  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
DEBUG = True
LISTA_USUARIO = []


def adicionar_usuario(usuario, cliente):
    novo_usuario = {}
    novo_usuario["name"] = usuario["name"]
    novo_usuario["connection"] = cliente
    novo_usuario["group_id"] = usuario["group_id"]
    LISTA_USUARIO.append(novo_usuario)


def server(udp):
    global LISTA_USUARIO
    print(f"Starting UDP Server on port {PORT}")
    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, cliente = udp.recvfrom(1024)
        msg_decoded = msg.decode('utf-8')
        if DEBUG:
            print(f"{msg_decoded}")
        try:
            string_dict = json.loads(msg_decoded)
            if string_dict["action"] == 1:
                adicionar_usuario(string_dict, cliente)
                msg = {
                    "action": 1,
                    "name": string_dict["name"],
                    "group_id": string_dict["group_id"],
                    "status": 1
                }

                msg_json = json.dumps(msg)
                if DEBUG:
                    # print(f"{msg_json} -> {cliente}")
                    udp.sendto(msg_json.encode("utf-8"), cliente)

            elif string_dict["action"] == 2:
                print("Saindo...")
                sys.exit(0)
            elif string_dict["action"] == 3:
                msg = {
                    "action": 3,
                    "name": string_dict["name"],
                    "group_id": string_dict["group_id"],
                    "msg_id": string_dict["msg_id"],
                    "status": 1
                }

                msg_json = json.dumps(msg)

                udp.sendto(msg_json.encode("utf-8"), cliente)

                msg = {
                    "group_id": string_dict["group_id"],
                    "name": string_dict["name"],
                    "msg": string_dict["msg"]
                }

                msg_json = json.dumps(msg)

                for users in LISTA_USUARIO:
                    if users["group_id"] == string_dict["group_id"]:
                        if users["connection"] != cliente:
                            udp.sendto(msg_json.encode(
                                "utf-8"), users["connection"])
        except Exception as ex:
            pass

    udp.close()


def client():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server(udp)


if __name__ == "__main__":
    client()
