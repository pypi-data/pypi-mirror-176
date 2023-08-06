#!/bin/python
import argparse
import json

from .config import get_config, get_config_file
from .utils import doPost, doGet
 

def doLogin(args):
    api_url = args.endpoint + "/token"
    if not args.username: args.username = input("Username: ")
    if not args.password: args.password = input("Password: ")

    payload = {
        "grant_type":"", "username": args.username, "password": args.password,
        "scope":"","client_id":"","client_secret":""
    }    

    res = doPost(args, api_url, data=payload)

    config = get_config()
    config["API"]["token"] = res["access_token"]
    with open(get_config_file(),"w") as fp:
        config.write(fp) 
    print("Login successfull!")

def doLogout(args):
    config = get_config()
    config["API"]["token"] = ""
    with open(get_config_file(),"w") as fp:
        config.write(fp) 

def doWhoami(args):
    hs = {"Authorization":"Bearer %s"%args.token}
    api_url = args.endpoint + "/users/me"
    res = doGet(args, api_url, headers=hs)
    print(res)

def doSearch(args):
    hs = {"Authorization":"Bearer %s"%args.token}
    api_url = args.endpoint + "/dna/search"
    payload = {"table_name":args.table,"query_sentence":args.query,"top_n":args.topn}
    res = doGet(args, api_url, headers=hs, params=payload)
    print("Writing response to", args.output)
    with open(args.output, "w") as fp:
        json.dump(res, fp, indent=2)

def main():
    config = get_config()

    ENDPOINT = config['API']['endpoint']
    TOKEN = config['API']['token']

    parser = argparse.ArgumentParser(description='Run vecb')
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--token", default=TOKEN)    
    parser.add_argument("--debug", action="store_true")        

    subparsers = parser.add_subparsers(help='sub-command help', required=True, dest='cmd')
    login = subparsers.add_parser('login', help='Authenticate to the api') 
    login.set_defaults(func=doLogin)
    login.add_argument("--username")
    login.add_argument("--password")

    logout = subparsers.add_parser('logout', help='Disconnect')        
    logout.set_defaults(func=doLogout)
    
    whoami = subparsers.add_parser('whoami', help='Check current auth info')        
    whoami.set_defaults(func=doWhoami)

    #Search parameters
    search = subparsers.add_parser('search', help='Run a search over the db')
    search.add_argument('query', type=str, 
                        help='Sequence to search for')
    search.add_argument('--table', type=str, default="viruses",
                        help='Sequence to search for')                        
    search.add_argument('--topn', type=str, default="10",
                        help='Sequence to search for')                        
    search.add_argument('-o','--output', type=str, default="res.json",
                        help='Output directory')                        
    search.add_argument('--format', type=str, default="json",
                        help='Output format')
    search.set_defaults(func=doSearch)

    args = parser.parse_args()
    if args.debug: print(args)

    args.func(args)

if __name__ == "__main__":
    main()

