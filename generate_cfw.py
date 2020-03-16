import requests
import json
import yaml
import time

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
    proxy_group_all = []
    proxy_group_cn = []
    proxy_group_us = []
    proxy_group_others = []
    for proxy in proxy_list:
        index += 1
        p = {}
        p['name'] = f"{index}"
        p['type'] = "http"
        p['server'] = proxy['host']
        p['port'] = proxy['port']
        p['remarks'] = str(index)
        if proxy['type'] == "https":
            # p['type'] = "https"
            p['tls']= True
            p['skip-cert-verify']= True
        if proxy['country'] == "CN":
            proxy_group_cn.append(str(index))
        elif proxy['country'] == "US":
            proxy_group_us.append(str(index))
        else:
            proxy_group_others.append(str(index))

        proxy_group_all.append(str(index))
        output['Proxy'].append(p)
    
    g = {
        'name':'Proxy',
        'proxies': proxy_group_all,
        'type':"select",
        # "url":"http://www.gstatic.com/generate_204",
        "interval":600
    }
    proxy_cn = {
        'name':'CN Proxy',
        'proxies': proxy_group_cn,
        'type':"url-test",
        "url":"http://www.baidu.com",
        "interval":600
    }
    proxy_us = {
        'name':'US Proxy',
        'proxies': proxy_group_us,
        'type':"url-test",
        "url":"http://www.gstatic.com/generate_204",
        "interval":600
    }
    proxy_others = {
        'name':'Others Proxy',
        'proxies': proxy_group_others,
        'type':"url-test",
        "url":"http://www.gstatic.com/generate_204",
        "interval":600
    }
    output['Proxy Group'].append(proxy_cn)
    output['Proxy Group'].append(proxy_us)
    output['Proxy Group'].append(proxy_others)
    output['Proxy Group'].append(g)
    # output['Rules'] = ['MATCH,CN Proxy']

    with open("temp_config.yml",'w') as fw:
        yaml.safe_dump(output,fw)


filename = 'proxy.list'
get_proxylist(filename)
generate_config(filename)

with open("changelog.txt","w",encoding="utf8") as fw:
    date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    fw.write(f"Updated at {date}.")