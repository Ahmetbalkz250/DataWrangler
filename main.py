import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sqlite3


class DataWranglerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- GLOBAL STATE & MEMORY ---
        self.df = None  # Main DataFrame to store the imported data
        self.current_file_ext = None  # Stores the current file extension for exporting
        self.error_count = 0  # Tracks consecutive invalid file uploads

        # --- MAIN WINDOW CONFIGURATION ---
        self.title("DataWrangler V1.0 - Data Preprocessing Terminal")
        self.geometry("1100x600")

        # Grid layout configuration (Left Panel: 1, Right Panel: 3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # 1. LEFT PANEL (CONTROL CENTER)
        # ==========================================
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.lbl_title = ctk.CTkLabel(self.left_frame, text="Control Panel", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(pady=(20, 30))

        self.btn_select = ctk.CTkButton(self.left_frame, text="📂 Select File (CSV/Excel/DB)", command=self.load_file)
        self.btn_select.pack(pady=10, padx=20, fill="x")

        self.lbl_status = ctk.CTkLabel(self.left_frame, text="Status: Waiting for input...", text_color="gray")
        self.lbl_status.pack(pady=5)

        # Dynamic Error Message Label (Hidden by default)
        self.lbl_error_msg = ctk.CTkLabel(self.left_frame, text="", text_color="#e74c3c",
                                          font=ctk.CTkFont(size=14, weight="bold"))

        self.spacer = ctk.CTkLabel(self.left_frame, text="")
        self.spacer.pack(expand=True, fill="both")

        self.btn_save = ctk.CTkButton(self.left_frame, text="💾 Save Cleaned Data", fg_color="#28a745",
                                      hover_color="#218838", command=self.save_file)
        self.btn_save.pack(pady=20, padx=20, fill="x")

        # ==========================================
        # 2. RIGHT PANEL (PREVIEW & OPERATIONS)
        # ==========================================
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        self.lbl_preview = ctk.CTkLabel(self.right_frame, text="Data Preview (Top 20 Rows)",
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_preview.pack(pady=(15, 5), padx=15, anchor="w")

        self.tree_frame = ctk.CTkFrame(self.right_frame)
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Treeview styling for a modern, dark-themed data grid
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#333333", foreground="white")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0,
                        font=("Arial", 12), rowheight=35)
        style.map('Treeview', background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Diagnostic Label
        self.lbl_diagnostic = ctk.CTkLabel(self.right_frame, text="Diagnostics: Please load a file to analyze.",
                                           text_color="#f39c12", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_diagnostic.pack(pady=(10, 5))

        # --- DYNAMIC ACTION BUTTONS ---
        self.action_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.action_frame.pack(pady=15, fill="x", padx=15)

        self.btn_drop = ctk.CTkButton(self.action_frame, text="🗑️ Drop Missing Values", fg_color="#c0392b",
                                      hover_color="#a93226", command=self.drop_nans)
        self.btn_drop.pack(side="left", padx=10)

        self.btn_show_fill = ctk.CTkButton(self.action_frame, text="✏️ Fill Missing Values", fg_color="#27ae60",
                                           hover_color="#2ecc71", command=self.show_fill_options)
        self.btn_show_fill.pack(side="left", padx=10)

        # Hidden elements for progressive disclosure
        self.entry_fill = ctk.CTkEntry(self.action_frame, placeholder_text="e.g., 0 or Unknown", width=150)
        self.btn_fill_confirm = ctk.CTkButton(self.action_frame, text="✅", width=40, fg_color="#2980b9",
                                              hover_color="#1f618d", command=self.fill_nans)
        self.btn_fill_cancel = ctk.CTkButton(self.action_frame, text="❌", width=40, fg_color="#c0392b",
                                             hover_color="#a93226", command=self.hide_fill_options)

    # ==========================================
    # UI ANIMATION & TOGGLE METHODS
    # ==========================================
    def show_fill_options(self):
        """Hides the 'Fill' button and exposes the entry field with confirm/cancel buttons."""
        self.btn_show_fill.pack_forget()
        self.entry_fill.pack(side="left", padx=(10, 10))
        self.btn_fill_confirm.pack(side="left")
        self.btn_fill_cancel.pack(side="left", padx=(5, 0))

    def hide_fill_options(self):
        """Restores the original button layout and clears the entry field."""
        self.entry_fill.delete(0, 'end')
        self.entry_fill.pack_forget()
        self.btn_fill_confirm.pack_forget()
        self.btn_fill_cancel.pack_forget()
        self.btn_show_fill.pack(side="left", padx=10)

    # ==========================================
    # CORE DATA ENGINE & EVENT HANDLERS
    # ==========================================
    def load_file(self):
        """Handles file selection, format validation, and initial data parsing."""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("SQLite Database", "*.db"),
                       ("All Files", "*.*"))
        )
        if not file_path: return

        # --- PROGRESSIVE ERROR HANDLING (Security Wall) ---
        valid_extensions = ('.csv', '.xlsx', '.xls', '.db')

        if not file_path.endswith(valid_extensions):
            self.error_count += 1
            self.lbl_error_msg.pack(pady=15)

            if self.error_count == 1:
                self.lbl_status.configure(text="Status: Invalid Format!", text_color="red")
                self.lbl_error_msg.configure(text="Invalid file type. Please try again.")
            else:
                self.lbl_status.configure(text="Status: Invalid Format!", text_color="red")
                self.lbl_error_msg.configure(text="Warning: You must select a\n.csv, .xlsx, or .db file!")

            return  # Interrupts execution, waiting for correct input

        # Reset error state upon valid file selection
        self.error_count = 0
        self.lbl_error_msg.pack_forget()

        filename = os.path.basename(file_path)
        if file_path.endswith('.csv'):
            self.current_file_ext = '.csv'
        elif file_path.endswith(('.xlsx', '.xls')):
            self.current_file_ext = '.xlsx'
        elif file_path.endswith('.db'):
            self.current_file_ext = '.db'

        self.lbl_status.configure(text=f"Loaded: {filename}", text_color="white")

        try:
            # Data Extraction Logic
            if self.current_file_ext == '.csv':
                self.df = pd.read_csv(file_path)
            elif self.current_file_ext == '.xlsx':
                self.df = pd.read_excel(file_path)
            elif self.current_file_ext == '.db':
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                if not tables:
                    self.lbl_status.configure(text="Error: No tables found in DB!", text_color="red")
                    conn.close()
                    return
                first_table_name = tables[0][0]
                self.df = pd.read_sql_query(f"SELECT * FROM '{first_table_name}'", conn)
                conn.close()

            self.run_diagnostics()
            self.update_table_preview()
            self.hide_fill_options()

        except Exception as e:
            self.lbl_status.configure(text="Read Error!", text_color="red")
            print("Exception Details:", e)

    def run_diagnostics(self):
        """Scans the DataFrame for missing values and updates the UI."""
        if self.df is not None:
            total_nans = self.df.isna().sum().sum()
            if total_nans > 0:
                self.lbl_diagnostic.configure(
                    text=f"Diagnostics: Found {total_nans} missing (NaN) values in the dataset!", text_color="#f39c12")
            else:
                self.lbl_diagnostic.configure(text="Diagnostics: Excellent! No missing values detected.",
                                              text_color="#2ecc71")

    def update_table_preview(self):
        """Renders the top 20 rows of the DataFrame into the Treeview grid."""
        if self.df is None: return
        df_preview = self.df.head(20)
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df_preview.columns)
        for col in df_preview.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        for index, row in df_preview.iterrows():
            row_cleaned = [str(x) if pd.notna(x) else "NaN" for x in row]
            self.tree.insert("", "end", values=row_cleaned)

    def drop_nans(self):
        """Removes any row containing at least one missing value."""
        if self.df is None: return
        self.df = self.df.dropna()
        self.run_diagnostics()
        self.update_table_preview()
        messagebox.showinfo("Success", "All rows containing missing values have been dropped!")

    def fill_nans(self):
        """Fills missing values with the user-provided input, preserving numeric types if applicable."""
        if self.df is None: return
        fill_val = self.entry_fill.get()
        if fill_val == "":
            messagebox.showwarning("Warning", "Please enter a value to fill!")
            return

        # Smart Type Casting
        try:
            if "." in fill_val:
                fill_val = float(fill_val)
            else:
                fill_val = int(fill_val)
        except ValueError:
            pass  # Keep as string if it's text

        self.df = self.df.fillna(fill_val)
        self.run_diagnostics()
        self.update_table_preview()
        self.hide_fill_options()
        messagebox.showinfo("Success", f"All missing values have been filled with '{fill_val}'!")

    def save_file(self):
        """Exports the cleaned DataFrame back to its original format."""
        if self.df is None:
            messagebox.showerror("Error", "No data to save! Please load a file first.")
            return

        if self.current_file_ext == '.csv':
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")],
                                                     title="Save Cleaned Data")
            if save_path:
                self.df.to_csv(save_path, index=False)
                messagebox.showinfo("Saved", "Data successfully saved as a CSV file!")

        elif self.current_file_ext == '.xlsx':
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel File", "*.xlsx")],
                                                     title="Save Cleaned Data")
            if save_path:
                self.df.to_excel(save_path, index=False)
                messagebox.showinfo("Saved", "Data successfully saved as an Excel file!")

        elif self.current_file_ext == '.db':
            save_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")],
                                                     title="Save Cleaned Data")
            if save_path:
                conn = sqlite3.connect(save_path)
                self.df.to_sql(name="CleanedData", con=conn, if_exists="replace", index=False)
                conn.close()
                messagebox.showinfo("Saved", "Data successfully saved to the Database!")


if __name__ == "__main__":
    app = DataWranglerApp()
    app.mainloop()