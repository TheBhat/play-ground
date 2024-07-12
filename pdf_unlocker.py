import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter
import os
import sys
import logging

# Setup logging
logging.basicConfig(filename='pdf_unlocker.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def unlock_pdf(pdf_file_path, password):
    logging.info(f"Attempting to unlock PDF: {pdf_file_path}")
    try:
        reader = PdfReader(pdf_file_path)
        if reader.is_encrypted:
            reader.decrypt(password)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            # Create output path with the same name appended with _ul
            dir_name = os.path.dirname(pdf_file_path)
            base_name = os.path.basename(pdf_file_path)
            output_path = os.path.join(dir_name, f"{os.path.splitext(base_name)[0]}_.pdf")
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logging.info(f"PDF unlocked and saved successfully as {output_path}.")
            messagebox.showinfo("Success", f"PDF unlocked and saved successfully as {output_path}.")
        else:
            logging.info("PDF is not password protected.")
            messagebox.showinfo("Info", "PDF is not password protected.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_pdf_and_unlock():
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_file_path:
        return
    
    logging.info(f"Selected PDF: {pdf_file_path}")
    password = simpledialog.askstring("Password", "Enter Password:", show='*')
    if password:
        unlock_pdf(pdf_file_path, password)

def main():
    app = tk.Tk()
    app.title("PDF Unlocker")

    tk.Label(app, text="Select a PDF to Unlock:").pack(pady=5)
    tk.Button(app, text="Select PDF", command=select_pdf_and_unlock).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    logging.info(f"input as argument: {sys.argv}")
    if len(sys.argv) > 1:
        pdf_file_path = sys.argv[1]
        logging.info(f"PDF file provided as argument: {pdf_file_path}")
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        password = simpledialog.askstring("Password", "Enter Password:", show='*')
        if password:
            unlock_pdf(pdf_file_path, password)
    else:
        logging.info("No PDF file provided as argument, launching GUI.")
        main()
