# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:46:04 2020

@author: amaury

"""
import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
