# a calculator needs to accept two inputs and an operator and print the result.
# it also needs to sanitize the inputs beforehand to make sure it is something that
# can be operated on.
# the main issue here is error handling, not the calculator logic itself.
# also i dont know python syntax so the biggest issue for me was realising that 
# there's a difference between true and True.
# the second issue was making the code smaller. and endless if-elif statement could do this same thing, after all.
# but i guess this is indeed how you learn.


num1 = input('your first number: ')
num2 = input('your second number: ')
operator = input('choose an operator: ')

try:
    n1 = float(num1)
    n2 = float(num2)
except ValueError:
    print("Invalid input. Please enter valid numbers.")
    exit(1)

if operator not in ["+", "-", "*", "/"]:
    print("Invalid operator. Please choose a valid operator.")
    exit(1)

if operator == "+":
    result = n1 + n2
elif operator == "-":
    result = n1 - n2
elif operator == "*":
    result = n1 * n2
elif operator == "/":
    if n2 == 0:
        print("Error: Division by zero is not allowed.")
        exit(1)
    result = n1 / n2

print(result)