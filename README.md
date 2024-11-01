Usage python Server.py

after change ip of client and 

python Client.py

if you want a exe use pyinstaller --onefile -w 


I made a backdoor in python using websockets with a server (attacker) and a client (victim), the server is composed of creating a web server by the flask lib where an ip:port is used in http where the server listens for new connections, when the client connects to it, this connection is maintained, how does it work? After this connection the server can send requests via post in real time to the client where the client will also listen for post requests, when the client receives this post it will interpret it as a string thus executing and translating it as cmd.exe commands, it is worth remembering that once an attacker has access to the victim's cmd he will also have access to powershell and thus be able to escalate to more privileges, the communication between client and server is done entirely via http headers, below I will put the codes.
