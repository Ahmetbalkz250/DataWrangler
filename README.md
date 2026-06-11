# DataWrangler V1.0 - Data Preprocessing Terminal
 
DataWrangler is a ETL and data cleaning tool to solve the "Dirty Data" problem, which is a biggest problem in the Machine Learning and Data science projects.
it processes datasets with millions of rows without overwhelming RAM, automatically diagnoses missing (NaN) values, and offers cleaning operations to users via a interface.

## Key Features
* **Multi-Format Support (Multi-Format I/O):** Seamleslly reads end exports flat text files ('.csv', '.xlsx') and relational databases ('.db' SQLite)
* **Smart Memory Management:** Regardless of the file size (e.g. 1 million rows), it only displays a preview of the first 20 rows on the screen to prevent the GUI freezing. It performs the actual operations on the main Dataframe in the background.
* **Automatic Diagnostics:** When the data is loaded, it scans the entire dataset in the background and notifies the users of total number of "NaN" cells.
* **Dynamic Data Cleaning:** 
  * **Drop:** Removes all rows containing missing data from database.
  * **Fill and Smart Type Casting:** Fill empty cells with specific value entered by the users. if the input is text, it is automatically detected as a "string"; if it is a number, it is detected as an `integer/float`. This prevents numerical data types from being corrupted.
* **Security Wall (Error Handling):** Features an Event-Driven error handling mechanism that prevents the `mainloop` from freezing when invalid or unsupported file formats are loaded.

## 🛠️ Technologies Used 
* **Python**
* **Pandas:** The background data manipulation and analysis engine.
* **CustomTkinter:** For user interface(GUI).
* **SQLite3:** Database connection and query operations (Internal library).

## Usage Guide
1. When you run the application, the following initial window will appear:

<img width="1367" height="784" alt="Ekran görüntüsü 2026-05-23 184541" src="https://github.com/user-attachments/assets/902e31b9-511c-434a-8d06-e6ad5513b323" />

2. Click the "Select File (CSV/Excel/DB)" button on the left pannel to choose the data file you want to clean. One selected, the program calculetes missing data, and a preview of the first 20 rows is displayed on the right panel. If the dataset is clean, "No missing values detected" massage will appear:

<img width="1369" height="781" alt="Ekran görüntüsü 2026-05-23 192746" src="https://github.com/user-attachments/assets/32d6809e-ddbe-48ac-9702-5a6d6e41efb2" />

4. If there are X missing values, a "Found X missing (NaN) values in the dataset!" message will appear. If you want to remove the rows containing '"NaN" cells, click the red "Drop Missing Values" button. If you want to enter specific values in place of the missing data, click the green "Fill Missing Values" button and enter the desired text or number. Once you have finished processing the data, click the "Save Cleaned Data" button at the bottom of the left panel to export the cleaned dataset to your preferred location.


## 💻 Installation & Setup (For Developers)

Install the required libraries to run the project from source code on your local machine:

```bash
pip install pandas openpyxl customtkinter
```
Then, run the main script:

```bash
python main.py
```

## 📦 Converting to a Desktop Application (EXE)
If you want to run this program on any Windows machine without Python, you can convert it into a single-click .exe file, just like a regular desktop application.

1. **Install PyInstaller:** Open your terminal (or CMD) and enter the following command:
```bash
pip install pyinstaller
```
2. **Build the exe file:** Open the terminal within the project folder and run the following command:
```bash
pyinstaller --noconsole --onefile main.py
```
Note: The --noconsole parameter prevents the command window from appearing in the backgraund while running the program, ensuring the only GUI (Graphical User Interface) is displayed

3. **Run the program:** You can use the "main.exe" file in this folder as you desire, or even you copy this file to any location you want. 
