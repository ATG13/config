my_list = [1, (2, "apple"), "hello", (3.14, False)]

extracted_tuples = []
for item in my_list:
  if isinstance(item, tuple):
    extracted_tuples.append(item)

print(extracted_tuples)