from pymongo.auth import authenticate


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class dbMessage:

    okWithAuth = bcolors.OKGREEN + """
<--- Server Connection Established --->
    host: '%s'                        
    user: '%s' 
    password: '***%s' (last 3 digits)
    server_os: %s
    database_version: %s
---------------------------------------
""" 

    ok = bcolors.OKGREEN + """
<--- Server Connection Established --->
    host: '%s'                        
    server_os: %s
    database_version: %s
---------------------------------------
""" 
