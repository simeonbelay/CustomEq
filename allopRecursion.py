import json
import numpy as np

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def delete_node(self, node):
        if self.head == node:
            self.head = node.next
        else:
            current = self.head
            while current.next != node:
                current = current.next
            current.next = node.next

    def operationOne(self):
        current = self.head
        while current and current.next:
            if current.next.data in ['**', '*', '/']:
                operand1 = current.data
                operand2 = current.next.next.data

                # Resolve operand1 if it's a variable
                if isinstance(operand1, str) and operand1 in variables:
                    operand1 = variables[operand1]

                # Resolve operand2 if it's a variable
                if isinstance(operand2, str) and operand2 in variables:
                    operand2 = variables[operand2]

                # Convert scalars to float
                if isinstance(operand1, str) and operand1.replace('.', '', 1).isdigit():
                    operand1 = float(operand1)
                if isinstance(operand2, str) and operand2.replace('.', '', 1).isdigit():
                    operand2 = float(operand2)

                # Handle exponentiation, multiplication, and division
                if current.next.data == '**':
                    if isinstance(operand1, list) and isinstance(operand2, (int, float)):
                        raise TypeError("Exponentiation with vectors is not supported.")
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, (int, float)):
                        current.data = operand1 ** operand2
                    else:
                        raise TypeError(f"Unsupported operation: Exponentiation between incompatible types: {type(operand1)} and {type(operand2)}")

                elif current.next.data == '*':
                    if isinstance(operand1, list) and isinstance(operand2, list):
                        current.data = vector_multiplication(operand1, operand2)
                    elif isinstance(operand1, list) and isinstance(operand2, (int, float)):
                        current.data = vector_multiplication(operand1, operand2)
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, list):
                        current.data = vector_multiplication(operand2, operand1)
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, (int, float)):
                        current.data = operand1 * operand2

                elif current.next.data == '/':
                    if isinstance(operand1, list) and isinstance(operand2, (int, float)):
                        current.data = vector_division(operand1, operand2)
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, (int, float)):
                        current.data = operand1 / operand2
                    else:
                        raise TypeError(f"Unsupported operation: Division between incompatible types: {type(operand1)} and {type(operand2)}")

                # Remove the operator and operand nodes
                self.delete_node(current.next)  # Remove the operator
                self.delete_node(current.next)  # Remove the second operand
            else:
                current = current.next

    def operationTwo(self):
        current = self.head
        while current and current.next:
            if current.next.data in ['+', '-']:
                operand1 = current.data
                operand2 = current.next.next.data

                # Resolve operand1 if it's a variable
                if isinstance(operand1, str) and operand1 in variables:
                    operand1 = variables[operand1]

                # Resolve operand2 if it's a variable
                if isinstance(operand2, str) and operand2 in variables:
                    operand2 = variables[operand2]

                # Convert scalars to float
                if isinstance(operand1, str) and operand1.replace('.', '', 1).isdigit():
                    operand1 = float(operand1)
                if isinstance(operand2, str) and operand2.replace('.', '', 1).isdigit():
                    operand2 = float(operand2)

                # Handle addition and subtraction
                if current.next.data == '+':
                    if isinstance(operand1, list) and isinstance(operand2, list):
                        current.data = vector_addition(operand1, operand2)
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, (int, float)):
                        current.data = operand1 + operand2
                    else:
                        raise TypeError(f"Unsupported operation: Addition between incompatible types: {type(operand1)} and {type(operand2)}")

                elif current.next.data == '-':
                    if isinstance(operand1, list) and isinstance(operand2, list):
                        current.data = vector_subtraction(operand1, operand2)
                    elif isinstance(operand1, (int, float)) and isinstance(operand2, (int, float)):
                        current.data = operand1 - operand2
                    else:
                        raise TypeError(f"Unsupported operation: Subtraction between incompatible types: {type(operand1)} and {type(operand2)}")

                # Remove the operator and operand nodes
                self.delete_node(current.next)  # Remove the operator
                self.delete_node(current.next)  # Remove the second operand
            else:
                current = current.next


    def get_result_list(self):
        current = self.head
        result = []
        while current:
            result.append(current.data)
            current = current.next
        return result

def vector_multiplication(vector1, operand2):
    if isinstance(operand2, (int, float)):
        return ['doubleV3'] + [v1 * operand2 for v1 in vector1[1:]]
    elif isinstance(operand2, list):
        if len(vector1) == len(operand2):
            return ['doubleV3'] + [v1 * v2 for v1, v2 in zip(vector1[1:], operand2[1:])]
        else:
            raise ValueError("Incompatible vector lengths for multiplication.")

def vector_division(vector1, operand2):
    if isinstance(operand2, (int, float)):
        if operand2 == 0:
            raise ZeroDivisionError("Division by zero encountered.")
        return ['doubleV3'] + [v1 / operand2 for v1 in vector1[1:]]
    else:
        raise ValueError("Vector division by another vector is not supported in this context.")

def vector_addition(vector1, vector2):
    return ['doubleV3'] + [v1 + v2 for v1, v2 in zip(vector1[1:], vector2[1:])]

def vector_subtraction(vector1, vector2):
    return ['doubleV3'] + [v1 - v2 for v1, v2 in zip(vector1[1:], vector2[1:])]

def vector_magnitude(vector):
    if isinstance(vector, list):
        vector = np.array(vector[1:])
    return float(np.linalg.norm(vector))

def tokenize(expression):
    return expression.split()

def get_parameter(json_data, name, parameter):
    for entity in json_data["DataManager"]["entities"]:
        if entity.get("#Required", {}).get("Name") == name:
            return entity.get(parameter)
    return None

def defineVariable(json_data, varName):
    splitVar = varName.split("#")
    parameter = splitVar[1].strip()
    value = get_parameter(json_data, splitVar[0].strip(), parameter)
    return value

def extract_variables(tokens, json_data):
    variables = {}
    for token in tokens:
        if '#' in token and token not in ['+', '-']:
            var_name = token
            if var_name not in variables:
                value = defineVariable(json_data, var_name)
                variables[var_name] = value
    return variables

def calculate_expression(expression, variables):
    tokens = tokenize(expression)
    tokens = handle_parentheses(tokens)
    
    linked_list = LinkedList()
    
    # Add tokens to linked list
    for token in tokens:
        linked_list.append(token)
    
    # Perform the first round of operations (exponentiation, multiplication, and division)
    linked_list.operationOne()

    # Get the simplified list of tokens after the first round of operations
    result_list = linked_list.get_result_list()

    # Rebuild the linked list with remaining tokens
    linked_list = LinkedList()
    for token in result_list:
        linked_list.append(token)

    # Perform the second round of operations (addition and subtraction)
    linked_list.operationTwo()

    # Get the final result from the linked list
    result_list = linked_list.get_result_list()
    result = None
    operator = None

    for token in result_list:
        if token in ['+', '-']:  # If the token is an operator
            operator = token
        else:
            # Handle vector and scalar results
            if isinstance(token, list):
                if result is None:
                    result = token
                else:
                    if operator == '+':
                        result = vector_addition(result, token)
                    elif operator == '-':
                        result = vector_subtraction(result, token)
            elif isinstance(token, (int, float)):
                if result is None:
                    result = token
                else:
                    if operator == '+':
                        result += token
                    elif operator == '-':
                        result -= token

    return result


def handle_parentheses(tokens):
    stack = []
    result = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            stack.append(i)
        elif token == ')':
            start = stack.pop()
            sub_expression = tokens[start + 1:i]
            sub_result = calculate_expression(" ".join(map(str, sub_expression)), variables)
            result.append(sub_result)
        else:
            if not stack:
                result.append(token)

        i += 1

    return result


def parse_expression(expression):
    tokens = tokenize(expression)
    tokens = handle_parentheses(tokens)

    # Convert all tokens to strings for joining
    tokens = list(map(str, tokens))
    return calculate_expression(" ".join(tokens), variables)


if __name__ == "__main__":
    file_name = "simfile.json"
    with open(file_name, "r") as file:
        data = json.load(file)

    expression = input("Enter a mathematical expression: ")
    tokens = tokenize(expression)
    variables = extract_variables(tokens, data)

    result = parse_expression(expression)
    print("Result:", result)

    if result is not None and isinstance(result, list):
        choice = input("Do you want the magnitude of the resulting vector? (yes/no): ")
        if choice.lower() == 'yes':
            result_magnitude = vector_magnitude(result)
            print("Magnitude of the resulting vector:", result_magnitude)
        else:
            print("Okay, no problem.")
    else:
        print("No resulting vector to calculate magnitude.")
