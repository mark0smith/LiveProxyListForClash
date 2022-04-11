import requests
import json
import yaml
import time
import concurrent.futures
import random


def get_proxylist(filename = 'proxy.list'):
    raw_url = "https://github.com/fate0/proxylist/raw/master/proxy.list"
    req = requests.get(raw_url)
    with open(filename,'wb') as fw:
        for iter in req.iter_content(1024):
            fw.write(iter)

def check_single_proxy(proxy):
    # always return True 😅
    return True

    proxies = {
        "http":f"http://{proxy['host']}:{proxy['port']}",
        "https":f"https://{proxy['host']}:{proxy['port']}",
    }
    try:
        if proxy['type'] == "https":
            url = "https://www.baidu.com/robots.txt"
        else:
            url = "http://baidu.com/robots.txt"
        req = requests.get(url,proxies=proxies,timeout=3)
        assert "Baiduspider" in req.text
        assert req.status_code == 200
        print(f"[+] Valid Proxy [{proxy['country']}] ==> {proxy['type']}://{proxy['host']}:{proxy['port']}")
        return True
    except Exception as e:
        pass

    return False


def check_valid(proxy_list):
    result = []
    # proxy_list = random.choices(proxy_list,k=min(100,len(proxy_list)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_single_proxy, proxy): proxy for proxy in proxy_list}
        for future in concurrent.futures.as_completed(future_to_url):
            proxy = future_to_url[future]
            try:
                data = future.result()
                if data == True:
                    result.append(proxy)
            except Exception as exc:
                pass

    return result

            

def generate_config(filename = 'proxy.list'):
    proxy_list = []
    output = {}

    with open(filename) as fr:
        for line in fr.readlines():
            proxy = json.loads(line.strip())
            proxy_list.append(proxy)
    
    proxy_list = check_valid(proxy_list)
    
    output['proxies'] = []
    output['Proxy Group'] = [] 


    index = 0
    proxy_group_all = []
    proxy_group_cn = []
    proxy_group_us = []
    proxy_group_others = []
    for proxy in proxy_list:
        index += 1
        p = {}
        p['name'] = f"{index} [{proxy['country']}] ==> {proxy['type']}://{proxy['host']}:{proxy['port']}"
        p['type'] = "http"
        p['server'] = proxy['host']
        p['port'] = proxy['port']
        p['remarks'] = str(index)
        if proxy['type'] == "https":
            # p['type'] = "https"
            p['tls']= True
            p['skip-cert-verify']= True
        if proxy['country'] == "CN":
            proxy_group_cn.append(p['name'])
        elif proxy['country'] == "US":
            proxy_group_us.append(p['name'])
        else:
            proxy_group_others.append(p['name'])

        # proxy_group_all.append(p['name'])
        output['proxies'].append(p)
    
    g = {
        'name':'Proxy',
        'proxies': ["CN Proxy","US Proxy","Others Proxy"],
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
    output['Proxy Group'].append(g)
    output['Proxy Group'].append(proxy_cn)
    output['Proxy Group'].append(proxy_us)
    output['Proxy Group'].append(proxy_others)
    
    # output['Rules'] = ['MATCH,CN Proxy']

    with open("temp_config.yml",'w') as fw:
        yaml.safe_dump(output,fw)


filename = 'proxy.list'
get_proxylist(filename)
generate_config(filename)

with open("changelog.txt","w",encoding="utf8") as fw:
    date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    fw.write(f"Updated at {date}.")
