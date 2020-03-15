import requests
import json
import yaml

def get_proxylist(filename = 'proxy.list'):
    raw_url = "https://github.com/fate0/proxylist/raw/master/proxy.list"
    req = requests.get(raw_url)
    with open(filename,'wb') as fw:
        for iter in req.iter_content(1024):
            fw.write(iter)

def generate_config(filename = 'proxy.list'):
    proxy_list = []
    output = {}

    with open(filename) as fr:
        for line in fr.readlines():
            proxy = json.loads(line.strip())
            proxy_list.append(proxy)
    
    output['Proxy'] = []
    output['Proxy Group'] = [] 


    index = 0
    for proxy in proxy_list:
        index += 1
        p = {}
        p['name'] = f"{index}"
        p['type'] = "http"
        p['server'] = proxy['host']
        p['port'] = proxy['port']
        if proxy['type'] == "https":
            # p['type'] = "https"
            p['tls']= True
            p['skip-cert-verify']= True
        output['Proxy'].append(p)
    g = {
        'name':'Proxy',
        'proxies': [str(x) for x in range(1,index)],
        'type':"url-test",
        "url":"http://www.gstatic.com/generate_204",
        "interval":600
    }
    output['Proxy Group'].append(g)
    with open("temp_config.yml",'w') as fw:
        yaml.safe_dump(output,fw)


filename = 'proxy.list'
get_proxylist(filename)
generate_config(filename)