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
import itertools

NEWLINE = "\n"
SPACE = " "

WELCOME_MESSAGE = "Welcome to SUpervisor!"

FIRST_SEMESTER_CONDITION_MESSAGE = "If this is your first semester, input 0."

REQUEST_PRIOR_CUMULATIVE_GPA = "Please enter your cumulative GPA at the beginning of this semester." \
                               + SPACE + FIRST_SEMESTER_CONDITION_MESSAGE

REQUEST_PRIOR_CREDITS = "Please enter the number of credits contributing to your CAP at the beginning of this semester." \
                        + SPACE + FIRST_SEMESTER_CONDITION_MESSAGE

REQUEST_NUM_CURRENT_MODULES = "Please enter the number of modules taken this semester."

MODULE_ENTRY_FORMAT = "[MODULE CODE] [LETTER GRADE] [NO. OF MODULAR CREDITS]"

MODULE_ENTRY_EXAMPLE = "e.g. CS1101S B+ 4"

REQUEST_CURRENT_RESULTS = "Please enter your actual results for the modules taken this semester, " \
                          + "in the following format:" + NEWLINE \
                          + MODULE_ENTRY_FORMAT + SPACE + MODULE_ENTRY_EXAMPLE + NEWLINE

SEMESTER_GPA_PREFIX = "Semester GPA: "

CUMULATIVE_GPA_PREFIX = "Cumulative GPA: "

REQUEST_SU_BALANCE = "Please enter your remaining S/U balance (in terms of number of modular credits)."


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
    S = 0
    U = 0


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

    def su(self):
        su_grade = LetterGrade.S if (self.letter_grade.value >= LetterGrade.C.value) else LetterGrade.U
        return Module(self.module_code, su_grade, 0)

    def is_sued(self):
        return self.letter_grade is LetterGrade.S or self.letter_grade is LetterGrade.U


class SuCombination():
    def __init__(self, original_results: iter, selected_results_to_su: iter):
        self.original_results = original_results
        self.selected_results_to_su = selected_results_to_su
        self.new_results = su_modules(original_results, selected_results_to_su)

    def get_new_semester_gpa(self):
        return calculate_semester_gpa(self.new_results)

    def get_new_cumulative_gpa(self):
        return calculate_cumulative_gpa(self.new_results, prior_cumulative_gpa, prior_credits)

    def get_sued_module_codes_str(self):
        return str(list(map(lambda m: m.get_module_code(), self.selected_results_to_su))) \
            if self.selected_results_to_su else "nothing"

    def get_statistics_str(self):
        return "If you S/U " + self.get_sued_module_codes_str() \
               + ", your semester and cumulative GPA will be " \
               + str(self.get_new_semester_gpa()) + " and " \
               + str(self.get_new_cumulative_gpa()) + " respectively."


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
        if module.is_sued():
            continue
        grade_credit_product += module.get_letter_grade().value * module.get_credits()
        credit_sum += module.get_credits()
    return float(grade_credit_product) / float(credit_sum)


def calculate_cumulative_gpa(modules: list, prior_cum_gpa: float, prior_credits: int):
    grade_credit_product = prior_cum_gpa * prior_credits
    credit_sum = prior_credits
    for module in modules:
        if module.is_sued():
            continue
        grade_credit_product += module.get_letter_grade().value * module.get_credits()
        credit_sum += module.get_credits()
    return float(grade_credit_product) / float(credit_sum)


def get_module_subsets(modules: list):
    return list(itertools.chain.from_iterable(itertools.combinations(modules, r) for r in range(len(modules) + 1)))


def has_exceeded_su_balance(selected_modules_to_su, balance):
    return sum(map(lambda module: module.get_credits(), selected_modules_to_su)) > balance


def su_modules(current_modules: iter, selected_modules_to_su: iter):
    new_modules = current_modules.copy()
    for mod in selected_modules_to_su:
        sued_mod = mod.su()
        new_modules = [sued_mod if m.get_module_code() is mod.get_module_code() else m for m in new_modules]
    return new_modules


print(WELCOME_MESSAGE)

# Request for all relevant information
prior_cumulative_gpa = float(input(REQUEST_PRIOR_CUMULATIVE_GPA))
prior_credits = int(input(REQUEST_PRIOR_CREDITS))
num_current_modules = int(input(REQUEST_NUM_CURRENT_MODULES))
su_balance = int(input(REQUEST_SU_BALANCE))

# Request for results of modules taken this semester
print(REQUEST_CURRENT_RESULTS)
current_results = receive_results(num_current_modules)

# Output current semester and cumulative GPA
current_semester_gpa = calculate_semester_gpa(current_results)
current_cumulative_gpa = calculate_cumulative_gpa(current_results, prior_cumulative_gpa, prior_credits)
print(SEMESTER_GPA_PREFIX + str(current_semester_gpa))
print(CUMULATIVE_GPA_PREFIX + str(current_cumulative_gpa))

# Print all available S/U combinations
combinations = get_module_subsets(current_results)
for combination in combinations:
    if has_exceeded_su_balance(combination, su_balance):
        continue
    su_combination = SuCombination(current_results, combination)
    is_useful = su_combination.get_new_semester_gpa() >= current_semester_gpa \
                and su_combination.get_new_cumulative_gpa() >= current_cumulative_gpa
    if is_useful:
        print(su_combination.get_statistics_str())


