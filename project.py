from tkinter import *
from tkinter import ttk
from win32 import win32api
from win32 import win32print
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os,sys
from functools import partial
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table
#from reportlab.platypus import letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import webbrowser
import datetime
from datetime import date
import shutil
import fitz
import cv2
import numpy as np
#import win32api
#import win32print
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io
from shutil import copyfile
import time
from num2words import num2words
import subprocess



top = tk.Tk(className=' Secure_Tech Bill Soft')
h = top.winfo_screenheight()
w = top.winfo_screenwidth()
global notes_from_db
global name
global address
global gst_no
global tax
global date
global type_of_pdf
x=1

def error(msg):
    messagebox.showinfo('error',msg)
    
def last_try(path):
    if sys.platform == 'win32':
        args = '"C:\\\\Program Files\\\\gs\\\\gs9.53.3\\\\bin\\\\gswin64c" ' \
               '-sDEVICE=mswinpr2 ' \
               '-dBATCH ' \
               '-dNOPAUSE ' \
               '-dFitPage ' \
               '-sOutputFile="%printer%myPrinterName" '
        ghostscript = args + os.path.join(os.getcwd(), path).replace('\\', '\\\\')
        subprocess.call(ghostscript, shell=True)

############################################################ SEARCH QUATATION ###########################################################\

def search_quotation(tree,name,gst_no,quotation_no,date):
    try:
        for i in tree.get_children():
            tree.delete(i)
    except:
        pass
    
    if name !="":
        query=("SELECT NAME, ID, DATE, GST from QUOTATION where NAME LIKE" +' \''+name+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif gst_no !="":
        query=("SELECT NAME, ID, DATE, GST from QUOTATION where GST LIKE" +' \''+gst_no+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif quotation_no !="":
        query=("SELECT NAME, ID, DATE, GST from QUOTATION where ID LIKE" +' \''+quotation_no+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif date !="":
        query=("SELECT NAME, ID, DATE, GST from QUOTATION where DATE LIKE" +' \''+str(date)+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    else:
        error("All Entries are Empty!")



######################################################### PRINT QUATATION FROM CREATE PDF #################################################################

def printer_print_q(copies):
    try:
        path=(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
        with open(path, 'rb') as file:
            file.close()
        
    except:
        path=(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
        with open(path, 'rb') as file:
            file.close()

            
    last_try(path)


    

###################################### SHOW INVOICE IS STARTED ######################################################
def print_from_list(copies,name):
    if name=="Original":
        path=(r"C:\ProgramData\Secure_Tech\file_from_db\original.pdf")
    elif name=="Duplicate":
        path=(r"C:\ProgramData\Secure_Tech\file_from_db\duplicate.pdf")

    elif name=="SAVE_PDF":
        path=(r"C:\ProgramData\Secure_Tech\file_from_db\duplicate.pdf")
        with open(path, 'rb') as file:
            file.close()
        webbrowser.open(r'file:///'+path)
        return


            
    last_try(path)

        
def writeTofile(data,filename):
    with open(filename, 'wb') as file:
        file.write(data)
        file.close()
    return

def invoice_preview_show(tree,type_of):
    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    invoice_num=item_list[2]
    if type_of =="quotation":
        query="""SELECT * FROM QUOTATION WHERE ID = ?"""
    else:
        query="""SELECT * FROM INVOICE WHERE ID = ?"""
    results=conn.execute(query, (invoice_num,))
    if type_of =="quotation":
        for i in results:
            duplicate = i[6]
    else:
        for i in results:
            original = i[6]
            duplicate= i[7]
        
    

    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\file_from_db"))
        time.sleep(0.3)
    except:
        pass
    
    path= (r"C:\ProgramData\Secure_Tech\file_from_db")
    os.mkdir(path)
    if type_of =="quotation":
        duplicatePath = (r"C:\ProgramData\Secure_Tech\file_from_db\duplicate.pdf")
        writeTofile(duplicate, duplicatePath)
    else:

        originalPath = (r"C:\ProgramData\Secure_Tech\file_from_db\original.pdf")
        duplicatePath = (r"C:\ProgramData\Secure_Tech\file_from_db\duplicate.pdf")
        writeTofile(duplicate, duplicatePath)
        writeTofile(original, originalPath)
    
    
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\img"))
        time.sleep(0.3)
    except:
        pass
    
    doc = fitz.open(duplicatePath)
    zoom = 2 # to increase the resolution
    mat = fitz.Matrix(zoom, zoom)
    noOfPages = doc.pageCount
    path=(r"C:\ProgramData\Secure_Tech\temp\img\\")
    os.mkdir(path)
    for pageNo in range(noOfPages):
        page = doc.loadPage(pageNo) #number of page
        pix = page.getPixmap(matrix = mat)
        if noOfPages ==1:
            output = path + "outfile.jpg" # you could change image format accordingly
        else:
            output = path + "outfile"+str(int(pageNo)+1) + '.jpg' # you could change image format accordingly
        pix.writePNG(output)
    doc.close()
    gui_preview("From List PDF",type_of)
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\file_from_db"))
    except:
        pass
def search_invoice(tree,name,gst_no,invoice_no,date):
    try:
        for i in tree.get_children():
            tree.delete(i)
    except:
        pass
    
    if name !="":
        query=("SELECT NAME, ID, DATE, GST from INVOICE where NAME LIKE" +' \''+name+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif gst_no !="":
        query=("SELECT NAME, ID, DATE, GST from INVOICE where GST LIKE" +' \''+gst_no+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif invoice_no !="":
        query=("SELECT NAME, ID, DATE, GST from INVOICE where ID LIKE" +' \''+invoice_no+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    elif date !="":
        query=("SELECT NAME, ID, DATE, GST from INVOICE where DATE LIKE" +' \''+str(date)+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name_1=i[0]
            invoice_1=i[1]
            date=i[2]
            gst=i[3]
            tree.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
            k=k+1
    else:
        error("All Entries are Empty!")


#################################################### SAVE INVOICE is STRATED ##############################################

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        filedata = file.read()
    return filedata



def save_files_db():
    global type_of_pdf
    global invoice_num
    global name
    global address
    global gst_no
    global tax
    global date
    global mobile_to_db
    global string_to_db



    if type_of_pdf == "invoice":
        query="SELECT ID from INVOICE"
        results=conn.execute(query)
        for i in results:
            if str(invoice_num) == str(i[0]):
                return
        query = """ INSERT INTO INVOICE (ID,NAME,ADDRESS,GST,DATE,MOBILE,DATA) VALUES ( ?,?,?,?,?,?,?)"""
        data_db= (invoice_num,name,address,gst_no,date,mobile_to_db,string_to_db)
        conn.execute(query, data_db)
        conn.commit()
        return
    elif type_of_pdf == "quotation":
        query="SELECT ID from QUOTATION"
        results=conn.execute(query)
        for i in results:
            if str(invoice_num) == str(i[0]):
                return
        query = """ INSERT INTO QUOTATION (ID,NAME,ADDRESS,GST,DATE,MOBILE,DATA) VALUES ( ?,?,?,?,?,?,?)"""
        data_db= (invoice_num,name,address,gst_no,date,mobile_to_db,string_to_db)
        conn.execute(query, data_db)
        conn.commit()
        return



        
############################################################### GUI and Functional Work For Preview Page #############################################################


def printer_print(copies,name):
    global top1
    try:
        top1.destroy()
    except:
        pass
    if name == "org+dup":       
        try:
            path=(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
        except:
            path=(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
        k=1
        
        for i in range(2):
            try:
                shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\temp1"))
            except:
                pass
            if k==2:
                copy_name="Duplicate Copy"
            else:
                copy_name="Original Copy"
                
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Times-Roman", 9)
            can.drawString(450, 800, copy_name)
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            try:
                existing_pdf = PdfFileReader(open(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf", "rb"))
            except:
                existing_pdf = PdfFileReader(open(r"C:\ProgramData\Secure_Tech\temp\hello.pdf", "rb"))
            output = PdfFileWriter()
            for i in range (existing_pdf.getNumPages()):
                page = existing_pdf.getPage(i)
                page.mergePage(new_pdf.getPage(0))
                output.addPage(page)
            try:
                path=(r"C:\ProgramData\Secure_Tech\temp\temp1")
                os.mkdir(path)
            except:
                pass
            outputStream = open(r"C:\ProgramData\Secure_Tech\temp\temp1\print.pdf", "wb")
            path=(r"C:\ProgramData\Secure_Tech\temp\temp1\print.pdf")
            output.write(outputStream)
            outputStream.close()
            time.sleep(0.3)
            if k==1:
                try:
                    shutil.rmtree((r"C:\ProgramData\Secure_Tech\save_db"))
                except:
                    pass
                try:
                    os.mkdir(r"C:\ProgramData\Secure_Tech\save_db")
                except:
                    pass
                dst=(r"C:\ProgramData\Secure_Tech\save_db\file_original.pdf")
                copyfile(path, dst)
            elif k==2:
                try:
                    os.mkdir(r"C:\ProgramData\Secure_Tech\save_db")
                except:
                    pass
                dst=(r"C:\ProgramData\Secure_Tech\save_db\file_duplicate.pdf")
                copyfile(path, dst)
            k=k+1
        global invoice_edit_true
        try:
            print(invoice_edit_true)
        except:
            invoice_edit_true = 0
            
        if invoice_edit_true !=1:
            save_files_db()
        else:
            invoice_edit_true = 0
        return


        global quotation_edit_true
        try:
            print(quotation_edit_true)
        except:
            quotation_edit_true = 0
            
        if quotation_edit_true !=1:
            save_files_db()
        else:
            quotation_edit_true = 0
        return
    elif name == "org+dup1":
        printer_print("org+dup","org+dup")
        try:
            shutil.rmtree(r"C:\ProgramData\Secure_Tech\temp\print.pdf")
        except:
            pass
        try:
            os.mkdir(r"C:\ProgramData\Secure_Tech\temp")
        except:
            pass
        
        pdfs = [r"C:\ProgramData\Secure_Tech\save_db\file_duplicate.pdf", r"C:\ProgramData\Secure_Tech\save_db\file_duplicate.pdf", r"C:\ProgramData\Secure_Tech\save_db\file_original.pdf"]
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(r"C:\ProgramData\Secure_Tech\temp\print.pdf")
        merger.close()
        time.sleep(0.15)
        path=(r"C:\ProgramData\Secure_Tech\temp\print.pdf")
        time.sleep(0.15)
        last_try(path)

        
        
        
    elif name == "Original":
        printer_print("org+dup","org+dup")
        
        '''try:
            path=(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
            with open(path, 'rb') as file:
                file.close()
        except:
            path=(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
            with open(path, 'rb') as file:
                file.close()
        try:
             shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\temp1\print.pdf"))
        except:
            pass
                
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Times-Roman", 9)
        can.drawString(450, 800, "Original Copy")
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open(path, "rb"))
        output = PdfFileWriter()
        for i in range (existing_pdf.getNumPages()):
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            try:
                path=(r"C:\ProgramData\Secure_Tech\temp\temp1")
                os.mkdir(path)
            except:
                pass
        outputStream = open(r"C:\ProgramData\Secure_Tech\temp\temp1\print.pdf", "wb")
        output.write(outputStream)
        outputStream.close()'''
        
        path=(r"C:\ProgramData\Secure_Tech\save_db\file_original.pdf")
        time.sleep(0.2)
        last_try(path)

        time.sleep(0.2)
    elif name == "Duplicate":
        printer_print("org+dup","org+dup")
        
        '''copy_name="Duplicate"
        try:
            path=(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
            with open(path, 'rb') as file:
                file.close()
        except:
            path=(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
            with open(path, 'rb') as file:
                file.close()
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Times-Roman", 9)
        can.drawString(450, 800, "Duplicate Copy")
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open(path, "rb"))
        output = PdfFileWriter()
        for i in range (existing_pdf.getNumPages()):
            page = existing_pdf.getPage(i)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            
            try:
                path=(r"C:\ProgramData\Secure_Tech\temp\temp1")
                os.mkdir(path)
                time.sleep(0.2)
            except:
                pass
        outputStream = open(r"C:\ProgramData\Secure_Tech\temp\temp1\print.pdf", "wb")
        output.write(outputStream)
        outputStream.close()'''

        time.sleep(0.2)
        path=(r"C:\ProgramData\Secure_Tech\save_db\file_duplicate.pdf")
        last_try(path)

        time.sleep(0.2)
    elif name=="SAVE_PDF":
        printer_print("org+dup","org+dup")
        try:
            path=(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
            with open(path, 'rb') as file:
                file.close()
            webbrowser.open(r'file:///'+path)
        except:
            path=(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
            with open(path, 'rb') as file:
                file.close()
            webbrowser.open(r'file:///'+path)
            time.sleep(0.3)

    
        


        
    '''try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\print"))
    except:
        pass
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp"))
    except:
        pass'''

def gui_preview(location,type_of):
    if location!="From List PDF":
        if type_of == "invoice" or type_of == "invoice_edit":
            query="SELECT ID from INVOICE"
            results=conn.execute(query)
            if type_of != "invoice_edit":
                for i in results:
                    if str(invoice_num) == str(i[0]):
                        error("Already This Invoice ID is Used!")
                        return


                    
        elif type_of == "quotation":
            query="SELECT ID from QUOTATION"
            results=conn.execute(query)
            for i in results:
                if str(invoice_num) == str(i[0]):
                    error("Already This Quotation ID is Used!")
                    return
    global invoice_edit_true
    if type_of == "invoice_edit":
        invoice_edit_true = 1
    global quotation_edit_true
    if type_of == "quotation_edit":
        quotation_edit_true = 1
    

            
    #top.destroy()     
    top_preview = tk.Toplevel()
    top_preview.geometry(str(w) + 'x' + str(h))
    top_preview.state('zoomed')   
    fpreview= tk.Frame(top_preview, bg = "gray99", height=h, width=(w/2.9))
    fpreview.pack(side=RIGHT)
    fpreview1= tk.Frame(top_preview, bg = "white", height=h, width=(w/10))
    fpreview1.pack(side=LEFT)
    #ecopies=tk.Entry(fpreview, width=13,bg="gray93", font=("Arial", 15 ))
    #ecopies.place(x=int(w/8),y=int(h/3.8))
    #ecopies.insert(0,'1')
                     
    bprint_od=tk.Button(fpreview,text="PRINT(3)",width=18, font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                          command=lambda: printer_print("org+dup","org+dup1"), relief=FLAT)
    bprint_od.place(x=int(w/8),y=int(h/3.2))
    
    bprint_o=tk.Button(fpreview,text="PRINT ORIGINAL",width=18, font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                          command=lambda: printer_print(1,"Original"), relief=FLAT)
    bprint_o.place(x=int(w/8),y=int(h/2.3))

    bprint_d=tk.Button(fpreview,text="PRINT DUPLICATE",width=18, font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                          command=lambda: printer_print(1,"Duplicate"), relief=FLAT)
    bprint_d.place(x=int(w/8),y=int(h/2.7))

    bsave_pdf=tk.Button(fpreview,text="SAVE PDF",width=18,font=("Arial",10,"bold"),bg="dodger blue",fg="white",relief=FLAT,
                        command=lambda: printer_print(1,"SAVE_PDF"))
    bsave_pdf.place(x=int(w/8),y=int(h/2))


    if location=="From List PDF":
        bprint_od.destroy()
        bprint_o.config(command=lambda: print_from_list(1,"Original"))
        bprint_d.config(command=lambda: print_from_list(1,"Duplicate"))
        bsave_pdf.config(command=lambda: print_from_list(1,"SAVE_PDF"))
        bsave_pdf.place(x=int(w/8),y=int(h/2))

    
    path=(r"C:\ProgramData\Secure_Tech\temp\img")
    canvas = Canvas(top_preview, bg="white", width=(w/1.6), height=h)
    canvas.pack(side=LEFT)
    #img = ImageTk.PhotoImage(Image.open(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg"))
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\com_img"))
    except:
        pass
    path=(r"C:\ProgramData\Secure_Tech\temp\com_img")
    os.mkdir(path)


    files = next(os.walk(r"C:\ProgramData\Secure_Tech\temp\img"))
    file_count=len(files[2])


    if file_count ==1:
        path=r"C:\ProgramData\Secure_Tech\temp\img\outfile.jpg"
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\img\outfile.jpg")
        img = img.resize((740, 1050), Image.ANTIALIAS)
    elif file_count ==2:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        vis = np.concatenate((img1, img2), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 2050), Image.ANTIALIAS)
    elif file_count ==3:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        vis = np.concatenate((img1, img2,img3), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 3150), Image.ANTIALIAS)
    elif file_count ==4:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        vis = np.concatenate((img1, img2,img3,img4), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 4150), Image.ANTIALIAS)
    elif file_count ==5:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 5250), Image.ANTIALIAS)
    elif file_count ==6:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        img6 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile6.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5,img6), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 6250), Image.ANTIALIAS)
    elif file_count ==7:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        img6 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile6.jpg")
        img7 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile7.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5,img6,img7), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 7350), Image.ANTIALIAS)
    elif file_count ==8:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        img6 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile6.jpg")
        img7 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile7.jpg")
        img8 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile8.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5,img6,img7,img8), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 7350), Image.ANTIALIAS)

    elif file_count ==9:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        img6 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile6.jpg")
        img7 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile7.jpg")
        img8 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile8.jpg")
        img9 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile9.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5,img6,img7,img8,img9), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 9450), Image.ANTIALIAS)
    elif file_count ==10:
        img1 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile1.jpg")
        img2 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile2.jpg")
        img3 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile3.jpg")
        img4 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile4.jpg")
        img5 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile5.jpg")
        img6 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile6.jpg")
        img7 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile7.jpg")
        img8 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile8.jpg")
        img9 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile9.jpg")
        img10 = cv2.imread(r"C:\ProgramData\Secure_Tech\temp\img\outfile10.jpg")
        vis = np.concatenate((img1, img2,img3,img4,img5,img6,img7,img8,img9,img10), axis=0)
        cv2.imwrite((r"C:\ProgramData\Secure_Tech\temp\com_img\out.png"), vis)
        img = Image.open(r"C:\ProgramData\Secure_Tech\temp\com_img\out.png")
        img = img.resize((740, 10550), Image.ANTIALIAS)
    
    
    #img = img._PhotoImage__photo.zoom(1,1)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(2, 2, anchor=tk.NW, image=img)
    vsb = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    vsb.place(x=740,y=1,width=16, height = (h/1.01))
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    
    if type_of == "invoice" or type_of == "invoice_edit":
        pass
    elif type_of == "quotation" or type_of == "quotation_edit":
        bprint_od.destroy()
        bprint_od=tk.Button(fpreview,text="PRINT & SAVES",width=18, font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                          command=lambda: printer_print_q(int(1)), relief=FLAT)
        bprint_od.place(x=int(w/8),y=int(h/2.7))
        bsave_pdf.place(x=int(w/8),y=int(h/2.2))
        bprint_o.destroy()
        bprint_d.destroy()
    mainloop()
    canvas.mainloop()
    
    '''
    C = Canvas(top_preview, bg="white", height=h, width=4)
    line = C.create_line(4,4,4,h,fill='black',width=1)
    C.place(x=int(w/7),y=int(h-h))'''
    
################################################################## Functional Work for PDF creation #####################################################################
def create_pdf(tree,einvoice_num,type_of):
    #top.destroy()
    global equotation_num
    global string_to_db
    list_to_db = []
    for i in tree.get_children():
        list_to_db+=tree.item(i)['values']
    string_to_db = ','.join(str(e) for e in list_to_db)
    print(string_to_db)
    global type_of_pdf
    type_of_pdf=type_of
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp"))
    except:
        pass
    global invoice_num
    global mobile_to_db

    if type_of == "invoice_edit":
        invoice_num=einvoice_num.get()
        global ecustomer2_ie
        global eaddress_ie
        global egst_ie
        global emobile_ie
        global eproduct_ie
        global eunit_price_ie
        global etax_ie
        global ehsn_ie
        global cal_new_invoice_ie
        global enote_ie
        mobile_to_db=emobile_ie.get()

    elif type_of == "quotation_edit":
        invoice_num=einvoice_num.get()
        global ecustomer2_qe
        global eaddress_qe
        global egst_qe
        global emobile_qe
        global eproduct_qe
        global eunit_price_qe
        global etax_qe
        global ehsn_qe
        global cal_new_quotation_qe
        global enote_qe
        mobile_to_db=emobile_qe.get()
    elif type_of == "invoice":
        invoice_num=einvoice_num.get()
        global ecustomer2
        global eaddress
        global egst
        global emobile
        global cal_new_invoice
        global enote
        mobile_to_db=emobile.get()
    elif type_of == "quotation":
        
        invoice_num=equotation_num.get()
        global ecustomer3
        global eaddress_q
        global egst_q
        global emobile_q
        global eproduct_q
        global cal_new_quotation
        global enote_q
        mobile_to_db=emobile_q.get()

    
    global name
    global address
    global gst_no
    global tax
    global date
    
    tax=12

    if type_of == "invoice_edit":
        name=ecustomer2_ie.get()
        address=eaddress_ie.get()
        gst_no=egst_ie.get()
        mobile_no=emobile_ie.get()
        date=cal_new_invoice_ie.get()
        note=enote_ie.get("1.0",'end-1c')
    if type_of == "quotation_edit":
        name=ecustomer2_qe.get()
        address=eaddress_qe.get()
        gst_no=egst_qe.get()
        mobile_no=emobile_qe.get()
        date=cal_new_quotation_qe.get()
        note=enote_qe.get("1.0",'end-1c')
    if type_of == "invoice":
        name=ecustomer2.get()
        address=eaddress.get()
        gst_no=egst.get()
        mobile_no=emobile.get()
        date=cal_new_invoice.get()
        note=enote.get("1.0",'end-1c')
    elif type_of == "quotation":
        name=ecustomer3.get()
        address=eaddress_q.get()
        gst_no=egst_q.get()
        mobile_no=emobile_q.get()
        date=cal_new_quotation.get()
        note=enote_q.get("1.0",'end-1c')


        
    address=address.replace(",","")
    sn_no=""
    p_name=""
    p_qty=""
    p_hsn=""
    p_price=""
    j=1
    items_list=[]
    sub_total=0.00
    gst=0
    d="""SELECT TAX FROM COMPANY"""
    e=conn.execute(d)
    for i in e:
        gst=i[0]
    temp_name=""
    if len(tree.get_children()) <= 20:
        for i in tree.get_children():
            items=tree.item(i)['values']
            if (items[5]) !="":
                sub_total=sub_total+int((items[5]))
            if sn_no =="":
                sn_no=str(j)
                p_name=(items[1])
                p_hsn=str((items[2]))
                p_qty=str((items[3]))
                p_price=str((items[5]))
                
            else:
                if (items[5]) !="":
                    j=j+1
                    sn_no=str(sn_no)+"\n"+str(j)

                else:   
                    sn_no=str(sn_no)+"\n"
                p_name=p_name+"\n"+(items[1])
                p_hsn=p_hsn+"\n"+str((items[2]))
                p_qty=p_qty+"\n"+str((items[3]))
                p_price=p_price+"\n"+str((items[5]))
            items_list.append(items)
        gst_cost=((gst*sub_total)/100)
        
        if (len(items_list)) ==1:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==2:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==3:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==4:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==5:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==6:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==7:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==8:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==9:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==10:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==11:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==12:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==13:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==14:
            sn_no=sn_no+"\n\n\n\n\n\n\n\n"
        elif (len(items_list)) ==15:
            sn_no=sn_no+"\n\n\n\n\n\n\n"
        elif (len(items_list)) ==16:
            sn_no=sn_no+"\n\n\n\n\n\n"
        elif (len(items_list)) ==17:
            sn_no=sn_no+"\n\n\n\n\n"
        elif (len(items_list)) ==18:
            sn_no=sn_no+"\n\n\n\n"
        elif (len(items_list)) ==19:
            sn_no=sn_no+"\n\n\n"
        elif (len(items_list)) ==20:
            sn_no=sn_no+"\n\n"



        try:
            shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp"))
        except:
            pass
        try:
            path= (r"C:\ProgramData\Secure_Tech\temp")
            os.mkdir(path)
        except:
            pass
        d="""SELECT GST, NOTES, PHONE FROM COMPANY"""
        e=conn.execute(d)
        gst_num=""
        notes_com=""
        phone_com=""
        for i in e:
            gst_num=i[0]
            notes_com=i[1]
            phone_com=i[2]

        c = canvas.Canvas(r"C:\ProgramData\Secure_Tech\temp\hello.pdf")
        PartnerLogo=("12.jpg")
        c.drawImage(PartnerLogo,37, 175, width=320, preserveAspectRatio=True, mask='auto')


        pdfmetrics.registerFont(TTFont('arial-black', 'arial-black.ttf'))
        pdfmetrics.registerFont(TTFont('arial', 'ArialUnicodeMS.ttf'))
        pdfmetrics.registerFont(TTFont('arial-bold', 'arial-bold.ttf'))
        pdfmetrics.registerFont(TTFont('arial-italic', 'arial-italic.ttf'))
        
       

        c.setFont("arial", 11)
        c.drawString(235,800,"Vetri! Guruve Thunai!")
        c.setFont("arial-black", 16)
        if type_of == "invoice" or type_of == "invoice_edit":
            c.drawString(420,720,"GST Invoice")
        elif type_of == "quotation" or type_of == "quotation_edit":
            c.drawString(420,720,"Quotation")
        c.setFont("arial-bold", 12)
        c.drawString(420,680,"Date : "+date) #420,700, 
        if type_of == "invoice" or type_of == "invoice_edit":
            c.drawString(420,700,"Invoice No : "+invoice_num[6:])
        elif type_of == "quotation" or type_of == "quotation_edit":
            c.drawString(420,700,"Quotation No : "+ invoice_num)

            
        c.setFont("arial-bold", 11)
        c.drawString(50,620,"Party's Name :-")
        c.setFont("arial-black", 12)
        c.drawString(50,597,name)
        c.drawString(50,574,address)
        c.drawString(50,550,("GST No :"+str(gst_no)))
        styles = getSampleStyleSheet()
        n=1
        total_to_words=int(sub_total+gst_cost)
        rs_in_words= num2words(total_to_words, lang='en_IN')
        rs_in_words = rs_in_words.replace("-", " ")
        rs_in_words = rs_in_words.replace (",", "")
        rs_in_words= rs_in_words.title()
        
        #notes_com.splitlines()[0]
        data=[("S.NO","                            Description                         ","Quantity","HSN","  Amount "),
            (str(sn_no),p_name,p_qty,p_hsn,p_price),
            (notes_com.splitlines()[0],"","","SUB TOTAL",str(sub_total)+"0"),
            (notes_com.splitlines()[1],"","","SGST "+str(gst/2)+"%",str(gst_cost/2)+'0'),
            (notes_com.splitlines()[2],"","","CGST "+str(gst/2)+"%",str(gst_cost/2)+'0'),
            (notes_com.splitlines()[3],"","","TOTAL","Rs. "+str(int(sub_total+gst_cost))+".00"),
            ("Rupees in Words: "+rs_in_words+" Only","",""),
            ("","","\nFor Sri Arulambikai Engineering Works\n\n\n","",""),
            ("Receiver Signature","","Authorised Signatory","","")]


        

        
        if len("Rs. "+str(int(sub_total+gst_cost))+".00") > 12:
            style= TableStyle([
                 ('FONTNAME',(0,0),(-1,-3),"arial-bold"),
                 ('FONTNAME',(0,-2),(-1,-1),"arial"),
                 ('FONTNAME',(0,2),(0,2),"arial-italic"),
                 ('FONTNAME',(0,3),(2,5),"arial"),
                 #('GRID',(0,0),(-1,-1),0.5,colors.black),
                 ('SPAN',(0,-1),(1,-1)),
                 ('SPAN',(0,6),(-1,6)),
                 ('SPAN',(2,7),(4,7)),
                 ('SPAN',(2,8),(4,8)),
                 ('SPAN',(0,5),(2,5)),
                 ('SPAN',(0,2),(2,2)),
                 ('SPAN',(0,3),(2,3)),
                 ('SPAN',(0,4),(2,4)),
                 ('LINEABOVE',(0,0),(-1,0),1,colors.black),
                 ('LINEABOVE',(0,2),(-1,2),1,colors.black),
                 ('LINEABOVE',(0,7),(-1,7),1,colors.black),
                 ('LINEABOVE',(0,6),(-1,6),1,colors.black),
                 ('LINEABOVE',(3,5),(-1,5),1,colors.black),
                 ('LINEABOVE',(3,4),(-1,4),1,colors.black),
                 ('LINEABOVE',(3,3),(-1,3),1,colors.black),
                 ('LINEBEFORE',(0,0),(0,6),1,colors.black),
                 ('LINEAFTER',(4,0),(4,6),1,colors.black),
                 ('LINEABOVE',(0,1),(-1,1),1,colors.black),
                 ('LINEBEFORE',(1,0),(1,1),1,colors.black),
                 ('LINEBEFORE',(2,0),(2,1),1,colors.black),
                 ('LINEBEFORE',(3,0),(3,5),1,colors.black),
                 ('LINEBEFORE',(4,0),(4,5),1,colors.black),
                 ('ALIGN',(4,2),(4,5),'RIGHT'),
                 ('ALIGN',(0,1),(-1,1),'CENTER'),
                 ('ALIGN',(2,2),(-1,2),'RIGHT'),
                 ('ALIGN',(0,0),(-1,0),'CENTER'),
                 ('ALIGN',(-3,-1),(-1,-1),'RIGHT'),
                 ('ALIGN',(0,1),(0,1),'CENTER'),
                 ('ALIGN',(1,1),(1,1),'LEFT'),
                 ('ALIGN',(3,2),(3,2),'LEFT'),
                 ('ALIGN',(4,1),(-1,1),'RIGHT'),             
                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                 ('FONTSIZE',(0,0),(-1,-1),11),
                 ('FONTSIZE',(4,2),(4,5),10),
                 ('BOTTOMPADDING', (0,0), (-1,0), 9)])
        else:
            style= TableStyle([
                 ('FONTNAME',(0,0),(-1,-3),"arial-bold"),
                 ('FONTNAME',(0,-2),(-1,-1),"arial"),
                 ('FONTNAME',(0,2),(0,2),"arial-italic"),
                 ('FONTNAME',(0,3),(2,5),"arial"),
                 #('GRID',(0,0),(-1,-1),0.5,colors.black),
                 ('SPAN',(0,-1),(1,-1)),
                 ('SPAN',(0,6),(-1,6)),
                 ('SPAN',(2,7),(4,7)),
                 ('SPAN',(2,8),(4,8)),
                 ('SPAN',(0,5),(2,5)),
                 ('SPAN',(0,2),(2,2)),
                 ('SPAN',(0,3),(2,3)),
                 ('SPAN',(0,4),(2,4)),
                 ('LINEABOVE',(0,0),(-1,0),1,colors.black),
                 ('LINEABOVE',(0,2),(-1,2),1,colors.black),
                 ('LINEABOVE',(0,7),(-1,7),1,colors.black),
                 ('LINEABOVE',(0,6),(-1,6),1,colors.black),
                 ('LINEABOVE',(3,5),(-1,5),1,colors.black),
                 ('LINEABOVE',(3,4),(-1,4),1,colors.black),
                 ('LINEABOVE',(3,3),(-1,3),1,colors.black),
                 ('LINEBEFORE',(0,0),(0,6),1,colors.black),
                 ('LINEAFTER',(4,0),(4,6),1,colors.black),
                 ('LINEABOVE',(0,1),(-1,1),1,colors.black),
                 ('LINEBEFORE',(1,0),(1,1),1,colors.black),
                 ('LINEBEFORE',(2,0),(2,1),1,colors.black),
                 ('LINEBEFORE',(3,0),(3,5),1,colors.black),
                 ('LINEBEFORE',(4,0),(4,5),1,colors.black),
                 ('ALIGN',(4,2),(4,5),'RIGHT'),
                 ('ALIGN',(0,1),(-1,1),'CENTER'),
                 ('ALIGN',(2,2),(-1,2),'RIGHT'),
                 ('ALIGN',(0,0),(-1,0),'CENTER'),
                 ('ALIGN',(-3,-1),(-1,-1),'RIGHT'),
                 ('ALIGN',(0,1),(0,1),'CENTER'),
                 ('ALIGN',(1,1),(1,1),'LEFT'),
                 ('ALIGN',(3,2),(3,2),'LEFT'),
                 ('ALIGN',(4,1),(-1,1),'RIGHT'),             
                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                 ('FONTSIZE',(0,0),(-1,-1),11),
                 ('BOTTOMPADDING', (0,0), (-1,0), 9)])   
            

        width = 10
        height = 200
        x = 50
        y = 50
        f = Table(data)
        f.setStyle(style)
        f.wrapOn(c, 1, 1)
        f.drawOn(c, x, y)
        c.showPage()
        c.save()
        

    else:
        listf=[]
        for i in tree.get_children():
            items=tree.item(i)['values']
            listf.append(items)
        list_length=len(listf)
        
        if list_length%20 == 0:
            piece=list_length//20
        else:
            piece=(list_length//20)+1

        list2=[]
        list_temp=[]
        list_compare=[]
        for i in listf:
            list_temp.append(i)
            if len(list_temp)==20:
                list2.append(list_temp)
                list_temp=[]
            else:
                pass
            
        for i in list2:
            for j in i:
                list_compare.append(j)

        #list_missing=set(listf).difference(list_compare)
        for i in list_compare:
            index = listf.index(i)
            listf.pop(index)
        list_missing=listf
        list_temp=[]
        for i in list_missing:
            list_temp.append(i)
        if list_temp != []:
            list2.append(list_temp)
        else:
            pass
        #print(list2)
        page_no=0
        j=1
        for list_20 in list2:
            page_no=page_no+1
            items=[]
            sn_no=""
            p_name=""
            p_hsn=""
            p_qty=""
            p_price=""
            for each_list in list_20:
                items = each_list
                if (items[5]) !="":
                    sub_total=sub_total+int((items[5]))
                if sn_no =="":
                    if (j%20)==0:
                        if (items[5]) !="":
                            j=j+1
                            sn_no=str(sn_no)+str(j)
                        else:
                            sn_no=str(sn_no)+"\n"
                            
                    else:
                        sn_no=str(j)
                    p_name=(items[1])
                    p_hsn=str((items[2]))
                    p_qty=str((items[3]))
                    p_price=str((items[5]))
                else:
                    if (items[5]) !="":
                        j=j+1
                        sn_no=str(sn_no)+"\n"+str(j)
                    else:
                        sn_no=str(sn_no)+"\n"
                    p_name=p_name+"\n"+(items[1])
                    p_hsn=p_hsn+"\n"+str((items[2]))
                    p_qty=p_qty+"\n"+str((items[3]))
                    p_price=p_price+"\n"+str((items[5]))
                items_list.append(items)
            gst_cost=((gst*sub_total)/100)
            if (len(list_20)) ==1:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==2:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==3:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==4:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==5:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==6:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==7:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==8:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==9:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==10:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==11:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==12:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==13:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==14:
                sn_no=sn_no+"\n\n\n\n\n\n\n\n"
            elif (len(list_20)) ==15:
                sn_no=sn_no+"\n\n\n\n\n\n\n"
            elif (len(list_20)) ==16:
                sn_no=sn_no+"\n\n\n\n\n\n"
            elif (len(list_20)) ==17:
                sn_no=sn_no+"\n\n\n\n\n"
            elif (len(list_20)) ==18:
                sn_no=sn_no+"\n\n\n\n"
            elif (len(list_20)) ==19:
                sn_no=sn_no+"\n\n\n"
            elif (len(list_20)) ==20:
                sn_no=sn_no+"\n\n"

            try:
                shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\com_img"))
            except:
                pass
            try:
                path= (r"C:\ProgramData\Secure_Tech\temp")
                os.mkdir(path)
            except:
                pass
            
            d="""SELECT GST, NOTES, PHONE FROM COMPANY"""
            e=conn.execute(d)
            gst_num=""
            notes_com=""
            phone_com=""
            for i in e:
                gst_num=i[0]
                notes_com=i[1]
                phone_com=i[2]
            

            c = canvas.Canvas(r"C:\ProgramData\Secure_Tech\temp\hello"+str(page_no)+".pdf")
            PartnerLogo=("12.jpg")
            c.drawImage(PartnerLogo,30, 150, width=300, preserveAspectRatio=True, mask='auto')


            pdfmetrics.registerFont(TTFont('arial-black', 'arial-black.ttf'))
            pdfmetrics.registerFont(TTFont('arial', 'ArialUnicodeMS.ttf'))
            
            now = datetime.datetime.now()
            this_year=str(now.year)[:2]
            next_year=int(this_year)+1  
            c.setFont("Times-Roman", 14)
            c.drawString(225,800,"Vertri! Guruvai Thunai!")
            c.setFont("Times-Bold", 17)
            if type_of == "invoice" or type_of == "invoice_edit":
                c.drawString(420,720,"GST INVOICE")
            elif type_of == "quotation" or type_of == "quotation_edit":
                c.drawString(420,720,"GST QUOTATION")
            c.setFont("Times-Roman", 14)
            c.drawString(420,700,"DATE : "+date)
            if type_of == "invoice" or type_of == "invoice_edit":
                c.drawString(420,680,"Invoice No : "+ invoice_num+" ("+str(this_year)+"/"+str(next_year)+")")
            elif type_of == "quotation" or type_of == "quotation_edit":
                c.drawString(420,680,"Quotation No : "+ invoice_num)
                
            c.setFont("arial-black", 12)
            c.drawString(50,660,"GST: "+gst_num)
            c.setFont("arial", 13)
            c.drawString(50,640,"Cell: "+mobile_no+", Phone: "+phone_com)
            c.setFont("arial-black", 12)
            c.drawString(50,600,"Party's Name    :")
            c.setFont("arial", 12)
            c.drawString(170,600,name)
            c.drawString(50,570,"Address                  : "+address)
            c.setFont("arial-black", 12)
            c.drawString(50,540,str("GST NO             : "+str(gst_no)))

            res123 = p_name.split(" ")
            temp_name=""
            o=1
            for i in res123:
                if o%7==0:
                    temp_name=temp_name+" \n "+str(i)
                else:
                    temp_name=temp_name+" "+str(i)
                o=o+1
            
            n=1
            data=[("S.NO","                            Description                         ","Quantity","  HSN   ","   Amount  "),
                (str(sn_no),temp_name,p_qty,p_hsn,p_price),
                (notes_com,"",
                     "Sub Total \nSGST "+str(gst/2)+"%\nCGST "+str(gst/2)+"%\n\nTotal ","",str(sub_total)+"\n"+str(gst_cost/2)+"\n"+str(gst_cost/2)+"\n\n"+"Rs.   "+str(int(sub_total+gst_cost))+".00"),
                ("Rupees in words: "+str(num2word.word(int(sub_total+gst_cost)))+" Only","","",""),
                ("","","\nFor Sri Arulambikai Engineering Works\n\n\n","",""),
                ("Receiver Signature","","Authorised Signatory","","")]


            
            style= TableStyle([
                 ('FONTNAME',(0,0),(-1,0),"arial"),
                 #('GRID',(0,0),(-1,-1),0.5,colors.black),
                 ('SPAN',(2,4),(4,4)),
                 ('SPAN',(2,5),(4,5)),
                 ('SPAN',(0,3),(4,3)),
                 ('SPAN',(2,2),(3,2)),
                 ('SPAN',(0,2),(1,2)),
                 ('SPAN',(0,-1),(1,-1)),
                 ('LINEABOVE',(0,0),(-1,0),1,colors.black),
                 ('LINEBEFORE',(0,0),(0,3),1,colors.black),
                 ('LINEBELOW',(0,3),(4,3),1,colors.black),
                 ('LINEAFTER',(4,0),(4,3),1,colors.black),
                 ('LINEABOVE',(0,1),(-1,1),1,colors.black),
                 ('LINEABOVE',(0,2),(-1,2),1,colors.black),
                 ('LINEABOVE',(0,3),(-1,3),1,colors.black),
                 ('LINEBEFORE',(1,0),(1,2),1,colors.black),
                 ('LINEBEFORE',(2,0),(2,3),1,colors.black),
                 ('LINEBEFORE',(3,0),(3,2),1,colors.black),
                 ('LINEBEFORE',(4,0),(4,3),1,colors.black),
                 ('ALIGN',(2,4),(2,5),'RIGHT'),
                 ('ALIGN',(0,1),(-1,1),'CENTER'),
                 ('ALIGN',(2,2),(-1,2),'RIGHT'),
                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                 ('FONTSIZE',(0,0),(-1,0),13),
                 ('BOTTOMPADDING', (0,0), (-1,0), 9)])


            width = 200
            height = 200
            x = 50
            y = 50
            f = Table(data)
            f.setStyle(style)
            f.wrapOn(c, width, height)
            f.drawOn(c, x, y)
            c.showPage()
            try:
                os.mkdir(r"C:\ProgramData\Secure_Tech\temp")
            except:
                pass
            c.save()
        
    items_listx=[]
    for i in items_list:
        items_listx.append(tuple(i))
    items_listx=tuple(items_listx)

    list_20=[]
    items_list=[]
    list2=[]
    list_temp=[]
    list_compare=[]
    sn_no=""
    p_name=""
    p_hsn=""
    p_qty=""
    p_price=""
    listf=[]
    files = next(os.walk(r"C:\ProgramData\Secure_Tech\temp"))
    file_count = len(files[2])
    try:
        shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\img"))
    except:
        pass
    if file_count == 1:
        path= (r"C:\ProgramData\Secure_Tech\temp\img")
        os.mkdir(path)
        pdffile = r"C:\ProgramData\Secure_Tech\temp\hello.pdf"
        doc = fitz.open(pdffile)
        page = doc.loadPage(0)  # number of page
        pix = page.getPixmap()
        output = r"C:\ProgramData\Secure_Tech\temp\img\outfile.jpg"
        zoom = 2    # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        pix = page.getPixmap(matrix = mat)
        pix.writePNG(output)
        doc.close()
    elif file_count >> 1:
        try:
            os.remove((r"C:\ProgramData\Secure_Tech\temp\hello.pdf"))
        except:
            pass
        file_count = len(files[2])
        if (files[2])[0] == "hello.pdf":
            file_count=file_count-1
        else:
            pass
        path= (r"C:\ProgramData\Secure_Tech\temp\img")
        os.mkdir(path)
        merger = PdfFileMerger()
        for ijk in range (1,file_count+1):
            pdffile = str(r"C:\ProgramData\Secure_Tech\temp\hello"+str(ijk)+".pdf")
            doc = fitz.open(pdffile)
            page = doc.loadPage(0)  # number of page
            pix = page.getPixmap()
            output = str(r"C:\ProgramData\Secure_Tech\temp\img\outfile"+str(ijk)+".jpg")
            zoom = 2    # zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix = mat)
            pix.writePNG(output)
            filename=(r"C:\ProgramData\Secure_Tech\temp\hello"+str(ijk)+".pdf")
            merger.append(PdfFileReader(open(filename, 'rb')))
        doc.close()
        try:
            shutil.rmtree((r"C:\ProgramData\Secure_Tech\temp\print"))
        except:
            pass

        path= (r"C:\ProgramData\Secure_Tech\temp\img\print")
        os.mkdir(path)
        merger.write(r"C:\ProgramData\Secure_Tech\temp\img\print\print-output.pdf")
        global top1
    
    #for i in tree.get_children():
        #tree.delete(i)
    global x_new_invoice_add
    x_new_invoice_add=+1
    try:
        #top1.destroy()
        pass
    except:
        pass
    gui_preview("From create PDF",type_of)

    
def preview():
    pass


################################################################## Functional Work For New Quotation ###############################################################

def new_quotation_clear(tree):
    try:
        curItem = tree.focus()
        tree.delete(curItem)
    except:
        pass
def new_quotation_add(tree,product_name,hsn,qty,tax,unit_price):
    global x_new_quotation_add
    res123 = product_name.split(" ")
    temp_name=""
    o=1
    for i in res123:
        if o%7==0:
            temp_name=temp_name+" \n "+str(i)
        else:
            temp_name=temp_name+" "+str(i)
        o=o+1
    kk=1
    q=0
    for x in tree.get_children():
        q=q+1
    if (len((temp_name.split('\n')))+q)>=20:
        error("Lines are exceeded the limit")
        return 
    
    for i in(temp_name.split('\n')):
        if kk==1:
            tree.insert("",index='end',  values=(str(x_new_quotation_add), str(i), str(hsn),str(qty),str(tax),str(int(unit_price))))
            kk=kk+1
        else:
            tree.insert("",index='end',  values=("", str(i), "","","",""))
    x_new_quotation_add=x_new_quotation_add+1
def CurSelet_product_q(event):
    selected_product_q=listbox1_q.get(listbox1_q.curselection())
    listbox1_q.delete(0,tk.END)
    listbox1_q.destroy()
    d="""SELECT * FROM PRODUCT where NAME = ?"""
    e=conn.execute(d, (selected_product_q,))
    for i in e:
        name_product= i[1]
        price_product=i[2]
        hsn_product=i[3]
        tax_product=i[4]
    
    global eproduct_q
    global eunit_price_q
    global etax_q
    global ehsn_q
    try:
        eproduct_q.delete(0,END)
        eunit_price_q.delete(0,END)
        etax_q.delete(0,END)
        ehsn_q.delete(0,END)
    except:
        pass
    eproduct_q.insert(0,name_product)
    eunit_price_q.insert(0,price_product)
    ehsn_q.insert(0,hsn_product)
    etax_q.insert(0,tax_product)
def new_quotation_check_product(event):
    product_q=eproduct_q.get()
    if len(product_q)>>1:
        global listbox1_q
        try:
            listbox1_q.delete(0,tk.END)
            listbox1_q.destroy()
        except:
            pass
        l=1
        statement1_q=("SELECT * FROM PRODUCT WHERE NAME LIKE" +' \''+product_q+'%\'')
        check=conn.execute(statement1_q)
        listbox1_q=tk.Listbox(fnew_quotation,width =20, font=("Arial", 15 ), bg= "gray93")  
        listbox1_q.place(x=int(w/9.8),y=int(h/3.22))
        for i in check:
            n=i[1]
            listbox1_q.insert(l, n)
            l=l+1
        listbox1_q.bind('<<ListboxSelect>>',CurSelet_product_q)
        fnew_quotation.bind("<Button-1>",leftclick_product)


def CurSelet_q(event):
    global listbox_q
    try:
        selected_name_q=listbox_q.get(listbox_q.curselection())
    except:
        listbox_q.destroy()
        selected_name_q=""
    try:
        listbox_q.delete(0,tk.END)
        listbox_q.destroy()
    except:
        pass
    b="""SELECT * FROM CUSTOMER where NAME = ?"""
    c=conn.execute(b, (selected_name_q,))
    #b="SELECT * FROM CUSTOMER where NAME="+str(selected_name)
    for i in c:
        name=i[1]
        address=i[2]
        gst=i[3]
        mobile=i[4]
        email=[5]
    
    global ecustomer3
    global eaddress_q
    global egst_q
    global emobile_q
    try:
        ecustomer3.delete(0,END)
        eaddress_q.delete(0,END)
        egst_q.delete(0,END)
        emobile_q.delete(0,END)
        eemail.delete(0,END)
    except:
        pass

    ecustomer3.insert(0,name)
    eaddress_q.insert(0,address)
    egst_q.insert(0,gst)
    emobile_q.insert(0,mobile)
    try:
        listbox_q.delete(0,tk.END)
        listbox_q.destroy()
    except:
        pass    
    
def new_quotation_check_name(event):
    global ecustomer3
    global fnew_quotation
    name_q=ecustomer3.get()
    
    if len(name_q)>>1:
        global listbox_q
        try:
            listbox_q.delete(0,tk.END)
            listbox_q.destroy()
        except:
            pass
        l=1
        statement=("SELECT * FROM CUSTOMER WHERE NAME LIKE" +' \''+name_q+'%\'')
        check=conn.execute(statement)
        listbox_q=tk.Listbox(fnew_quotation,width =25, font=("Arial", 15 ), bg= "gray93")
        listbox_q.place(x=int(w/5.3),y=int(h/12))
        for i in check:
            n=i[1]
            listbox_q.insert(l, n)
            l=l+1
        listbox_q.bind('<<ListboxSelect>>',CurSelet_q)
        fnew_quotation.bind("<Button-1>",leftclick)

        
    else:
        pass


    
    

################################################################## Functional Work For New Invoice ###############################################################
def new_invoice_clear(tree):
    try:
        curItem = tree.focus()
        tree.delete(curItem)
    except:
        pass
def new_invoice_add(tree,p_name,hsn,qty,tax,p_price,eproduct_e,eqty_e,etax_e,eunit_price_e,ehsn_e):
    global x_new_invoice_add
    if p_name =="":
        error("Check All Fields!")
        return
    elif hsn =="":
        error("Check All Fields!")
        return
    elif qty =="":
        error("Check All Fields!")
        return
    elif tax =="":
        error("Check All Fields!")
        return
    elif p_price =="":
        error("Check All Fields!")
        return
    try:
        int(tax)
        int(p_price)
    except:
        error("Check All Fields!")
        return
    if str(p_name.find(',',1)) != "-1":
        error("Product Name Should Not Contain Comma(,)!")
        return

    res123 = p_name.split(" ")
    temp_name=""
    o=1
    for i in res123:
        if o%6==0:
            temp_name=temp_name+" \n "+str(i)
        else:
            temp_name=temp_name+" "+str(i)
        o=o+1
    kk=1
    

    q=0
    for x in tree.get_children():
        q=q+1
    if (len((temp_name.split('\n')))+q)>=20:
        error("Lines are exceeded the limit")
        return 
    global last_tree_number_invoice_edit
    global invoice_edit_id
    global quotation_edit_id
    
    try:
        try:
            if invoice_edit_id==1:
                x_new_invoice_add=int(last_tree_number_invoice_edit)+1
                invoice_edit_id=0
        except:
            x_new_invoice_add=1
        try:
            if quotation_edit_id ==1 :
                x_new_invoice_add=int(last_tree_number_invoice_edit)+1
                quotation_edit_id=0
        except:
            pass
    except:
        pass
    for i in(temp_name.split('\n')):
        if kk==1:
            tree.insert("",index='end',  values=(str(x_new_invoice_add), str(i), str(hsn),str(qty),str(tax),str(int(p_price))))
            kk=kk+1
        else:
            tree.insert("",index='end',  values=("", str(i), "","","",""))
    x_new_invoice_add=x_new_invoice_add+1

    
    query="SELECT NAME from PRODUCT"
    results=conn.execute(query)
    for i in results:
        if p_name ==str(i[0]):
                eproduct_e.delete(0, 'end')
                eqty_e.delete(0, 'end')
                eunit_price_e.delete(0, 'end')
                etax_e.delete(0, 'end')
                try:
                    query="SELECT TAX from COMPANY"
                    results=conn.execute(query)
                    for i in results:
                        etax_e.insert(0,str(i[0]))
                except:
                    pass
                etax_e.insert(0,"")
                return
    
        
    conn.execute("INSERT INTO PRODUCT (NAME,PRICE,HSN,TAX) \
                    VALUES ( ?,?,?,? )",(p_name,p_price,hsn,tax))
    conn.commit()

    
    eproduct_e.delete(0, 'end')
    eqty_e.delete(0, 'end')
    eunit_price_e.delete(0, 'end')
    etax_e.delete(0, 'end')
    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            etax_e.insert(0,str(i[0]))
    except:
        pass
    etax_e.insert(0,"")
    

    
    
def CurSelet_product(event):
    selected_product=listbox1.get(listbox1.curselection())
    listbox1.delete(0,tk.END)
    listbox1.destroy()
    d="""SELECT * FROM PRODUCT where NAME = ?"""
    e=conn.execute(d, (selected_product,))
    for i in e:
        name_product= i[1]
        price_product=i[2]
        hsn_product=i[3]
        tax_product=i[4]
    
    global eproduct
    global eunit_price
    global etax
    global ehsn
    
    try:
        eproduct.delete(0,END)
        eunit_price.delete(0,END)
        etax.delete(0,END)
        ehsn.delete(0,END)
    except:
        pass

    try:
        eproduct_ie.delete(0,END)
        eunit_price_ie.delete(0,END)
        etax_ie.delete(0,END)
        ehsn_ie.delete(0,END)
    except:
        pass
    try:
        eproduct_qe.delete(0,END)
        eunit_price_qe.delete(0,END)
        etax_qe.delete(0,END)
        ehsn_qe.delete(0,END)
    except:
        pass
    
    try:
        eproduct_ie.insert(0,name_product)
        eunit_price_ie.insert(0,price_product)
        ehsn_ie.insert(0,hsn_product)
        etax_ie.insert(0,tax_product)
    except:
        pass


    try:
        eproduct_qe.insert(0,name_product)
        eunit_price_qe.insert(0,price_product)
        ehsn_qe.insert(0,hsn_product)
        etax_qe.insert(0,tax_product)
    except:
        pass
    
    try:
        eproduct.insert(0,name_product)
        eunit_price.insert(0,price_product)
        ehsn.insert(0,hsn_product)
        etax.insert(0,tax_product)
    except:
        pass
        
def leftclick_product(event):
    try:
        listbox1.delete(0,tk.END)
        listbox1.destroy()
    except:
        pass
    try:
        listbox1_q.delete(0,tk.END)
        listbox1_q.destroy()
    except:
        pass
def new_invoice_check_product(event):
    try:
        try:
            product1=eproduct.get()
        except:
            product1=eproduct_ie.get()
    except:
        product1=eproduct_qe.get()
    if len(product1)>>1:
        global listbox1
        try:
            listbox1.delete(0,tk.END)
            listbox1.destroy()
        except:
            pass
        l=1
        statement1=("SELECT * FROM PRODUCT WHERE NAME LIKE" +' \''+product1+'%\'')
        check=conn.execute(statement1)
        try:
            try:
                listbox1=tk.Listbox(fnew_invoice,width =90, font=("Arial", 15 ), bg= "gray93")
            except:
                listbox1=tk.Listbox(fedit_invoice,width =90, font=("Arial", 15 ), bg= "gray93")
        except:
            listbox1=tk.Listbox(qedit_quotation,width =90, font=("Arial", 15 ), bg= "gray93")
        listbox1.place(x=int(w/10),y=int(h/3.22))
        for i in check:
            n=i[1]
            listbox1.insert(l, n)
            l=l+1
        listbox1.bind('<<ListboxSelect>>',CurSelet_product)
    try:
        try:
            fnew_invoice.bind("<Button-1>",leftclick_product)
        except:
            fedit_invoice.bind("<Button-1>",leftclick_product)
    except:
        try:
            qedit_quotation.bind("<Button-1>",leftclick_product)
        except:
            pass


def leftclick(event):
    try:
        listbox.destroy()
    except:
        pass
    try:
        listbox_q.destroy()
    except:
        pass

    try:
        listbox_q.delete(0,tk.END)
    except:
        pass
    try:
        listbox.delete(0,tk.END)
    except:
        pass
def CurSelet(event):
    
    try:
        selected_name=listbox.get(listbox.curselection())
    except:
        listbox.destroy()
        selected_name=""
    try:
        listbox.delete(0,tk.END)
        listbox.destroy()
    except:
        pass
    b="""SELECT * FROM CUSTOMER where NAME = ?"""
    c=conn.execute(b, (selected_name,))
    #b="SELECT * FROM CUSTOMER where NAME="+str(selected_name)
    for i in c:
        name=i[1]
        address=i[2]
        gst=i[3]
        mobile=i[4]
        email=[5]
    
    global ecustomer2
    global eaddress
    global egst
    try:
        ecustomer2.delete(0,END)
        eaddress.delete(0,END)
        egst.delete(0,END)
        emobile.delete(0,END)
        eemail.delete(0,END)
    except:
        pass

    ecustomer2.insert(0,name)
    eaddress.insert(0,address)
    egst.insert(0,gst)
    emobile.insert(0,mobile)
    try:
        listbox.delete(0,tk.END)
        listbox.destroy()
    except:
        pass
def new_invoice_check_name(event,name):
    name1=ecustomer2.get()
    if len(name1)>>1:
        global listbox
        try:
            listbox.delete(0,tk.END)
            listbox.destroy()
        except:
            pass
        l=1
        statement=("SELECT * FROM CUSTOMER WHERE NAME LIKE" +' \''+name1+'%\'')
        check=conn.execute(statement)
        listbox=tk.Listbox(fnew_invoice,width =25, font=("Arial", 15 ), bg= "gray93")
        listbox.place(x=int(w/5.3),y=int(h/12))
        for i in check:
            n=i[1]
            listbox.insert(l, n)
            l=l+1
        listbox.bind('<<ListboxSelect>>',CurSelet)
        fnew_invoice.bind("<Button-1>",leftclick)

        
    else:
        pass
    

    






    
########################################################### Functional Work For New Customers (ADD Customers) ###########################################################
def new_customer_save(tree,win):
    for i in tree.get_children():
        items=tree.item(i)['values']
        name=items[1]
        address=items[2]
        gst=items[3]
        mobile=items[4]
        email=items[5]
        conn.execute("INSERT INTO CUSTOMER (NAME,ADDRESS,GST,MOBILE,EMAIL) \
                    VALUES ( ?,?,?,?,? )",(name,address,gst,mobile,email))
        conn.commit()
        error("Saved Successfully!")
        win.destroy()
        new_customer()

def new_customer_clear(tree):
    try:
        curItem = tree.focus()
        tree.delete(curItem)
    except:
        pass

def new_customer_add(tree,name,address,gst,mobile,email):
    global x_new_customer
    address = address.replace(',', '.').replace('\n', ', ')
    address=address[:-2]
    tree.insert("",index='end',  values=(str(x_new_customer), str(name), str(address),str(gst),str(mobile),str(email)))
    x_new_customer=x_new_customer+1


def new_customer_edit_select(tree):
    tree=tree
    curItem = tree.focus()
    items_to_update=tree.item(curItem)['values']
    x=items_to_update[0]
    name=items_to_update[1]
    address=items_to_update[2]
    gst=items_to_update[3]
    mobile=items_to_update[4]
    email=items_to_update[5]
    
    top_customer_edit = tk.Tk(className=' Edit Info ')
    top_customer_edit.geometry("700x600")
    fedit_window= tk.Frame(top_customer_edit, bg = "white", height=h, width=w)
    fedit_window.pack()
    l_name=tk.Label(fedit_window, text="Name\t:", bg="white", font=("Arial", 15 ))
    l_name.place(x=150,y=100)
    l_address=tk.Label(fedit_window, text="Address\t:", bg="white", font=("Arial", 15 ))
    l_address.place(x=150,y=175)
    l_gst=tk.Label(fedit_window, text="GST NO\t:", bg="white", font=("Arial", 15 ))
    l_gst.place(x=150,y=300)
    l_mobile=tk.Label(fedit_window, text="Mobile\t:", bg="white", font=("Arial", 15 ))
    l_mobile.place(x=150,y=375)
    l_email=tk.Label(fedit_window, text="Email\t:", bg="white", font=("Arial", 15 ))
    l_email.place(x=150,y=450)
    
    e_name=tk.Entry(fedit_window,  bg="gray93",width=25, font=("Arial", 15 ))
    e_name.place(x=270,y=100)
    e_address=tk.Text(fedit_window, width =25,height=3, font=("Arial", 15 ), bg= "gray93")
    e_address.place(x=270,y=175)
    e_gst=tk.Entry(fedit_window,bg="gray93",width=25, font=("Arial", 15 ))
    e_gst.place(x=270,y=300)
    e_mobile=tk.Entry(fedit_window,bg="gray93",width=25, font=("Arial", 15 ))
    e_mobile.place(x=270,y=375)
    e_email=tk.Entry(fedit_window,bg="gray93",width=25, font=("Arial", 15 ))
    e_email.place(x=270,y=450)

    b_save=tk.Button(fedit_window,width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",relief=FLAT,
                     command= lambda: new_customer_edit_save(top_customer_edit,tree,x,e_name.get(),e_address.get('1.0', END),e_gst.get(),e_mobile.get(),e_email.get()))
    b_save.place(x=270,y=525)


    address = address.replace(',', '\n').replace('.', ',')
    e_name.insert(0,str(name))
    e_address.insert("1.0", str(address),END)
    e_gst.insert(0,str(gst))
    e_mobile.insert(0,str(mobile))
    e_email.insert(0,str(email))

def new_customer_edit_save(top_customer_edit,tree,x,name,address,gst,mobile,email):
    address = address.replace(',', '.').replace('\n', ', ')
    address=address[:-2]
    curItem = tree.focus()
    items_to_update=tree.item(curItem)['values']
    y=items_to_update[0]
    tree.insert("", str(curItem)[1:], values=(str(x),str(name),str(address),str(gst),str(mobile),str(email)))
    tree.delete(curItem)
    top_customer_edit.destroy()
    

    
########################################################### Functional Work For New Product (ADD Product) ###########################################################

def new_product_save(tree,win):
    for i in tree.get_children():
        items=tree.item(i)['values']
        name=items[1]
        price=items[2]
        hsn=items[3]
        tax=items[4]
        conn.execute("INSERT INTO PRODUCT (NAME,PRICE,HSN,TAX) \
                    VALUES ( ?,?,?,? )",(name,price,hsn,tax))
        conn.commit()
        error("New Product Saved!")
        win.destroy()
        new_product()

def NEW_PRODUCT_clear(tree):
    try:
        curItem = tree.focus()
        tree.delete(curItem)
    except:
        pass
    

def NEW_PRODUCT_edit_select(tree):
    curItem = tree.focus()
    items_to_update=tree.item(curItem)['values']
    tree=tree
    y=items_to_update[0]
    name=items_to_update[1]
    price=items_to_update[2]
    hsn=items_to_update[3]
    tax=items_to_update[4]
    top_product_edit = tk.Tk(className=' Edit Info ')
    top_product_edit.geometry("750x500")
    fedit_window= tk.Frame(top_product_edit, bg = "white", height=h, width=w)
    fedit_window.pack()
    l_name=tk.Label(fedit_window, text="Name\t:", bg="white", font=("Arial", 15 ))
    l_name.place(x=200,y=100)
    l_price=tk.Label(fedit_window, text="Price\t:", bg="white", font=("Arial", 15 ))
    l_price.place(x=200,y=175)
    l_hsn=tk.Label(fedit_window, text="HSN NO\t:", bg="white", font=("Arial", 15 ))
    l_hsn.place(x=200,y=250)
    l_tax=tk.Label(fedit_window, text="Tax\t:", bg="white", font=("Arial", 15 ))
    l_tax.place(x=200,y=325)
    
    e_name=tk.Entry(fedit_window,  bg="white", font=("Arial", 15 ))
    e_name.place(x=350,y=100)
    e_price=tk.Entry(fedit_window, bg="white", font=("Arial", 15 ))
    e_price.place(x=350,y=175)
    e_hsn=tk.Entry(fedit_window,bg="white", font=("Arial", 15 ))
    e_hsn.place(x=350,y=250)

    b_save=tk.Button(fedit_window,width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                     command= lambda: NEW_PRODUCT_save(tree,e_name.get(),e_price.get(),e_hsn.get(),taxchoosen.get(),top_product_edit),relief=FLAT)
    b_save.place(x=350,y=400)

    taxchoosen = tk.Entry(fedit_window,bg="white", font=("Arial", 15 )) 
    taxchoosen.place(x=350,y=325)



    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            taxchoosen.insert(0,str(i[0]))
    except:
        pass

    
    e_name.insert(0,str(name))
    e_price.insert(0,str(price))
    e_hsn.insert(0,str(hsn))
    
def NEW_PRODUCT_save(tree,name,price,hsn,tax,top):
    curItem = tree.focus()
    items_to_update=tree.item(curItem)['values']
    y=items_to_update[0]
    tree.insert("", str(curItem)[1:], values=(str(y),str(name),str(price),str(hsn),str(tax)))
    tree.delete(curItem)
    #top.destroy()

def NEW_PRODUCT_add_to_list(name,price,hsn,tax,tree):
    name1=name.get()
    price1=price.get()
    hsn1=hsn.get()
    tax1=tax.get()
    global x
    try:
        int(float(price1))
        try:
            int(hsn1)
            if name1 != "":
                tree.insert("",index='end',  values=(str(x), str(name1), str(price1),str(hsn1),str(tax1)))
                x=x+1
            else:
                raise error
        except:
            error("Please check all entries!")
    except:
        error("Please check all entries!")
                        
    name.delete(0, 'end')
    price.delete(0, 'end')
    
######################################################################### Customers Data List #######################################################################    

def show_customers_from_db(tree,name,mobile,gst):
    name=name.get()
    mobile=mobile.get()
    gst=gst.get()
    try:
        for i in tree.get_children():
            tree.delete(i)
    except:
        pass
    
    if name !="":
        query=("SELECT * from CUSTOMER where NAME LIKE" +' \''+name+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            address=i[2]
            gst=i[3]
            mobile=i[4]
            email=i[5]
            tree.insert("",index='end',  values=(str(k), str(name), str(address),str(gst),str(mobile),str(email)))
            k=k+1
    elif mobile !="":
        query=("SELECT * from CUSTOMER where MOBILE LIKE" +' \''+mobile+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            address=i[2]
            gst=i[3]
            mobile=i[4]
            email=i[5]
            tree.insert("",index='end',  values=(str(k), str(name), str(address),str(gst),str(mobile),str(email)))
            k=k+1
    elif gst !="":
        query=("SELECT * from from CUSTOMER where GST LIKE" +' \''+gst+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            address=i[2]
            gst=i[3]
            mobile=i[4]
            email=i[5]
            tree.insert("",index='end',  values=(str(k), str(name), str(address),str(gst),str(mobile),str(email)))
            k=k+1
    else:
        error("All Entries are Empty!")




        

##########################################################################  PRODUCT Data List #######################################################################


def show_product_from_db(tree,name,hsn,tax,price):
    name=name.get()
    hsn=hsn.get()
    tax=tax.get()
    price=price.get()
    
    try:
        for i in tree.get_children():
            tree.delete(i)
    except:
        pass
    
    if name !="":
        query=("SELECT * from PRODUCT where NAME LIKE" +' \''+name+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            price=i[2]
            hsn=i[3]
            tax=i[4]
            tree.insert("",index='end',  values=(str(k), str(name), str(hsn),str(tax),str(price)))
            k=k+1
    elif hsn !="":
        query=("SELECT * from PRODUCT where HSN LIKE" +' \''+hsn+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            price=i[2]
            hsn=i[3]
            tax=i[4]
            tree.insert("",index='end',  values=(str(k), str(name), str(hsn),str(tax),str(price)))
            k=k+1
    elif tax !="":
        query=("SELECT * from PRODUCT where TAX LIKE" +' \''+tax+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            price=i[2]
            hsn=i[3]
            tax=i[4]
            tree.insert("",index='end',  values=(str(k), str(name), str(hsn),str(tax),str(price)))
            k=k+1
    elif price !="":
        query=("SELECT * from PRODUCT where PRICE LIKE" +' \''+price+'%\'')
        data=conn.execute(query,)
        k=1
        for i in data:
            name=i[1]
            price=i[2]
            hsn=i[3]
            tax=i[4]
            tree.insert("",index='end',  values=(str(k), str(name), str(hsn),str(tax),str(price)))
            k=k+1
    else:
        error("All Entries are Empty!")


    
####################################################################### SAVE COMPANY DEATILS TO DATABASE ############################################################



def save_company_details_db(name,address,mobile,tax,gst,mail,phone,notes,hsn):
    name=name.get()
    mobile=mobile.get()
    tax=tax.get()
    gst=gst.get()
    mail=mail.get()
    phone=phone.get()
    hsn=hsn.get()
    address=address.get("1.0",'end-1c')
    notes=notes.get("1.0",'end-1c')
    if name == "":
        error("Enter Company Name!")
        return
    elif mobile == "":
        error("Enter mobile number!")
        return
    elif address == "":
        error("Enter address!")
        return
    elif tax == "":
        error("Enter tax value!")
        return
    elif hsn == "":
        error("Enter HSN value!")
        return
    else:
        name123=""
        query=("SELECT NAME from COMPANY")
        data=conn.execute(query,)
        for i in data:
            name123=i[0]
        if name123 !="":
            cursor.execute('''UPDATE COMPANY SET NAME = ?, ADDRESS= ?,MOBILE =?,PHONE =?,EMAIL =?,TAX =?, GST= ?, NOTES = ?, HSN =?''',
                       (name, address,mobile, phone,mail, tax, gst,notes, hsn))
            conn.commit()
            error("Successfully Updated!")
        else:
            query = """ INSERT INTO COMPANY (NAME,ADDRESS,MOBILE,PHONE,EMAIL,TAX, GST, NOTES, HSN) VALUES ( ?,?,?,?,?,?,?,?,?)"""
            data_db= (name,address,mobile,phone,mail,tax,gst,notes,hsn)
            conn.execute(query, data_db)
            conn.commit()
            error("Successfully Saved!")
    

def list_customer_edit_save(win,old_name,old_address,old_phone,new_name,new_address,new_gst,new_phone,new_mail):
    new_name=new_name.get()
    new_address=new_address.get("1.0",'end-1c')
    new_gst=new_gst.get()
    new_phone=new_phone.get()
    new_mail=new_mail.get()

    if new_name !="" and new_address!="" and new_phone!="":
        cursor.execute('''UPDATE CUSTOMER SET NAME = ?, ADDRESS= ?,GST =?,MOBILE =?,EMAIL =? WHERE NAME= ? AND ADDRESS = ? AND MOBILE =?''',
                       (new_name, new_address, new_gst, new_phone,new_mail, old_name, old_address, old_phone ))
        conn.commit()
        win.destroy()
    else:
        error("Name, Address, Phone details must be filled!")



def list_customer_delete(tree,win):
    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        error("Select Any item first!")
        return
    name=item_list[1]
    address=item_list[2]
    phone=item_list[4]
    cursor.execute('''DELETE FROM CUSTOMER WHERE NAME=? AND ADDRESS=? AND MOBILE=? ''',(name,address,phone))
    conn.commit()
    win.destroy()
    list_customer()


def list_product_edit_save(win,old_name,old_price,new_name,new_price,new_hsn,new_tax):
    new_name=new_name.get()
    new_price=new_price.get()
    new_hsn=new_hsn.get()
    new_tax=new_tax.get()
    

    if new_name !="" :
        cursor.execute('''UPDATE PRODUCT SET NAME = ?, PRICE= ?,HSN =?,TAX =? WHERE NAME= ?''',
                       (new_name, new_price, new_hsn, new_tax, old_name ))
        conn.commit()
        win.destroy()
        try:
            global top_list_products
            top_list_products.destroy()
            list_products()
        except:
            pass
    else:
        error("Name, Price sdetails must be filled!")



def list_product_delete(tree,win):
    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        error("Select Any item first!")
        return
    name=item_list[1]
    cursor.execute('''DELETE FROM PRODUCT WHERE NAME=? ''',(str(name),))
    conn.commit()
    win.destroy()
    list_products()


def list_invoice_delete(tree,win):
    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        error("Select Any item first!")
        return
    res=messagebox.askyesno("Delete Invoice"," Do you want to delete this invoice?")
    if res == True:
        invoice_id=item_list[2]
        cursor.execute('''DELETE FROM INVOICE WHERE ID=?''',(str(invoice_id),))
        conn.commit()
        win.destroy()
        list_invoice()
    else:
        pass

def list_quotation_delete(tree,win):
    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        error("Select Any item first!")
        return
    quotation_id=item_list[2]
    cursor.execute('''DELETE FROM QUOTATION WHERE ID=?''',(str(quotation_id),))
    conn.commit()
    win.destroy()
    list_quotation()
    

def password_update_to_db(old,new,confirm):
    query="SELECT PASSWORD from USERS"
    passwd_db=""
    results=conn.execute(query)
    
    for i in results:
        passwd_db=str(i[0])

    if old.get() != passwd_db:
        error("Old Password is Wrong!")
        return
    if new.get() != confirm.get():
        error("Passwords Does Not Match!")
        return
    name_admin="admin"
    cursor.execute('''UPDATE USERS SET PASSWORD = ? where NAME = ?''',
                       (str(new.get()),name_admin))
    conn.commit()
    error("Password Successfully Changed!")

def update_invoice_db(typeof,invoice_num,name,address,gst,mobile,date,tree,window):
    list_to_db = []
    for i in tree.get_children():
        list_to_db+=tree.item(i)['values']
    data = ','.join(str(e) for e in list_to_db)
    if typeof == "invoice":
        cursor.execute('''UPDATE INVOICE SET NAME = ?, ADDRESS= ?,GST =?,DATE =?,MOBILE =?,DATA =? WHERE ID =?''',
                           (name,address,gst,date,mobile,data,invoice_num))
        conn.commit()
        error("Invoice Successfully Updated!")
    elif typeof == "quotation":
        cursor.execute('''UPDATE QUOTATION SET NAME = ?, ADDRESS= ?,GST =?,DATE =?,MOBILE =?,DATA =? WHERE ID =?''',
                           (name,address,gst,date,mobile,data,invoice_num))
        conn.commit()
        error("Quotation Successfully Updated!")
    
    window.destroy()
    
#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################
####################################################################################################################################################################   
############################################################################ GUI FINISHED ###########################################################################





def quotation_edit(tree):
    curItem = tree.focus()
    quotation_num=((tree.item(curItem)["values"])[2])
    
    global top_qe
    global quotation_edit_id
    top_qe = tk.Tk(className=' Edit Quotation')
    top_qe.geometry(str(w) + 'x' + str(h))
    top_qe.state('zoomed')
    global qedit_quotation
    qedit_quotation= tk.Frame(top_qe, bg = "white", height=h, width=w)
    qedit_quotation.grid(row=0,column=0)

    
    lcustomer2_qe= tk.Label(qedit_quotation, text="Customer: ", font=("Arial", 15 ), bg= "white")
    lcustomer2_qe.place(x=int(w/10),y=int(h/20))
    laddress_qe= tk.Label(qedit_quotation, text="Address  : ", font=("Arial", 15 ), bg= "white")
    laddress_qe.place(x=int(w/10),y=int(h/8.5))
    lgst_qe= tk.Label(qedit_quotation, text="GST NO  : ", font=("Arial", 15 ), bg= "white")
    lgst_qe.place(x=int(w/10),y=int(h/5.5))
    lquotation_num_qe=tk.Label(qedit_quotation, text="Invoice No  : ", font=("Arial", 15 ), bg= "white")
    lquotation_num_qe.place(x=int(w/1.8),y=int(h/8.5))
    ldate_qe=tk.Label(qedit_quotation, text="Date      \t   : ", font=("Arial", 15 ), bg= "white")
    ldate_qe.place(x=int(w/1.8),y=int(h/5.5))
    lproduct_qe=tk.Label(qedit_quotation, text="Product:", font=("Arial", 15 ), bg= "white")
    lproduct_qe.place(x=int(w/10),y=int(h/4.2))
    lqty_qe=tk.Label(qedit_quotation, text="QTY:", font=("Arial", 15 ), bg= "white")
    lqty_qe.place(x=int(w/10),y=int(h/3))
    lunit_price_qe=tk.Label(qedit_quotation, text="Unit Price:", font=("Arial", 15 ), bg= "white")
    lunit_price_qe.place(x=int(w/3.9),y=int(h/3))
    ltax_qe=tk.Label(qedit_quotation, text="Tax:", font=("Arial", 15 ), bg= "white")
    ltax_qe.place(x=int(w/2.2),y=int(h/3))
    lmobile_qe=tk.Label(qedit_quotation, text="Mobile\t  :", font=("Arial", 15 ), bg= "white")
    lmobile_qe.place(x=int(w/1.8),y=int(h/20))
    lhsn_qe=tk.Label(qedit_quotation, text="HSN:", font=("Arial", 15 ), bg= "white")
    lhsn_qe.place(x=int(w/1.6),y=int(h/3))    
    
    lnote_qe=tk.Label(qedit_quotation, text="Note  : ", font=("Arial", 15 ), bg= "white")
    lnote_qe.place(x=int(w/10),y=int(h/1.35))
    
    global ecustomer2_qe
    global eaddress_qe
    global egst_qe
    global emobile_qe
    global eproduct_qe
    global eunit_price_qe
    global etax_qe
    global ehsn_qe
    global cal_new_quotation_qe
    global enote_qe
    
    ecustomer2_qe= tk.Entry(qedit_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    ecustomer2_qe.place(x=int(w/5.3),y=int(h/19))
    eaddress_qe= tk.Entry(qedit_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    eaddress_qe.place(x=int(w/5.3),y=int(h/8))
    egst_qe= tk.Entry(qedit_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    egst_qe.place(x=int(w/5.3),y=int(h/5.3))
    emobile_qe= tk.Entry(qedit_quotation, width =15, font=("Arial", 15 ), bg= "gray93")
    emobile_qe.place(x=int(w/1.49),y=int(h/19))
    equotation_num_qe= tk.Entry(qedit_quotation, width =15, font=("Arial", 15 ), bg= "gray93")
    equotation_num_qe.place(x=int(w/1.49),y=int(h/8))
    cal_new_quotation_qe= DateEntry(qedit_quotation, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_new_quotation_qe.place(x=int(w/1.49),y=int(h/5.3))

    enote_qe= tk.Text(qedit_quotation, width =30, height =5 , font=("Arial", 15 ), bg= "gray93")
    enote_qe.place(x=int(w/6),y=int(h/1.35))
    
    eproduct_qe= tk.Entry(qedit_quotation, width =90, font=("Arial", 15 ), bg= "gray93")
    eproduct_qe.place(x=int(w/10),y=int(h/3.6))
    eqty_qe= tk.Entry(qedit_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    eqty_qe.place(x=int(w/10),y=int(h/2.6))
    eunit_price_qe= tk.Entry(qedit_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    eunit_price_qe.place(x=int(w/3.9),y=int(h/2.6))
    etax_qe= tk.Entry(qedit_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    etax_qe.place(x=int(w/2.2),y=int(h/2.6))
    ehsn_qe= tk.Entry(qedit_quotation, width =10, font=("Arial", 15 ), bg= "gray93")
    ehsn_qe.place(x=int(w/1.6),y=int(h/2.6))

    badd_qe=tk.Button(qedit_quotation, text="ADD", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",
                   command= lambda: new_invoice_add(tree_qe,
                                                        eproduct_qe.get(),
                                                        ehsn_qe.get(),
                                                        eqty_qe.get(),
                                                        etax_qe.get(),
                                                        eunit_price_qe.get(),
                                                        eproduct_qe,
                                                        eqty_qe,
                                                        etax_qe,
                                                        eunit_price_qe,
                                                        ehsn_qe))
    badd_qe.place(x=int(w/1.33),y=int(h/2.7))
    bclear_qe=tk.Button(qedit_quotation, text="CLEAR", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: new_invoice_clear(tree_qe))
    bclear_qe.place(x=int(w/1.5),y=int(h/1.28))
    bupdate_qe=tk.Button(qedit_quotation, text="UPDATE", font=("Arial", 13) , bg= "dodger blue", fg="white",
                       command= lambda: update_invoice_db("quotation",quotation_num,ecustomer2_qe.get(),\
                                                          eaddress_qe.get(),egst_qe.get(),emobile_qe.get(),cal_new_quotation_qe.get(),tree_qe,top_qe))
    bupdate_qe.place(x=int(w/1.3),y=int(h/1.28))
    


    bpreview_qe=tk.Button(qedit_quotation, text="PREVIEW", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: create_pdf(tree_qe,equotation_num_qe
                                                                                                                                                     ,"quotation_edit"))
    bpreview_qe.place(x=int(w/1.77),y=int(h/1.28))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree_qe = ttk.Treeview(qedit_quotation, columns=('0', '1', '2','3','4','5'), show='headings')
    tree_qe.heading('0', text="S.NO")
    tree_qe.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_qe.heading('1', text="Product/Service")
    tree_qe.column('1', anchor=CENTER,minwidth=0, width=375, stretch=NO)
    tree_qe.heading('2', text="HSN Code")
    tree_qe.column('2', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_qe.heading('3', text="Quantity")
    tree_qe.column('3', anchor=CENTER,minwidth=0, width=100, stretch=NO)
    tree_qe.heading('4', text="Tax")
    tree_qe.column('4', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_qe.heading('5', text="Amount")
    tree_qe.column('5', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_qe.place(x=int(w/9.8),y=int(h/2.3))
    vsb_qe = ttk.Scrollbar(qedit_quotation, orient="vertical", command=tree_qe.yview)
    vsb_qe.place(x=int(w/9.8+1000),y=int(h/2.3),width=16, height = 230)
    tree_qe.configure(yscrollcommand=vsb_qe.set)
    
    
    eproduct_qe.bind("<Key>",new_invoice_check_product)
    global typed
    typed =""
    global x_new_quotation_add
    x_new_quotation_add=1

    
    quotation_edit_id= 1
    global notes_from_db
    try:
        enote_qe.insert(END, notes_from_db)
    except:
        pass

    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            etax_qe.insert(0,str(i[0]))
    except:
        pass

    try:
        query =("SELECT HSN FROM COMPANY")
        results=conn.execute(query)
        for i in results:
            ehsn_qe.insert(0,(i))
        
    except:
        pass
    

    query="""SELECT * FROM QUOTATION WHERE ID = ?"""
    results=conn.execute(query, (quotation_num,))
    for i in results:
        name=(i[1])
        address=(i[2])
        gst=(i[3])
        date=(i[4])
        mobile=(i[5])
        data=(i[6])
    
    ecustomer2_qe.insert(0,name)
    eaddress_qe.insert(0,address)
    egst_qe.insert(0,gst)
    cal_new_quotation_qe.set_date(date)
    emobile_qe.insert(0,mobile)
    equotation_num_qe.insert(0,quotation_num)
    equotation_num_qe.config(state='disabled')
    test_list=data.split(",")
    j=1
    temp_list=[]
    final_list=[]
    for i in test_list:
        if j%6==0 and j!=0:
            temp_list.append(i)
            final_list.append(temp_list)
            temp_list=[]
        else:
            temp_list.append(i)
            
        j=j+1
    global last_tree_number_invoice_edit
    
    quotation_edit_id=1
    for i in final_list:
        if i[0]!="":
            last_tree_number_invoice_edit=str(i[0])
        tree_qe.insert("",index='end',  values=(str(i[0]), str(i[1]), str(i[2]),str(i[3]),str(i[4]),str(i[5])))

            
            
            

def invoice_edit(tree):
    curItem = tree.focus()
    invoice_num=((tree.item(curItem)["values"])[2])
    
    global top_ie
    top_ie = tk.Tk(className=' New Invoice')
    top_ie.geometry(str(w) + 'x' + str(h))
    top_ie.state('zoomed')
    global fedit_invoice
    fedit_invoice= tk.Frame(top_ie, bg = "white", height=h, width=w)
    fedit_invoice.grid(row=0,column=0)

    
    lcustomer2_ie= tk.Label(fedit_invoice, text="Customer: ", font=("Arial", 15 ), bg= "white")
    lcustomer2_ie.place(x=int(w/10),y=int(h/20))
    laddress_ie= tk.Label(fedit_invoice, text="Address  : ", font=("Arial", 15 ), bg= "white")
    laddress_ie.place(x=int(w/10),y=int(h/8.5))
    lgst_ie= tk.Label(fedit_invoice, text="GST NO  : ", font=("Arial", 15 ), bg= "white")
    lgst_ie.place(x=int(w/10),y=int(h/5.5))
    linvoice_num_ie=tk.Label(fedit_invoice, text="Invoice No  : ", font=("Arial", 15 ), bg= "white")
    linvoice_num_ie.place(x=int(w/1.8),y=int(h/8.5))
    ldate_ie=tk.Label(fedit_invoice, text="Date      \t   : ", font=("Arial", 15 ), bg= "white")
    ldate_ie.place(x=int(w/1.8),y=int(h/5.5))
    lproduct_ie=tk.Label(fedit_invoice, text="Product:", font=("Arial", 15 ), bg= "white")
    lproduct_ie.place(x=int(w/10),y=int(h/4.2))
    lqty_ie=tk.Label(fedit_invoice, text="QTY:", font=("Arial", 15 ), bg= "white")
    lqty_ie.place(x=int(w/10),y=int(h/3))
    lunit_price_ie=tk.Label(fedit_invoice, text="Unit Price:", font=("Arial", 15 ), bg= "white")
    lunit_price_ie.place(x=int(w/3.9),y=int(h/3))
    ltax_ie=tk.Label(fedit_invoice, text="Tax:", font=("Arial", 15 ), bg= "white")
    ltax_ie.place(x=int(w/2.2),y=int(h/3))
    lmobile_ie=tk.Label(fedit_invoice, text="Mobile\t  :", font=("Arial", 15 ), bg= "white")
    lmobile_ie.place(x=int(w/1.8),y=int(h/20))
    lhsn_ie=tk.Label(fedit_invoice, text="HSN:", font=("Arial", 15 ), bg= "white")
    lhsn_ie.place(x=int(w/1.6),y=int(h/3))    
    
    lnote_ie=tk.Label(fedit_invoice, text="Note  : ", font=("Arial", 15 ), bg= "white")
    lnote_ie.place(x=int(w/10),y=int(h/1.35))
    
    global ecustomer2_ie
    global eaddress_ie
    global egst_ie
    global emobile_ie
    global eproduct_ie
    global eunit_price_ie
    global etax_ie
    global ehsn_ie
    global cal_new_invoice_ie
    global enote_ie
    
    ecustomer2_ie= tk.Entry(fedit_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    ecustomer2_ie.place(x=int(w/5.3),y=int(h/19))
    eaddress_ie= tk.Entry(fedit_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    eaddress_ie.place(x=int(w/5.3),y=int(h/8))
    egst_ie= tk.Entry(fedit_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    egst_ie.place(x=int(w/5.3),y=int(h/5.3))
    emobile_ie= tk.Entry(fedit_invoice, width =15, font=("Arial", 15 ), bg= "gray93")
    emobile_ie.place(x=int(w/1.49),y=int(h/19))
    einvoice_num_ie= tk.Entry(fedit_invoice, width =15, font=("Arial", 15 ), bg= "gray93")
    einvoice_num_ie.place(x=int(w/1.49),y=int(h/8))
    cal_new_invoice_ie= DateEntry(fedit_invoice, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_new_invoice_ie.place(x=int(w/1.49),y=int(h/5.3))

    enote_ie= tk.Text(fedit_invoice, width =30, height =5 , font=("Arial", 15 ), bg= "gray93")
    enote_ie.place(x=int(w/6),y=int(h/1.35))
    
    eproduct_ie= tk.Entry(fedit_invoice, width =90, font=("Arial", 15 ), bg= "gray93")
    eproduct_ie.place(x=int(w/10),y=int(h/3.6))
    eqty_ie= tk.Entry(fedit_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    eqty_ie.place(x=int(w/10),y=int(h/2.6))
    eunit_price_ie= tk.Entry(fedit_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    eunit_price_ie.place(x=int(w/3.9),y=int(h/2.6))
    etax_ie= tk.Entry(fedit_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    etax_ie.place(x=int(w/2.2),y=int(h/2.6))
    ehsn_ie= tk.Entry(fedit_invoice, width =10, font=("Arial", 15 ), bg= "gray93")
    ehsn_ie.place(x=int(w/1.6),y=int(h/2.6))

    badd_ie=tk.Button(fedit_invoice, text="ADD", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",
                   command= lambda: new_invoice_add(tree_ie,
                                                        eproduct_ie.get(),
                                                        ehsn_ie.get(),
                                                        eqty_ie.get(),
                                                        etax_ie.get(),
                                                        eunit_price_ie.get(),
                                                        eproduct_ie,
                                                        eqty_ie,
                                                        etax_ie,
                                                        eunit_price_ie,
                                                        ehsn_ie))
    badd_ie.place(x=int(w/1.33),y=int(h/2.7))
    bclear_ie=tk.Button(fedit_invoice, text="CLEAR", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: new_invoice_clear(tree_ie))
    bclear_ie.place(x=int(w/1.5),y=int(h/1.28))
    bupdate_ie=tk.Button(fedit_invoice, text="UPDATE", font=("Arial", 13) , bg= "dodger blue", fg="white",
                       command= lambda: update_invoice_db("invoice",invoice_num,ecustomer2_ie.get(),\
                                                          eaddress_ie.get(),egst_ie.get(),emobile_ie.get(),cal_new_invoice_ie.get(),tree_ie,top_ie))
    bupdate_ie.place(x=int(w/1.3),y=int(h/1.28))
    


    bpreview_ie=tk.Button(fedit_invoice, text="PREVIEW", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: create_pdf(tree_ie,einvoice_num_ie
                                                                                                                                                     ,"invoice_edit"))
    bpreview_ie.place(x=int(w/1.77),y=int(h/1.28))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree_ie = ttk.Treeview(fedit_invoice, columns=('0', '1', '2','3','4','5'), show='headings')
    tree_ie.heading('0', text="S.NO")
    tree_ie.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_ie.heading('1', text="Product/Service")
    tree_ie.column('1', anchor=CENTER,minwidth=0, width=375, stretch=NO)
    tree_ie.heading('2', text="HSN Code")
    tree_ie.column('2', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_ie.heading('3', text="Quantity")
    tree_ie.column('3', anchor=CENTER,minwidth=0, width=100, stretch=NO)
    tree_ie.heading('4', text="Tax")
    tree_ie.column('4', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_ie.heading('5', text="Amount")
    tree_ie.column('5', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_ie.place(x=int(w/9.8),y=int(h/2.3))
    vsb_ie = ttk.Scrollbar(fedit_invoice, orient="vertical", command=tree_ie.yview)
    vsb_ie.place(x=int(w/9.8+1000),y=int(h/2.3),width=16, height = 230)
    tree_ie.configure(yscrollcommand=vsb_ie.set)
    
    
    eproduct_ie.bind("<Key>",new_invoice_check_product)
    global typed
    typed =""
    global x_new_invoice_add
    x_new_invoice_add=1

    global notes_from_db
    try:
        enote_ie.insert(END, notes_from_db)
    except:
        pass

    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            etax_ie.insert(0,str(i[0]))
    except:
        pass

    try:
        query =("SELECT HSN FROM COMPANY")
        results=conn.execute(query)
        for i in results:
            ehsn_ie.insert(0,(i))
        
    except:
        pass

    query="""SELECT * FROM INVOICE WHERE ID = ?"""
    results=conn.execute(query, (invoice_num,))
    for i in results:
        name=(i[1])
        address=(i[2])
        gst=(i[3])
        date=(i[4])
        mobile=(i[5])
        data=(i[6])
    
    ecustomer2_ie.insert(0,name)
    eaddress_ie.insert(0,address)
    egst_ie.insert(0,gst)
    cal_new_invoice_ie.set_date(date)
    emobile_ie.insert(0,mobile)
    einvoice_num_ie.insert(0,invoice_num)
    einvoice_num_ie.config(state='disabled')
    test_list=data.split(",")
    j=1
    temp_list=[]
    final_list=[]
    for i in test_list:
        if j%6==0 and j!=0:
            temp_list.append(i)
            final_list.append(temp_list)
            temp_list=[]
        else:
            temp_list.append(i)
        
            
        j=j+1
    global last_tree_number_invoice_edit
    global invoice_edit_id
    invoice_edit_id=1
    for i in final_list:
        if i[0]!="":
            last_tree_number_invoice_edit=str(i[0])
        tree_ie.insert("",index='end',  values=(str(i[0]), str(i[1]), str(i[2]),str(i[3]),str(i[4]),str(i[5])))
    
            
            
            

    







def password_change(frame_o,win):
    frame_o.destroy()
    fcompany_details= tk.Frame(win, bg = "white", height=h, width=w)
    fcompany_details.pack()
    l_old_pass=tk.Label(fcompany_details, text="Old Password         :", bg="white", font=("Arial", 15 ))
    l_old_pass.place(x=int(w/6),y=int(h/3))
    l_new_pass=tk.Label(fcompany_details, text="New Password         :", bg="white", font=("Arial", 15 ))
    l_new_pass.place(x=int(w/6),y=int(h/2.4))
    l_pass_conf=tk.Label(fcompany_details, text="Confirm Password    :", bg="white", font=("Arial", 15 ))
    l_pass_conf.place(x=int(w/6),y=int(h/2))

    e_old_pass=tk.Entry(fcompany_details,width=25,  bg="gray93",show="*", font=("Arial", 15 ))
    e_old_pass.place(x=int(w/3.1),y=int(h/3))
    e_new_pass=tk.Entry(fcompany_details,width=25, bg="gray93",show="*", font=("Arial", 15 ))
    e_new_pass.place(x=int(w/3.1),y=int(h/2.4))
    e_pass_conf=tk.Entry(fcompany_details,width=25, bg="gray93",show="*", font=("Arial", 15 ))
    e_pass_conf.place(x=int(w/3.1),y=int(h/2))

    b_passwd_save= tk.Button(fcompany_details, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                             command= lambda: password_update_to_db(e_old_pass,e_new_pass,e_pass_conf))
    b_passwd_save.place(x=int(w/3.1),y=int(h/1.6))


def list_product_edit_gui(tree):
    top_list_product_edit_gui = tk.Toplevel()
    top_list_product_edit_gui.geometry(str(int(w/2)) + 'x' + str(int(h/1.3)))
    flist_product_edit_gui= tk.Frame(top_list_product_edit_gui, bg = "white", height=int(h/1.3), width=int(w/2))
    flist_product_edit_gui.pack()
    l_product_name=tk.Label(flist_product_edit_gui, text="Name             :", bg="white", font=("Arial", 15 ))
    l_product_name.place(x=int(w/12),y=int(h/8))
    l_product_price=tk.Label(flist_product_edit_gui, text="Price            :", bg="white", font=("Arial", 15 ))
    l_product_price.place(x=int(w/12),y=int(h/5))
    l_product_hsn=tk.Label(flist_product_edit_gui, text="Hsn No         :", bg="white", font=("Arial", 15 ))
    l_product_hsn.place(x=int(w/12),y=int(h/3))
    l_product_tax=tk.Label(flist_product_edit_gui, text="Tax             :", bg="white", font=("Arial", 15 ))
    l_product_tax.place(x=int(w/12),y=int(h/2.5))
    


    e_product_name=tk.Entry(flist_product_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_product_name.place(x=int(w/4.3),y=int(h/8))
    e_product_price= tk.Entry(flist_product_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_product_price.place(x=int(w/4.3),y=int(h/5))
    e_product_hsn=tk.Entry(flist_product_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_product_hsn.place(x=int(w/4.3),y=int(h/3))
    e_product_tax=tk.Entry(flist_product_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_product_tax.place(x=int(w/4.3),y=int(h/2.5))

    b_product_save= tk.Button(flist_product_edit_gui, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                              command = lambda : list_product_edit_save (top_list_product_edit_gui,name,price,e_product_name,e_product_price,e_product_hsn,e_product_tax))
    b_product_save.place(x=int(w/3.7),y=int(h/1.7))

    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        top_list_product_edit_gui.destroy()
        error("Select Any item first!")
        return
    name=item_list[1]
    price=item_list[4]
    hsn=item_list[2]
    tax=item_list[3]


    e_product_name.insert(0,name)
    e_product_price.insert(0,price)
    e_product_hsn.insert(0,hsn)
    e_product_tax.insert(0,tax)

def list_customer_edit_gui(tree):
    top_list_customer_edit_gui = tk.Toplevel()
    top_list_customer_edit_gui.geometry(str(int(w/2)) + 'x' + str(int(h/1.3)))
    flist_customer_edit_gui= tk.Frame(top_list_customer_edit_gui, bg = "white", height=int(h/1.3), width=int(w/2))
    flist_customer_edit_gui.pack()
    l_company_name=tk.Label(flist_customer_edit_gui, text="Name             :", bg="white", font=("Arial", 15 ))
    l_company_name.place(x=int(w/12),y=int(h/8))
    l_company_address=tk.Label(flist_customer_edit_gui, text="Address         :", bg="white", font=("Arial", 15 ))
    l_company_address.place(x=int(w/12),y=int(h/5))
    l_company_gst=tk.Label(flist_customer_edit_gui, text="GST NO         :", bg="white", font=("Arial", 15 ))
    l_company_gst.place(x=int(w/12),y=int(h/3))
    l_company_phone=tk.Label(flist_customer_edit_gui, text="Phone NO      :", bg="white", font=("Arial", 15 ))
    l_company_phone.place(x=int(w/12),y=int(h/2.5))
    l_company_mail=tk.Label(flist_customer_edit_gui, text="Email             :", bg="white", font=("Arial", 15 ))
    l_company_mail.place(x=int(w/12),y=int(h/2.1))
    


    e_company_name=tk.Entry(flist_customer_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_name.place(x=int(w/4.3),y=int(h/8))
    e_company_address= tk.Text(flist_customer_edit_gui,width=25,height=4, bg="gray93", font=("Arial", 15 ))
    e_company_address.place(x=int(w/4.3),y=int(h/5))
    e_company_gst=tk.Entry(flist_customer_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_gst.place(x=int(w/4.3),y=int(h/3))
    e_company_phone=tk.Entry(flist_customer_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_phone.place(x=int(w/4.3),y=int(h/2.5))
    e_company_mail=tk.Entry(flist_customer_edit_gui,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_mail.place(x=int(w/4.3),y=int(h/2.1))

    b_company_save= tk.Button(flist_customer_edit_gui, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                              command= lambda : list_customer_edit_save(top_list_customer_edit_gui,name,address,phone,e_company_name,e_company_address,e_company_gst,e_company_phone,e_company_mail) )
    b_company_save.place(x=int(w/3.7),y=int(h/1.7))

    curItem = tree.focus()
    items = (tree.item(curItem))
    item_list=(items.get("values"))
    if item_list == "":
        top_list_customer_edit_gui.destroy()
        error("Select Any item first!")
        return
    name=item_list[1]
    address=item_list[2]
    gst=item_list[3]
    phone=item_list[4]
    email=item_list[5]

    e_company_name.insert(0,name)
    e_company_address.insert(END,address)
    e_company_gst.insert(0,gst)
    e_company_phone.insert(0,phone)
    e_company_mail.insert(0,email)


    
    
        

def company_details():                                           ###Company Details Settings
    top_company_details = tk.Tk(className=' Company Details ')
    top_company_details.geometry(str(w) + 'x' + str(h))
    top_company_details.state('zoomed')   
    fcompany_details= tk.Frame(top_company_details, bg = "white", height=h, width=w)
    fcompany_details.pack()
    l_company_details=tk.Label(fcompany_details, text="Company Details", bg="white", font=("Arial", 20, "bold" ))
    l_company_details.place(x=int(w/13),y=int(h/18))
    l_company_name=tk.Label(fcompany_details, text="Name         :", bg="white", font=("Arial", 15 ))
    l_company_name.place(x=int(w/6),y=int(h/6))
    l_company_address=tk.Label(fcompany_details, text="Address      :", bg="white", font=("Arial", 15 ))
    l_company_address.place(x=int(w/6),y=int(h/4))
    l_company_Mobile=tk.Label(fcompany_details, text="Mobile         :", bg="white", font=("Arial", 15 ))
    l_company_Mobile.place(x=int(w/6),y=int(h/2.4))
    l_company_tax=tk.Label(fcompany_details, text="Tax            :", bg="white", font=("Arial", 15 ))
    l_company_tax.place(x=int(w/6),y=int(h/2))

    l_company_hsn=tk.Label(fcompany_details, text="HSN            :", bg="white", font=("Arial", 15 ))
    l_company_hsn.place(x=int(w/6),y=int(h/1.7))

    
    l_company_gst=tk.Label(fcompany_details, text="GST       :", bg="white", font=("Arial", 15 ))
    l_company_gst.place(x=int(w/1.6),y=int(h/6))
    l_company_mail=tk.Label(fcompany_details, text="Mail        :", bg="white", font=("Arial", 15 ))
    l_company_mail.place(x=int(w/1.6),y=int(h/4))
    l_company_phone=tk.Label(fcompany_details, text="Phone      :", bg="white", font=("Arial", 15 ))
    l_company_phone.place(x=int(w/1.6),y=int(h/3))
    l_company_notes=tk.Label(fcompany_details, text="Notes      :", bg="white", font=("Arial", 15 ))
    l_company_notes.place(x=int(w/1.6),y=int(h/2.5))
    

    e_company_name=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_name.place(x=int(w/3.7),y=int(h/6))
    e_company_address=tk.Text(fcompany_details,width=25, height=5, bg="gray93", font=("Arial", 15 ))
    e_company_address.place(x=int(w/3.7),y=int(h/4))
    e_company_Mobile=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_Mobile.place(x=int(w/3.7),y=int(h/2.4))
    e_company_tax=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_tax.place(x=int(w/3.7),y=int(h/2))

    e_company_hsn=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_hsn.place(x=int(w/3.7),y=int(h/1.7))

    
    e_company_gst=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_gst.place(x=int(w/1.4),y=int(h/6))
    e_company_mail=tk.Entry(fcompany_details,width=25, bg="gray93", font=("Arial", 15 ))
    e_company_mail.place(x=int(w/1.4),y=int(h/3.95))
    e_company_phone=tk.Entry(fcompany_details,width=25,bg="gray93", font=("Arial", 15 ))
    e_company_phone.place(x=int(w/1.4),y=int(h/2.98))
    e_company_notes=tk.Text(fcompany_details,width=25, height=5, bg="gray93", font=("Arial", 15 ))
    e_company_notes.place(x=int(w/1.4),y=int(h/2.5))

    b_company_save= tk.Button(fcompany_details, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                              command = lambda: save_company_details_db(e_company_name,e_company_address,e_company_Mobile,e_company_tax,e_company_gst,e_company_mail,
                                                                        e_company_phone,e_company_notes,e_company_hsn))
    b_company_save.place(x=int(w/3.7),y=int(h/1.4))
    

    b_user_details= tk.Button(fcompany_details, width=20, text="Change Password", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                              command = lambda: password_change(fcompany_details,top_company_details))
    b_user_details.place(x=int(w/1.4),y=int(h/1.6))

    
    query="SELECT * from COMPANY"
    results=conn.execute(query)
    try:
        for i in results:
            name=i[0]
            address=i[1]
            mobile=i[2]
            phone=i[3]
            email=i[4]
            tax=i[5]
            gst=i[6]
            notes=i[7]
            hsn=i[8]

            e_company_name.insert(0,name)
            e_company_address.insert(END,str(address))
            e_company_Mobile.insert(0,str(mobile))
            e_company_tax.insert(0,tax)
            e_company_gst.insert(0,str(gst))
            e_company_mail.insert(0,str(email))
            e_company_phone.insert(0,str(phone))
            e_company_notes.insert(END,str(notes))
            e_company_hsn.insert(0,str(hsn))
    except:
        pass

            
    mainloop()
    

def button_backup_save(entry):
    filename=entry.get()
    if filename != "":
        dst=filename+"/backup.db"
        src=(r"C:\ProgramData\Secure_Tech\Secure Tech.db")
        copyfile(src, dst)
        error("Backup Saved")
    else:
        pass

def button_restore_save(entry):
    filename=entry.get()
    if filename != "" :
        global conn
        global cursor
        conn.close()
        dst=(r"C:\ProgramData\Secure_Tech\Secure Tech.db")
        copyfile(filename, dst)
        conn = sqlite3.connect(r'C:\ProgramData\Secure_Tech\Secure Tech.db')
        cursor= conn.cursor()
        error("Successfully Restored!")
    else:
        pass

def button_backup(entry):
    filename = filedialog.askdirectory()
    entry.insert(0,str(filename))
def button_restore(entry):
    filename = askopenfilename(filetypes=[('Data Base File','*.db')])
    entry.insert(0,str(filename))
def new_restore():                      #Start A Restore from a restore file 
    filename = askopenfilename(filetypes=[('Data Base File','*.db')])
    if filename != "" :
        global conn
        global cursor
        conn.close()
        dst=(r"C:\ProgramData\Secure_Tech\Secure Tech.db")
        copyfile(filename, dst)
        conn = sqlite3.connect(r'C:\ProgramData\Secure_Tech\Secure Tech.db')
        cursor= conn.cursor()
        error("Backup file Restored!")
    else:
        pass
    

def new_backup():                       # Create a backup file

    filename = filedialog.askdirectory()
    if filename != "":
        dst=filename+"/backup.db"
        src=(r"C:\ProgramData\Secure_Tech\Secure Tech.db")
        copyfile(src, dst)
        error("Backup file Saved!")
    else:
        pass
    


def list_invoice():
    top_list_invoice = tk.Tk(className=' Search invoice ')
    top_list_invoice.geometry(str(w) + 'x' + str(h))
    top_list_invoice.state('zoomed')   
    flist_invoice= tk.Frame(top_list_invoice, bg = "white", height=h, width=w)
    flist_invoice.pack()


    l_customer_name=tk.Label(flist_invoice, text="Customer's Name         :", bg="white", font=("Arial", 15 ))
    l_customer_name.place(x=int(w/6),y=int(h/8))
    l_gst_no=tk.Label(flist_invoice, text="GST No         :", bg="white", font=("Arial", 15 ))
    l_gst_no.place(x=int(w/1.6),y=int(h/20))
    l_invoice_no=tk.Label(flist_invoice, text="Invoice No   \t      :", bg="white", font=("Arial", 15 ))
    l_invoice_no.place(x=int(w/6),y=int(h/20))    
    l_date_from=tk.Label(flist_invoice, text="Date              :", bg="white", font=("Arial", 15 ))
    l_date_from.place(x=int(w/1.6),y=int(h/8))



    e_customer_name=tk.Entry(flist_invoice, width=25, bg= "gray93", font=("Arial", 15 ))
    e_customer_name.place(x=int(w/3),y=int(h/7.8))
    e_gst_no=tk.Entry(flist_invoice, width=25, bg= "gray93", font=("Arial", 15 ))
    e_gst_no.place(x=int(w/1.37),y=int(h/20))
    e_invoice_no=tk.Entry(flist_invoice, width=25, bg= "gray93", font=("Arial", 15 ))
    e_invoice_no.place(x=int(w/3),y=int(h/20))

    cal_from = DateEntry(flist_invoice, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_from.place(x=int(w/1.37),y=int(h/7.6))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree_list_invoice = ttk.Treeview(flist_invoice, columns=('0', '1', '2','3','4'), show='headings', height=15)
    tree_list_invoice.heading('0', text="S.NO")
    tree_list_invoice.column('0',anchor=CENTER, minwidth=0, width=70, stretch=NO)
    tree_list_invoice.heading('1', text="Customer's Name")
    tree_list_invoice.column('1',anchor=CENTER, minwidth=0, width=300, stretch=NO)
    tree_list_invoice.heading('2', text="Invoice No")
    tree_list_invoice.column('2',anchor=CENTER, minwidth=0, width=160, stretch=NO)
    tree_list_invoice.heading('3', text="Date")
    tree_list_invoice.column('3',anchor=CENTER, minwidth=0, width=160, stretch=NO)
    tree_list_invoice.heading('4', text="GST No")
    tree_list_invoice.column('4',anchor=CENTER, minwidth=0, width=200, stretch=NO)
    tree_list_invoice.place(x=int(w/6),y=int(h/3.4))

    b_invoice_search= tk.Button(flist_invoice, width=10, text="SEARCH", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                 command= lambda: search_invoice(tree_list_invoice,e_customer_name.get(),e_gst_no.get(),e_invoice_no.get(),cal_from.get()))
    b_invoice_search.place(x=int(w/1.415), y=int(h/4.7))
    #b_invoice_preview= tk.Button(flist_invoice, width=10, text="PREVIEW", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                 #command= lambda: invoice_preview_show(tree_list_invoice,"invoice"))
    #b_invoice_preview.place(x=int(w/1.5), y=int(h/1.27))
    b_invoice_delete= tk.Button(flist_invoice, width=10, text="DELETE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                command= lambda: list_invoice_delete(tree_list_invoice,top_list_invoice))
    b_invoice_delete.place(x=int(w/1.7), y=int(h/1.27))
    
    b_invoice_edit= tk.Button(flist_invoice, width=10, text="VIEW", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                 command= lambda: invoice_edit(tree_list_invoice))
    b_invoice_edit.place(x=int(w/1.97), y=int(h/1.27))
    
    vsb = ttk.Scrollbar(flist_invoice, orient="vertical", command=tree_list_invoice.yview)
    vsb.place(x=int((w/6)+880),y=int(h/3.45),width=16, height = 330)
    tree_list_invoice.configure(yscrollcommand=vsb.set)


    query=("SELECT NAME, ID, DATE, GST from INVOICE ORDER BY SNO DESC")
    data=conn.execute(query,)
    k=1
    list_abcd=[]
    for i in data:
        name_1=i[0]
        invoice_1=i[1]
        date=i[2]
        gst=i[3]
        tree_list_invoice.insert("",index='end',  values=(str(k),str(name_1), str(invoice_1),str(date),str(gst)))
        k=k+1
        
        



def list_quotation():
    top_list_quotation = tk.Tk(className=' Search Quotation ')
    top_list_quotation.geometry(str(w) + 'x' + str(h))
    top_list_quotation.state('zoomed')   
    flist_quotation= tk.Frame(top_list_quotation, bg = "white", height=h, width=w)
    flist_quotation.pack()
    l_customer_name=tk.Label(flist_quotation, text="Customer's Name         :", bg="white", font=("Arial", 15 ))
    l_customer_name.place(x=int(w/6),y=int(h/8))
    l_gst_no=tk.Label(flist_quotation, text="GST No         :", bg="white", font=("Arial", 15 ))
    l_gst_no.place(x=int(w/1.6),y=int(h/20))
    l_invoice_no=tk.Label(flist_quotation, text="Quotation No   \t      :", bg="white", font=("Arial", 15 ))
    l_invoice_no.place(x=int(w/6),y=int(h/20))    
    l_date_from=tk.Label(flist_quotation, text="Date              :", bg="white", font=("Arial", 15 ))
    l_date_from.place(x=int(w/1.6),y=int(h/8))

    e_customer_name=tk.Entry(flist_quotation, width=25, bg= "gray93", font=("Arial", 15 ))
    e_customer_name.place(x=int(w/3),y=int(h/7.8))
    e_gst_no=tk.Entry(flist_quotation, width=25, bg= "gray93", font=("Arial", 15 ))
    e_gst_no.place(x=int(w/1.37),y=int(h/20))
    e_quotation_no=tk.Entry(flist_quotation, width=25, bg= "gray93", font=("Arial", 15 ))
    e_quotation_no.place(x=int(w/3),y=int(h/20))
    cal_from = DateEntry(flist_quotation, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_from.place(x=int(w/1.37),y=int(h/7.6))



    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree_list_quotation = ttk.Treeview(flist_quotation, columns=('0', '1', '2','3','4'), show='headings', height=15)
    tree_list_quotation.heading('0', text="S.NO")
    tree_list_quotation.column('0',anchor=CENTER, minwidth=0, width=70, stretch=NO)
    tree_list_quotation.heading('1', text="Customer's Name")
    tree_list_quotation.column('1',anchor=CENTER, minwidth=0, width=300, stretch=NO)
    tree_list_quotation.heading('2', text="Quotation No")
    tree_list_quotation.column('2',anchor=CENTER, minwidth=0, width=160, stretch=NO)
    tree_list_quotation.heading('3', text="Date")
    tree_list_quotation.column('3',anchor=CENTER, minwidth=0, width=160, stretch=NO)
    tree_list_quotation.heading('4', text="GST No")
    tree_list_quotation.column('4',anchor=CENTER, minwidth=0, width=200, stretch=NO)
    tree_list_quotation.place(x=int(w/6),y=int(h/3.4))


    b_quotation_search= tk.Button(flist_quotation, width=10, text="SEARCH", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                  command= lambda: search_quotation(tree_list_quotation,e_customer_name.get(),e_gst_no.get(),e_quotation_no.get(),cal_from.get()))
    b_quotation_search.place(x=int(w/1.415), y=int(h/4.7))
    #b_quotation_preview= tk.Button(flist_quotation, width=10, text="PREVIEW", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                    #command= lambda: invoice_preview_show(tree_list_quotation,"quotation"))
    #b_quotation_preview.place(x=int(w/1.5), y=int(h/1.27))
    b_quotation_delete= tk.Button(flist_quotation, width=10, text="DELETE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                  command= lambda: list_quotation_delete(tree_list_quotation,top_list_quotation))
    b_quotation_delete.place(x=int(w/1.45), y=int(h/1.27))

    
    b_quotation_edit= tk.Button(flist_quotation, width=10, text="VIEW", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                  command= lambda: quotation_edit(tree_list_quotation))
    
    b_quotation_edit.place(x=int(w/1.72), y=int(h/1.27))
    vsb = ttk.Scrollbar(flist_quotation, orient="vertical", command=tree_list_quotation.yview)
    vsb.place(x=int(w/6+888),y=int(h/3.45),width=16, height = 330)
    tree_list_quotation.configure(yscrollcommand=vsb.set)

    

    query=("SELECT NAME, ID, DATE, GST from QUOTATION")
    data=conn.execute(query,)
    k=1
    for i in data:
        name_1=i[0]
        invoice_1=i[1]
        date=i[2]
        gst=i[3]
        tree_list_quotation.insert("",index='end',  values=(str(k), str(name_1), str(invoice_1),str(date),str(gst)))
        k=k+1







def list_products():
    global top_list_products
    top_list_products = tk.Tk(className=' Search Products ')
    top_list_products.geometry(str(w) + 'x' + str(h))
    top_list_products.state('zoomed')
    flist_products= tk.Frame(top_list_products, bg = "white", height=h, width=w)
    flist_products.pack()
    l_name=tk.Label(flist_products, text="Name         :", bg="white", font=("Arial", 15 ))
    l_name.place(x=int(w/6),y=int(h/8))
    l_price=tk.Label(flist_products, text="Price\t   :", bg="white", font=("Arial", 15 ))
    l_price.place(x=int(w/6),y=int(h/5))
    l_hsn=tk.Label(flist_products, text="HSN No   :", bg="white", font=("Arial", 15 ))
    l_hsn.place(x=int(w/1.6),y=int(h/8))
    l_tax=tk.Label(flist_products, text="Tax     \t :", bg="white", font=("Arial", 15 ))
    l_tax.place(x=int(w/1.6),y=int(h/5))

    
    e_name=tk.Entry(flist_products, width=25, bg= "gray93", font=("Arial", 15 ))
    e_name.place(x=int(w/3.8),y=int(h/7.8))
    e_price=tk.Entry(flist_products, width=25, bg= "gray93", font=("Arial", 15 ))
    e_price.place(x=int(w/3.8),y=int(h/4.95))
    e_hsn=tk.Entry(flist_products, width=25, bg= "gray93", font=("Arial", 15 ))
    e_hsn.place(x=int(w/1.41),y=int(h/7.8))
    e_tax=tk.Entry(flist_products, width=25, bg= "gray93", font=("Arial", 15 ))
    e_tax.place(x=int(w/1.41),y=int(h/4.95))

    b_product_search= tk.Button(flist_products, width=10, text="SEARCH", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                command = lambda : show_product_from_db(tree_list_product,e_name,e_hsn,e_tax,e_price))
    b_product_search.place(x=int(w/1.415), y=int(h/3.5))
    b_product_edit= tk.Button(flist_products, width=10, text="EDIT", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                              command =lambda :list_product_edit_gui(tree_list_product))
    b_product_edit.place(x=int(w/1.415), y=int(h/1.2))
    b_product_delete= tk.Button(flist_products, width=10, text="DELETE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                command= lambda : list_product_delete(tree_list_product,top_list_products))
    b_product_delete.place(x=int(w/1.25), y=int(h/1.2))


    
    tree_list_product = ttk.Treeview(flist_products, columns=('0', '1', '2','3','4'), show='headings', height=17)
    tree_list_product.heading('0', text="S.NO")
    tree_list_product.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_list_product.heading('1', text="Name")
    tree_list_product.column('1', anchor=CENTER,minwidth=0, width=410, stretch=NO)
    tree_list_product.heading('2', text="HSN")
    tree_list_product.column('2', anchor=CENTER,minwidth=0, width=180, stretch=NO)
    tree_list_product.heading('3', text="Tax")
    tree_list_product.column('3', anchor=CENTER,minwidth=0, width=140, stretch=NO)
    tree_list_product.heading('4', text="Price")
    tree_list_product.column('4', anchor=CENTER,minwidth=0, width=190, stretch=NO)
    tree_list_product.place(x=int(w/5.9),y=int(h/3))
    vsb = ttk.Scrollbar(flist_products, orient="vertical", command=tree_list_product.yview)
    vsb.place(x=int(w/5.9+1000),y=int(h/3),width=16, height = 370)
    tree_list_product.configure(yscrollcommand=vsb.set)



    query=("SELECT * from PRODUCT")
    data=conn.execute(query,)
    k=1
    for i in data:
        name=i[1]
        price=i[2]
        hsn=i[3]
        tax=i[4]
        tree_list_product.insert("",index='end',  values=(str(k), str(name), str(hsn),str(tax),str(price)))
        k+=1


#########################################################################################################################################################################



    
def list_customer():                                        ###########################################
    top_list_customer = tk.Tk(className=' Search Customers ')
    top_list_customer.geometry(str(w) + 'x' + str(h))
    top_list_customer.state('zoomed')
    flist_customer= tk.Frame(top_list_customer, bg = "white", height=h, width=w)
    flist_customer.pack()
    l_name=tk.Label(flist_customer, text="Name         :", bg="white", font=("Arial", 15 ))
    l_name.place(x=int(w/6),y=int(h/8))
    l_phone=tk.Label(flist_customer, text="Phone No   :", bg="white", font=("Arial", 15 ))
    l_phone.place(x=int(w/6),y=int(h/5))
    l_gst=tk.Label(flist_customer, text="GST No   :", bg="white", font=("Arial", 15 ))
    l_gst.place(x=int(w/1.6),y=int(h/8))


    e_name=tk.Entry(flist_customer, width=25, bg= "gray93", font=("Arial", 15 ))
    e_name.place(x=int(w/3.8),y=int(h/7.8))
    e_phone=tk.Entry(flist_customer, width=25, bg= "gray93", font=("Arial", 15 ))
    e_phone.place(x=int(w/3.8),y=int(h/4.95))
    e_gst=tk.Entry(flist_customer, width=25, bg= "gray93", font=("Arial", 15 ))
    e_gst.place(x=int(w/1.41),y=int(h/7.8))

    
    b_customer_search= tk.Button(flist_customer, width=10, text="SEARCH", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                 command= lambda :show_customers_from_db(tree_list_customer,e_name,e_phone,e_gst))
    b_customer_search.place(x=int(w/1.415), y=int(h/5))
    b_customer_edit= tk.Button(flist_customer, width=10, text="EDIT", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                               command= lambda :list_customer_edit_gui(tree_list_customer))
    b_customer_edit.place(x=int(w/1.415), y=int(h/1.2))
    b_customer_delete= tk.Button(flist_customer, width=10, text="DELETE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                                 command= lambda :list_customer_delete(tree_list_customer,top_list_customer))
    b_customer_delete.place(x=int(w/1.2), y=int(h/1.2))




    tree_list_customer = ttk.Treeview(flist_customer, columns=('0', '1', '2','3','4','5'), show='headings', height=17)
    tree_list_customer.heading('0', text="S.NO")
    tree_list_customer.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_list_customer.heading('1', text="Name")
    tree_list_customer.column('1', anchor=CENTER,minwidth=0, width=200, stretch=NO)
    tree_list_customer.heading('2', text="Address")
    tree_list_customer.column('2', anchor=CENTER,minwidth=0, width=350, stretch=NO)
    tree_list_customer.heading('3', text="GST No")
    tree_list_customer.column('3', anchor=CENTER,minwidth=0, width=120, stretch=NO)
    tree_list_customer.heading('4', text="Phone Number")
    tree_list_customer.column('4', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree_list_customer.heading('5', text="Email")
    tree_list_customer.column('5', anchor=CENTER,minwidth=0, width=250, stretch=NO)
    tree_list_customer.place(x=int(w/9.8),y=int(h/3))
    vsb = ttk.Scrollbar(flist_customer, orient="vertical", command=tree_list_customer.yview)
    vsb.place(x=int(w/9.8+1150),y=int(h/3),width=16, height = 370)
    tree_list_customer.configure(yscrollcommand=vsb.set)

    
    query=("SELECT * from CUSTOMER")
    data=conn.execute(query,)
    k=1
    for i in data:
        name=i[1]
        address=i[2]
        gst=i[3]
        mobile=i[4]
        email=i[5]
        tree_list_customer.insert("",index='end',  values=(str(k), str(name), str(address),str(gst),str(mobile),str(email)))
        k+=1



    
def backup():
    top4 = tk.Toplevel()
    top4.geometry(str(w) + 'x' + str(h))
    top4.state('zoomed')
    fbackup= tk.Frame(top4, bg = "white", height=h, width=w)
    fbackup.pack()
    l_backup=tk.Label(fbackup, text="Backup", font=("Arial", 15, "bold" ) , bg = "white")
    l_backup.place(x=int(w/10),y=int(h/8))
    l_backup_location=tk.Label(fbackup, text="Location: ", font=("Arial", 15 ) , bg = "white")
    l_backup_location.place(x=int(w/6),y=int(h/4.4)) 


    l_restore=tk.Label(fbackup, text="Restore", font=("Arial", 15, "bold" ) , bg = "white")
    l_restore.place(x=int(w/10),y=int(h/2.5))
    l_restore_location=tk.Label(fbackup, text="Location: ", font=("Arial", 15 ) , bg = "white")
    l_restore_location.place(x=int(w/6),y=int(h/2))


    e_location1=tk.Entry(fbackup, width=50, bg= "gray93", font=("Arial", 15 ))
    e_location1.place(x=int(w/4.1),y=int(h/4.3))
    e_location2=tk.Entry(fbackup, width=50, bg= "gray93", font=("Arial", 15 ))
    e_location2.place(x=int(w/4.1),y=int(h/1.98))
    


    b_backup= tk.Button(fbackup, width=10, text="BACKUP", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                        command= lambda: button_backup_save(e_location1))
    b_backup.place(x=int(w/1.71), y=int(h/3))
    b_restore= tk.Button(fbackup, width=10, text="RESTORE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white", relief=FLAT,
                         command= lambda: button_restore_save(e_location2))
    b_restore.place(x=int(w/1.71), y=int(h/1.6))

    img = tk.PhotoImage(master = top4, file="folder.png")
    
    b_folder1=tk.Button(fbackup, image=img, relief=FLAT, bg="white",command= lambda: button_backup(e_location1))
    b_folder1.place(x=int(w/1.59),y=int(h/4.35))
    b_folder2=tk.Button(fbackup, image=img, relief=FLAT, bg="white",command= lambda: button_restore(e_location2))
    b_folder2.place(x=int(w/1.59),y=int(h/2)) 
    mainloop()







    
def new_product():
    #top.destroy()
    top3 = tk.Tk(className=' New Product')
    top3.geometry(str(w) + 'x' + str(h))
    top3.state('zoomed')
    fnew_product= tk.Frame(top3, bg = "white", height=h, width=w)
    fnew_product.grid(row=0,column=0)
    lproduct_name=tk.Label(top3, text="Product Name  :", bg="white", font=("Arial", 15 ))
    lproduct_name.place(x=int(w/10),y=int(h/10))    
    lproduct_price=tk.Label(top3, text="Product Price   :", bg="white", font=("Arial", 15 ))
    lproduct_price.place(x=int(w/10),y=int(h/6))
    lproduct_hsn=tk.Label(top3, text="HSN  :", bg="white", font=("Arial", 15 ))
    lproduct_hsn.place(x=int(w/1.8),y=int(h/10))
    lproduct_Tax=tk.Label(top3, text="Tax   :", bg="white", font=("Arial", 15 ))
    lproduct_Tax.place(x=int(w/1.8),y=int(h/6))
    


    eproduct_name= tk.Entry(top3, width =25, font=("Arial", 15 ), bg= "gray93")
    eproduct_name.place(x=int(w/4.4),y=int(h/9.7))
    eproduct_price= tk.Entry(top3, width =25, font=("Arial", 15 ), bg= "gray93")
    eproduct_price.place(x=int(w/4.4),y=int(h/5.8))
    eproduct_hsn= tk.Entry(top3, width =25, font=("Arial", 15 ), bg= "gray93")
    eproduct_hsn.place(x=int(w/1.6),y=int(h/9.7))
    n = tk.StringVar() 
    taxchoosen = tk.Entry(top3, width =25, font=("Arial", 15 ), bg= "gray93")
    taxchoosen.place(x=int(w/1.6),y=int(h/6))


    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            taxchoosen.insert(0,str(i[0]))
    except:
        pass
    try:
        query =("SELECT HSN FROM COMPANY")
        results=conn.execute(query)
        for i in results:
            eproduct_hsn.insert(0,(i))
        
    except:
        pass


    b_product_add= tk.Button(top3, width=10, text="ADD", font=("Arial", 10, "bold"), bg="dodger blue",
                             fg="white", relief=FLAT, command= lambda: NEW_PRODUCT_add_to_list(eproduct_name,eproduct_price,eproduct_hsn,taxchoosen,tree_product))
    b_product_add.place(x=int(w/1.45), y=int(h/3))
    b_product_save= tk.Button(top3, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                              command= lambda: new_product_save(tree_product,top3),relief=FLAT)
    b_product_save.place(x=int(w/1.45), y=int(h/1.3))
    b_product_edit= tk.Button(top3, width=10, text="EDIT", font=("Arial", 10, "bold"), bg="dodger blue",
                              command= lambda: NEW_PRODUCT_edit_select(tree_product), fg="white", relief=FLAT)
    b_product_edit.place(x=int(w/1.64), y=int(h/1.3))
    b_product_clear= tk.Button(top3, width=10, text="CLEAR", font=("Arial", 10, "bold"), bg="dodger blue",
                               command= lambda: NEW_PRODUCT_clear(tree_product),fg="white", relief=FLAT)
    b_product_clear.place(x=int(w/1.3), y=int(h/1.3))
    tree_product = ttk.Treeview(top3, columns=('0', '1', '2','3','4'), show='headings')


    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 12))
    
    tree_product.heading('0', text="S.NO")
    tree_product.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_product.heading('1', text="Product Name")
    tree_product.column('1', anchor=CENTER,minwidth=0, width=350, stretch=NO)
    tree_product.heading('2', text="Price")
    tree_product.column('2', anchor=CENTER,minwidth=0, width=110, stretch=NO)
    tree_product.heading('3', text="HSN No")
    tree_product.column('3', anchor=CENTER,minwidth=0, width=220, stretch=NO)
    tree_product.heading('4', text="Tax")
    tree_product.column('4', anchor=CENTER,minwidth=0, width=110, stretch=NO)
    tree_product.place(x=int(w/6.5),y=int(h/2.4))
    tree_product.tag_configure('monospace', font='courier')

    vsb = ttk.Scrollbar(top3, orient="vertical", command=tree_product.yview)
    vsb.place(x=int(w/6.5+870),y=int(h/2.41),width=16, height = 230)
    tree_product.configure(yscrollcommand=vsb.set)
    mainloop()



    
def new_customer():
    global x_new_customer
    x_new_customer=1
    #top.destroy()
    top2 = tk.Tk(className=' New Customer')
    top2.geometry(str(w) + 'x' + str(h))
    top2.state('zoomed')
    fcustomer= tk.Frame(top2, bg = "white", height=h, width=w)
    fcustomer.grid(row=0,column=0)
    lname=tk.Label(top2, text="Customer Name  :", bg="white", font=("Arial", 15 ))
    lname.place(x=int(w/10),y=int(h/20))
    laddress= tk.Label(top2, text="Address\t           :", font=("Arial", 15 ), bg= "white")
    laddress.place(x=int(w/10),y=int(h/8.5))
    lgst= tk.Label(top2, text="GST No              : ", font=("Arial", 15 ), bg= "white")
    lgst.place(x=int(w/10),y=int(h/3.9))
    ldate=tk.Label(top2, text="Date     \t           :", font=("Arial", 15 ), bg= "white")
    ldate.place(x=int(w/1.8),y=int(h/3.9))
    lmobile=tk.Label(top2, text="Mobile Number    : ", font=("Arial", 15 ), bg= "white")
    lmobile.place(x=int(w/1.8),y=int(h/6.6))
    lemail=tk.Label(top2, text="Email ID\t           :", font=("Arial", 15 ), bg= "white")
    lemail.place(x=int(w/1.8),y=int(h/20))
    


    ename= tk.Entry(top2, width =25, font=("Arial", 15 ), bg= "gray93")
    ename.place(x=int(w/4.4),y=int(h/19))
    eaddress= tk.Text(top2, width =25,height=3, font=("Arial", 15 ), bg= "gray93")
    eaddress.place(x=int(w/4.4),y=int(h/8.3))
    egst= tk.Entry(top2, width =25, font=("Arial", 15 ), bg= "gray93")
    egst.place(x=int(w/4.4),y=int(h/3.8))
    edate= DateEntry(top2, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    edate.place(x=int(w/1.45),y=int(h/3.84))
    emobile= tk.Entry(top2, width =25, font=("Arial", 15 ), bg= "gray93")
    emobile.place(x=int(w/1.45),y=int(h/6.5))
    email= tk.Entry(top2, width =25, font=("Arial", 15 ), bg= "gray93")
    email.place(x=int(w/1.45),y=int(h/19))


    b_add= tk.Button(top2, width=10, text="ADD", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                      command= lambda: new_customer_add(tree_customer,ename.get(),eaddress.get('1.0', END),egst.get(),emobile.get(),email.get()),relief=FLAT)
    b_add.place(x=int(w/1.45), y=int(h/3))
    b_save= tk.Button(top2, width=10, text="SAVE", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                      command= lambda: new_customer_save(tree_customer,top2),relief=FLAT)
    b_save.place(x=int(w/1.45), y=int(h/1.3))
    b_edit= tk.Button(top2, width=10, text="EDIT", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                      command= lambda: new_customer_edit_select(tree_customer),relief=FLAT)
    b_edit.place(x=int(w/1.64), y=int(h/1.3))
    b_clear= tk.Button(top2, width=10, text="CLEAR", font=("Arial", 10, "bold"), bg="dodger blue", fg="white",
                       command= lambda: new_customer_clear(tree_customer), relief=FLAT)
    b_clear.place(x=int(w/1.3), y=int(h/1.3))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))

    tree_customer = ttk.Treeview(top2, columns=('0', '1', '2','3','4','5'), show='headings')
    tree_customer.heading('0', text="S.NO")
    tree_customer.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree_customer.heading('1', text="Name")
    tree_customer.column('1', anchor=CENTER,minwidth=0, width=170, stretch=NO)
    tree_customer.heading('2', text="Address")
    tree_customer.column('2', anchor=CENTER,minwidth=0, width=300, stretch=NO)
    tree_customer.heading('3', text="GST No")
    tree_customer.column('3', anchor=CENTER,minwidth=0, width=175, stretch=NO)
    tree_customer.heading('4', text="Mobile No")
    tree_customer.column('4', anchor=CENTER,minwidth=0, width=175, stretch=NO)
    tree_customer.heading('5', text="Email")
    tree_customer.column('5', anchor=CENTER,minwidth=0, width=175, stretch=NO)
    tree_customer.place(x=int(w/9.8),y=int(h/2.4))
    vsb = ttk.Scrollbar(top2, orient="vertical", command=tree_customer.yview)
    vsb.place(x=int(w/9.8+1070),y=int(h/2.41),width=16, height = 230)
    tree_customer.configure(yscrollcommand=vsb.set)




    
def new_quotation():
    #top.destroy()
    global top1
    top1 = tk.Tk(className=' New Quotation')
    top1.geometry(str(w) + 'x' + str(h))
    top1.state('zoomed')
    global fnew_quotation
    fnew_quotation= tk.Frame(top1, bg = "white", height=h, width=w)
    fnew_quotation.grid(row=0,column=0)

    lcustomer2= tk.Label(fnew_quotation, text="Customer: ", font=("Arial", 15 ), bg= "white")
    lcustomer2.place(x=int(w/10),y=int(h/20))
    laddress= tk.Label(fnew_quotation, text="Address  : ", font=("Arial", 15 ), bg= "white")
    laddress.place(x=int(w/10),y=int(h/8.5))
    lgst= tk.Label(fnew_quotation, text="GST NO  : ", font=("Arial", 15 ), bg= "white")
    lgst.place(x=int(w/10),y=int(h/5.5))
    lquotation_num=tk.Label(fnew_quotation, text="Quotation No  : ", font=("Arial", 15 ), bg= "white")
    lquotation_num.place(x=int(w/1.8),y=int(h/8.5))
    ldate=tk.Label(fnew_quotation, text="Date\t       :", font=("Arial", 15 ), bg= "white")
    ldate.place(x=int(w/1.8),y=int(h/5.5))
    lproduct=tk.Label(fnew_quotation, text="Product:", font=("Arial", 15 ), bg= "white")
    lproduct.place(x=int(w/10),y=int(h/4.2))
    lqty=tk.Label(fnew_quotation, text="QTY:", font=("Arial", 15 ), bg= "white")
    lqty.place(x=int(w/3.5),y=int(h/4.2))
    lunit_price=tk.Label(fnew_quotation, text="Unit Price:", font=("Arial", 15 ), bg= "white")
    lunit_price.place(x=int(w/2.5),y=int(h/4.2))
    ltax=tk.Label(fnew_quotation, text="Tax:", font=("Arial", 15 ), bg= "white")
    ltax.place(x=int(w/1.95),y=int(h/4.2))
    
    lhsn=tk.Label(fnew_quotation, text="HSN:", font=("Arial", 15 ), bg= "white")
    lhsn.place(x=int(w/1.61),y=int(h/4.2))
    lmobile= tk.Label(fnew_quotation, text="Mobile\t      : ", font=("Arial", 15 ), bg= "white")
    lmobile.place(x=int(w/1.8),y=int(h/20))
    
    lnote=tk.Label(fnew_quotation, text="Note  : ", font=("Arial", 15 ), bg= "white")
    lnote.place(x=int(w/10),y=int(h/1.5))


    global ecustomer3
    global eaddress_q
    global egst_q
    global emobile_q
    global eproduct_q
    global ehsn_q
    global eunit_price_q
    global etax_q
    global cal_new_quotation
    global enote_q
    global equotation_num
    ecustomer3= tk.Entry(fnew_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    ecustomer3.place(x=int(w/5.3),y=int(h/19))
    eaddress_q= tk.Entry(fnew_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    eaddress_q.place(x=int(w/5.3),y=int(h/8))
    egst_q= tk.Entry(fnew_quotation, width =25, font=("Arial", 15 ), bg= "gray93")
    egst_q.place(x=int(w/5.3),y=int(h/5.3))
    equotation_num= tk.Entry(fnew_quotation, width =20, font=("Arial", 15 ), bg= "gray93")
    equotation_num.place(x=int(w/1.49),y=int(h/8.4))
    emobile_q= tk.Entry(fnew_quotation, width =20, font=("Arial", 15 ), bg= "gray93")
    emobile_q.place(x=int(w/1.49),y=int(h/20))



    cal_new_quotation= DateEntry(fnew_quotation, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_new_quotation.place(x=int(w/1.49),y=int(h/5.3))


    
    enote_q= tk.Text(fnew_quotation, width =30, height =5 , font=("Arial", 15 ), bg= "gray93")
    enote_q.place(x=int(w/9),y=int(h/1.4))
    
    eproduct_q= tk.Entry(fnew_quotation, width =20, font=("Arial", 15 ), bg= "gray93")
    eproduct_q.place(x=int(w/9.7),y=int(h/3.6))
    eqty_q= tk.Entry(fnew_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    eqty_q.place(x=int(w/3.45),y=int(h/3.6))
    eunit_price_q= tk.Entry(fnew_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    eunit_price_q.place(x=int(w/2.47),y=int(h/3.6))
    etax_q= tk.Entry(fnew_quotation, width =8, font=("Arial", 15 ), bg= "gray93")
    etax_q.place(x=int(w/1.93),y=int(h/3.6))
    ehsn_q=tk.Entry(fnew_quotation, width =10, font=("Arial", 15 ), bg= "gray93")
    ehsn_q.place(x=int(w/1.6),y=int(h/3.6))

    badd=tk.Button(fnew_quotation, text="ADD", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",
                   command= lambda: new_quotation_add(tree,
                                                        #c_name=ecustomer2.get()
                                                       # c_address=eaddress.get()
                                                       # c_gst_no=egst.get()
                                                       # c_mobile=emobile.get()
                                                       # invoice_no=einvoice_num.get()
                                                       # date=cal_new_invoice.get()
                                                       # note=enote.get()
                                                        eproduct_q.get(),
                                                        ehsn_q.get(),
                                                        eqty_q.get(),
                                                        etax_q.get(),
                                                        eunit_price_q.get()))
    badd.place(x=int(w/1.35),y=int(h/3.7))
    quatation_num=0
    bpreview=tk.Button(fnew_quotation, text="PREVIEW", font=("Arial", 13) , bg= "dodger blue", fg="white",
                       command= lambda: create_pdf(tree,quatation_num,"quotation"))
    bpreview.place(x=int(w/1.3),y=int(h/1.28))
    bclear=tk.Button(fnew_quotation, text="CLEAR", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: new_quotation_clear(tree))
    bclear.place(x=int(w/1.5),y=int(h/1.28))





    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree = ttk.Treeview(fnew_quotation, columns=('0', '1', '2','3','4','5'), show='headings')
    tree.heading('0', text="S.NO")
    tree.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree.heading('1', text="Product/Service")
    tree.column('1', anchor=CENTER,minwidth=0, width=300, stretch=NO)
    tree.heading('2', text="HSN Code")
    tree.column('2', anchor=CENTER,minwidth=0, width=175, stretch=NO)
    tree.heading('3', text="Quantity")
    tree.column('3', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.heading('4', text="Tax")
    tree.column('4', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.heading('5', text="Amount")
    tree.column('5', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.place(x=int(w/9.8),y=int(h/3))
    vsb = ttk.Scrollbar(fnew_quotation, orient="vertical", command=tree.yview)
    vsb.place(x=int((w/9.8+1000)),y=int(h/3),width=16, height = 230)
    tree.configure(yscrollcommand=vsb.set)
    ecustomer3.bind("<Key>", new_quotation_check_name)
    eproduct_q.bind("<Key>",new_quotation_check_product)
    global x_new_quotation_add
    x_new_quotation_add=1

    global notes_from_db
    try:
        enote_q.insert(END, notes_from_db)
    except:
        pass
    try:
        cursor.execute ("SELECT * FROM QUOTATION ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        equotation_no_db = result[0]
    except:
        pass
    try:
        equotation_num.delete(0,END)
    except:
        pass
    try:
        equotation_num.insert(0,(int(equotation_no_db)+1))
    except:
        equotation_num.insert(0,(1))
    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            etax_q.insert(0,str(i[0]))
    except:
        pass

def new_invoice():
    global top1
    global invoice_edit_id
    global x_new_invoice_add
    invoice_edit_id=0
    x_new_invoice_add=1
    top1 = tk.Tk(className=' New Invoice')
    top1.geometry(str(w) + 'x' + str(h))
    top1.state('zoomed')
    global fnew_invoice
    fnew_invoice= tk.Frame(top1, bg = "white", height=h, width=w)
    fnew_invoice.grid(row=0,column=0)

    
    lcustomer2= tk.Label(fnew_invoice, text="Customer: ", font=("Arial", 15 ), bg= "white")
    lcustomer2.place(x=int(w/10),y=int(h/20))
    laddress= tk.Label(fnew_invoice, text="Address  : ", font=("Arial", 15 ), bg= "white")
    laddress.place(x=int(w/10),y=int(h/8.5))
    lgst= tk.Label(fnew_invoice, text="GST NO  : ", font=("Arial", 15 ), bg= "white")
    lgst.place(x=int(w/10),y=int(h/5.5))
    linvoice_num=tk.Label(fnew_invoice, text="Invoice No  : ", font=("Arial", 15 ), bg= "white")
    linvoice_num.place(x=int(w/1.8),y=int(h/8.5))
    ldate=tk.Label(fnew_invoice, text="Date      \t   : ", font=("Arial", 15 ), bg= "white")
    ldate.place(x=int(w/1.8),y=int(h/5.5))
    lproduct=tk.Label(fnew_invoice, text="Product:", font=("Arial", 15 ), bg= "white")
    lproduct.place(x=int(w/10),y=int(h/4.2))
    lqty=tk.Label(fnew_invoice, text="QTY:", font=("Arial", 15 ), bg= "white")
    lqty.place(x=int(w/10),y=int(h/3))
    lunit_price=tk.Label(fnew_invoice, text="Unit Price:", font=("Arial", 15 ), bg= "white")
    lunit_price.place(x=int(w/3.9),y=int(h/3))
    ltax=tk.Label(fnew_invoice, text="Tax:", font=("Arial", 15 ), bg= "white")
    ltax.place(x=int(w/2.2),y=int(h/3))
    lmobile=tk.Label(fnew_invoice, text="Mobile\t  :", font=("Arial", 15 ), bg= "white")
    lmobile.place(x=int(w/1.8),y=int(h/20))
    lhsn=tk.Label(fnew_invoice, text="HSN:", font=("Arial", 15 ), bg= "white")
    lhsn.place(x=int(w/1.6),y=int(h/3))    
    
    lnote=tk.Label(fnew_invoice, text="Note  : ", font=("Arial", 15 ), bg= "white")
    lnote.place(x=int(w/10),y=int(h/1.35))
    
    global ecustomer2
    global eaddress
    global egst
    global emobile
    global eproduct
    global eunit_price
    global etax
    global ehsn
    global cal_new_invoice
    global enote
    
    ecustomer2= tk.Entry(fnew_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    ecustomer2.place(x=int(w/5.3),y=int(h/19))
    eaddress= tk.Entry(fnew_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    eaddress.place(x=int(w/5.3),y=int(h/8))
    egst= tk.Entry(fnew_invoice, width =25, font=("Arial", 15 ), bg= "gray93")
    egst.place(x=int(w/5.3),y=int(h/5.3))
    emobile= tk.Entry(fnew_invoice, width =15, font=("Arial", 15 ), bg= "gray93")
    emobile.place(x=int(w/1.49),y=int(h/19))
    einvoice_num= tk.Entry(fnew_invoice, width =15, font=("Arial", 15 ), bg= "gray93")
    einvoice_num.place(x=int(w/1.49),y=int(h/8))
    cal_new_invoice= DateEntry(fnew_invoice, width=20, background='blue2', foreground='white', borderwidth=5,date_pattern='dd/mm/yyyy')
    cal_new_invoice.place(x=int(w/1.49),y=int(h/5.3))

    enote= tk.Text(fnew_invoice, width =30, height =5 , font=("Arial", 15 ), bg= "gray93")
    enote.place(x=int(w/6),y=int(h/1.35))
    
    eproduct= tk.Entry(fnew_invoice, width =90, font=("Arial", 15 ), bg= "gray93")
    eproduct.place(x=int(w/10),y=int(h/3.6))
    eqty= tk.Entry(fnew_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    eqty.place(x=int(w/10),y=int(h/2.6))
    eunit_price= tk.Entry(fnew_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    eunit_price.place(x=int(w/3.9),y=int(h/2.6))
    etax= tk.Entry(fnew_invoice, width =8, font=("Arial", 15 ), bg= "gray93")
    etax.place(x=int(w/2.2),y=int(h/2.6))
    ehsn= tk.Entry(fnew_invoice, width =10, font=("Arial", 15 ), bg= "gray93")
    ehsn.place(x=int(w/1.6),y=int(h/2.6))

    badd=tk.Button(fnew_invoice, text="ADD", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",
                   command= lambda: new_invoice_add(tree,
                                                        #c_name=ecustomer2.get()
                                                       # c_address=eaddress.get()
                                                       # c_gst_no=egst.get()
                                                       # c_mobile=emobile.get()
                                                       # invoice_no=einvoice_num.get()
                                                       # date=cal_new_invoice.get()
                                                       # note=enote.get()
                                                        eproduct.get(),
                                                        ehsn.get(),
                                                        eqty.get(),
                                                        etax.get(),
                                                        eunit_price.get(),
                                                        eproduct,
                                                        eqty,
                                                        etax,
                                                        eunit_price,
                                                        ehsn))
    badd.place(x=int(w/1.33),y=int(h/2.7))
    bclear=tk.Button(fnew_invoice, text="CLEAR", width=10, font=("Arial", 13) , bg= "dodger blue", fg="white",command= lambda: new_invoice_clear(tree))
    bclear.place(x=int(w/1.5),y=int(h/1.28))
    bpreview=tk.Button(fnew_invoice, text="PREVIEW", font=("Arial", 13) , bg= "dodger blue", fg="white",
                       command= lambda: create_pdf(tree,einvoice_num,"invoice"))
    bpreview.place(x=int(w/1.3),y=int(h/1.28))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 13))
    style.configure("Treeview", font=("Arial", 11))
    tree = ttk.Treeview(fnew_invoice, columns=('0', '1', '2','3','4','5'), show='headings')
    tree.heading('0', text="S.NO")
    tree.column('0', anchor=CENTER,minwidth=0, width=80, stretch=NO)
    tree.heading('1', text="Product/Service")
    tree.column('1', anchor=CENTER,minwidth=0, width=375, stretch=NO)
    tree.heading('2', text="HSN Code")
    tree.column('2', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.heading('3', text="Quantity")
    tree.column('3', anchor=CENTER,minwidth=0, width=100, stretch=NO)
    tree.heading('4', text="Tax")
    tree.column('4', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.heading('5', text="Amount")
    tree.column('5', anchor=CENTER,minwidth=0, width=150, stretch=NO)
    tree.place(x=int(w/9.8),y=int(h/2.3))
    vsb = ttk.Scrollbar(fnew_invoice, orient="vertical", command=tree.yview)
    vsb.place(x=int(w/9.8+1000),y=int(h/2.3),width=16, height = 230)
    tree.configure(yscrollcommand=vsb.set)
    
    

    ecustomer2.bind("<Key>", partial(new_invoice_check_name,name=ecustomer2.get()))
    eproduct.bind("<Key>",new_invoice_check_product)
    global typed
    typed =""
    

    global notes_from_db
    try:
        enote.insert(END, notes_from_db)
    except:
        pass
    try:
        einvoice_num.delete(0,END)
    except:
        pass

    from datetime import date
    today= date.today()
    this_year=(str(today.year)[-2:])
    previous_year=int(this_year)-1
    next_year=(int(this_year)+1)


    global financial_year
    if int(today.month) < 4:
        financial_year=str(previous_year)+"/"+str(this_year)
    else:
        financial_year=str(this_year)+"/"+str(next_year)
    
    try:
        cursor.execute ("SELECT * FROM INVOICE ORDER BY SNO DESC LIMIT 1")
        result = cursor.fetchone()
        invoice_no_db = result[0]
        einvoice_num.insert(0, str(financial_year)+" "+ str(int(str(invoice_no_db)[6:])+1))
    except:
        einvoice_num.insert(0,str(financial_year)+" "+str(1))

    try:
        cursor.execute ("SELECT * FROM INVOICE ORDER BY SNO DESC LIMIT 1")
        result = cursor.fetchone()
        invoice_no_db = result[0]
        if int(today.month) >= 4:
            if str(invoice_no_db[:5]) !=  str(financial_year):
                try:
                    einvoice_num.delete(0,END)
                except:
                    pass
                einvoice_num.insert(0,str(financial_year)+" "+str(1))
            else:
                pass
        else:
            pass
    except:
        pass
                

    try:
        query="SELECT TAX from COMPANY"
        results=conn.execute(query)
        for i in results:
            etax.insert(0,str(i[0]))
    except:
        pass

    try:
        query =("SELECT HSN FROM COMPANY")
        results=conn.execute(query)
        for i in results:
            ehsn.insert(0,(i))
        
    except:
        pass
    
def dashboard(euser,epass):
    query="SELECT PASSWORD, NAME from USERS"
    passwd_db=""
    name_db=""
    results=conn.execute(query)
    for i in results:
        passwd_db=str(i[0])
        name_db=str(i[1])
    if name_db != euser.get():
        error("Wrong Username")
    elif passwd_db != epass.get():
        error("Wrong Password")
        
    else: 
    
        flogin2.destroy()
        C.destroy()
        llogin.destroy()
        label.destroy()
        flogin.config(bg="white")
        bnew_invoice= tk.Button(flogin, text="NEW INVOICE", height=4, width=25, font=("Arial", 13, "bold"), bg= "green3",
                       fg ="white", activebackground= "green3", activeforeground= 'white', command= lambda: new_invoice())
        bnew_invoice.place(x=int(w/3.5),y=int(h/3))

        bquotation= tk.Button(flogin, text="QUOTATION", height=3, width=17, font=("Arial", 9, "bold"), bg= "green3",
                       fg ="white", activebackground= "green3", activeforeground= 'white', command= lambda: new_quotation())
        bquotation.place(x=int(w/3.5),y=int(h/2.06))


        bcustomer= tk.Button(flogin, text="CUSTOMER", height=3, width=17, font=("Arial", 9, "bold"), bg= "green3",
                       fg ="white", activebackground= "green3", activeforeground= 'white', command= lambda: new_customer())
        bcustomer.place(x=int(w/2.62),y=int(h/2.06))

        bproducts= tk.Button(flogin, text="PRODUCTS", height=3, width=17, font=("Arial", 9, "bold"), bg= "green3",
                       fg ="white", activebackground= "green3", activeforeground= 'white', command= lambda: new_product())
        bproducts.place(x=int(w/2.62),y=int(h/1.75))

        bbackup= tk.Button(flogin, text="BACKUP", height=3, width=17, font=("Arial", 9, "bold"), bg= "green3",
                       fg ="white", activebackground= "green3", activeforeground= 'white', command= lambda: backup())
        bbackup.place(x=int(w/3.5),y=int(h/1.75))

        total_product=""
        total_customer=""
        total_invoice=""
        total_quatation=""
        d=conn.execute("SELECT Count(*) FROM PRODUCT")
        conn.commit()             
        for i in d:
            total_product=(i[0])

        d=conn.execute("SELECT Count(*) FROM CUSTOMER")
        conn.commit()             
        for i in d:
            total_customer=(i[0])

        d=conn.execute("SELECT Count(*) FROM INVOICE")
        conn.commit()             
        for i in d:
            total_invoice=(i[0])

        d=conn.execute("SELECT Count(*) FROM QUOTATION")
        conn.commit()             
        for i in d:
            total_quatation=(i[0])


        lsales= tk.Label (flogin, text = "SALES", font=("Arial", 20, "bold"), fg="green3", bg="white")
        lsales.place(x=int(w/1.9),y=int(h/3.7))

        bcustomers1= tk.Button (flogin, text = "Customers", font=("Arial", 15), fg="gray26", bg="white", relief= FLAT,
                                activebackground= 'white', command= lambda: list_customer())
        bcustomers1.place(x=int(w/1.87),y=int(h/3.2))

        bproducts1= tk.Button (flogin, text = "Products", font=("Arial", 15), fg="gray26", bg="white",
                               relief= FLAT, activebackground= 'white', command= lambda: list_products())
        bproducts1.place(x=int(w/1.87),y=int(h/2.85))
        
        bquotation1= tk.Button (flogin, text = "Quotation", font=("Arial", 15), fg="gray26", bg="white",
                                relief= FLAT, activebackground= 'white', command= lambda: list_quotation())
        bquotation1.place(x=int(w/1.87),y=int(h/2.57))
        
        binvoice1= tk.Button (flogin, text = "Invoice", font=("Arial", 15), fg="gray26", bg="white",
                              relief= FLAT, activebackground= 'white',  command= lambda: list_invoice())
        binvoice1.place(x=int(w/1.87),y=int(h/2.34))





        lsales= tk.Label (flogin, text = "TOOLS", font=("Arial", 20, "bold"), fg="green3", bg="white")
        lsales.place(x=int(w/1.9),y=int(h/2.08))
        bbackup_data= tk.Button (flogin, text = "Backup Data", font=("Arial", 15), fg="gray26", bg="white",
                                relief= FLAT, activebackground= 'white',command= lambda: new_backup())
        bbackup_data.place(x=int(w/1.87),y=int(h/1.92))

        brestore_data= tk.Button (flogin, text = "Restore Data", font=("Arial", 15), fg="gray26", bg="white",
                               relief= FLAT, activebackground= 'white', command= lambda: new_restore())
        brestore_data.place(x=int(w/1.87),y=int(h/1.78))




        lsettings1= tk.Label (flogin, text = "SETTINGS", font=("Arial", 20, "bold"), fg="green3", bg="white")
        lsettings1.place(x=int(w/1.9),y=int(h/1.64))    

        bcompany_details= tk.Button (flogin, text = "Company Details", font=("Arial", 15), fg="gray26", bg="white",
                               relief= FLAT, activebackground= 'white', command= lambda: company_details())
        bcompany_details.place(x=int(w/1.87),y=int(h/1.54))




        lInvoices= tk.Label (flogin, text = "Invoices: "+str(total_invoice), font=("Arial", 13, "bold"), fg="green3", bg="white")
        lInvoices.place(x=int(w/3.7),y=int(h/5))
        lProducts= tk.Label (flogin, text = "Products: "+str(total_product), font=("Arial", 13, "bold"), fg="green3", bg="white")
        lProducts.place(x=int(w/2.8),y=int(h/5))
        lCustomers= tk.Label (flogin, text = "Customers: "+str(total_customer), font=("Arial", 13, "bold"), fg="green3", bg="white")
        lCustomers.place(x=int(w/2.25),y=int(h/5))
        lQuotations= tk.Label (flogin, text = "Quotations: "+str(total_quatation), font=("Arial", 13, "bold"), fg="green3", bg="white")
        lQuotations.place(x=int(w/1.85),y=int(h/5))



        C1 = tk.Canvas(flogin, bg="gray96", height=1, width=550)

        C1.place(x=int(w/4),y=int(h/4))

        
        fcompany= tk.Frame(flogin,background="white", height=int((h)/5.5), width=int(w))
        fcompany.place(x=int(w/1600),y=int(h/5000))
        llogo= tk.Label (fcompany, text = "SRI ARULAMBIKAI ENGINEERING WORKS", font=("Arial", 40, "bold"), fg="Black", bg="white")
        llogo.place(x=int(w/10),y=int(h/25))  
        #llogo1= tk.Label (fcompany, text = "Tirupur", font=("Arial", 20, "bold"), fg="Black", bg="white")
        #llogo1.place(x=int(w/1.8),y=int(h/8.2))      
        
        fcompany= tk.Frame(flogin,background="white", height=int((h)/14), width=int(w))
        fcompany.place(x=int(w/1600),y=int(h/1.179))
        
    


top.geometry(str(w) + 'x' + str(h))
top.state('zoomed')
flogin = tk.Frame (top, background="white", height=int(h), width=int(w))


flogin.pack()
flogin2 = tk.Frame (flogin, background="white", height=int((h)/2.5), width=int((w)/2.5))
flogin2.place(x=int((w/16)), y=int(h/3.8))
luser= tk.Label (flogin2, text="Username", font=("Arial", 15, 'bold'), bg="white")
luser.place(x=int(w/40),y=int(h/15))
lpass= tk.Label (flogin2, text="Password : ", font=("Arial", 15, 'bold'), bg="gray99")
lpass.place(x=int(w/40),y=int(h/5.5))
llogin= tk.Label (flogin, text="LOGIN", font=("Arial", 20, 'bold'),bg="white")
llogin.place(x=int(w/4.3),y=int(h/5))

img12 = tk.PhotoImage(master = flogin2, file="logo square.png")

euser= tk.Entry(flogin2, width=43, bg="gray95", font=("Arial", 15))
euser.place(x=int(w/40),y=int(h/9))
epass= tk.Entry(flogin2, width=43,show="*", bg="gray95", font=("Arial", 15))
epass.place(x=int(w/38),y=int(h/4.5))
blogin = tk.Button(flogin2, width=52, text="LOGIN",font=("Arial", 13) , height = 1, relief= GROOVE, bg= "deep sky blue",
                   fg ="white", activebackground= "deep sky blue", activeforeground= 'white', command= lambda: dashboard(euser,epass))
blogin.place(x=int(w/38),y=int(h/3.3))
label = Label(flogin, image=img12)
label.place(x=int(w/1.8),y=int(h/3))

C = tk.Canvas(flogin, bg="black", height=500, width=2)
C.place(x=int(w/2),y=int(h/8))

    




######################################################################      DATABASE LOGICS      #######################################################################
global conn
global cursor
try:
    os.mkdir(r"C:\ProgramData\Secure_Tech")
except:
    pass
conn = sqlite3.connect(r'C:\ProgramData\Secure_Tech\Secure Tech.db')
cursor= conn.cursor()
conn.execute("VACUUM")
conn.commit()
try:
    conn.execute('''CREATE TABLE CUSTOMER
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    ADDRESS CHAR(50) NOT NULL,
    GST CHAR(50),
    MOBILE CHAR(15),
    EMAIL CHAR(35));''')

except:
    pass

try:
    conn.execute('''CREATE TABLE USERS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    PASSWORD CHAR(50) NOT NULL);''')

    name="admin"
    passwd="123456"
    conn.execute("INSERT INTO USERS (NAME,PASSWORD) \
                    VALUES ( ?,? )",(name,passwd))
    conn.commit()
except:
    pass

try:
    conn.execute('''CREATE TABLE PRODUCT
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    PRICE CHAR(10) NOT NULL,
    HSN CHAR(50),
    TAX CHAR(5));''')
except:
    pass

try:
    conn.execute('''CREATE TABLE INVOICE
    (SNO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ID CHAR(50),
    NAME TEXT NOT NULL,
    ADDRESS CHAR(100) NOT NULL,
    GST CHAR(50),
    DATE CHAR(50),
    MOBILE CHAR(15),
    DATA BLOB NOT NULL);''')
except:
    pass

try:
    conn.execute('''CREATE TABLE QUOTATION
    (ID CHAR(50),
    NAME TEXT NOT NULL,
    ADDRESS CHAR(100) NOT NULL,
    GST CHAR(50),
    DATE CHAR(50),
    MOBILE CHAR(15),
    DATA BLOB NOT NULL);''')
except:
    pass

try:
    conn.execute('''CREATE TABLE COMPANY
    (NAME TEXT NOT NULL,
    ADDRESS CHAR(100) NOT NULL,
    MOBILE CHAR(50),
    PHONE CHAR(50),
    EMAIL CHAR(50),
    TAX INT(10),
    GST CHAR(30),
    NOTES CHAR(100),
    HSN CHAR(30));''')
except:
    pass
'''
statement=("SELECT * FROM PRODUCT")
c=conn.execute(statement)
for i in c:
    print(i)
'''

try:
    d="""SELECT NOTES FROM COMPANY"""
    e=conn.execute(d)
    for i in e:
        notes_from_db=i[0]
except:
    pass



top.mainloop()

