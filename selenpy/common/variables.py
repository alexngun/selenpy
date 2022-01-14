from colorama import Fore, Back, Style

class dbMessage:

    def serverOkwithAuth(host, user, password, server_os, database_version):

        okWithAuth = Back.WHITE + Fore.GREEN + "\n=== Server Connection Established ===\n"
        temp = "| host: %s                           " % host
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| user: %s                           " % user
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| password: '***...%s'               " % password
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| server_os: %s                      " % server_os
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| database_version: %s               " % database_version
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        okWithAuth += "====================================="
        
        return okWithAuth

    def serverOk(host, server_os, database_version):

        okWithAuth = Fore.GREEN + "\n=== Server Connection Established ===\n"
        temp = "| host: %s                           " % host
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| server_os: %s                      " % server_os
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        temp = "| database_version: %s               " % database_version
        temp = temp[:36] + "|\n"
        okWithAuth += temp
        okWithAuth += "====================================="
        
        return okWithAuth

class Mode:

    AUTO = "auto"
    SELFDEFINED = "self-defined"

    LOCAL = "local"
    SELF = "self"
    PRIVATE = "private"
    FREE = "free"

    DEFAULT = "default"