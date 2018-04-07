
import SocketServer
from threading import Thread
import socket
import numpy as np
import math
import time


class SocketManager(SocketServer.BaseRequestHandler,Thread):
    """
    This class handels the connection with the app.

    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.

    """


    def __init__(self,mainclass):
        Thread.__init__(self)

        self.mainclass = mainclass

        self.requested = 1

        self.host = ''
        self.port = 20009

        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexionApp = socket.socket()


    def run(self):
        """This accepts connection and sends stuff.



        """

        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((self.host, self.port))

        while(self.requested):

            self.connexion.listen(5)

            print("Le serveur ecoute a present sur le port {}".format(self.port))

            self.connexionApp, infos_connexion = self.connexion.accept()

            msg_recu = b""

            try:
                while msg_recu != b"fin":
                    msg_recu = self.connexionApp.recv(1024)

                    # L'instruction ci-dessous peut lever une exception si le message
                    # Receptionne comporte des accents

                    print(msg_recu.decode())
                    self.parseMatrix(msg_recu.decode())
                    #self.sendMatrix()
                    #self.connexionApp.send(b"5 / 5")
            except Exception as e:
                print(e)
                print ("hey, failure")

            print("Fermeture de la connexion")

            self.connexionApp.close()

            self.connexion.close()






    def send(self,text):
        """Sends a normal text"""
        try:
            self.connexionApp.send(text + "\n")
            #self.connexionApp.sendall(text)

            #my_writer_obj = self.connexionApp.makefile(mode='w')
            #my_writer_obj.write('my stuff')
            #my_writer_obj.flush()
            print ("I sent :" + text)
            #self.connexionApp.close()


        except:
            return



    def sendMatrix(self):
        """
        Sends the matrix.

        """

        stringFormMap = ""

        for i in range(self.mainclass.MATRIX_SIZE):
            for j in range(self.mainclass.MATRIX_SIZE):
                self.send(str(i) + "," + str(j) + "," + str(self.mainclass.ma_room[i][j]))
                #stringFormMap += str(self.mainclass.ma_room[i][j]) + ","
            #stringFormMap = stringFormMap[:-1] + ";"
            #self.send(stringFormMap)

        #stringFormMap = stringFormMap[:-1]
        #self.send(stringFormMap)


    def parseMatrix(self,com):
        """
        This parses the matrix that the app sends and saves it in the main stuff
        """
        #a = "abds"
        #a.__contains__("a")
        if(com.__contains__("startMapping")):
            print ("starting mapping!")
            #self.mainclass.startMapping()
            self.mainclass.update_matrix()
            time.sleep(1)
            self.mainclass.update_matrix()

        # TODO : parse matrix!!!


