import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
import os

class AirbnbAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Analityczny Airbnb: Rio de Janeiro")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.default_db_path = '/Users/marcingorecki/Desktop/Python/Big Data/projekt_airbnb.db'
        self.db_path = self.default_db_path if os.path.exists(self.default_db_path) else ""

        self.current_df = None

        self.setup_styles()

        self.create_widgets()

        if self.db_path:
            self.lbl_status.config(text=f"Polaczono automatycznie z: {os.path.basename(self.db_path)}", foreground="#2ecc71")
            self.btn_load.config(text="Zmien baze danych")
            self.cb_tables.state(['!disabled'])
            self.load_data_preview()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.primary_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.bg_color = "#ecf0f1"

        self.root.configure(bg=self.bg_color)

        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TFrame", background=self.primary_color)
        self.style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)

        self.style.configure("TLabel", background=self.bg_color, font=("Helvetica", 10))
        self.style.configure("Header.TLabel", background=self.primary_color, foreground="white", font=("Helvetica", 14, "bold"))
        self.style.configure("CardTitle.TLabel", background="white", font=("Helvetica", 11, "bold"), foreground=self.primary_color)

        self.style.configure("TButton", font=("Helvetica", 10, "bold"), background=self.accent_color, foreground="white", borderwidth=0)
        self.style.map("TButton", background=[('active', '#2980b9')])

        self.style.configure("Success.TButton", font=("Helvetica", 10, "bold"), background="#2ecc71", foreground="white", borderwidth=0)
        self.style.map("Success.TButton", background=[('active', '#27ae60')])

        self.style.configure("TCombobox", arrowsize=15)

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        header_frame.pack(fill="x", side="top")

        lbl_title = ttk.Label(header_frame, text="System Wspomagania Decyzji: Airbnb Rio de Janeiro", style="Header.TLabel")
        lbl_title.pack(side="left")

        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill="x", side="top")

        self.btn_load = ttk.Button(control_frame, text="Wybierz plik bazy (.db)", command=self.browse_database)
        self.btn_load.pack(side="left", padx=5)

        self.lbl_status = ttk.Label(control_frame, text="Brak polaczenia z baza danych SQLite", foreground="#e74c3c", font=("Helvetica", 9, "italic"))
        self.lbl_status.pack(side="left", padx=10)

        self.btn_export = ttk.Button(control_frame, text="Eksportuj widok do CSV", command=self.export_to_csv)
        self.btn_export.pack(side="right", padx=5)

        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill="both", expand=True)

        left_panel = ttk.Frame(main_container, width=300, padding=10)
        left_panel.pack(fill="y", side="left", padx=(0, 10))
        left_panel.pack_propagate(False)

        card_select = ttk.Frame(left_panel, style="Card.TFrame", padding=15)
        card_select.pack(fill="both", expand=True)

        lbl_select_title = ttk.Label(card_select, text="PANEL ANALITYCZNY", style="CardTitle.TLabel")
        lbl_select_title.pack(anchor="w", pady=(0, 15))

        lbl_instruction = ttk.Label(card_select, text="Wybierz dane do analizy:", background="white")
        lbl_instruction.pack(anchor="w", pady=(0, 5))

        self.options = [
            "--- SUROWE TABELE ---",
            "Tabela_Oferty (Wszystkie dane)",
            "Tabela_Dzielnice (Slownik dzielnic)",
            "--- KWERENDY ANALITYCZNE ---",
            "Kwerenda 1: Renta Geograficzna (Top 10)",
            "Kwerenda 2: Ekonomia Zaufania (Superhost)",
            "Kwerenda 3: Struktura Podazy (Typy pokoi)",
            "Kwerenda 4: Okazje inwestycyjne (Nadmorskie)"
        ]

        self.cb_tables = ttk.Combobox(card_select, values=self.options, state="readonly")
        self.cb_tables.pack(fill="x", pady=(0, 15))
        self.cb_tables.current(1)
        self.cb_tables.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.cb_tables.state(['disabled'])

        self.btn_refresh = ttk.Button(card_select, text="Odswiez Widok", command=self.load_data_preview)
        self.btn_refresh.pack(fill="x", pady=(0, 15))

        lbl_stats_title = ttk.Label(card_select, text="METRYKI ZBIORU", style="CardTitle.TLabel")
        lbl_stats_title.pack(anchor="w", pady=(20, 10))

        self.lbl_row_count = ttk.Label(card_select, text="Liczba wierszy: 0", background="white", font=("Helvetica", 10))
        self.lbl_row_count.pack(anchor="w", pady=2)

        self.lbl_avg_price = ttk.Label(card_select, text="Srednia cena w widoku: N/A", background="white", font=("Helvetica", 10))
        self.lbl_avg_price.pack(anchor="w", pady=2)

        right_panel = ttk.Frame(main_container, padding=5)
        right_panel.pack(fill="both", expand=True, side="right")

        table_container = ttk.Frame(right_panel)
        table_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_container, show="headings", selectmode="browse")

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

    def browse_database(self):
        file_path = filedialog.askopenfilename(
            title="Wybierz baze danych SQLite dla Rio Airbnb",
            filetypes=[("Bazy danych SQLite", "*.db *.sqlite"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            self.db_path = file_path
            self.lbl_status.config(text=f"Polaczono z: {os.path.basename(file_path)}", foreground="#2ecc71")
            self.btn_load.config(text="Zmien baze danych")
            self.cb_tables.state(['!disabled'])
            self.load_data_preview()

    def on_selection_change(self, event):
        selection = self.cb_tables.get()
        if selection.startswith("---"):
            return
        self.load_data_preview()

    def get_query_for_selection(self, selection):
        if selection == "Tabela_Oferty (Wszystkie dane)":
            return "SELECT * FROM Tabela_Oferty"

        elif selection == "Tabela_Dzielnice (Slownik dzielnic)":
            return "SELECT field2 AS Nazwa_Dzielnicy FROM neighbourhoods"

        elif selection == "Kwerenda 1: Renta Geograficzna (Top 10)":
            return """
            SELECT 
                Dzielnica, 
                COUNT(ID_oferty) AS Liczba_Ofert,
                ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_R$,
                ROUND(AVG(Ocena_lokalizacji), 2) AS Srednia_Ocena_Lokalizacji
            FROM 
                Tabela_Oferty
            GROUP BY 
                Dzielnica
            HAVING 
                Liczba_Ofert >= 30
            ORDER BY 
                Srednia_Cena_R$ DESC
            LIMIT 10;
            """

        elif selection == "Kwerenda 2: Ekonomia Zaufania (Superhost)":
            return """
            SELECT 
                Czy_Superhost, 
                COUNT(ID_oferty) AS Liczba_Ofert,
                ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_R$,
                ROUND(AVG(Ocena_ogolna), 2) AS Srednia_Ocena
            FROM 
                Tabela_Oferty
            WHERE 
                Czy_Superhost IS NOT NULL AND Czy_Superhost != ''
            GROUP BY 
                Czy_Superhost;
            """

        elif selection == "Kwerenda 3: Struktura Podazy (Typy pokoi)":
            return """
            SELECT 
                Typ_pokoju,
                COUNT(ID_oferty) AS Liczba_Ofert,
                ROUND((COUNT(ID_oferty) * 100.0) / (SELECT COUNT(*) FROM Tabela_Oferty), 2) AS Udzial_Procentowy,
                ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_R$,
                ROUND(AVG(Minimalna_liczba_nocy), 1) AS Srednia_Min_Nocy
            FROM 
                Tabela_Oferty
            GROUP BY 
                Typ_pokoju
            ORDER BY 
                Liczba_Ofert DESC;
            """

        elif selection == "Kwerenda 4: Okazje inwestycyjne (Nadmorskie)":
            return """
            SELECT 
                Nazwa_oferty,
                Dzielnica,
                Cena_R$,
                Ocena_ogolna,
                Liczba_recenzji
            FROM 
                Tabela_Oferty
            WHERE 
                Cena_R$ < (SELECT AVG(Cena_R$) FROM Tabela_Oferty)
                AND Ocena_ogolna >= 4.9
                AND Liczba_recenzji >= 10
                AND Dzielnica IN ('Copacabana', 'Ipanema', 'Leblon')
            ORDER BY 
                Cena_R$ ASC
            LIMIT 15;
            """
        return ""

    def load_data_preview(self):
        if not self.db_path:
            return

        selection = self.cb_tables.get()
        if selection.startswith("---"):
            return

        sql_query = self.get_query_for_selection(selection)
        if not sql_query:
            return

        try:
            conn = sqlite3.connect(self.db_path)
            self.current_df = pd.read_sql_query(sql_query, conn)
            conn.close()

            self.update_treeview_data()
            self.update_sidebar_metrics()

        except Exception as e:
            messagebox.showerror("Blad zapytania SQL", f"Nie udalo sie wykonac zapytania:\n{str(e)}")

    def update_treeview_data(self):
        self.tree.delete(*self.tree.get_children())

        columns = list(self.current_df.columns)
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            max_len = max(self.current_df[col].astype(str).map(len).max(), len(col)) if not self.current_df.empty else len(col)
            width = min(max(max_len * 10, 80), 300)
            self.style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
            self.tree.column(col, width=width, anchor="w")

        for index, row in self.current_df.iterrows():
            values = ["" if pd.isna(val) else val for val in row]
            self.tree.insert("", "end", values=values)

    def update_sidebar_metrics(self):
        if self.current_df is None or self.current_df.empty:
            self.lbl_row_count.config(text="Liczba wierszy: 0")
            self.lbl_avg_price.config(text="Srednia cena w widoku: N/A")
            return

        row_count = len(self.current_df)
        self.lbl_row_count.config(text=f"Liczba wierszy: {row_count}")

        price_col = [col for col in self.current_df.columns if 'cena' in col.lower() or 'price' in col.lower()]
        if price_col:
            avg_price = self.current_df[price_col[0]].mean()
            self.lbl_avg_price.config(text=f"Srednia cena w widoku: {avg_price:.2f} R$")
        else:
            self.lbl_avg_price.config(text="Srednia cena w widoku: N/A")

    def export_to_csv(self):
        if self.current_df is None or self.current_df.empty:
            messagebox.showwarning("Brak danych", "Nie ma zadnych danych do wyeksportowania!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Zapisz wyniki do pliku CSV",
            defaultextension=".csv",
            filetypes=[("Plik CSV", "*.csv")],
            initialfile="raport_airbnb_wynik.csv"
        )

        if file_path:
            try:
                self.current_df.to_csv(file_path, index=False, encoding='utf-8')
                messagebox.showinfo("Sukces!", f"Dane zostały pomyślnie zapisane do pliku:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Blad eksportu", f"Nie udalo sie zapisac pliku:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AirbnbAnalyzerApp(root)
    root.mainloop()