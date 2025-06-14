import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import Style
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

KEYS = ['SAIL_PERNO', 'UNIT_PERNO']
EXCLUDE_COLUMNS = ['YYYYMM']
NEW_JOINEE_FIELDS = ['DOJ_SAIL', 'DOB', 'IFSC_CD', 'DOA']

class CSVComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Comparator")
        self.root.geometry("1100x750")
        self.dark_mode = False

        self.master_file = ""
        self.slave_file = ""
        self.data = {'diff': [], 'new': []}

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        self.style = Style()
        self.apply_light_mode()

    def apply_light_mode(self):
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#1513bd")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f4f4f4")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TNotebook", background="#11bb2b")
        self.style.configure("TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10))
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.root.configure(bg="#f4f4f4")

    def apply_dark_mode(self):
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TNotebook", background="#3c3f41")
        self.style.configure("TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10))
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#3c3f41", foreground="#ffffff", fieldbackground="#3c3f41")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2e2e2e", foreground="#ffffff")
        self.root.configure(bg="#2e2e2e")

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.apply_light_mode()
            self.dark_mode = False
        else:
            self.apply_dark_mode()
            self.dark_mode = True

    def create_widgets(self):
        frm_top = ttk.Frame(self.root, padding=10)
        frm_top.pack(pady=10, fill='x')

        title = ttk.Label(frm_top, text="CSV Comparator", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=5, pady=(0, 20), sticky="w")

        ttk.Label(frm_top, text="Master CSV:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.master_entry = ttk.Entry(frm_top, width=60)
        self.master_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frm_top, text="Browse", command=self.browse_master).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frm_top, text="Slave CSV:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.slave_entry = ttk.Entry(frm_top, width=60)
        self.slave_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frm_top, text="Browse", command=self.browse_slave).grid(row=2, column=2, padx=5, pady=5)

        btn_frame = ttk.Frame(frm_top)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="Compare", command=self.compare_csvs).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Export Differences", command=lambda: self.export_to_pdf('diff')).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Export New Joinees", command=lambda: self.export_to_pdf('new')).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack(side='left', padx=10)

        self.status = tk.Label(self.root, text="Welcome to CSV Comparator", anchor='w', bg="#e6e6e6", relief='sunken')
        self.status.pack(fill='x', side='bottom')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)

        self.tabs = {}
        self.create_table_tabs()

    def create_table_tabs(self):
        self.tables = {}
        self.search_entries = {}

        for key in ['diff', 'new']:
            tab = ttk.Frame(self.notebook)
            self.tabs[key] = tab
            self.notebook.add(tab, text=f"{key.title()} (0)")

            top = ttk.Frame(tab, padding=10)
            top.pack(fill='x')

            ttk.Label(top, text="Search:").pack(side='left')
            search_entry = ttk.Entry(top)
            search_entry.pack(side='left', fill='x', expand=True, padx=(5, 10))
            search_entry.bind('<KeyRelease>', lambda e, k=key: self.update_table_filter(k))
            self.search_entries[key] = search_entry

            tree_frame = ttk.Frame(tab)
            tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

            cols = ("Employee Key", "Field", "Old Value", "New Value")
            tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscroll=vsb.set, xscroll=hsb.set)

            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')

            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)

            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, anchor='w')

            self.tables[key] = tree

    def browse_master(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            self.master_entry.delete(0, tk.END)
            self.master_entry.insert(0, file)
            self.status.config(text=f"Selected Master: {os.path.basename(file)}")

    def browse_slave(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            self.slave_entry.delete(0, tk.END)
            self.slave_entry.insert(0, file)
            self.status.config(text=f"Selected Slave: {os.path.basename(file)}")

    def compare_csvs(self):
        self.master_file = self.master_entry.get()
        self.slave_file = self.slave_entry.get()
        if not self.master_file or not self.slave_file:
            messagebox.showwarning("Warning", "Please select both Master and Slave CSV files.")
            return

        try:
            df1 = pd.read_csv(self.master_file, dtype=str).fillna('')
            df2 = pd.read_csv(self.slave_file, dtype=str).fillna('')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV files: {e}")
            return

        df1.set_index(KEYS, inplace=True)
        df2.set_index(KEYS, inplace=True)

        self.data = {'diff': [], 'new': []}
        matched_keys = df1.index.intersection(df2.index)

        for key in matched_keys:
            row1 = df1.loc[key]
            row2 = df2.loc[key]
            differences = []
            for col in df1.columns:
                if col in EXCLUDE_COLUMNS:
                    continue
                val1 = str(row1[col]) if col in row1 else ''
                val2 = str(row2[col]) if col in row2 else ''
                if val1 != val2:
                    differences.append((col, val1, val2))
            if differences:
                emp_key = key[0]
                self.data['diff'].append({'key': f"--- Employee: {emp_key} ---", 'field': '', 'old': '', 'new': ''})
                for col, val1, val2 in differences:
                    self.data['diff'].append({'key': emp_key, 'field': col, 'old': val1, 'new': val2})

        new_keys = df2.index.difference(df1.index)
        for key in new_keys:
            emp_key = key[0]
            self.data['new'].append({'key': f"--- Employee: {emp_key} ---", 'field': '', 'old': '', 'new': ''})
            for col in NEW_JOINEE_FIELDS:
                val = df2.loc[key][col] if col in df2.columns and col in df2.loc[key] else ''
                self.data['new'].append({'key': emp_key, 'field': col, 'old': '', 'new': val})

        self.update_tabs()
        self.status.config(text="Comparison completed successfully.")

    def update_tabs(self):
        for tab_key, tree in self.tables.items():
            tree.delete(*tree.get_children())
            for row in self.data[tab_key]:
                values = (row['key'], row['field'], row['old'], row['new'])
                tree.insert('', 'end', values=values)

            if tab_key == 'diff':
                count = sum(1 for row in self.data[tab_key] if row['field'] == '' and row['key'].startswith('---'))
            else:
                count = len(self.data[tab_key]) // (len(NEW_JOINEE_FIELDS) + 1)
            self.notebook.tab(self.tabs[tab_key], text=f"{tab_key.title()} ({count})")

    def update_table_filter(self, tab_key):
        query = self.search_entries[tab_key].get().lower()
        tree = self.tables[tab_key]
        tree.delete(*tree.get_children())
        for row in self.data[tab_key]:
            if any(query in str(v).lower() for v in row.values()):
                tree.insert('', 'end', values=(row['key'], row['field'], row['old'], row['new']))

    def export_to_pdf(self, tab_key):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=f"Save {tab_key.title()} Report")
        if not file_path:
            return
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            elements.append(Paragraph(f"{tab_key.title()} Report", styles['Title']))
            data = [["Employee Key", "Field", "Old Value", "New Value"]]
            for row in self.data[tab_key]:
                data.append([row['key'], row['field'], row['old'], row['new']])
            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(table)
            doc.build(elements)
            messagebox.showinfo("Success", f"{tab_key.title()} PDF exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVComparatorApp(root)
    root.mainloop()