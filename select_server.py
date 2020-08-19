from socket import *
from select import select

#创建好监听套接字
sockfd = socket()
sockfd.bind(("0.0.0.0",8888))
sockfd.listen(5)

sockfd.setblocking(False)

#准备IO进行监控
rlist = [sockfd]
wlist = []
xlist = []


while True:
    #开始监控IO发生
    rs,ws,xs = select(rlist,wlist,xlist)
    for r in rs:
        #有客户端连接
        if r is sockfd:
            connfd,addr = r.accept()
            print("Connect from",addr)
            connfd.setblocking(False)
            rlist.append(connfd)
        else:
            #某个客户端发消息给我
            data = r.recv(1024).decode()
            if not data:
                #客户端退出
                rlist.remove(r)#移除监控
                r.close()
                continue
            print("收到:",data)
            wlist.append(r)
    for w in ws:
        w.send(b"ok")
        wlist.remove(w)