import csv
import os
import sys

# ANSI Colors for terminal output
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

class StudentData:
    """Handles reading, validating, and exporting student academic records."""

    def __init__(self):
        self.raw_data = []
        self.validated_data = []

    def load_csv(self, file_path: str) -> bool:
        """Reads student data from a CSV file."""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.raw_data.append([
                        row['UniID'], 
                        row['SubID'], 
                        row['SubName'], 
                        float(row['ICT']), 
                        float(row['ICW']), 
                        float(row['Final'])
                    ])
            print(f"{GREEN}Successfully loaded: {file_path}{RESET}\n")
            return True
        except FileNotFoundError:
            print(f"{RED}Error: File '{file_path}' not found.{RESET}")
            return False
        except (ValueError, KeyError) as e:
            print(f"{RED}Error: Invalid CSV format - {e}{RESET}")
            return False

    def calculate_status(self, ict: float, icw: float, final: float) -> str:
        """Determines Pass/Refer/Retake based on individual component marks."""
        # Validation: Marks must be between 0-100
        if not all(0 <= m <= 100 for m in [ict, icw, final]):
            return "Error"

        # Count components that failed to meet the 25% threshold
        fail_count = sum(1 for mark in [ict, icw, final] if mark < 25)

        if fail_count == 0:
            return "Pass"
        elif fail_count == 1:
            return "Refer"
        else:
            return "Retake"

    def calculate_final_mark(self, ict: float, icw: float, final: float, status: str) -> str:
        """Calculates the weighted average or applies a cap for Retakes."""
        if status == "Error":
            return "Error"
        
        if status == "Retake":
            return "39%"
        
        average = (ict + icw + final) / 3
        return f"{int(average)}%"

    def process_data(self):
        """Validates all raw records and prepares them for output."""
        for row in self.raw_data:
            uni_id, sub_id, name, ict, icw, fin = row
            
            status = self.calculate_status(ict, icw, fin)
            total = self.calculate_final_mark(ict, icw, fin, status)

            # Format marks for display (show 'ER' if out of bounds)
            f_ict = f"{int(ict)}%" if 0 <= ict <= 100 else "ER"
            f_icw = f"{int(icw)}%" if 0 <= icw <= 100 else "ER"
            f_fin = f"{int(fin)}%" if 0 <= fin <= 100 else "ER"

            self.validated_data.append([
                uni_id, sub_id, name, f_ict, f_icw, f_fin, total, status
            ])

    def display_table(self):
        """Prints a formatted table to the terminal."""
        header = f"{'UniID':<15} {'SubID':<10} {'SubName':<20} {'ICT':<6} {'ICW':<6} {'Final':<6} {'Total':<8} {'Status'}"
        print(header)
        print("-" * len(header))
        for s in self.validated_data:
            print(f"{s[0]:<15} {s[1]:<10} {s[2]:<20} {s[3]:<6} {s[4]:<6} {s[5]:<6} {s[6]:<8} {s[7]}")

    def export_reports(self, single_file=False):
        """Saves results to the 'results' folder."""
        os.makedirs("results", exist_ok=True)
        
        if single_file:
            # Export everything into one text file
            with open('results/all_results.txt', 'w') as f:
                for s in self.validated_data:
                    f.write(f"STUDENT REPORT: {s[0]}\n" + "="*25 + "\n")
                    f.write(f"Subject: {s[2]} ({s[1]})\nMarks: ICT:{s[3]}, ICW:{s[4]}, Final:{s[5]}\n")
                    f.write(f"Result: {s[6]} - {s[7]}\n\n" + "-"*25 + "\n\n")
        else:
            # Export individual files per student
            for s in self.validated_data:
                with open(f"results/{s[0]}.txt", 'w') as f:
                    f.write(f"STUDENT REPORT CARD\n" + "="*19 + "\n")
                    labels = ["ID", "SubCode", "Name", "ICT", "ICW", "Final", "Mark", "Status"]
                    for label, val in zip(labels, s):
                        f.write(f"{label:<12} : {val}\n")

def main():
    # 1. Check Arguments
    if len(sys.argv) < 2:
        print(f"{RED}Usage: python script.py <filename.csv> [/full] [/each]{RESET}")
        sys.exit(1)

    csv_file = sys.argv[1]
    commands = [arg.lower() for arg in sys.argv]

    # 2. Initialize and Run
    processor = StudentData()
    
    if processor.load_csv(csv_file):
        processor.process_data()

        if "/full" in commands:
            processor.display_table()
        
        if "/each" in commands:
            processor.export_reports(single_file=False)
            print(f"{GREEN}Individual reports generated in /results{RESET}")
        
        # Default behavior: save summary if no flags provided
        if len(commands) == 2:
            processor.export_reports(single_file=True)
            print(f"{GREEN}Summary report generated in /results/all_results.txt{RESET}")

if __name__ == "__main__":
    main()