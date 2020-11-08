def sum_to_one(n):
  result = 1
  call_stack = []
  
  while n != 1:
    execution_context = {"n_value": n}
    call_stack.append(execution_context)
    n -= 1
    print(call_stack)
  print("BASE CASE REACHED")
  while call_stack:
    return_value = call_stack[-1]
    call_stack.pop(-1)
    print(call_stack)
    print("Adding {} to {}".format(return_value["n_value"], result))
    result += return_value["n_value"]
  return result, call_stack

sum_to_one(4)


def power_set(my_list):
    # base case: an empty list
    if len(my_list) == 0:
        return [[]]
    # recursive step: subsets without first element
    power_set_without_first = power_set(my_list[1:])
    # subsets with first element
    with_first = [ [my_list[0]] + rest for rest in power_set_without_first ]
    # return combination of the two
    return with_first + power_set_without_first
  
universities = ['MIT', 'UCLA', 'Stanford', 'NYU']
power_set_of_universities = power_set(universities)

for set in power_set_of_universities:
  print(set)

  def flatten(my_list):
  result = []
  for i in my_list:
    if isinstance(i, list):
      print("List found!")
      flat_list = flatten(i)
      result.extend(flat_list)
      print(result)
    else:
      result.append(i)
  return result


### reserve for testing...
planets = ['mercury', 'venus', ['earth'], 'mars', [['jupiter', 'saturn']], 'uranus', ['neptune', 'pluto']]

flatten(planets)


def fibonacci(n):
  if n <= 1:
    return n
  print(n)
  return fibonacci(n-1) + fibonacci(n-2)



fibonacci(5)
# set the appropriate runtime:
# 1, logN, N, N^2, 2^N, N!
fibonacci_runtime = "2^N"


# Define build_bst() below...

def build_bst(my_list):
  if not my_list:
    return "No Child"

  middle_idx = len(my_list) // 2
  middle_value = my_list[middle_idx]
  print("Middle index: " + str(middle_idx))
  print("Middle value: " + str(middle_value))
  tree_node = {"data":middle_value}
  tree_node["left_child"] = build_bst(my_list[:middle_idx])
  tree_node["right_child"] = build_bst(my_list[middle_idx + 1:])
  return tree_node


# For testing
sorted_list = [12, 13, 14, 15, 16]
binary_search_tree = build_bst(sorted_list)
print(binary_search_tree)

# fill in the runtime as a string
# 1, logN, N, N*logN, N^2, 2^N, N!
runtime = "N*logN"


def depth(tree):
  if not tree:
    return 0

  left_depth = depth(tree["left_child"])
  right_depth = depth(tree["right_child"])

  if left_depth > right_depth:
    return left_depth + 1
  else:
    return right_depth + 1

# HELPER FUNCTION TO BUILD TREES
def build_bst(my_list):
  if len(my_list) == 0:
    return None

  mid_idx = len(my_list) // 2
  mid_val = my_list[mid_idx]

  tree_node = {"data": mid_val}
  tree_node["left_child"] = build_bst(my_list[ : mid_idx])
  tree_node["right_child"] = build_bst(my_list[mid_idx + 1 : ])

  return tree_node

# HELPER VARIABLES
tree_level_1 = build_bst([1])
tree_level_2 = build_bst([1, 2, 3])
tree_level_4 = build_bst([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) 

# test cases
print(depth(tree_level_1) == 1)
print(depth(tree_level_2) == 2)
print(depth(tree_level_4) == 4)