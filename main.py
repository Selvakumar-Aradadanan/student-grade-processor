import csv
import os
import sys

# ANSI Colors for a professional terminal look
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

class StudentData:
    """Handles reading, validating, and exporting student academic records."""

    def __init__(self):
        self.student_data_no_val = []
        self.student_data_val = []

    def read_csv(self, source: str) -> bool:
        """Reads student data from a CSV file with error handling."""
        try:
            with open(source, 'r', encoding='utf-8') as file:
                data = csv.DictReader(file)
                for row in data:  
                    student_row = [
                        row['UniID'], 
                        row['SubID'], 
                        row['SubName'], 
                        float(row['ICT']), 
                        float(row['ICW']), 
                        float(row['Final'])
                    ]  
                    self.student_data_no_val.append(student_row)
            print(f"{GREEN}Finished reading CSV file: {source}{RESET}\n")
            return True
        except FileNotFoundError:
            print(f"{RED}Error: File not found.{RESET}")
            return False
        except (ValueError, KeyError):
            print(f"{RED}Error: Invalid data format or missing columns in CSV.{RESET}")
            return False

    def get_status(self, ict_val, icw_val, fin_val, ict_marks, icw_marks, fin_marks):
        """Your original logic for determining Pass/Refer/Retake."""
        error_count = 0
        
        # Check if any marks were 'ER' (Error)
        if ict_val != 'ER' and icw_val != 'ER' and fin_val != 'ER':
            if ict_marks < 25:
                error_count += 1
            if icw_marks < 25:
                error_count += 1
            if fin_marks < 25:
                error_count += 1
        else:
            return "Error"
            
        # Determine status based on the count of failed components
        if error_count == 0:
            return "Pass"
        if error_count == 1:
            return "Refer"
        elif error_count >= 2:
            return "Retake"

    def get_final_marks(self, ict_val, icw_val, fin_val, ict_marks, icw_marks, fin_marks, status):
        """Your original logic for final mark calculation and capping."""
        if ict_val != 'ER' and icw_val != 'ER' and fin_val != 'ER':
            if status == "Retake":
                return '39%'
            else:
                # Calculating the average of the three components
                total_marks = (ict_marks + icw_marks + fin_marks) / 3
                return f"{int(total_marks)}%"
        else:
            return 'Error'

    def validate_and_process(self):
        """Processes the raw data using your logic blocks."""
        for student in self.student_data_no_val:
            # Convert to integers for calculation
            ict_num, icw_num, fin_num = int(student[3]), int(student[4]), int(student[5])
            
            # Validation check for range
            ict_str = f"{ict_num}%" if 0 <= ict_num <= 100 else 'ER'
            icw_str = f"{icw_num}%" if 0 <= icw_num <= 100 else 'ER'
            fin_str = f"{fin_num}%" if 0 <= fin_num <= 100 else 'ER'
            
            # Applying your status and final mark logic
            res_status = self.get_status(ict_str, icw_str, fin_str, ict_num, icw_num, fin_num)
            res_final = self.get_final_marks(ict_str, icw_str, fin_str, ict_num, icw_num, fin_num, res_status) 

            self.student_data_val.append([
                student[0], student[1], student[2], 
                ict_str, icw_str, fin_str, 
                res_final, res_status
            ])

    def print_table(self):
        """Prints a nicely formatted table to the console."""
        header = f"{'UniID':<15} {'SubID':<10} {'SubName':<20} {'ICT':<6} {'ICW':<6} {'Final':<6} {'Total':<8} {'Status'}"
        print(header)
        print("-" * len(header))
        for s in self.student_data_val:
            print(f"{s[0]:<15} {s[1]:<10} {s[2]:<20} {s[3]:<6} {s[4]:<6} {s[5]:<6} {s[6]:<8} {s[7]}")

    def export_each_report(self):
        """Generates individual text files for each student."""
        os.makedirs("results", exist_ok=True)
        for s in self.student_data_val:
            filename = f"results/{s[0]}.txt"
            with open(filename, 'w') as file:
                file.write("STUDENT REPORT CARD\n" + "=" * 19 + "\n")
                labels = ["Student ID", "Subject Code", "Subject Name", "ICT", "ICW", "Final Exam", "Module Mark", "Status"]
                for label, value in zip(labels, s):
                    file.write(f"{label:<12} : {value}\n")

def main():
    # Capture commands from terminal
    user_commands = [arg.lower() for arg in sys.argv]

    if len(user_commands) < 2:
        print(f"{RED}Error: No CSV file provided.{RESET}")
        print("Usage: python script.py data.csv [/full] [/each]")
        sys.exit(1)

    stu_processor = StudentData()
    
    # Run the workflow
    if stu_processor.read_csv(sys.argv[1]):
        stu_processor.validate_and_process()

        if "/full" in user_commands:
            stu_processor.print_table()
        
        if "/each" in user_commands:
            stu_processor.export_each_report()
            print(f"{GREEN}Individual reports saved in /results{RESET}")

        # Default action if no flags are used
        if len(user_commands) == 2:
            print(f"{GREEN}Data processed. Use /full to see the table or /each to export files.{RESET}")

if __name__ == "__main__":
    main()
