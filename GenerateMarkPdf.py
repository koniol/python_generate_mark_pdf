#!/usr/bin/env python

import sys
import imp
import StringIO
from time import gmtime, strftime
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from shutil import copyfile
import os

#from reportlab.lib.pagesizes import letter

class GenerateMarkPdf(object):


    # Wstaw parametry do listy
    def __init__(self, args):
        self.params = args
        # 0 nazwa skryptu
        # 1 nazwa orginalnego dokumentu
        # 2 polozenie znacznik na osi X
        # 3 polozenie znacznika na osi Y
        # 4 dane ktore trzeba zapisac
        # 5 dane2 ktore trzeba zapisac
        # 6 nazwa pliku: output default true

        # if len(args) < 5:
        #     self.logger("Brak wszytkich parametrow")
        #     return
        #
        # if len(self.params) < 7:
        #     self.params.append(self.params[1])

        

    ######################## Output    
    # Utworz plik dla ktorego zostanie wygenerowany nowy PDF 
    def setFilename(self, filename):
        self.output = PdfFileWriter()
        #@TODO ustaw nazwe pliku
        self.filename = filename


    ######################## logi
    # Trzeba utworzyc plik w lokalizacji i nadac mu uprawnienia
    def logger(self, data):
        try:
            logfile = open("/var/log/pdf_error.log","a")
            today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            logfile.write(str(today) + " " + str(data) + "\r\n")
        except Exception as e:
            print("Nie mozna utworzyc pliku" )
        except UnboundLocalError as u:
            print("Nie mozna utworzyc pliku" )
        finally:
            logfile.close()


    # Ustaw orginalny plik 
    def setOrginalPdfFile(self):
        try:
            # copyfile(params[1], "")
            # wa = os.access(params[1], os.W_OK)
            # print(wa)
            self.input1 = PdfFileReader(file(self.params[1], "rb"))

            if self.input1.isEncrypted:
                self.input1.decrypt()
        except IOError as ie:
            self.logger("Nie ma takiego pliku " + " "+ str(ie))
        except Exception as e:
            self.logger(e)


    # W obiekcie page.mediaBox jest trzymana rozmiar strony
    # def getXPosition(self, page):
    #     x = 20
    #     if self.params[2] == 'Left':
    #         x = 20
    #     if self.params[2] == 'Right':
    #         x = page.mediaBox[2] - 60
    #     return x
    #
    #
    # # W obiekcie page.mediaBox jest trzymana rozmiar strony
    # def getY(self, page):
    #     y = 20
    #
    #     if self.params[2] == 'Left':
    #         y = 20
    #     if self.params[2] == 'Right':
    #         y = page.mediaBox[2] - 60
    #
    #     return y


    ######################### Watermark
    # Generuj plik PDF
    def watermark(self, x, y, z, w):
        packet = StringIO.StringIO()
        #x = self.params[2]
        #y = self.params[3]
        data = self.params[4]
        # data2 = self.params[5]

        can = canvas.Canvas(packet)
        can.drawString(int(x), int(y), str(data))
        
        # can.drawString(int(z), int(w), str(data2))
        can.save()

        #Ustaw kurson na poczatek bufora
        packet.seek(0)
        return PdfFileReader(packet)



    def createNewPdf(self):
        iloscStron = int(self.input1.getNumPages())

        i = 0
        while i < iloscStron: 
            # Orginalna strona
            page = self.input1.getPage(i)
            x = 20
            y = page.mediaBox[3] - 10

            z = page.mediaBox[2] - 100
            w = page.mediaBox[3] - 10 
            watermark = self.watermark(x ,y, z, w)
            w = watermark.getPage(0)
            page.mergePage(w)
            self.output.addPage(page)
            i += 1

        try:
            w = os.access('/home/edokumenty/public_html/apps/edokumenty/var/tmp', os.W_OK)

            # Gdzie zapisac dane
            outputStream = file(self.filename, "wb")
            self.output.write(outputStream)
        except Exception as e:
            self.logger("Blad " + str(e))
        # finally:
            #outputStream.close()
            #self.output.close()


m = GenerateMarkPdf(sys.argv)
params = sys.argv
basename = os.path.basename(params[1])
m.setFilename("/home/edokumenty/public_html/apps/edokumenty/scripts/python/temp/" + basename )
m.setOrginalPdfFile()
m.createNewPdf()
print(1)

