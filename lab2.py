# response = '''HTTP/1.1 {status}
# Connection: Close
#
# {html}
# '''
#
# context = {}
#
# context['status'] = 200
# context['html'] = '<html></html>'
#
# response.format(**context)

LISTING = '<a href="{file}">{file}<a/><br>'


import SocketServer		#Подключаем модули
import re
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer  # Класс-заголовок для реализации обработчика запросов

ROOT = '/'		# Место, откуда будем читать

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # Обнаружена запрашиваемая страница
        self.send_header('content-type', 'text/html')  # Интерпритация текста в HTML-разметку
        self.end_headers()

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        path = re.findall('^GET (.*) HTTP\/1\.1$', self.data.splitlines()[0])[0]
        target = os.path.join(ROOT, *path.split('/'))
        print path.split('/')
        if os.path.exists(target):   # Если путь существует
            # TODO: check if target is directory return list of files
            print target  # Печатаем его в консоль
            if os.path.isdir(target):  # Если это папка
                content = '\n'.join([LISTING.format(file=f) for f in os.listdir(target)])  # Выводим содержимое
            else:   # Иначе позволяем открыть элементы
                content = open(target).read()
            content = """HTTP/1.1 200
            Content-Type: text/html
            """ + content

            self.request.sendall(content)
        else:
            self.request.sendall('404 not found')  # Если не существует выбранного пути

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

# Create the server, binding to localhost on port 9999

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
print 'listening on ', HOST, ':', PORT  # Выдаем информацию кого прослушиваем

server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
# serv = HTTPServer((HOST, PORT), HttpProcessor)
server.serve_forever()   # Задаем длительность жизни сервера
