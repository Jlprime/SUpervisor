"""
SUpervisor is a script that determines the best choice of S/Us that will maximise your cap.

Sketch of algorithm:
1. User inputs prior cumulative GPA and number of credits earned.
2. For every module taken this semester, user inputs module code, credits earned and grade.
3. SUpervisor calculates current semester CAP and cumulative CAP.
4. User inputs remaining S/U options.
5. SUpervisor calculates all combinations of S/U options (including the zero S/U option).
6. For each combination, SUpervisor calculates current semester CAP, cumulative CAP.
7. SUpervisor outputs the top 3 optimal options.
"""
from enum import Enum

NEWLINE = "\n"
SPACE = " "
WELCOME_MESSAGE = "Welcome to SUpervisor!"
REQUEST_PRIOR_CUMULATIVE_GPA = "Please enter your cumulative GPA at the beginning of this semester."
REQUEST_PRIOR_CREDITS = "Please enter the number of credits earned at the beginning of this semester."
REQUEST_NUM_CURRENT_MODULES = "Please enter the number of modules taken this semester."
MODULE_ENTRY_FORMAT = "[MODULE CODE] [LETTER GRADE] [NO. OF MODULAR CREDITS]"
MODULE_ENTRY_EXAMPLE = "e.g. CS1101S B+ 4"
REQUEST_CURRENT_RESULTS = "Please enter your actual results for the modules taken this semester, " \
                          + "in the following format:" + NEWLINE \
                          + MODULE_ENTRY_FORMAT + SPACE + MODULE_ENTRY_EXAMPLE + NEWLINE
SEMESTER_GPA_PREFIX = "Semester GPA: "
CUMULATIVE_GPA_PREFIX = "Cumulative GPA: "


class LetterGrade(Enum):
    A_PLUS = 5.0
    A = 5.0
    A_MINUS = 4.5
    B_PLUS = 4.0
    B = 3.5
    B_MINUS = 3.0
    C_PLUS = 2.5
    C = 2.0
    D_PLUS = 1.5
    D = 1.0
    F = 0
    S = 1000
    U = 1001


class Module():
    def __init__(self, module_code: str, letter_grade: LetterGrade, credits: int):
        self.module_code = module_code
        self.letter_grade = letter_grade
        self.credits = credits

    def get_module_code(self):
        return self.module_code

    def get_letter_grade(self):
        return self.letter_grade

    def get_credits(self):
        return self.credits


def to_letter_grade(letter_grade_string: str):
    letter_grade_map = {
        "A+": LetterGrade.A_PLUS,
        "A": LetterGrade.A,
        "A-": LetterGrade.A_MINUS,
        "B+": LetterGrade.B_PLUS,
        "B": LetterGrade.B,
        "B-": LetterGrade.B_MINUS,
        "C+": LetterGrade.C_PLUS,
        "C": LetterGrade.C,
        "D+": LetterGrade.D_PLUS,
        "D": LetterGrade.D,
        "F": LetterGrade.F,
        "S": LetterGrade.S,
        "U": LetterGrade.U
    }
    return letter_grade_map[letter_grade_string]


def receive_results(num: int):
    modules = []
    for i in range(num):
        args = input("Module " + str(i + 1) + ":").split()
        module = Module(args[0], to_letter_grade(args[1]), int(args[2]))
        modules.append(module)
    return modules


def calculate_semester_gpa(modules: list):
    grade_credit_product = 0
    credit_sum = 0
    for module in modules:
        grade_credit_product += module.get_letter_grade().value * module.get_credits()
        credit_sum += module.get_credits()
    return float(grade_credit_product) / float(credit_sum)


def calculate_cumulative_gpa(modules: list, prior_cum_gpa: float, prior_credits: int):
    grade_credit_product = prior_cum_gpa * prior_credits
    credit_sum = prior_credits
    for module in modules:
        grade_credit_product += module.get_letter_grade().value * module.get_credits()
        credit_sum += module.get_credits()
    return float(grade_credit_product) / float(credit_sum)


print(WELCOME_MESSAGE)

prior_cumulative_gpa = float(input(REQUEST_PRIOR_CUMULATIVE_GPA))
prior_credits = int(input(REQUEST_PRIOR_CREDITS))
num_current_modules = int(input(REQUEST_NUM_CURRENT_MODULES))

print(REQUEST_CURRENT_RESULTS)
current_results = receive_results(num_current_modules)

print(SEMESTER_GPA_PREFIX + str(calculate_semester_gpa(current_results)))
print(CUMULATIVE_GPA_PREFIX + str(calculate_cumulative_gpa(current_results, prior_cumulative_gpa, prior_credits)))




