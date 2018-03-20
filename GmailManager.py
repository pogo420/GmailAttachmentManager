from GmailEngine.GmailMaster import GmailMaster
from json import load



cmd_list = {}  # dictionary to store function utility.
CONFIG = r"../Credentials/config.json"  # path of config file


def function_name(func):
    cmd_list[func.__name__] = func.__doc__


def bank_download():
    with open(CONFIG) as f:
        json_data = load(f)
        QUERY = json_data.get("BANK").get("QUERY")
        STORE = json_data.get("STORE")
        LABEL = json_data.get("BANK").get("LABEL")
        msg_ids = GmailMaster(CONFIG).view_messages(LABEL, QUERY)
        if len(msg_ids) != 0:
            GmailMaster(CONFIG).download_attachment(msg_ids,STORE)
        else:
            pass

def ola_download():
    with open(CONFIG) as f:
        json_data = load(f)
        QUERY = json_data.get("OLA").get("QUERY")
        STORE = json_data.get("STORE")
        LABEL = json_data.get("OLA").get("LABEL")
        msg_ids = GmailMaster(CONFIG).view_messages(LABEL, QUERY)
        if len(msg_ids) != 0:
            GmailMaster(CONFIG).download_attachment(msg_ids,STORE)
        else:
            pass

def input_router():
    welcome = "Welcome to Google Manager 1.0"
    prompt = "GmailManager>"
    exit = "bye"
    print(welcome)
    while True:
        command = input(prompt)

        if command == exit:
            print("Exiting Gmail Manager")
            break

        elif command == "help":
            for i in cmd_list.keys():
                print(i,cmd_list.get(i))

        elif command == "bank_download":
            bank_download()

        elif command == "ola_download":
            ola_download()

        else:
            print("wrong command,enter help")


if __name__ == "__main__":
    input_router()