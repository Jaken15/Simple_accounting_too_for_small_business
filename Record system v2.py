from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from data_validation import valid_date as Data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class simple_accountant_tool:
    def __init__(self,root):
        root.title("Expense tracker")
        root.geometry("1000x550")
        root.config(bg="#f5f6fa")
        root.resizable(False,False)
        self.process = Data()

        self.header = Frame(root,bg="#40739e",height=60)
        self.header.pack(fill='x')
        self.expenses_listbox = None

        header_label = Label(self.header,
                                text="     Simple Accounting Tool For Small Business",
                                font=("arial",18,"bold"),
                                fg="white",
                                bg="#40739e")
        header_label.pack(pady=15,padx=45)

        self.sidebar = Frame(root,bg="#2f3640",width=200)
        self.sidebar.pack(side='left',fill='y')
        self.expenses_listbox = None
        self.trasaction_history = None

        self.sidebar_button("Home",self.Home_frame).pack(fill='x')
        self.sidebar_button("History",self.history_frame).pack(fill='x')
        self.sidebar_button("Settings",self.Home_frame).pack(fill='x')

        self.main_frame = Frame(root,bg="#f5f6fa")
        self.main_frame.pack(fill=BOTH,expand=True)
        self.Home_frame()

    def Home_frame(self):
        self.clear_widget()
        content = Frame(self.main_frame,bg="#f5f6fa")
        content.pack(fill=BOTH,side='left',expand=True,padx=20,pady=20)

        Uppper_frame = Frame(content,bg='white',bd=1,relief='solid')
        Uppper_frame.pack(fill='x',pady=10)

        add_expenses_label = Label(Uppper_frame,
                                   text="Add Expenses",
                                   font=("arial",12,"bold"),
                                   bg='white')
        add_expenses_label.pack(anchor='center',padx=10,pady=10)

        add_expenses_entry = Entry(Uppper_frame,
                                   font=("arial",12))
        add_expenses_entry.insert(0," Enter Amount")
        add_expenses_entry.pack(fill='x',padx=10,pady=5)
        add_expenses_entry.bind("<FocusIn>",self.clear_entry)


        category_expenses_entry = ttk.Combobox(Uppper_frame,
                                               values=self.process.categories(),
                                        font=("arial",12),)
        
        category_expenses_entry.insert(0,"Enter category")
        category_expenses_entry.pack(fill='x',padx=10,pady=5)
        
        expenses_add_button = Button(Uppper_frame,
                                     text="Add Expenses",
                                     font=("arial",12),
                                     bg="#40739e",
                                     fg='white',
                                     relief='flat',
                                     command=lambda:self.add_data(add_expenses_entry,
                                                                  "expense",category_expenses_entry,expense_listbox))
        expenses_add_button.pack(padx=10,pady=10,side='right')

        income_add_button = Button(Uppper_frame,
                                   text="Add Income",
                                   font=("arial",12),
                                   bg="#40739e",
                                   fg="white",
                                   relief="flat",
                                   command=lambda:self.add_data(add_expenses_entry,
                                                                "income",category_expenses_entry,expense_listbox))
        income_add_button.pack(padx=10,pady=10,side='right')
        
        lower_frame = Frame(content,bg='white')
        lower_frame.pack(fill='both',expand=True)

        # list frame 

        list_frame = Frame(lower_frame,bg='white',bd=1,relief='solid',width=300,)
        list_frame.pack(side=LEFT,fill=Y)
        list_frame.pack_propagate(False)

        expenses_list_label =Label(list_frame,
                                   text="Expenses",
                                   font=("arial",14,"bold"),
                                   bg='white'
                                   )
        expenses_list_label.pack(padx=10,pady=10,anchor='center')

        expense_listbox = Listbox(list_frame,
                                    font=("arial",12),
                                    bd=0)
        categories_and_expenses = self.process.recent_category_expenses()
        for data in categories_and_expenses:
            expense_listbox.insert(0,f"{data[0]} $: {data[1]}")
        expense_listbox.pack(fill='both',expand=True,padx=10,pady=5)

        # Bar chart frame

        chart_container = Frame(lower_frame,bg='white',bd=1,relief='solid')
        chart_container.pack(side='left',expand=True,fill='both',padx=10,pady=5)

        canvas = Canvas(chart_container)
        canvas.pack(side='left',fill='both',expand=True)

        v_scroll = Scrollbar(chart_container, orient='vertical', command=canvas.yview)
        v_scroll.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=v_scroll.set)

        scrollable_frame = Frame(canvas)
        canvas.create_window((0,0), window=scrollable_frame, anchor='nw')

        def configure_scrollable_frame(event):
           canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scrollable_frame)

        categories = [item[0] for item in categories_and_expenses]
        amount = [item[1] for item in categories_and_expenses]

# Adjust figure height based on number of categories
        fig_height = max(len(categories) * 0.4, 4)
        fig, ax = plt.subplots(figsize=(6, fig_height))

        ax.barh(categories, amount)
        ax.set_title("Expenses By Category")
        ax.set_xlabel("Category")
        fig.tight_layout()

        chart_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(side='left')

        def start_scroll(event):
           canvas.scan_mark(event.x, event.y)

        def move_scroll(event):
           canvas.scan_dragto(event.x, event.y, gain=1)

        canvas.bind("<ButtonPress-1>", start_scroll)
        canvas.bind("<B1-Motion>", move_scroll)

# ---- Optional: Shift + Mouse Wheel horizontal scroll ----
        def shift_mouse_scroll(event):
            if event.state & 0x0001:  # Shift key pressed
               canvas.xview_scroll(-int(event.delta/120), "units")

        canvas.bind_all("<MouseWheel>", shift_mouse_scroll)  # Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.xview_scroll(-1, "units"))  # Linux up
        canvas.bind_all("<Button-5>", lambda e: canvas.xview_scroll(1, "units")) 
        
    def sidebar_button(self,Text,command):
        sidebar_button = Button(self.sidebar,
                                text=Text,
                                font=("arial",12),
                                fg='white',
                                bg="#353b48",
                                activebackground="#353b48",
                                activeforeground='white',
                                padx=20,
                                pady=10,
                                relief='flat',
                                command=command)
        return sidebar_button
    
    def history_frame(self):
        self.clear_widget()
        content = Frame(self.main_frame,bg="#f5f6fa")
        content.pack(fill='both',expand=True,pady=(30))

        trasaction_label = Label(content,
                                 text="My Transaction History",
                                 font=("arial",18,"bold"),
                                 bg="#f5f6fa",
                                 fg="#353b48")
        
        trasaction_label.pack(pady=(10,20))
        label_frame = Frame(content,bg="#f5f6fa")
        label_frame.pack(fill='x')

        body_frame = Frame(content, bg="#f5f6fa")
        body_frame.pack(fill='both', expand=True)

        type_label = Label(label_frame,
                           text="type :",
                           bg="#f5f6fa",
                           font=("arial",10))
        type_label.pack(side='left',padx=20)

        type_combobox = ttk.Combobox(label_frame,
                                     values=("income","expense","all"),
                           font=("arial",10),
                           width=8)
        type_combobox.pack(side='left')

        data = self.process.Database
        item_label = Label(label_frame,
                           text="Category :",
                           bg="#f5f6fa",
                           font=("arial",10))
        item_label.pack(side='left',padx=5)

        item_entry = ttk.Combobox(label_frame,
                           font=("arial",10),
                           width=10,
                           values=self.process.categories())
        item_entry.pack(side='left',padx=5)

        from_label = Label(label_frame,
                           text="from :",
                           bg="#f5f6fa",
                           font=("arial",10))
        from_label.pack(side='left',padx=5)

        date_list = self.process.list_of_date()
        start_date = ttk.Combobox(label_frame,
                           font=("arial",10),
                           width=10,
                           values=(date_list))
        start_date.pack(side='left',padx=5)

        end_date = Label(label_frame,
                           text="to :",
                           bg="#f5f6fa",
                           font=("arial",10))
        end_date.pack(side='left',padx=5)

        to_entry = ttk.Combobox(label_frame,
                           font=("arial",10),
                           width=10,
                           values=(date_list))
        to_entry.pack(side='left',padx=5)

        apply_date_filter = Button(label_frame,
                                   text="Apply date filter",
                                   font=("arial",10),
                                   bg="#40739e",
                                   fg="white",
                                   command=lambda:self.clear_treeview(trasaction_history,type_combobox,item_entry,start_date,to_entry))
        apply_date_filter.pack(side='left',padx=15)

        clear_date_filter = Button(label_frame,
                                   text="Clear date filter",
                                   font=("arial",10),
                                   bg="#c94c57",
                                   fg="white",
                                   command=lambda:self.clear_filter(type_combobox,item_entry,start_date,to_entry))
        clear_date_filter.pack(side='left',padx=15)

        treeview_frame = Frame(body_frame,bg="#f5f6fa",relief='raised',bd=2,
                               width=500,height=250)
        treeview_frame.pack(side='left',fill='both',expand=True,padx=20,pady=10)
        treeview_frame.pack_propagate(False)

        trasaction_history = ttk.Treeview(treeview_frame,
                                          columns=("id","amount","type","category","date"),
                                          show='headings')
        
        trasaction_history.column("id",anchor='center',width=70,stretch=False)
        trasaction_history.column("amount",anchor='center',width=70,stretch=False)
        trasaction_history.column("type",anchor='center',width=100,stretch=False)
        trasaction_history.column("category",anchor='center',width=120,stretch=False)
        trasaction_history.column("date",anchor='center',width=120,stretch=False)

        trasaction_history.heading("id",anchor="center",text="id")
        trasaction_history.heading("amount",anchor="center",text="amount")
        trasaction_history.heading("type",anchor="center",text="type")
        trasaction_history.heading("category",anchor="center",text="categiory")
        trasaction_history.heading("date",anchor="center",text="date")       
        
        data = self.process.all_data()
        for index,value in enumerate(data):
            trasaction_history.insert(parent='',index='end',iid=index,values=value)

        chart_container = Frame(body_frame, bg="#f5f6fa")
        chart_container.pack(side='right',fill='both',expand=True)

        sample_data = ["Expenses","Income","Balance"]
        colors = ["red","green","blue"]
        rate = self.process.balance_income_expense()
        fig,ax = plt.subplots(figsize=(3,4))

        ax.pie(rate,labels=sample_data,colors=colors,autopct="%1.1f%%")
        ax.set_title("Overall View")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig,master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        trasaction_history.pack(expand=True,fill='both')
        self.trasaction_history = trasaction_history

    def clear_widget(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def clear_entry(self,event):
        event.widget.delete(0,END)

    def add_data(self,amount,type,category,listbox):
        amount_value = amount.get()
        category_value = category.get()
        if amount_value and category_value:
            try:
                num = int(amount_value)
                result = category_value[0].upper() + category_value[1:]
                self.process.add_data_by_category(num,type,result)
                amount.delete(0,END)
                category.delete(0,END)
                self.refresh_listbox(listbox)
                
            except ValueError:
                messagebox.showwarning("Dinied","Enter a amount")
        else:
            messagebox.showwarning("Dinied","Cant add to database")

    def refresh_listbox(self,listbox):
        listbox.delete(0,END)
        data = self.process.recent_category_expenses()
        for i in data:
            listbox.insert(0,f"{i[0]} $: {i[1]}")

    def clear_filter(*widgets):
           for widget in widgets:
               try:
                   widget.delete(0,END)
               except:
                     try:
                        widget.set('')
                     except:
                         pass

    def clear_treeview(self,treeviw,type,category,start,end_date):

        type_value = type.get().strip() or None
        category_value = category.get().strip() or None
        start_value = start.get().strip() or None
        end_value = end_date.get().strip() or None

        for rows in treeviw.get_children():
            treeviw.delete(rows)

        results = self.process.filter_data(type_value,category_value,start_value,end_value)

        for row in results:
            treeviw.insert("","end",values=row)

        self.clear_filter(type,category,start,end_date)

root = Tk()
testing = simple_accountant_tool(root)
root.mainloop()
