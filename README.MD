# Student Grade Processor

A Python-based CLI tool that automates the processing of student academic records. It reads data from CSV files, calculates final grades based on institutional rules, and generates formatted report cards.

## 🚀 Features
* **Automated Validation**: Checks if marks are within the 0-100 range.
* **Smart Status Logic**: Automatically determines if a student passes, requires a referral, or must retake the module.
* **Flexible Exports**: 
  * View a summary table directly in the terminal.
  * Generate a single summary text file.
  * Export individual, professionally formatted report cards for every student.

## 🛠️ Usage
Run the script via the terminal by providing a CSV file as the first argument.

### Commands
| Command | Description |
| :--- | :--- |
| `python main.py data.csv` | Generates a summary file in the `results/` folder. |
| `python main.py data.csv /full` | Displays the full table in the terminal. |
| `python main.py data.csv /each` | Generates individual `.txt` report cards for every student. |

## 📊 CSV Format
The input CSV should contain the following headers:
`UniID, SubID, SubName, ICT, ICW, Final`

## 📂 Project Structure
* `main.py`: The core logic and processing script.
* `test_data.csv`: Sample data for testing.
* `results/`: Output directory for generated reports.