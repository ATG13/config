def arithmetic_arranger(problems, show_answers=False):

  # Error handling
  if len(problems) > 5:
    return "Error: Too many problems."
  
  valid_operators = "+-"
  for problem in problems:
    parts = problem.split()
    if len(parts) != 3 or parts[1] not in valid_operators:
      return "Error: Operator must be '+' or '-'."
    if not all(part.isdigit() for part in parts[:2]):
      return "Error: Numbers must only contain digits."
    if max(len(part) for part in parts[:2]) > 4:
      return "Error: Numbers cannot be more than four digits."

  # Calculate maximum operand length and spacing
  max_len = max(len(part) for problem in problems for part in problem.split())

  # Build the arranged problems
  arranged_problems = []
  for problem in problems:
    parts = problem.split()
    operand1, operator, operand2 = parts

    # Right-align operands and add spaces
    operand1_padded = operand1.rjust(max_len)
    operand2_padded = operand2.rjust(max_len)
    operator_line = operator + " " * (max_len - len(operator))

    arranged_problems.append([operand1_padded, operator_line, operand2_padded])

  # Add answer line if requested
  if show_answers:
    answers = [str(eval(problem.split()[0] + problem.split()[1] + problem.split()[2])) for problem in problems]
    answer_line = [answer.rjust(max_len) for answer in answers]
    arranged_problems.append(["-" * (max_len + 2)] * len(problems))
    arranged_problems.extend(answer_line)

  # Combine arranged lines with spacing
  return "\n".join(" ".join(line) for line in zip(*arranged_problems))
