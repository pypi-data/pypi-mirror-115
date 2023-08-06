def rotateLeft(array_list,num_rotate):
  new_array_list = []
  for i in range(len(array_list)):
    new_array_list.append(array_list[(i+num_rotate)% len(array_list)]) 
  return new_array_list


def rotateRight(array_list,num_rotate):
  new_array_list = []
  for i in range(len(array_list)):
    new_array_list.append(array_list[(i-num_rotate)% len(array_list)]) 
  return new_array_list

