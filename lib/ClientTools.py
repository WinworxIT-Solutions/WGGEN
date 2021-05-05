from lib.Utils import Logger as Logger
from lib.LDAPTools import LDAPTools


class ClientTools:
    @staticmethod
    def get_client_list(args):

        target_clients = []
        clients = []

        # get ldap clients
        ldap = LDAPTools(args)
        ldap_clients = ldap.get_ldap_clients()

        if args.list:
            for c in args.list:
                if c not in ldap_clients:
                    target_clients.append(c)
            for c in ldap_clients:
                target_clients.append(c)
        else:
            target_clients = ldap_clients

        # create counter for clients
        for client in target_clients:
            if client == "SERVER":
                Logger.error("Cannot create client {}: Invalid Name".format(client))
            else:
                for i in range(0, args.count):
                    clients.append("{}-{}".format(client, i))

        return clients

    @staticmethod
    def write_config_files(actual_clients):
        n_actual_clients = len(actual_clients)
        for i, client in enumerate(actual_clients):
            print("Writing config files: {}%".format(int((i / (n_actual_clients - 1)) * 100)), end="\r")
            client.write_client_config()
        print("\nWritten {} config files".format(n_actual_clients))
