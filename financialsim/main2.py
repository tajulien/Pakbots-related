import tkinter as tk
import json
import os
import tkinter as tk  
from tkinter import font as tkfont 
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from financialsim import chargefon


NORM_FONT = ("Verdana", 10)


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        label = tk.Label(self, text="Financial sim 2020", width=20, font=self.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.master.title("Financial Sim 2020")
        #self.master.geometry("200x200")
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="Open page three",
                  command=lambda: master.switch_frame(PageThree)).pack()
        label = tk.Label(self, text="", width=20, font=self.title_font).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        global img
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        img = ImageTk.PhotoImage(Image.open("bckgrnd.jpg"))
        panel = tk.Label(self, image=img).pack(fill="both", expand="yes")
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class PageTwo(tk.Frame):
    file_contain = {}
    i = 0

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.entries = []
        self.master.title("Data inputs")
        PageTwo.read_json()
        self.entryWidgets = []
        self.buttonWidgets = [] 
        labelWidgets = []

        v = StringVar()

        prixttcInput = []
        namesInput = []
        for p in PageTwo.file_contain['financialsim']['charges_foncieres']['attribs']:
            for elt in PageTwo.file_contain['financialsim']['charges_foncieres']['attribs'][p].items():
                if elt[0] == "name":
                    namesInput.append(elt[1])
                if elt[0] == "prixttc":
                    prixttcInput.append(elt[1])
        #print(namesInput)
        for i in range(0, len(namesInput)):
            #print(prixttcInput[i])
            labelWidgets.append(Label(self, text=namesInput[i]))
            self.buttonWidgets.append(Button(self, text="- show -", command=lambda name=namesInput[i], refid=i:popupmsg(name,'charges_foncieres', refid)))
            labelWidgets[-1].grid(row=i + 1, column=0, sticky='e')
            self.buttonWidgets[-1].grid(row=i + 1, column=2, sticky='w')
            v8 = StringVar(self.master)
            self.entryWidgets.append(Entry(self,state="readonly", justify=CENTER, textvariable=v8).grid(row=i + 1, column=1, sticky='w'))
            v8.set(prixttcInput[i])


        prixttcInput = []
        namesInput = []
        for p in PageTwo.file_contain['financialsim']['construction']['attribs']:
            for elt in PageTwo.file_contain['financialsim']['construction']['attribs'][p].items():
                if elt[0] == "name":
                    namesInput.append(elt[1])
                if elt[0] == "prixttc":
                    prixttcInput.append(elt[1])
        #print(namesInput)
        for i in range(0, len(namesInput)):
            labelWidgets.append(Label(self, text=namesInput[i]))
            self.buttonWidgets.append(
            Button(self, text="- show -", command=lambda name=namesInput[i], refid=i:popupmsg(name,'construction', refid)).grid(row=i + 1, column=5, sticky='w'))
            #self.entryWidgets.append(Entry(self))
            labelWidgets[-1].grid(row=i + 1, column=3, sticky='e')
            v9 = StringVar(self.master)
            self.entryWidgets.append(
            Entry(self, state="readonly", justify=CENTER, textvariable=v9).grid(row=i + 1, column=4, sticky='w'))
            v9.set(prixttcInput[i])
            #self.entryWidgets[-1].grid(row=i + 1, column=3, sticky='w')


        prixttcInput = []
        namesInput = []
        for p in PageTwo.file_contain['financialsim']['fonctionnement']['attribs']:
            for elt in PageTwo.file_contain['financialsim']['fonctionnement']['attribs'][p].items():
                if elt[0] == "name":
                    namesInput.append(elt[1])
                if elt[0] == "prixttc":
                    prixttcInput.append(elt[1])
        for i in range(0, len(namesInput)):
            labelWidgets.append(Label(self, text=namesInput[i]))
            #self.entryWidgets.append(Entry(self, textvariable=v))
            labelWidgets[-1].grid(row=i + 1, column=6, sticky='e')
            self.buttonWidgets.append(
                Button(self, text="- show -", command=lambda name=namesInput[i], refid=i:popupmsg(name,'fonctionnement', refid)).grid(
                    row=i + 1, column=8, sticky='w'))
            #self.entryWidgets[-1].grid(row=i + 1, column=7, sticky='w')
            v10 = StringVar(self.master)
            self.entryWidgets.append(
            Entry(self, state="readonly", justify=CENTER, textvariable=v10).grid(row=i + 1, column=7, sticky='w'))
            v10.set(prixttcInput[i])


        prixttcInput = []
        namesInput = []
        for p in PageTwo.file_contain['financialsim']['commercialisation']['attribs']:
            for elt in PageTwo.file_contain['financialsim']['commercialisation']['attribs'][p].items():
                if elt[0] == "name":
                    namesInput.append(elt[1])
                if elt[0] == "prixttc":
                    prixttcInput.append(elt[1])
        #print(namesInput)
        for i in range(0, len(namesInput)):
            labelWidgets.append(Label(self, text=namesInput[i]))
            self.entryWidgets.append(Entry(self))
            labelWidgets[-1].grid(row=i + 1, column=9, sticky='e')
            #self.entryWidgets[-1].grid(row=i + 1, column=10, sticky='w')
            self.buttonWidgets.append(
                Button(self, text="- show -", command=lambda name=namesInput[i], refid=i:popupmsg(name,'commercialisation', refid)).grid(
                    row=i + 1, column=11, sticky='w'))
            v11 = StringVar(self.master)
            self.entryWidgets.append(
            Entry(self, state="readonly", justify=CENTER, textvariable=v11).grid(row=i + 1, column=10, sticky='w'))
            v11.set(prixttcInput[i])

        submit = Button(self, text="Update", command=lambda: master.switch_frame(PageTwo))
        submit.grid(row=12, column=0, columnspan=2)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=12, row=PageTwo.i + 20)



    def getEntries(self):
        results = []
        for x in self.entryWidgets:
            results.append(x.get())
        print(results)

    @staticmethod
    def read_json():
        with open(os.getcwd() + "\\datas\\datas.json", 'r') as json_file:
            datas_cons = json.load(json_file)
            PageTwo.file_contain = datas_cons
        json_file.close()

    #def reload(self):


class PageThree(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #self.master.title("")
        label = tk.Label(self, text="Open Existing file")
        label.pack(side="top", fill="x", pady=10)
        btn = Button(self, text='Open', command=lambda: self.open_file())
        btn.pack(pady=10)
        button = tk.Button(self, text="Return to start page",
                           command=lambda: master.switch_frame(StartPage))
        button.pack()

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('Json Files', '*.json')])
        if file is not None:
            content = file.read()
            #print(content)

def popupmsg(msg, where, refid):
    labelWidgets2 = []
    entryWidgets2 = []
    result = find_in_json(msg, where)
    popup = Tk()
    v2 = StringVar(popup)
    v3 = StringVar(popup)
    v4 = StringVar(popup)
    v5 = StringVar(popup)
    v6 = StringVar(popup)
    v7 = StringVar(popup)
    popup.wm_title("details")
    id_but = tk.Label(popup, text=result[0][0], justify=CENTER).grid(row=1, column=0, sticky='e')
    id_field = tk.Entry(popup, state="readonly", textvariable=v2, justify=CENTER).grid(row=1, column=1, sticky=N + S + E + W)
    v2.set(result[0][1])
    id_but2 = tk.Label(popup, text=result[1][0], justify=CENTER).grid(row=2, column=0, sticky='e')
    id_field2 = tk.Entry(popup, state="readonly", width=35, justify=CENTER, textvariable=v3)
    id_field2.grid(row=2, column=1, sticky=N + S + E + W)
    v3.set(result[1][1])
    id_but3 = tk.Label(popup, text=result[2][0], justify=CENTER).grid(row=3, column=0, sticky='e')
    id_field3 = tk.Entry(popup, textvariable=v4, justify=CENTER)
    id_field3.grid(row=3, column=1, sticky=N + S + E + W)
    v4.set(result[2][1])
    id_but4 = tk.Label(popup, text=result[3][0], justify=CENTER).grid(row=4, column=0, sticky='e')
    id_field4 = tk.Entry(popup, textvariable=v5, justify=CENTER)
    id_field4.grid(row=4, column=1, sticky=N + S + E + W)
    v5.set(result[3][1])
    id_but5 = tk.Label(popup, text=result[4][0], justify=CENTER).grid(row=5, column=0, sticky='e')
    id_field5 = tk.Entry(popup, state="readonly", textvariable=v6, justify=CENTER).grid(row=5, column=1, sticky=N + S + E + W)
    v6.set(result[4][1])
    id_but6 = tk.Label(popup, text=result[5][0], justify=CENTER).grid(row=6, column=0, sticky='e')
    id_field6 = tk.Entry(popup, state="readonly", textvariable=v7, justify=CENTER).grid(row=6, column=1, sticky=N + S + E + W)
    v7.set(result[5][1])
    entryWidgets2.append(id_field2)
    entryWidgets2.append(id_field3)
    entryWidgets2.append(id_field4)
    #label = ttk.Label(popup, text=msg, font=NORM_FONT)
    #label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Submit", command=lambda: [send_update(entryWidgets2, msg, where, refid),popup.destroy(),popupmsg(msg,where,refid)])
    B1.grid(row=len(result) + 1, column=0, sticky=N + S + E + W)
    B2 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B2.grid(row=len(result) + 1, column=2, sticky=N + S + E + W)
    popup.mainloop()

def send_update(entryWidgets2,msg, where, refid):
    results = []
    where = str(where)
    refid = str(refid)
    for x in entryWidgets2:  # i.e for each widget in entryWidget list
        print(where)
        print(refid)
        results.append(x.get())
        print(results)
    with open(os.getcwd() + "\\datas\\datas.json", 'r') as json_file:
        yet = json.load(json_file)
        if results[0] == yet["financialsim"][where]["attribs"][refid]["name"]:
            yet["financialsim"][where]["attribs"][refid]["coeff"] = int(results[1])
            yet["financialsim"][where]["attribs"][refid]["prixht"] = int(results[2])
            json_file.seek(0)
            with open(os.getcwd() + "\\datas\\datas.json", 'w') as json_file:
                json.dump(yet, json_file, indent=2)
                json_file.truncate()
            chargefon.main()
        else:
            print("rip")
        #print(yet['financialsim'][where]["attribs"][refid]["prixht"])
        #with open(os.getcwd() + "\\datas\\datas.json", 'w+') as json_file:
        #    json.dump(yet, json_file)

def find_in_json(msg, where):
    with open(os.getcwd() + "\\datas\\datas.json", 'r') as json_file:
        datas_cons = json.load(json_file)
        result = []
        for p in datas_cons['financialsim'][where]['attribs'].items():
            #print(p[1].values())
            if msg in p[1].values():
                #print(p[1])
                #print(type(p[1]))
                for key, value in p[1].items():
                    result.append((key,value))
                return result
            # for elt in datas_cons['financialsim'][where]['attribs'][p].items():
            #    print(elt)


if __name__ == "__main__":
    app = SampleApp()
    # app.geometry("1280x720")
    app.mainloop()
