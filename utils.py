import threading
import socketserver
import webbrowser
import json
import subprocess
import sys

import os
os.chdir(os.path.dirname(__file__))

def get_headers():
    headers={}

    try:
        j=json.load(open('headers.json'))
        assert 'User-Agent' in j
        return headers
    except:
        print('No cached headers found. Retrieving...',file = sys.stderr)
        class H(socketserver.BaseRequestHandler):
            def handle(self): # well it turned out spawning a raw TCP server is the easiest way for this
                data=self.request.recv(8192).decode()
                self.request.send(
                    b'HTTP/1.1 404 Not Found\nContent-Type:text/html\nContent-Length:24\n\n<script>close()</script>\n'
                ) # 404 so the page is not cached...it shouldn't be anyway
                for line in data.splitlines():
                    if line.startswith('GET'):
                        continue
                    try:
                        key,val=line.split(': ')

                        if key.lower() not in ('host','connection','accept','cookie','accept-encoding'):
                            headers[key]=val
                    except ValueError:
                        pass

                threading.Thread(target = self.server.shutdown,args = ()).start()
        socketserver.TCPServer.allow_reuse_address = True
        server=socketserver.TCPServer(('localhost',8003),H)
        try:
            webbrowser.open('http://localhost:8003')
        except:
            print('Cannot open a browser for you. Please manually launch your favorite browser and navigate to http://localhost:8003',file = sys.stderr)
        server.serve_forever()
        print("Headers:",headers,file = sys.stderr)
        json.dump(headers, open('headers.json','w'),indent = 4)
        return headers

def get_cookies():
    try:
        j=json.load(open('cookies.json',))
        return j
    except:
        print('No cached cookies found. Retrieving...',file = sys.stderr)
        os.chdir('electron')
        bin_loc=subprocess.Popen('npm bin',shell = True, stdout = subprocess.PIPE,encoding = 'utf-8')
        bin_loc.wait()
        if bin_loc.returncode!=0:
            raise OSError("npm not installed")
        bin_loc=bin_loc.stdout.read().strip()
        os.chdir(os.path.dirname(__file__))
        p=subprocess.Popen(f'{bin_loc}/electron electron',shell = True, stderr=open(os.devnull,'w'))
        p.wait()
        j=json.load(open('cookies.json',))
        print('Cookies:',j,file = sys.stderr)
        return j

