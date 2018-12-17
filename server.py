#-*- coding: utf-8 -*-
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi
from sql_interface import DbSchool
from handler_logic import Pupil_mark
from gui_window import Window

sql = DbSchool()

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        w.log_list.insert(END, "1")
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
        print ctype
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        print ("Incoming Post")    
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        start_time=time.time()
        # Перевірка по базі даних і створення об'єкта учня
        pupil = Pupil_mark(classroom=message['classroom'], 
                           key_uid_code=message['key_uid'],
                           sql_conn=sql)
        print("--- %s seconds ---" % (time.time() - start_time)) 
        info = pupil.stamp.strftime("%Y-%m-%d %H:%M:%S")
        if pupil.is_ready:
            info =u" ".join((info, pupil.pupil_info[0][1],
                               pupil.pupil_info[0][2],
                               pupil.group_name)).encode('utf-8')
        else:
            info =u" ".join((info, u"не знайдено в базі даних"))
        # відображаємо результати запитів до бази даних у логах серверу
        w.log_list.insert(END, info)
        if pupil.is_ready and pupil.is_on_schedule:
            if pupil.current_lesson["end"]:
                w.log_list.itemconfig(END, {'fg': 'green4'})
            else:
                w.log_list.itemconfig(END, {'fg': 'green'})
            message['status'] = 'confirmed'
        elif pupil.is_ready:
            message['status'] = 'not_confirmed'
            w.log_list.itemconfig(END, {'fg': 'blue'})
        else:
            message['status'] = 'not_in_DB'
            w.log_list.itemconfig(END, {'fg': 'red'})
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('192.168.43.214', port) #192.168.43.214
    httpd = server_class(server_address, handler_class)
    
    print 'Starting httpd on port %d...' % port
    httpd.serve_forever()
    
if __name__ == "__main__":
    import threading
    from Tkinter import *
    root = Tk()
    w = Window(root)
    t1 = threading.Thread(target=root.mainloop)
    t1.start()
    run()
