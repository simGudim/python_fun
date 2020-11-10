import tkinter
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from tools import Tools
from functools import partial


class Interface(Tools):
    def __init__(self):
        super().__init__()

        self.root = Tk()
        self.root.title("Welcome to the ADW Runner!")
        self.root.geometry("750x600")
        self.root.resizable(width = True, height = True)

        self.geo_tools = {
            "DriveDistance" : self.drive_distance_gui,
            "DriveDistanceStore" : self.drive_distance_store_gui,
            "Geocode": self.geocode_gui,
            "GrandOpening" : self.go_gui,
            "LightWeekReport" : self.light_week_report_gui,
            "PcInterpolation" : self.pc_interpolation_gui,
            "Prorate" : self.prorate_gui,
            "MobileErrorAnalysis" : self.mobile_error_analysis_gui
        }

        #OptionMenu for Tools
        self.report = StringVar(self.root)
        self.report.set("Choose")
        self.choices_2 =  [
            "DriveDistance",
            "DriveDistanceStore",
            "Geocode",
            "GrandOpening",
            "LightWeekReport", 
            "PcInterpolation",
            "Prorate",
            "MobileErrorAnalysis"
                        ]

        self.intial_state()
        self.intitialize_input(self.getInputCSVFile, "Input csv file")
        self.intitialize_output(self.getOutputFile)

    def getInputCSVFile(self, idx):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("CSV File", "*.csv"), ("all files", "*.*")))
        self.input_entry.insert(idx, filename)
        if len(self.params) == idx:
            self.params.append(self.input_entry.get())
        else:
            self.params[idx] = self.input_entry.get()

    def getInputCSV2File(self, idx, entry):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("KML File", "*.kml *.csv"), ("all files", "*.*")))
        entry.insert(idx, filename)
        if len(self.params) >= idx + 1:
            self.params[idx] = entry.get()
            print(self.params)
        elif len(self.params) < idx +1:
            self.params.append(entry.get())
            print(self.params)

    def getInputKMLFile(self, idx, entry):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("KML File", "*.kml *.csv"), ("all files", "*.*")))
        entry.insert(idx, filename)
        if len(self.params) >= idx + 1:
            self.params[idx] = entry.get()
            print(self.params)
        elif len(self.params) < idx +1:
            self.params.append(entry.get())
            print(self.params)


    def getInputAccessFile(self, idx):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("Access Files", "*.accdb"), ("all files", "*.*")))
        self.input_entry.insert(idx, filename)
        if len(self.params) == idx:
            self.params.append(self.input_entry.get())
        else:
            self.params[idx] = self.input_entry.get()

    def getOutputFile(self, idx):
        outfilename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("CSV File", "*.csv"),("all files","*.*")))
        self.output_entry.insert(idx, outfilename)
        if len(self.params) >= idx + 1:
            self.params[idx] = self.output_entry.get()
            print(self.params)
        elif len(self.params) < idx +1:
            self.params.append(self.output_entry.get())
            print(self.params)

    def getOutputExcelFile(self, idx):
        outfilename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("Excel File", ".xlsx"),("all files","*.*")))
        self.output_entry.insert(idx, outfilename)
        if len(self.params) == idx:
            self.params.append(self.output_entry.get() + ".xlsx")
        else:
            self.params[idx] = self.output_entry.get() + ".xlsx"

    def change_dropdown(self, *args):
        return self.report.get()
 
    def change_gui(self, name):
        return self.geo_tools.get(name)()

    def choice_callback(self,*args):
        for i in args:
            if i in self.choices_2:
                return self.change_gui(i)

    def typedChoice_callback(self, var, index, *args):
        for i in args:
            if len(self.params) >= index + 1:
                self.params[index] = var
                print(self.params)
            elif len(self.params) < index +1:
                self.params.append(var)
                print(self.params)
            else:
                print("varible type doesn't match")
    
    def execute_tool(self, *args):
        return self.toolbox.get(self.change_dropdown())(*self.params)
        print(self.params)

    def intial_state(self):
        self.img2 = ImageTk.PhotoImage(Image.open(r"Z:\Base6\General\Processes\ADW_runner\images\geomedia.jpg"))
        self.panel2 = Label(image = self.img2).grid(row = 15, column = 0,
                                            sticky=W+E+N+S,
                                            padx=5, pady=5)

        self.popupMenu1 = OptionMenu(self.root, self.report, *self.choices_2, command = self.choice_callback).grid(row = 20, column = 0)
        self.drop2 = Label(text = "Choose a Report Type").grid(row = 21, column = 0)
        self.report.trace("w", self.change_dropdown)

        self.params = []

        #Run Butoon
        self.run_btn = Button(self.root, text="Run", command=self.execute_tool)
        self.run_btn.grid(row=7, column=4)

    def intitialize_input(self, input_type, input_lbls, idx = 0):
        # Name Input
        self.input_index = idx
        self.input_var = StringVar()
        self.input_lbl = Label(self.root, textvariable=self.input_var)
        self.input_var.set(input_lbls)
        self.input_lbl.grid(row=idx, column=0)
        self.input_entry = Entry(self.root, bd=5, width=50)
        self.input_entry.grid(row=idx, column=1)

        self.in_btn = Button(self.root, text="...", command=partial(input_type, idx))
        self.in_btn.grid(row=idx, column=2)

    def intitialize_beta_input(self, beta_Var, beta_lbl, beta_entry, beta_btn, input_type, input_lbls, idx):
        # Name Input
        beta_var = StringVar()
        beta_lbl = Label(self.root, textvariable=beta_var)
        beta_var.set(input_lbls)
        beta_lbl.grid(row=idx, column=0)
        beta_entry = Entry(self.root, bd=5, width=50)
        beta_entry.grid(row=idx, column=1)

        beta_btn = Button(self.root, text="...", command=partial(input_type, idx, beta_entry))
        beta_btn.grid(row=idx, column=2)

    def intitialize_output(self, output_type, index = 1):
        # output file name
        self.output_index = index
        self.output_var = StringVar()
        self.output_lbl = Label(self.root, textvariable=self.output_var)
        self.output_var.set("Output csv/excel file name:")
        self.output_lbl.grid(row=index, column=0)
        self.output_entry = Entry(self.root, bd=5, width=50)
        self.output_entry.grid(row=index, column=1)

        self.out_btn = Button(self.root, text="...", command=partial(output_type, index))
        self.out_btn.grid(row=index, column=2)

    def intitialize_description(self, desc):
        self.description = tkinter.Text(self.root, height = 10, width = 50)
        self.description.grid(row = 10, column=1)
        self.description.insert(tkinter.INSERT, """{}""".format(desc))
        self.description.config(state = "disabled")

    def intitialize_typedVar(self, lbl_var, lbl, var, entry, idx, var_type, desc):
        lbl_var = StringVar()
        lbl_var.set("{}".format(desc))
        lbl = Label(self.root, textvariable=lbl_var).grid(row=idx, column=0)
        var = var_type
        var.trace("w", lambda name, index, mode, sv=var: self.typedChoice_callback(var.get(), 
                                                                                    idx,
                                                                                    sv))
        entry = Entry(self.root, textvariable=var, bd=5, width=20).grid(row=idx, column=1)

    
    def drive_distance_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()

        self.intitialize_input(self.getInputCSVFile, "Input csv file")
        self.intitialize_output(self.getOutputFile, 1)

        self.pc_index = 2
        self.pc_var, self.pc_lbl, self.pc, self.pc_entry = None, None, None, None
        self.intitialize_typedVar(self.pc_var, self.pc_lbl, self.pc,self.pc_entry,self.pc_index,StringVar(),"Output PC2STR Fieldname")

        self.dd_index = 3
        self.dd_var, self.dd_lbl, self.dd, self.dd_entry = None, None, None, None
        self.intitialize_typedVar(self.dd_var, self.dd_lbl, self.dd,self.dd_entry,self.dd_index,StringVar(),"Output DD Fieldname")
        self.intitialize_description("""Calculates DD and PC2STR based on Source \nand Destination coordinates.\nRequires three columns: label, lng, lat.The columns can be names anything, but\n second columns needs to be lng and third lat.""")

    def drive_distance_store_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()
        self.intitialize_output(self.getOutputFile, 0)

        self.pc_index = 1
        self.pc_var, self.pc_lbl, self.pc, self.pc_entry = None, None, None, None
        self.intitialize_typedVar(self.pc_var, self.pc_lbl, self.pc,self.pc_entry,self.pc_index,StringVar(),"Output PC2STR Fieldname")

        self.dd_index = 2
        self.dd_var, self.dd_lbl, self.dd, self.dd_entry = None, None, None, None
        self.intitialize_typedVar(self.dd_var, self.dd_lbl, self.dd,self.dd_entry,self.dd_index,StringVar(),"Output DD Fieldname")

        self.client_index = 3
        self.client_var, self.client_lbl, self.client, self.client_entry = None, None, None, None
        self.intitialize_typedVar(self.client_var, self.client_lbl, self.client,self.client_entry,self.client_index,IntVar(),"Input Client ID")

        self.division_index = 4
        self.division_var, self.division_lbl, self.division, self.division_entry = None, None, None, None
        self.intitialize_typedVar(self.division_var, self.division_lbl, self.division,self.division_entry,self.division_index,IntVar(),"Input Client Division")
        
        self.store_index = 5
        self.store_var, self.store_lbl, self.store, self.store_entry = None, None, None, None
        self.intitialize_typedVar(self.store_var, self.store_lbl, self.store,self.store_entry,self.store_index,StringVar(),"Input Store #")
        self.intitialize_description("""Calculates DD and PC2STR based on one store number.\nInput client_id, client_divison_id and store_number""")

    def geocode_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()
        
        self.intial_state()
        self.intitialize_input(self.getInputCSVFile, "Input csv file")
        self.intitialize_output(self.getOutputFile)
        self.intitialize_description("""Get lat and lng from address.\nRequired: First column of file to be the address.\nInput:csv file""")

    
    def go_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()
        
        self.intial_state()
        self.intitialize_input(self.getInputAccessFile, "Input Access Db")
        self.intitialize_output(self.getOutputExcelFile)
        self.intitialize_description( """Generates GO report from Access DB.\nInput:Aceess database and other variables""")

        self.storeNum_index = 2
        self.storeNum_var, self.storeNum_lbl, self.storeNum, self.storeNum_entry = None, None, None, None
        self.intitialize_typedVar(self.storeNum_var, self.storeNum_lbl, self.storeNum, self.storeNum_entry, self.storeNum_index,StringVar(),"Input Store Number")

        self.pc2str_index = 3
        self.pc2str_var, self.pc2str_lbl, self.pc2str, self.pc2str_entry = None, None, None, None
        self.intitialize_typedVar(self.pc2str_var, self.pc2str_lbl,self.pc2str, self.pc2str_entry,self.pc2str_index,StringVar(),"Input Pc2STR Fieldname")

        self.dd_index = 4
        self.dd_var, self.dd_lbl, self.dd, self.dd_entry = None, None, None, None
        self.intitialize_typedVar(self.dd_var,  self.dd_lbl, self.dd, self.dd_entry, self.dd_index,StringVar(),"Input Drive Distance Fieldname")

        self.sales_index = 5
        self.sales_var, self.sales_lbl, self.sales, self.sales_entry = None, None, None, None
        self.intitialize_typedVar(self.sales_var,  self.sales_lbl,self.sales, self.sales_entry, self.sales_index, StringVar(),"Input Sales Fieldname")

        self.csp_index = 6
        self.csp_var, self.csp_lbl, self.csp, self.csp_entry = None, None, None, None
        self.intitialize_typedVar(self.csp_var, self.csp_lbl, self.csp, self.csp_entry, self.csp_index,StringVar(),"Input CSP Fieldname")

        self.keep_index = 7
        self.keep_var, self.keep_lbl, self.keep, self.keep_entry = None, None, None, None
        self.intitialize_typedVar(self.keep_var, self.keep_lbl, self.keep,self.keep_entry,self.keep_index,StringVar(),"Input Keep Fieldname")

        self.cur_index = 8
        self.cur_var, self.cur_lbl, self.cur, self.cur_entry = None, None, None, None
        self.intitialize_typedVar(self.cur_var, self.cur_lbl,self.cur, self.cur_entry,self.cur_index,StringVar(),"Input Current Flag Fieldname")

        self.rec_index = 9
        self.rec_var, self.rec_lbl, self.rec, self.rec_entry = None, None, None, None
        self.intitialize_typedVar(self.rec_var, self.rec_lbl,self.rec,self.rec_entry,self.rec_index,StringVar(),"Input Rec Flag Fieldname")

    def light_week_report_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()
        self.intitialize_input(self.getInputAccessFile, "Input Access Db")
        self.intitialize_output(self.getOutputExcelFile)
        self.intitialize_description( """Generates Light Week report from Access DB.\nInput:Aceess database and other variables""")

        self.keep_index = 2
        self.keep_var, self.keep_lbl, self.keep, self.keep_entry = None, None, None, None
        self.intitialize_typedVar(self.keep_var, self.keep_lbl, self.keep,self.keep_entry,self.keep_index,StringVar(),"Input Keep Fieldname")

        self.cur_index = 3
        self.cur_var, self.cur_lbl, self.cur, self.cur_entry = None, None, None, None
        self.intitialize_typedVar(self.cur_var, self.cur_lbl,self.cur, self.cur_entry,self.cur_index,StringVar(),"Input Current Flag Fieldname")

        self.light_index = 4
        self.light_var, self.light_lbl, self.light, self.light_entry = None, None, None, None
        self.intitialize_typedVar(self.light_var, self.light_lbl,self.light, self.light_entry,self.light_index,StringVar(),"Input Light Flag Fieldname")

        self.pc2str_index = 5
        self.pc2str_var, self.pc2str_lbl, self.pc2str, self.pc2str_entry = None, None, None, None
        self.intitialize_typedVar(self.pc2str_var, self.pc2str_lbl,self.pc2str, self.pc2str_entry,self.pc2str_index,StringVar(),"Input Pc2STR Fieldname")

        self.sales_index = 6
        self.sales_var, self.sales_lbl, self.sales, self.sales_entry = None, None, None, None
        self.intitialize_typedVar(self.sales_var,  self.sales_lbl,self.sales, self.sales_entry, self.sales_index, StringVar(),"Input Sales Fieldname")
    
    def pc_interpolation_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()
        self.intitialize_input(self.getInputCSVFile, "Input csv file")
        self.intitialize_output(self.getOutputFile)
        self.intitialize_description("""5,4,3 interpolation.\nRequired: First column of file to be postalcodes\nInput: csv file""")

    def prorate_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()
        self.intitialize_input(self.getInputAccessFile, "Input Access DB")

        self.in2_var, self.in2_lbl, self.in2_entry, self.in2_btn = None, None, None, None
        self.intitialize_beta_input(self.in2_var, self.in2_lbl, self.in2_entry, self.in2_btn, self.getInputCSV2File, "Input CSV File", 1)

        self.type_index = 2
        self.type_var, self.type_lbl, self.type, self.type_entry = None, None, None, None
        self.intitialize_typedVar(self.type_var, self.type_lbl,self.type, self.type_entry,self.type_index,StringVar(),"Input Proration Type")
        
        self.intitialize_description("""Prorates one or multiple variables based on \nTypes: average, min, text. Only multiple variable of the same proration type \ncan be used! First column needs to be PC value""")



    def mobile_error_analysis_gui(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        self.intial_state()

        self.in1_var, self.in1_lbl, self.in1_entry, self.in1_btn = None, None, None, None
        self.intitialize_beta_input(self.in1_var, self.in1_lbl, self.in1_entry, self.in1_btn, self.getInputKMLFile, "Input Polygon File", 0)

        self.in2_var, self.in2_lbl, self.in2_entry, self.in2_btn = None, None, None, None
        self.intitialize_beta_input(self.in2_var, self.in2_lbl, self.in2_entry, self.in2_btn, self.getInputKMLFile, "Input Points File", 1)
        
        self.intitialize_output(self.getOutputFile, 2)
        self.intitialize_description("""Analyzes the count and area of pings outside \nthe store poly \nInput: polygon kml file, kml/csv file of pings,\nbuffer raduis of the ping""")
        
        self.buffer_index = 3
        self.buffer_var, self.buffer_lbl, self.buffer, self.buffer_entry = None, None, None, None
        self.intitialize_typedVar(self.buffer_var, self.buffer_lbl,self.buffer,self.buffer_entry,self.buffer_index,IntVar(),"Input Buffer Radius")       
            
e = Interface()
e.root.mainloop()