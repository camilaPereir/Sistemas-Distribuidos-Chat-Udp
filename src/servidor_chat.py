from distutils.debug import DEBUG
import socket
import json
import sys

HOST = ""  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
DEBUG = True
USER_LIST = []


def add_user(user, cliente):
    new_user = {}
    new_user["name"] = user["name"]
    new_user["connection"] = cliente
    new_user["group_id"] = user["group_id"]
    USER_LIST.append(new_user)


def remove_user(user, cliente):
    removed_user = {}
    removed_user["name"] = user["name"]
    removed_user["connection"] = cliente
    removed_user["group_id"] = user["group_id"]
    USER_LIST.remove(removed_user)


def server(udp):
    global USER_LIST
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
                add_user(string_dict, cliente)
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
                remove_user(string_dict, cliente)
                msg = {
                    "action": 2,
                    "name": string_dict["name"],
                    "group_id": string_dict["group_id"],
                    "status": 1
                }

                msg_json = json.dumps(msg)

                udp.sendto(msg_json.encode("utf-8"), cliente)

                msg = {
                    "group_id": string_dict["group_id"],
                    "name": string_dict["name"],
                    "msg": f"{string_dict['name']} SAIU DO GRUPO"
                }

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

                for users in USER_LIST:
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
