from ControlNode import ControlNode
from NodeStatus import *
import time
import socket
import sys
BUFSIZE = 4096




class SequenceNode(ControlNode):

    def __init__(self,name):
        ControlNode.__init__(self,name)
        self.nodeType = 'Sequence'
        self.accepted = False




    def Execute(self,args):
        if (self.isRoot):
            try:
                message = self.GetString("")

                if(not self.accepted):

                    # Start listening
                    self.s.listen(10)
                    print("Socket Listening")

                    # Accept connection
                    print("Accepting Connection")

                    self.conn, self.addr = self.s.accept()
                    print("Connected to %s:%s" % (self.addr[0], self.addr[1]))
                    self.accepted = True

                BUFFER = bytes()

                while (True):
                    data = self.conn.recv(BUFSIZE)
                    if not data:
                        break

                message = self.GetString('')


                message = message + "|END"
                self.conn.sendall(message.encode('utf-8'))
            except (ConnectionAbortedError, BrokenPipeError):
                self.s.close()
                print('The game has stopped')
                sys.exit()


            #print 'Starting Children Threads'
        self.SetStatus(NodeStatus.Idle)


        while self.GetStatus() != NodeStatus.Success and self.GetStatus() != NodeStatus.Failure:

            #check if you have to tick a new child or halt the current
            i = 0
            #try:
            for c in self.Children:
                i = i + 1

                if c.GetStatus() == NodeStatus.Idle:
                    #print 'starting tread ' + c.name + ' from thread ' + str(thread.get_ident())
                    #thread.start_new_thread(c.Execute,())
                    c.Execute(args)
                   # print '???' + str(i)
                while c.GetStatus() == NodeStatus.Idle:
                    #print 'waiting child ' + c.name + ' thread ' + str(thread.get_ident())
                    time.sleep(0.1)


                if c.GetStatus() == NodeStatus.Running:
                    self.SetStatus(NodeStatus.Running)
                    self.SetColor(NodeColor.Gray)
                  #  print 'Breaking'  + str(i)
                    self.HaltChildren(i + 1)
                    break
                elif c.GetStatus() == NodeStatus.Success:
                    c.SetStatus(NodeStatus.Idle)
                    self.SetStatus(NodeStatus.Running)

                    if i == len(self.Children):
                        self.SetStatus(NodeStatus.Success)
                        self.SetColor(NodeColor.Green)
                        break
                        #while self.GetStatus() != NodeStatus.Idle:
                            #time.sleep(0.1)

                elif c.GetStatus() == NodeStatus.Failure:
                    c.SetStatus(NodeStatus.Idle)
                    self.HaltChildren(i + 1)
                    self.SetStatus(NodeStatus.Failure)
                    self.SetColor(NodeColor.Red)

                    #while self.GetStatus() != NodeStatus.Idle:
                    #       time.sleep(0.1)
                    #print 'Failure'  + str(i)
                    break

                else:
                    raise Exception('Node ' +self.name + ' does not recognize the status of child ' + str(i) +'. (1 is the first)' )
        #print 'SEQUENCE DONE'


           # except:
             #   print 'Error'

