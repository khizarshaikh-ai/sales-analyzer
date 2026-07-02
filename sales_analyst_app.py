import os
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure modern, sleek look matching high-contrast requirements
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")  # High contrast neon-blue accents


class SalesAnalystApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gexton Education - Sales Data Analysis Dashboard")
        self.geometry("1100x700")

        self.df = None

        # Intercept the window close action to prevent background thread crashes
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- GUI Layout ---
        # Sidebar for controls
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="GEXTON",
                                       font=ctk.CTkFont(size=22, weight="bold", family="Helvetica"))
        self.logo_label.pack(padx=20, pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(self.sidebar, text="Summer Internship Program",
                                           font=ctk.CTkFont(size=12, slant="italic"))
        self.subtitle_label.pack(padx=20, pady=(0, 20))

        self.load_btn = ctk.CTkButton(self.sidebar, text="📁 Load Sales CSV", command=self.load_csv, fg_color="#1f538d",
                                      hover_color="#14375e")
        self.load_btn.pack(padx=20, pady=10, fill="x")

        # Action Buttons (Disabled until data is loaded)
        self.btn_overview = ctk.CTkButton(self.sidebar, text="📊 Data Overview", command=self.show_overview,
                                          state="disabled")
        self.btn_overview.pack(padx=20, pady=10, fill="x")

        self.btn_trends = ctk.CTkButton(self.sidebar, text="📈 Sales Trends", command=self.show_trends, state="disabled")
        self.btn_trends.pack(padx=20, pady=10, fill="x")

        self.btn_products = ctk.CTkButton(self.sidebar, text="🏆 Top 10 Products", command=self.show_top_products,
                                          state="disabled")
        self.btn_products.pack(padx=20, pady=10, fill="x")

        self.btn_region = ctk.CTkButton(self.sidebar, text="🗺️ Regional Distribution", command=self.show_regional_dist,
                                        state="disabled")
        self.btn_region.pack(padx=20, pady=10, fill="x")

        self.btn_report = ctk.CTkButton(self.sidebar, text="📝 Generate Report", command=self.generate_report,
                                        state="disabled", fg_color="#2b712b", hover_color="#1e4e1e")
        self.btn_report.pack(padx=20, pady=10, fill="x")

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Output Text Box
        self.text_output = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=13))
        self.text_output.pack(fill="both", expand=True, padx=15, pady=15)
        self.text_output.insert("0.0", "Welcome, Analyst.\nPlease load a Sales CSV file to begin analysis.")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            # Load Data (Task 1.1)
            self.df = pd.read_csv(file_path)

            # Check for and handle missing values (Task 1.3)
            self.df.dropna(inplace=True)

            # Convert Date column if it exists in data
            if 'Date' in self.df.columns:
                self.df['Date'] = pd.to_datetime(self.df['Date'])

            self.reset_text_view()
            self.text_output.insert("0.0",
                                    f"Data successfully loaded!\nFile: {os.path.basename(file_path)}\nRows: {self.df.shape[0]} | Columns: {self.df.shape[1]}\n\nSelect an option on the left side menu.")

            # Enable operational buttons
            self.btn_overview.configure(state="normal")
            self.btn_trends.configure(state="normal")
            self.btn_products.configure(state="normal")
            self.btn_region.configure(state="normal")
            self.btn_report.configure(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse CSV file.\nDetails: {str(e)}")

    def clear_main_frame_for_plot(self):
        """Clears embedded elements to isolate chart canvas mounts."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def reset_text_view(self):
        """Reconstructs text workspace pane on selection toggles."""
        self.clear_main_frame_for_plot()
        self.text_output = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=13))
        self.text_output.pack(fill="both", expand=True, padx=15, pady=15)

    # --- Task 1: Sales Data Overview ---
    def show_overview(self):
        self.reset_text_view()

        # Total Sales Calculation (Task 1.4)
        total_sales = self.df['Sales'].sum() if 'Sales' in self.df.columns else 0

        # Sales by Category Grouping (Task 1.5)
        cat_sales = ""
        if 'Category' in self.df.columns and 'Sales' in self.df.columns:
            cat_sales = self.df.groupby('Category')['Sales'].sum().to_string()

        # Build overview display metrics (Task 1.2)
        overview_text = f"""=== SALES DATA OVERVIEW ===

[First 5 Rows]:
{self.df.head().to_string()}

[Basic Statistics]:
{self.df.describe().to_string()}

[Column Information]:
{self.df.dtypes.to_string()}

[Total Sales for the Month]:
${total_sales:,.2f}

[Sales by Category]:
{cat_sales}
"""
        self.text_output.insert("0.0", overview_text)

    # --- Task 2.1: Monthly Sales Trend Plot ---
    def show_trends(self):
        if 'Date' not in self.df.columns or 'Sales' not in self.df.columns:
            messagebox.showerror("Missing Data", "Dataset requires 'Date' and 'Sales' columns.")
            return

        self.clear_main_frame_for_plot()
        trend_df = self.df.groupby('Date')['Sales'].sum().sort_index()

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2b2b2b')
        ax.set_facecolor('#2b2b2b')

        ax.plot(trend_df.index, trend_df.values, color='#00d2ff', linewidth=2, marker='o')
        ax.set_title("Monthly Sales Trend", color='white', fontsize=14, weight='bold')
        ax.set_xlabel("Date", color='white')
        ax.set_ylabel("Total Sales ($)", color='white')
        ax.tick_params(colors='white')
        ax.grid(True, color='#444444', linestyle='--')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- Task 2.2: Top 10 Products by Sales ---
    def show_top_products(self):
        if 'Product' not in self.df.columns or 'Sales' not in self.df.columns:
            messagebox.showerror("Missing Data", "Dataset requires 'Product' and 'Sales' columns.")
            return

        self.reset_text_view()
        top_10 = self.df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)

        output = "=== TOP 10 PRODUCTS BY SALES ===\n\n"
        for idx, (prod, val) in enumerate(top_10.items(), 1):
            output += f"{idx}. {prod:<25} -> ${val:,.2f}\n"

        self.text_output.insert("0.0", output)

    # --- Task 2.3: Sales Distribution by Region Bar Chart ---
    def show_regional_dist(self):
        if 'Region' not in self.df.columns or 'Sales' not in self.df.columns:
            messagebox.showerror("Missing Data", "Dataset requires 'Region' and 'Sales' columns.")
            return

        self.clear_main_frame_for_plot()
        region_df = self.df.groupby('Region')['Sales'].sum()

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2b2b2b')
        ax.set_facecolor('#2b2b2b')

        region_df.plot(kind='bar', color='#a855f7', ax=ax)
        ax.set_title("Sales Distribution by Region", color='white', fontsize=14, weight='bold')
        ax.set_xlabel("Region", color='white')
        ax.set_ylabel("Total Sales ($)", color='white')
        ax.tick_params(colors='white')
        plt.xticks(rotation=45)
        ax.grid(True, color='#444444', linestyle='--', axis='y')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- Task 2.4 & 2.5: Correlation & Summary Report Construction ---
    def generate_report(self):
        self.reset_text_view()

        total_sales = self.df['Sales'].sum() if 'Sales' in self.df.columns else 0
        cat_sales = self.df.groupby('Category')['Sales'].sum() if 'Category' in self.df.columns else pd.Series()
        region_sales = self.df.groupby('Region')['Sales'].sum() if 'Region' in self.df.columns else pd.Series()
        top_p = self.df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(
            3) if 'Product' in self.df.columns else pd.Series()

        # Correlation Matrix Analysis Calculation (Task 2.4)
        numeric_df = self.df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr().to_string() if not numeric_df.empty else "No matching numerical dimensions found."

        # Compile final structural report string (Task 2.5)
        report = f"""======================================================
                  SALES SUMMARY REPORT
======================================================
Generated for Management Review

[1] EXECUTIVE SUMMARY
Total Monthly Revenue Generated: ${total_sales:,.2f}

[2] TOP PERFORMING PRODUCTS (TOP 3)
{top_p.to_string()}

[3] PERFORMANCE BREAKDOWN BY CATEGORY
{cat_sales.to_string()}

[4] GEOGRAPHIC REGIONAL DISTRIBUTION
{region_sales.to_string()}

[5] NUMERICAL CO-RELATION COEFFICIENTS
{corr_matrix}

======================================================
Gexton Education - Task #08 Execution Summary Complete.
"""
        self.text_output.insert("0.0", report)

    def on_closing(self):
        """Safely clean up active sub-processes to avoid bgerror lifecycle crashes."""
        try:
            plt.close('all')  # Erases reference to charts
            self.quit()  # Stops active loop callbacks
            self.destroy()  # Tears down the main Tk engine layout smoothly
        except Exception:
            pass


if __name__ == "__main__":
    app = SalesAnalystApp()
    app.mainloop()