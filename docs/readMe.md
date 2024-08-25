https://www.youtube.com/live/95Qwsi5cs78 
Video Pamela Fox FastAPI

Repos used : 
aka.ms/python-web-apps-fastapi
aka.ms/fastapi-starter
aka.ms/fastapi-postgres-app
aka.ms/fastapi-azure-functions
aka.ms/fastapi-functions-apim

# HTTP HyperText Transfer Protocol
This is what the web is built on 
- A client sends an HTTP request
- A server sends back an HTTP response. 

> inspect (dev tools in browser) > Network tab > all : to see all the requests that were made to load the page. 

## Action verb
- GET : retrieve data from a servers (the client wants to get the web page)
- POST : send data to a server
- PUT : send data to a server, replacing existing data 
- PATCH : send data to a server, updating part of existing data 
- DELETE : delete data from a server

## HTTP Status code
- 200 successful
- 301 moved permanently (redirection)
- 401 not authorized
- 404 not found
- 500 Server error

# HTTP API

## API vs HTTP API

*API* = Application programming interface. 
A way for a program to talk to another program. 
Not all APIs are HTTP APIs 

*HTTP API* = any API that uses HTTP as its communication protocol. (a computer sends an HTTP request and another computer sends back an HTTP response, a program to another program).
![HTTP APIs](image.png)

## HTTP API response formats
- JSON
- XML
- image
![HTTP API response format](image-1.png)