"""
Title: GradeBook Analyzer CLI
Name:Pragya Agarwal
Roll no.-2501010161
Date: 29 November 2025

Description:
A command-line GradeBook Analyzer that reads student marks
(manual input or CSV), performs statistical analysis,
assigns grades, filters pass/fail students, and prints a formatted table.
"""

import csv
import statistics

def print_welcome():
    print("\n==============================")
    print("   GRADEBOOK ANALYZER CLI")
    print("==============================")
    print("1. Manual Entry")
    print("2. Load from CSV File")
    print("3. Exit")
    print("==============================")

def manual_input():
    marks = {}
    n = int(input("\nEnter number of students: "))
    for _ in range(n):
        name = input("Enter student name: ")
        score = float(input(f"Enter marks for {name}: "))
        marks[name] = score
    return marks

def load_csv():
    filename = input("\nEnter CSV filename (example: data.csv): ")
    marks = {}
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if len(row) >= 2:
                    name = row[0]
                    score = float(row[1])
                    marks[name] = score
        print("CSV loaded successfully!")
    except FileNotFoundError:
        print("ERROR: File not found. Try again.")
    return marks

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    return max(marks_dict.values())

def find_min_score(marks_dict):
    return min(marks_dict.values())

def assign_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

def create_gradebook(marks):
    grades = {}
    for name, score in marks.items():
        grades[name] = assign_grade(score)
    return grades

def grade_distribution(grades):
    dist = {"A":0, "B":0, "C":0, "D":0, "F":0}
    for g in grades.values():
        dist[g] += 1
    return dist

def pass_fail_lists(marks):
    passed = [name for name, score in marks.items() if score >= 40]
    failed = [name for name, score in marks.items() if score < 40]
    return passed, failed

def print_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("---------------------------------------")
    for name, score in marks.items():
        print(f"{name}\t\t{score}\t{grades[name]}")

def export_csv(marks, grades):
    filename = "grade_output.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Marks", "Grade"])
        for name in marks:
            writer.writerow([name, marks[name], grades[name]])
    print(f"\nCSV exported successfully as {filename}")

def main():
    while True:
        print_welcome()
        choice = input("Choose option (1/2/3): ")

        if choice == "1":
            marks = manual_input()
        elif choice == "2":
            marks = load_csv()
            if not marks:
                continue
        elif choice == "3":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
            continue

        avg = calculate_average(marks)
        median = calculate_median(marks)
        max_score = find_max_score(marks)
        min_score = find_min_score(marks)

        grades = create_gradebook(marks)
        dist = grade_distribution(grades)

        passed, failed = pass_fail_lists(marks)

        print("\n===== STATISTICAL ANALYSIS =====")
        print(f"Average Score: {avg:.2f}")
        print(f"Median Score: {median}")
        print(f"Highest Score: {max_score}")
        print(f"Lowest Score: {min_score}")

        print("\n===== GRADE DISTRIBUTION =====")
        for g, count in dist.items():
            print(f"{g}: {count}")

        print("\n===== PASS / FAIL SUMMARY =====")
        print(f"Passed ({len(passed)}): {passed}")
        print(f"Failed ({len(failed)}): {failed}")

        print("\n===== RESULTS TABLE =====")
        print_table(marks, grades)

        export = input("\nExport results to CSV? (y/n): ")
        if export.lower() == "y":
            export_csv(marks, grades)

        repeat = input("\nRun another analysis? (y/n): ")
        if repeat.lower() != "y":
            print("Goodbye!")
            break
           
           
           
if __name__ == "__main__":
      main()
