
from Tkinter import *
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from numpy import pi, mgrid, arctan2, log, sin, arctan, cos

from tkColorChooser import askcolor
from ttk import Treeview

class App:
    def __init__(self,master):
        self.master = master
        self.master.resizable(0,0)
        self.master.update_idletasks()
        self.master.overrideredirect(1)
        self.master.attributes("-topmost",True)
        self.master.title("New Graph")
        self.master.lift()
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.default_color = self.master.cget("bg")
        self.active_edit_flag = 0
        self.modify_flag = 0
        self.graph_types = ['Default','Maelstrom','Rankine Half-Body','Rankine Oval', 'Cylinder','Stagnation & Vortex']
       #-----------------------------------------------------------------------
        self.file_menu = Menu(self.menubar)
        
        self.Fig = matplotlib.figure.Figure(figsize=(2.148,1.777),dpi=100,tight_layout=True)
        self.FigSubPlot = self.Fig.add_subplot(111)     
        frame = Frame(master,bg='#%02x%02x%02x' % (231, 231, 231))
        frame.pack(fill=BOTH, expand=1)
        frame2 = Frame(frame,bg='#%02x%02x%02x' % (221, 221, 221))
        frame2.pack(fill=BOTH, expand=1,padx=20,pady=23)
        self.frame3 = Frame(frame2, bg='#%02x%02x%02x' % (221, 221, 221))
        self.frame3.pack(fill=BOTH, padx=17,pady=17,expand=1)
        self.radio_frame = Frame(self.frame3,bg='#%02x%02x%02x' % (221, 221, 221))
      
        #self.listbox = Listbox(self.frame3)
        self.radio_var = StringVar()
        self.radio_var.set('Default')
        for key in self.graph_types:
            b = Radiobutton(self.radio_frame,text=key,variable=self.radio_var,value = key,bg='#%02x%02x%02x' % (221, 221, 221),indicatoron=1)
            b.pack(anchor=W)
#        for key_num in range(0,len(self.graph_types)):
#            self.listbox.insert(END,self.graph_types[key_num])
#        self.listbox.select_set(0)
#        self.listbox.bind('<<ListboxSelect>>',self.changegraph)
        self.radio_var.trace('w',self.changegraph)
#        self.old = self.listbox.get(self.listbox.curselection())
        self.blankc = Canvas(self.frame3,width=225,height=188)
        self.canvas = FigureCanvasTkAgg(self.Fig, master=self.frame3)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=RIGHT,padx=0,pady=5)
        self.radio_frame.pack(side=LEFT,anchor=W,padx=8,pady=5,fill=BOTH,expand=1) 
        #self.listbox.pack(side=LEFT,anchor=W,padx=8,pady=5,fill=BOTH,expand=1)   
        self.button_frame = Frame(frame,bg='#%02x%02x%02x' % (231, 231, 231))
        self.button_frame.pack(side=RIGHT)
        self.buffer_frame = Frame(self.button_frame,bg='#%02x%02x%02x' % (231, 231, 231))
        self.buffer_frame.pack(side=BOTTOM,pady=8)
        self.buffer_frame2 = Frame(self.button_frame,bg='#%02x%02x%02x' % (231, 231, 231))
        self.buffer_frame2.pack(side=RIGHT,padx=11)
        self.button_c = Button(self.button_frame,width=9, text='Choose',bg='#%02x%02x%02x' % (231, 231, 231),command=self.Continue)
        self.button_x = Button(self.button_frame,text='Cancel',bg='#%02x%02x%02x' % (231, 231, 231),width=9,command=self.quit)
        self.button_c.focus()
        self.button_c.pack(side=RIGHT)
        self.button_x.pack(side=RIGHT,padx=14)
        self.line_color = StringVar()
        self.line_color.set('#000000')
        self.wt_var = StringVar()
        self.wt_var.set('- WT:')
        self.wt_var.trace('w',self.wt_update)
        self.linet_var = StringVar()
        self.linet_var.set('-')
        self.linet_var.trace('w',self.line_style_update)
        self.line_var = IntVar()
        self.line_var.set(25)
        self.line_val = 25
        self.div_check_var = IntVar()
        self.div_check_var.set(50)
        self.div_val = 50
        self.density_var = IntVar()
        self.density_var.set(35)
        self.density_val = 35
        self.arrow_var = IntVar()
        self.arrow_var.set(25) 
        self.arrow_val = 25
        self.div_var = IntVar()
        self.div_var.set(0)
        self.mark_var = IntVar()
        self.mark_var.set(0)
        self.lock_var = IntVar()
        self.lock_var.set(1)
        self.active_numbers = {'s':0,'v':0,'u':0,'d':0,'n':0}
        self.sel_point = None
        self.selected = None
    def changegraph(self,*args):
        self.xlim = [-5.0,5.0]
        self.ylim = [-5.0,5.0]
        Y, X = mgrid[-5:5:100j, -5:5:100j]
        self.X,self.Y = X,Y
        self.FigSubPlot.clear()
        #if self.listbox.get(self.listbox.curselection()) == 'Default':
        if self.radio_var.get() == 'Default':
            self.U = 0*X
            self.V = 0*X
            self.FigSubPlot.streamplot(X,Y,self.U,self.V)
        #elif self.listbox.get(self.listbox.curselection()) == 'Maelstrom':
        elif self.radio_var.get() == 'Maelstrom':    
            self.U = self.source(X,Y,1)[0]+self.vortex(X,Y,1)[0]
            self.V = self.source(X,Y,1)[1]+self.vortex(X,Y,1)[1]
            self.FigSubPlot.streamplot(X,Y,self.U,self.V, color='k', linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle='-')
        #elif self.listbox.get(self.listbox.curselection()) == 'Rankine Half-Body':
        elif self.radio_var.get() == 'Rankine Half-Body':
            self.U = self.source(X,Y,10)[0]+self.uniform(X,Y,1,1,0)[0]
            self.V = self.source(X,Y,10)[1]+self.uniform(X,Y,1,1,0)[1]
            self.FigSubPlot.streamplot(X, Y,self.U,self.V, color='k', linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle='-')
        #elif self.listbox.get(self.listbox.curselection()) == 'Rankine Oval':
        elif self.radio_var.get() == 'Rankine Oval':
            self.U = self.source(X+2,Y,10)[0]+self.source(X-2,Y,-10)[0]+self.uniform(X,Y,1,1,0)[0]
            self.V = self.source(X+2,Y,10)[1]+self.source(X-2,Y,-10)[1]+self.uniform(X,Y,1,1,0)[1]
            self.FigSubPlot.streamplot(X, Y,self.U,self.V, color='k', linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle='-')
        #elif self.listbox.get(self.listbox.curselection()) == 'Cylinder':
        elif self.radio_var.get() == 'Cylinder':
            self.U = self.doublet(X,Y,25)[0]+self.uniform(X,Y,1,1,0)[0]
            self.V = self.doublet(X,Y,25)[1]+self.uniform(X,Y,1,1,0)[1]
            self.FigSubPlot.streamplot(X, Y,self.U,self.V, color='k', linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle='-')
        #elif self.listbox.get(self.listbox.curselection()) == 'Stagnation & Vortex':
        elif self.radio_var.get() == 'Stagnation & Vortex':
            self.U = self.vortex(X,Y,25)[0]+self.corner(X,Y,'2,1')[0]
            self.V = self.vortex(X,Y,25)[1]+self.corner(X,Y,'2,1')[1]
            self.FigSubPlot.streamplot(X, Y,self.U,self.V, color='k', linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle='-')
        self.FigSubPlot.set_xlim(self.xlim)
        self.FigSubPlot.set_ylim(self.ylim)
        self.canvas.draw()
#        self.old = self.listbox.get(self.listbox.curselection())
    def source(self,X,Y,l):
        l = float(l)
        U = (l/(2*pi))*X/(X*X + Y*Y)
        V = (l/(2*pi))*Y/(X*X + Y*Y)
        return (U,V)
    def vortex(self,X,Y,g):
        g = float(g)
        U = (g/(2*pi))*Y/(X*X + Y*Y)
        V = (g/(2*pi))*-X/(X*X + Y*Y)
        return (U,V)
    def uniform(self,X,Y,v_0,x_0,y_0):
        v_0 = float(v_0)
        x_0 = float(x_0)
        y_0 = float(y_0)
        U = v_0*x_0/(x_0*x_0+y_0*y_0)**0.5
        V = v_0*y_0/(x_0*x_0+y_0*y_0)**0.5
        return (U,V)
    def doublet(self,X,Y,k):
        k = float(k)
        U = (k/(2*pi))*((2*Y*Y/((X*X+Y*Y)*(X*X+Y*Y)))-(1/(X*X+Y*Y)))
        V = -(k/(2*pi))*(2*X*Y/((X*X+Y*Y)*(X*X+Y*Y)))
        return (U,V)
    def corner(self,X,Y,tup):
        comma_flag = 0
        A = ''
        n = ''
        for char in tup:
            if char == ',':
                comma_flag = 1
            elif comma_flag == 0:
                n += char
            elif comma_flag == 1:
                A += char
        A = float(A)
        n = float(n)
        R = (X*X+Y*Y)**0.5
        t = arctan2(-Y,-X)
        U = -A*n*R**(n-1)*(cos(n*t)*cos(t)+sin(n*t)*sin(t))
        V = -A*n*R**(n-1)*(cos(n*t)*sin(t)-sin(n*t)*cos(t))
        return (U,V)
    def stream_source(self,X,Y,l):
        l = float(l)
        stream = (l/(2*pi))*arctan2(-Y,-X)
        return stream
    def stream_vortex(self,X,Y,g):
        g = float(g)
        stream = (g/(2*pi))*log((X*X + Y*Y)**0.5)
        return stream
    def stream_uniform(self,X,Y,v_0,x_0,y_0):
        v_0 = float(v_0)
        x_0 = float(x_0)
        y_0 = float(y_0)
        stream = (v_0*Y*x_0/(x_0*x_0+y_0*y_0)**0.5)-(v_0*X*y_0/(x_0*x_0+y_0*y_0)**0.5)
        return stream
    def stream_doublet(self,X,Y,k):
        k = float(k)
        stream = -(k/(2*pi))*Y/(X*X+Y*Y)
        return stream
    def stream_corner(self,X,Y,tup):
        comma_flag = 0
        A = ''
        n = ''
        for char in tup:
            if char == ',':
                comma_flag = 1
            elif comma_flag == 0:
                n += char
            elif comma_flag == 1:
                A += char
        A = float(A)
        n = float(n)
        stream = A*(X*X+Y*Y)**(n*0.5)*sin(n*arctan2(-Y,-X))
        return stream
    def quit(self):
        self.master.destroy()    
    def Continue(self):
        self.master.withdraw()
        self.main = Toplevel(self.master)
        self.main.geometry("%dx%d+%d+%d" % (1038-206, 
                               694,
                               int((500.0/2560.0)*screen_resolution[0]), 
                               int((60.0/1440.0)*screen_resolution[1])))
        self.main.minsize(376,227)                      
        self.interior = PanedWindow(self.main,sashwidth=5)
        self.interior.pack(fill=BOTH, expand=1)

        self.elements_frame = Frame(self.interior, height=1038, width=212,relief=RIDGE,borderwidth=0)
        self.interior.add(self.elements_frame) 
        self.interior.paneconfig(self.elements_frame,minsize=130)
        self.graph_frame = Frame(self.interior)
        self.interior.add(self.graph_frame)
        self.interior.paneconfig(self.graph_frame,minsize=130)

        self.main.bind("<ButtonRelease-1>",self.pan_update)
        self.main.bind("<ButtonRelease-3>",self.pan_update)
        self.main.bind("<Button-3>",self.right_menu)
        
        self.edit_frame = Frame(self.graph_frame)
        self.edit_frame.pack(side=TOP,fill=X,padx=10)
        self.canvas = FigureCanvasTkAgg(self.Fig, master=self.graph_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=1)
        self.nav_frame = Frame(self.edit_frame)
        self.nav_frame.pack(side=LEFT,anchor=W)
        self.toolbar = NavigationToolbar(self.canvas, self.nav_frame)
        
        self.main.protocol('WM_DELETE_WINDOW',self.master.destroy) 
        self.elements = Treeview(self.elements_frame,columns=("values","xlocations","ylocations"),selectmode=BROWSE)
        self.elements.heading("#0",text="Components")
        self.elements.heading("values",text="Str")
        self.elements.heading("xlocations",text="X")
        self.elements.heading("ylocations",text="Y")
        self.elements.column("#0",width=90,anchor=CENTER)
        self.elements.column("values",width=45,anchor=CENTER)
        self.elements.column("xlocations",width=26,anchor=CENTER)
        self.elements.column("ylocations",width=26,anchor=CENTER)
        self.elements.pack(fill=BOTH,expand=1)
        
        self.as_button_frame = Frame(self.elements_frame)
        self.add_button = Button(self.as_button_frame,text = '+',width=2,command=self.add)       
        self.sub_button = Button(self.as_button_frame,text = '-',width=2,command=self.subtract) 
        self.options_button = Button(self.as_button_frame,text='Options',command=self.options)
        self.as_button_frame.pack(side=BOTTOM,anchor=W)
        self.options_button.pack(side=RIGHT)
        self.sub_button.pack(side=RIGHT,anchor=W)
        self.add_button.pack(side=LEFT,anchor=W)
        self.addsub_menu = Menu(self.as_button_frame,tearoff=0)
        self.addsub_menu.add_command(command=self.add_source,label='Source')
        self.addsub_menu.add_command(command=self.add_vortex,label='Vortex')
        self.addsub_menu.add_command(command=self.add_uniform,label='Uniform')
        self.addsub_menu.add_command(command=self.add_doublet,label='Doublet')
        self.addsub_menu.add_command(command=self.add_corner,label='Corner')
        

        #if self.listbox.get(self.listbox.curselection()) == 'Default':
        if self.radio_var.get() == 'Default':
            self.active_components = []
            self.active_calls = {} 
            pass
        #elif self.listbox.get(self.listbox.curselection()) == 'Maelstrom':
        elif self.radio_var.get() == 'Maelstrom':
            self.elements.insert("",0,"M",text="Maelstrom",open=TRUE)
            self.active_components = ['M']
            self.elements.insert("M",0,iid='s%s'%self.active_numbers['s'],text="Source",values=("%s"%1,0,0))
            self.elements.insert("M",0,iid='v%s'%self.active_numbers['v'],text="Vortex",values=("%s"%1,0,0))
            self.active_calls = {'s%s'%self.active_numbers['s']:("s",self.elements.item('s%s'%self.active_numbers['s'],"values")),
                                 'v%s'%self.active_numbers['v']:("v",self.elements.item('v%s'%self.active_numbers['v'],"values"))}
            self.active_numbers['s'] += 1
            self.active_numbers['v'] += 1
        elif self.radio_var.get() == 'Rankine Half-Body':
            self.elements.insert("",0,"RHF",text="Rankine Half-Body",open=TRUE)
            self.active_components = ['RHF']
            self.elements.insert("RHF",0,iid='s%s'%self.active_numbers['s'],text="Source",values=("%s"%10,0,0))
            self.elements.insert("RHF",0,iid='u%s'%self.active_numbers['u'],text="Uniform",values=("%s"%1,1,0))
            self.active_calls = {'s%s'%self.active_numbers['s']:("s",self.elements.item('s%s'%self.active_numbers['s'],"values")),
                                 'u%s'%self.active_numbers['u']:("u",self.elements.item('u%s'%self.active_numbers['u'],"values"))}
            self.active_numbers['s'] += 1
            self.active_numbers['u'] += 1
        elif self.radio_var.get() == 'Rankine Oval':
            self.elements.insert("",0,"RO",text="Rankine Oval",open=TRUE)
            self.active_components = ['RO']
            self.elements.insert("RO",0,iid='s%s'%self.active_numbers['s'],text="Source",values=("%s"%10,-2,0))
            self.elements.insert("RO",0,iid='s%s'%(self.active_numbers['s']+1),text="Source",values=("%s"%-10,2,0))
            self.elements.insert("RO",0,iid='u%s'%self.active_numbers['u'],text="Uniform",values=("%s"%1,1,0))
            self.active_calls = {'s%s'%self.active_numbers['s']:("s",self.elements.item('s%s'%self.active_numbers['s'],"values")),
                                 's%s'%(self.active_numbers['s']+1):("s",self.elements.item('s%s'%(self.active_numbers['s']+1),"values")),
                                 'u%s'%self.active_numbers['u']:("u",self.elements.item('u%s'%self.active_numbers['u'],"values"))}
            self.active_numbers['s'] += 2
            self.active_numbers['u'] += 1       
        elif self.radio_var.get() == 'Cylinder':
            self.elements.insert("",0,'D+U',text="Cylinder",open=TRUE)
            self.active_components = ['D+U']
            self.elements.insert('D+U',0,iid='d%s'%self.active_numbers['d'],text="Doublet",values=("%s"%25,0,0))
            self.elements.insert('D+U',0,iid='u%s'%self.active_numbers['u'],text="Uniform",values=("%s"%1,1,0))
            self.active_calls = {'d%s'%self.active_numbers['d']:("d",self.elements.item('d%s'%self.active_numbers['d'],"values")),
                                 'u%s'%self.active_numbers['u']:("u",self.elements.item('u%s'%self.active_numbers['u'],"values"))}
            self.active_numbers['d'] += 1
            self.active_numbers['u'] += 1
        elif self.radio_var.get() == 'Stagnation & Vortex':
            self.elements.insert("",0,'S+V',text="Stag+Vort",open=TRUE)
            self.active_components = ['S+V']
            self.elements.insert('S+V',0,iid='n%s'%self.active_numbers['n'],text="C (n,A)",values=("%s,%s"%(2,1),0,0))
            self.elements.insert('S+V',0,iid='v%s'%self.active_numbers['v'],text="Vortex",values=("%s"%25,0,0))
            self.active_calls = {'n%s'%self.active_numbers['n']:("n",self.elements.item('n%s'%self.active_numbers['n'],"values")),
                                 'v%s'%self.active_numbers['v']:("v",self.elements.item('v%s'%self.active_numbers['v'],"values"))}
            self.active_numbers['n'] += 1
            self.active_numbers['v'] += 1
        self.elements.bind("<Double-Button-1>",self.edit)
        self.elements.bind('<<TreeviewSelect>>',self.treeview_select)
        self.main.bind("<Return>",self.edit_return)
        self.main.bind("<Escape>",self.edit_return)

        
        self.rightc_menu = Menu(self.graph_frame,tearoff=0)
        self.add_menu = Menu(self.rightc_menu,tearoff=0)
        self.rightc_menu.add_cascade(label="Add",menu=self.add_menu)
        self.add_menu.add_command(command=self.addm_source,label='Source')
        self.add_menu.add_command(command=self.addm_vortex,label='Vortex')
        self.add_menu.add_command(command=self.addm_uniform,label='Uniform')
        self.add_menu.add_command(command=self.addm_doublet,label='Doublet')
        self.add_menu.add_command(command=self.addm_corner,label='Corner')
    def right_menu(self,event):
        print "event", event.x,event.y
        #print "graph", self.main.winfo_x()+self.interior.winfo_x()+self.graph_frame.winfo_x(), self.main.winfo_y()+self.interior.winfo_y()+self.graph_frame.winfo_y()
        self.plot_x,self.plot_y = self.FigSubPlot.transData.inverted().transform((event.x,event.y+20))
        self.plot_y = -self.plot_y
        self.rightc_menu.post(self.main.winfo_x()+self.interior.winfo_x()+self.graph_frame.winfo_x()+event.x+9,self.main.winfo_y()+self.graph_frame.winfo_y()+event.y+66)
        
    def treeview_select(self,event):
        if self.elements.get_children(self.elements.selection()[0]) == ():
            if self.mark_var.get() == 0 or self.selected == self.elements.selection():
                pass
            elif self.mark_var.get() == 1:
                
                #add red markers here
                
                if self.elements.selection() != '':
                    child = self.elements.selection()[0]
                    if child != '':
                        self.sel_point = (self.elements.item(child,"values")[1],self.elements.item(child,"values")[2])
                        self.graph_update()
                        self.selected = self.elements.selection()
                else:
                    pass
        else:
            if self.mark_var.get() == 0 or self.selected == self.elements.selection():
                pass
            elif self.mark_var.get() == 1:
                if self.elements.selection() != '':
                    child = self.elements.selection()[0]
                    if child != '':
                        self.sel_point = None
                        self.graph_update()
                        self.selected = self.elements.selection()
    def mark_check_fun(self):
        if self.mark_var.get() == 0:
            self.sel_point = None
            self.graph_update()
        elif self.elements.selection() != '':
            child = self.elements.selection()[0]
            self.sel_point = [self.elements.item(child,"values")[1],self.elements.item(child,"values")[2]]
            self.graph_update()
            
    def add(self):
        self.addsub_menu.post(self.main.winfo_x()+self.as_button_frame.winfo_x()+self.add_button.winfo_x(),self.main.winfo_y()+self.as_button_frame.winfo_y()+self.add_button.winfo_y()-len(self.active_numbers.keys())*14)
    def subtract(self):
        if self.active_edit_flag == 1:
            self.del_edit(self)
        child = self.elements.selection()[0]
        if child == '':
            return
        if self.elements.parent(child) == '':
            ID = child
            self.active_components.remove(child)
            self.elements.delete(child)
        else:
            ID = self.elements.parent(child)
            self.active_components.remove(ID)
            for comp in self.elements.get_children(ID):
                if comp != child:
                    self.active_components.append(comp)
                    self.elements.move(comp,"",0)
            self.elements.delete(ID)
        self.sel_point = None
        self.graph_update()
    def options(self):
        self.options_window = Toplevel(self.main)
        self.options_window.geometry("%dx%d+%d+%d" % (280, 
                                                      200+20,
                                                      self.main.winfo_x()+self.as_button_frame.winfo_x()+self.options_button.winfo_x()-272+26+72+86,
                                                      self.main.winfo_y()+self.as_button_frame.winfo_y()+self.options_button.winfo_y()-196-20))
        self.main.bind('<FocusIn>',self.close_options)
        self.options_window.title("Options")
        self.options_window.update_idletasks()
        self.options_window.bind("<ButtonRelease-1>",self.pan_update)
        self.options_frame = Frame(self.options_window)
        self.options_frame.pack(fill=BOTH,expand=1)
        self.options_window.attributes("-topmost",True)

        self.line_frame = Frame(self.options_frame,bd=2,relief=RIDGE)
        self.line_frame.grid(row=0,column=1,sticky=N+S+E+W,ipady=7)
        self.color_frame = Frame(self.options_frame,bd=2,relief=RIDGE,padx=2)
        self.color_frame.grid(row=0,column=0,sticky=N+S+E+W)
        
        self.color_button = Label(self.color_frame,bg=self.line_color.get(),text = '     ')
        self.color_button.pack(side=RIGHT)
        Label(self.color_frame,text='C:').pack(side=RIGHT)
        self.color_button.bind('<Button-1>',self.getColor)
        
        self.wt_slider = Scale(self.line_frame,from_=1,to=100,orient=HORIZONTAL,variable=self.line_var)
        if self.wt_var.get() == '-> WT:':
            self.wt_slider.config(variable=self.arrow_var)
        elif self.wt_var.get() == '- WT:':
            self.wt_slider.config(variable=self.line_var)
        elif self.wt_var.get() == 'div WT:':
            self.wt_slider.config(variable=self.div_check_var)
        self.wt_slider.pack(side=RIGHT)
        
        self.wt_menu = OptionMenu(self.line_frame,self.wt_var,'- WT:','-> WT:','div WT:')
        self.wt_menu.pack(side=RIGHT,anchor='center',fill=X,expand=1)
        self.wt_menu.config(width=8)
        self.density_frame = Frame(self.options_frame,bd=2,relief=RIDGE)
        self.density_frame.grid(row=1,column=1,sticky=N+S+E+W)
        self.density_slider = Scale(self.density_frame,from_=1,to=100,orient=HORIZONTAL,variable=self.density_var)
        self.density_slider.pack(side=RIGHT)
        Label(self.density_frame,text='Density').pack(side=LEFT,anchor=CENTER,fill=X,expand=1)
        
        self.linet_frame = Frame(self.options_frame,bd=2,relief=RIDGE)
        self.linet_frame.grid(row=1,column=0,sticky=N+S+E+W)
        Label(self.linet_frame,text='Style').pack(anchor='n')
        self.linet_menu = OptionMenu(self.linet_frame,self.linet_var,'-','->','-|>')
        self.linet_menu.pack(anchor='s',side=BOTTOM)
        self.linet_menu.config(width=5)
        
        self.div_check = Checkbutton(self.options_frame,text = 'Dividing Streamline',variable=self.div_var,onvalue=1,offvalue=0,command = self.graph_update)
        self.div_check.grid(row=2,column=1,sticky=W)
        self.mark_check = Checkbutton(self.options_frame,text = 'Selection Marker',variable=self.mark_var,onvalue=1,offvalue=0,command = self.mark_check_fun)
        self.mark_check.grid(row=3,column=1,sticky=W)
        
        self.limit_frame = Frame(self.options_frame)
        self.limit_frame.grid(row=4,column=1,sticky=W)
        #self.aspect_lock = Checkbutton(self.limit_frame,text='LK',variable = self.lock_var)
        #self.aspect_lock.grid(row=0,column=4,rowspan=2,sticky=E)
        
        Label(self.limit_frame,text='x').grid(row=0,column=0)
        self.xlimlow_var = DoubleVar()
        self.xlimlow_var.set(self.FigSubPlot.get_xlim()[0])
        self.xlimlow_entry = Entry(self.limit_frame,textvariable=self.xlimlow_var,width=5)
        self.xlimlow_entry.grid(row=0,column=1)
        Label(self.limit_frame,text='...').grid(row=0,column=2)
        self.xlimhigh_var = DoubleVar()
        self.xlimhigh_var.set(self.FigSubPlot.get_xlim()[1])
        self.xlimhigh_entry = Entry(self.limit_frame,textvariable=self.xlimhigh_var,width=5)
        self.xlimhigh_entry.grid(row=0,column=3)
        Label(self.limit_frame,text='y').grid(row=1,column=0)
        self.ylimlow_var = DoubleVar()
        self.ylimlow_var.set(self.FigSubPlot.get_ylim()[0])
        self.ylimlow_entry = Entry(self.limit_frame,textvariable=self.ylimlow_var,width=5)
        self.ylimlow_entry.grid(row=1,column=1)
        Label(self.limit_frame,text='...').grid(row=1,column=2)
        self.ylimhigh_var = DoubleVar()
        self.ylimhigh_var.set(self.FigSubPlot.get_ylim()[1])
        self.ylimhigh_entry = Entry(self.limit_frame,textvariable=self.ylimhigh_var,width=5)
        self.ylimhigh_entry.grid(row=1,column=3)
        
        
        #self.limit_frame.bind('<FocusOut>',self.limits_update)
        self.xlimhigh_var.trace('w',self.limits_update)
        self.ylimhigh_var.trace('w',self.limits_update)
        self.xlimlow_var.trace('w',self.limits_update)
        self.ylimlow_var.trace('w',self.limits_update)
        
    def limits_update(self,*args):

        if self.xlimlow_entry.get() == '' or self.ylimlow_entry.get() == '' or self.xlimhigh_entry.get() == '' or self.ylimhigh_entry.get() == '':
            pass
        elif self.xlimlow_entry.get() == '-' or self.ylimlow_entry.get() == '-' or self.xlimhigh_entry.get() == '-' or self.ylimhigh_entry.get() == '-':
            pass
        elif self.xlimlow_entry.get() == '.' or self.ylimlow_entry.get() == '.' or self.xlimhigh_entry.get() == '.' or self.ylimhigh_entry.get() == '.':
            pass
        else:
            self.xlim = [float(self.xlimlow_var.get()),float(self.xlimhigh_var.get())]
            self.ylim = [float(self.ylimlow_var.get()),float(self.ylimhigh_var.get())]

            self.FigSubPlot.set_xlim(self.xlim)
            self.FigSubPlot.set_ylim(self.ylim)
            self.graph_update()
    def getColor(self,event):
        color=askcolor(self.line_color.get())
        if color != "None":
            self.line_color.set(color[1])
            self.graph_update()
    def wt_update(self,*args):
        if self.wt_var.get() == '-> WT:':
            self.wt_slider.config(variable=self.arrow_var)
        elif self.wt_var.get() == '- WT:':
            self.wt_slider.config(variable=self.line_var)
        elif self.wt_var.get() == 'div WT:':
            self.wt_slider.config(variable=self.div_check_var)
    def line_style_update(self,*args):
        self.graph_update()
    def close_options(self,event):
        self.options_window.destroy()
    def add_source(self):
        if self.modify_flag == 0:
            self.plot_x,self.plot_y = 0,0
        self.elements.insert("",0,iid='s%s'%self.active_numbers['s'],text="Source",values=("%s"%1,self.plot_x,self.plot_y))
        self.active_calls['s%s'%self.active_numbers['s']] = ("s",self.elements.item('s%s'%self.active_numbers['s'],"values"))
        self.active_components.append('s%s'%self.active_numbers['s'])
        if self.modify_flag == 1:
            self.elements.selection_set('s%s'%self.active_numbers['s'])
            self.modify_flag = 0
        self.graph_update()
        self.active_numbers['s'] += 1
        
    def add_vortex(self):
        if self.modify_flag == 0:
            self.plot_x,self.plot_y = 0,0
        self.elements.insert("",0,iid='v%s'%self.active_numbers['v'],text="Vortex",values=("%s"%1,self.plot_x,self.plot_y))
        self.active_calls['v%s'%self.active_numbers['v']] = ("v",self.elements.item('v%s'%self.active_numbers['v'],"values"))
        self.active_components.append('v%s'%self.active_numbers['v'])

        if self.modify_flag == 1:
            self.elements.selection_set('v%s'%self.active_numbers['v'])
            self.modify_flag = 0
        self.graph_update()
        self.active_numbers['v'] += 1
    def add_uniform(self):
        if self.modify_flag == 0:
            self.plot_x,self.plot_y = 1,0
        self.elements.insert("",0,iid='u%s'%self.active_numbers['u'],text="Uniform",values=("%s"%1,self.plot_x,self.plot_y))
        self.active_calls['u%s'%self.active_numbers['u']] = ("u",self.elements.item('u%s'%self.active_numbers['u'],"values"))
        self.active_components.append('u%s'%self.active_numbers['u'])
        if self.modify_flag == 1:
            self.elements.selection_set('u%s'%self.active_numbers['u'])
            self.modify_flag = 0
        self.graph_update()
        self.active_numbers['u'] += 1
    def add_doublet(self):
        if self.modify_flag == 0:
            self.plot_x,self.plot_y = 0,0
        self.elements.insert("",0,iid='d%s'%self.active_numbers['d'],text="Doublet",values=("%s"%1,self.plot_x,self.plot_y))
        self.active_calls['d%s'%self.active_numbers['d']] = ("d",self.elements.item('d%s'%self.active_numbers['d'],"values"))
        self.active_components.append('d%s'%self.active_numbers['d'])
        if self.modify_flag == 1:
            self.elements.selection_set('d%s'%self.active_numbers['d'])
            self.modify_flag = 0
        self.graph_update()
        self.active_numbers['d'] += 1
    def add_corner(self):
        if self.modify_flag == 0:
            self.plot_x,self.plot_y = 0,0
        self.elements.insert("",0,iid='n%s'%self.active_numbers['n'],text="Corner (n,A)",values=("%s,%s"%(2,1),self.plot_x,self.plot_y))
        self.active_calls['n%s'%self.active_numbers['n']] = ("n",self.elements.item('n%s'%self.active_numbers['n'],"values"))
        self.active_components.append('n%s'%self.active_numbers['n'])
        if self.modify_flag == 1:
            self.elements.selection_set('n%s'%self.active_numbers['n'])
            self.modify_flag = 0
        self.graph_update()
        self.active_numbers['n'] += 1
    def addm_source(self):
        self.modify_flag = 1 
        self.add_source()
    def addm_vortex(self):
        self.modify_flag = 1
        self.add_vortex()
    def addm_uniform(self):
        self.modify_flag = 1
        self.add_uniform()
    def addm_doublet(self):
        self.modify_flag = 1
        self.add_doublet()
    def addm_corner(self):
        self.modify_flag = 1
        self.add_corner()
    def pan_update(self,event):
        if [self.FigSubPlot.get_xlim()[0],self.FigSubPlot.get_xlim()[1]] != self.xlim or [self.FigSubPlot.get_ylim()[0],self.FigSubPlot.get_ylim()[1]] != self.ylim or self.density_var.get() != self.density_val or self.line_var.get() != self.line_val or self.arrow_var.get() != self.arrow_val or self.arrow_var.get() != self.arrow_val or self.div_check_var.get() != self.div_val:
            self.graph_update()
            self.density_val = self.density_var.get()
            self.line_val = self.line_var.get()
            self.arrow_val = self.arrow_var.get()
            self.div_val = self.div_check_var.get()
        else:
            return
    def graph_update(self):
        self.FigSubPlot.clear()
        Y, X = mgrid[self.FigSubPlot.get_ylim()[0]:self.FigSubPlot.get_ylim()[1]:100j, self.FigSubPlot.get_xlim()[0]:self.FigSubPlot.get_xlim()[1]:100j]     
        self.xlim = [self.FigSubPlot.get_xlim()[0],self.FigSubPlot.get_xlim()[1]]
        self.ylim = [self.FigSubPlot.get_ylim()[0],self.FigSubPlot.get_ylim()[1]]
        self.U = 0*X
        self.V = 0*X      
        self.stream = 0*X
        for ID in self.active_components:
            if self.elements.get_children(ID) == ():
                child = ID
                self.active_calls[child] = (child[0],self.elements.item(child,"values"))
                if self.active_calls[child][0] == "s":
                    self.U += self.source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                    self.V += self.source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                    self.stream += self.stream_source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                elif self.active_calls[child][0] == 'v':
                    self.U += self.vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                    self.V += self.vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                    self.stream += self.stream_vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                elif self.active_calls[child][0] == 'u':
                    if self.active_calls[child][1][1] == '0' and self.active_calls[child][1][2] == '0':
                        pass
                    else:
                        self.U += self.uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])[0]
                        self.V += self.uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])[1]
                        self.stream += self.stream_uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])
                elif self.active_calls[child][0] == 'd':
                    self.U += self.doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                    self.V += self.doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                    self.stream += self.stream_doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                elif self.active_calls[child][0] == 'n':
                    self.U += self.corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                    self.V += self.corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                    self.stream += self.stream_corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
            else:
                for child in self.elements.get_children(ID):
                    self.active_calls[child] = (child[0],self.elements.item(child,"values"))
                    if self.active_calls[child][0] == "s":
                        self.U += self.source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                        self.V += self.source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                        self.stream += self.stream_source(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                    elif self.active_calls[child][0] == 'v':
                        self.U += self.vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                        self.V += self.vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                        self.stream += self.stream_vortex(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                    elif self.active_calls[child][0] == 'u':
                        if self.active_calls[child][1][1] == '0' and self.active_calls[child][1][2] == '0':
                            pass
                        else:
                            self.U += self.uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])[0]
                            self.V += self.uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])[1]
                            self.stream += self.stream_uniform(X,Y,self.active_calls[child][1][0],self.active_calls[child][1][1],self.active_calls[child][1][2])
                    elif self.active_calls[child][0] == 'd':
                        self.U += self.doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                        self.V += self.doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                        self.stream += self.stream_doublet(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])
                    elif self.active_calls[child][0] == 'n':
                        self.U += self.corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[0]
                        self.V += self.corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])[1]
                        self.stream += self.stream_corner(X-float(self.active_calls[child][1][1]),Y-float(self.active_calls[child][1][2]),self.active_calls[child][1][0])

        self.FigSubPlot.streamplot(X,Y,self.U,self.V,color=self.line_color.get(), linewidth=(2.0/71.0)*self.line_var.get()+(13.0/71.0),density=(2.0/71.0)*self.density_var.get()+(13.0/71.0),arrowstyle=self.linet_var.get(),arrowsize=(4.0/71.0)*self.arrow_var.get()+(13.0/71.0))
        if self.div_var.get() == 1:
            #self.FigSubPlot.contour(X,Y,self.stream,[-0.01,0.01],linewidths=[(4.0/71.0)*self.div_check_var.get()+(13.0/71.0),(4.0/71.0)*self.div_check_var.get()+(13.0/71.0)])
            
            self.FigSubPlot.contour(X,Y,self.stream,[0],linewidths=[(4.0/71.0)*self.div_check_var.get()+(13.0/71.0)])
        if self.mark_var.get() == 1:
            if self.sel_point != None:
                self.plot_point()
        self.FigSubPlot.set_xlim(self.xlim)
        self.FigSubPlot.set_ylim(self.ylim)
        self.canvas.draw()
    def plot_point(self):
        if self.elements.selection()[0][0] == 'u':
            norm = float(float(self.sel_point[0])*float(self.sel_point[0])+float(self.sel_point[1])*float(self.sel_point[1]))**0.5
            if norm == 0:
                norm = 1
            X,Y,U,V = 0,0, float(self.sel_point[0])/norm,float(self.sel_point[1])/norm
            self.FigSubPlot.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1,color='g')
        else:
            self.FigSubPlot.plot([self.sel_point[0]],[self.sel_point[1]],'r^',ms=10)
    def edit(self,event):
        if self.active_edit_flag == 1 or self.elements.identify_row(event.y) == '':
            pass
        else:
            self.rowid = self.elements.identify_row(event.y)
            self.column = self.elements.identify_column(event.x)
            self.edit_var = StringVar()
            if int(self.column[-1]) == 0:
                self.edit_var.set('%s'%self.elements.item("%s"%self.elements.identify("item",event.x, event.y))['text'])

            else:
                self.edit_var.set('%s'%self.elements.item("%s"%self.elements.identify("item",event.x, event.y))['values'][int(self.column[-1])-1])

            x,y,width,height = self.elements.bbox(self.rowid, self.column)
            self.edit_entry = Entry(self.elements_frame,textvariable=self.edit_var)
            self.edit_entry.place(x=x,y=y,width=width)
            self.edit_entry.focus_force()
            self.edit_entry.bind("<FocusOut>", self.del_edit)
            self.active_edit_flag = 1
    def edit_return(self,event):
        self.main.focus()
    def del_edit(self,event):
        if self.column[-1] == '0':
            self.elements.item(self.rowid,text='%s'%self.edit_var.get())
        elif self.rowid[0] == 'n' and self.column[-1] == '1' and ',' not in self.edit_var.get():
            pass
        else:
            value = ''
            initial_value = str(self.elements.item(self.rowid)['values'][int(self.column[-1])-1])
            comma_flag = 0
            div_flag = 0
            for index in range(0,len(self.edit_var.get())):
                char = self.edit_var.get()[index]
                if char in '-0123456789.':
                    value += char
                elif self.rowid[0] == 'n' and char == ',':
                    if comma_flag == 1:
                        self.edit_entry.destroy()
                        self.active_edit_flag = 0
                        return
                    value += char
                    comma_flag = 1
                    comma_index = index
                if char == '/':
                    if div_flag == 0:
                        div_flag = 1
                        div_index = index
                    elif div_flag == 1 and comma_flag == 1:
                        div_flag = 2
                        div_index2 = index
                    elif div_flag == 1 and comma_flag == 0 or div_flag == 2:
                        self.edit_entry.destroy()
                        self.active_edit_flag = 0
                        return
                   
            if div_flag == 1:
                if comma_flag == 1:
                    if div_index < comma_index:
                        arg = int(float(value[:div_index])*100/float(value[div_index:comma_index-1]))/100.0
                        value = str(arg)+value[comma_index-1:]
                    elif div_index > comma_index:
                        arg = int(float(value[comma_index+1:div_index])*100/float(value[div_index:]))/100.0
                        value = value[:comma_index+1]+str(arg)
                else:
                    arg = int(float(value[:div_index])*100/float(value[div_index:]))/100.0
                    value = str(arg)
            elif div_flag == 2: 
                arg1 = int(float(value[:div_index])*100/float(value[div_index:comma_index-1]))/100.0
                arg2 = int(float(value[comma_index:div_index2-1])*100/float(value[div_index2-1:]))/100.0
                value = str(arg1)+','+str(arg2)
            if value == '' or value == initial_value:
                self.edit_entry.destroy()
                self.active_edit_flag = 0
                return
            
            self.elements.set(self.rowid,column=(int(self.column[-1])-1),value=value)
            if self.mark_var.get() == 1:
                self.sel_point = [self.elements.item(self.rowid,"values")[1],self.elements.item(self.rowid,"values")[2]]
            self.graph_update()
        self.edit_entry.destroy()
        self.active_edit_flag = 0
class NavigationToolbar(NavigationToolbar2TkAgg):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2TkAgg.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
root = Tk()
screen_resolution = (root.winfo_screenwidth(),root.winfo_screenheight())
root.geometry("%dx%d+%d+%d" % (470, 
                               315,
                               int((1045.0/2560.0)*screen_resolution[0]), 
                               int((280.0/1440.0)*screen_resolution[1])))
app=App(root)
root.mainloop()