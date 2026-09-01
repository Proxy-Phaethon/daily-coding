# a calculator needs to accept two inputs and an operator and print the result.
# it also needs to sanitize the inputs beforehand to make sure it is something that
# can be operated on.
# the main issue here is error handling, not the calculator logic itself.
# also i dont know python syntax so the biggest issue for me was realising that 
# there's a difference between true and True.
# the second issue was making the code smaller. and endless if-elif statement could do this same thing, after all.
# but i guess this is indeed how you learn.


def calculate(num1, num2, operator):
    try:
        n1 = float(num1)
        n2 = float(num2)
    except ValueError:
        raise ValueError("Invalid input. Please enter valid numbers.")

    if operator not in ["+", "-", "*", "/"]:
        raise ValueError("Invalid operator.")

    if operator == "+":
        return n1 + n2

    if operator == "-":
        return n1 - n2

    if operator == "*":
        return n1 * n2

    if operator == "/":
        if n2 == 0:
            raise ValueError("Division by zero is not allowed.")

        return n1 / n2