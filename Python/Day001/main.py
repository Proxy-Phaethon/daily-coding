from calculator import calculate


num1 = input("Your first number: ")
num2 = input("Your second number: ")
operator = input("Choose an operator (+, -, *, /): ")

try:
    result = calculate(num1, num2, operator)
    print(result)
except ValueError as error:
    print(error)