import requests

def show_error(res):
    if res.status_code == 401:
        print("ERROR -> You are not authenticated: please run 'login' command first")
    else:
        print(res.status_code)
        print(res.headers)    

def doGet(args, api_url, *kargs, **kwargs):
    if args.debug: print("Calling %s with params: %s %s"%(api_url,str(kargs),str(kwargs)))
    res = requests.get(api_url, *kargs, **kwargs)
    if res.status_code == 200:
        if args.debug: print("Response headers:",res.headers)
        return res.json()
    
    show_error(res)
    return {}

def doPost(args, api_url, *kargs, **kwargs):
    if args.debug: print("Calling %s with params: %s %s"%(api_url,str(kargs),str(kwargs)))
    res = requests.post(api_url, *kargs, **kwargs)
    if res.status_code == 200:
        if args.debug: print("Response headers:",res.headers)
        return res.json()
    
    show_error(res)
    return {}   