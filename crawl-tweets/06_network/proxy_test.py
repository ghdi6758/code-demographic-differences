
import requests
import httplib
import os

# proxy_file = "./list_of_proxies.txt"
# with open(proxy_file) as fi, open("./valid_proxies.txt", "w") as output:
#     for line_cnt, line in enumerate(fi):
        
#         proxies = {}

#         terms = [term.strip() for term in line.split()]
#         ip = terms[0]
#         port = terms[1]
#         login = terms[2]
#         pwd = terms[3]

#         proxy_url = 'http://%s:%s@%s:%s' % (login, pwd, ip, port)
#         proxies['http'] = proxy_url
#         # temp_url = proxy_url.replace("http","https")
#         # proxies['https'] = temp_url

#         print proxies

#         try:        
#             response = requests.get("http://www.google.com/", proxies=proxies)
#             print response.status_code
#             if response.status_code == httplib.OK:
#                 print line
#                 output.write(line)
#         except:
#             print response.status_code
#             print "Proxy not working", line_cnt


proxy_file = "./new_proxies.txt"
with open(proxy_file) as fi, open("./new_valid_proxies.txt", "w") as output, open("./html_test_proxy.html", "w") as html_output:
    for line_cnt, line in enumerate(fi):
        
        proxies = {}

        terms = [term.strip() for term in line.split(":")]
        ip = terms[0]
        port = terms[1]
        login = terms[2]
        pwd = terms[3]

        proxy_url = 'http://%s:%s@%s:%s' % (login, pwd, ip, port)
        # proxy_url = 'http://jisun:ekdrh@10.10.10.199:2999'
        proxies['http'] = proxy_url
        # os.environ['http_proxy'] = proxy_url

        # temp_url = proxy_url.replace("http","https")
        # proxies['https'] = temp_url

        # print proxies

        try:        
            
            response = requests.get("http://www.lagado.com/proxy-test")

            print response.status_code

            if response.status_code == httplib.OK:
                print line
                html_output.write(response.content)
                output.write(line)
        except:
            print response.status_code
            print "Proxy not working", line_cnt
            raise
        # break


print "DONE"
