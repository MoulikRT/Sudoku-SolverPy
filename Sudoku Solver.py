### Sudoku Solver

# https://www.thonky.com/sudoku/ -- Generate puzzles
# https://qqwing.com/generate.html -- Generate puzzles (Select output format as 'one line'.)
# Puzzles must be an 81 digit string with '0's or '.'s to represent blank numbers.

# Sample puzzles - 
# 004006079000000602056092300078061030509000406020540890007410920105000000840600100
# 4...8..2..6..31..48.....3..5...928.....5.......6.1....3.5..4....8495....12.6..... -- "Hard" according to other solvers; takes 0.5 seconds for mine.
# ......9.77....8..2...9.563.94.....5.6..5.2.........32......98.....68.793...3.4...
# ..65.81............8.21...54.....7..5.........6..513.4...9..81.62.......7...2.63. -- "Easy" according to other solvers; takes 20 seconds for mine.


# Input and variable declaration - 

#sudoku_input = str(input("Enter a 81 character string. :"))
sudoku_input = '4...8..2..6..31..48.....3..5...928.....5.......6.1....3.5..4....8495....12.6.....' #Input the string inside these apostrophes.
sudoku_input = sudoku_input.replace('.','0')
solution = []
master_list = []


#Function definitions - 

def sudoku_print(sudoku_input):
    line_break_counter, new_batch, new_set = 0,0,0
    for i in range(0, len(sudoku_input)):
        print(sudoku_input[i], end = '\t') if (sudoku_input[i] != '0') else print('_', end = '\t')

        line_break_counter+=1
        if line_break_counter%3==0: 
            print(end = '\t')
            new_batch+=1
    
        if new_batch%3==0 and new_batch !=0: 
            print('\n')
            new_batch = 0
            new_set+=1
    
        if new_set%3==0 and new_set !=0:
            print('\n')
            new_set = 0


def sudoku_identify_row(row_input):
    row_list =[]
    for j in range(0,81,9):
        present_list = [1,2,3,4,5,6,7,8,9]
        for i in range(1,10):
            if str(i) in row_input[j:j+9]: 
                present_list.remove(i)
        row_list.append(present_list)
    return(row_list)


def sudoku_identify_column(column_input):
    column_list=[]
    for j in range(0,9):
        present_list = [1,2,3,4,5,6,7,8,9]
        for i in range(1,10):
            if str(i) in column_input[j:j+73:9]:
                present_list.remove(i)
        column_list.append(present_list)
    return(column_list)


def sudoku_identify_box(box_input):
    box_list=[]
    temp_string = ''
    for i in range(0,55,27):
        for j in range(i,i+9,3):
            temp_string = temp_string + box_input[j:j+3] + box_input[j+9:j+12] + box_input[j+18:j+21]
    for j in range(0,81,9):
        present_list = [1,2,3,4,5,6,7,8,9]
        for i in range(1,10):
            if str(i) in temp_string[j:j+9]:
                present_list.remove(i)
        box_list.append(present_list)
    return(box_list)


def sudoku_identify(n):
    Complete_list = sudoku_identify_row(n) + sudoku_identify_column(n) + sudoku_identify_box(n)
    return(Complete_list)


def get_permutations(my_list):
  if len(my_list) == 0 or len(my_list) == 1: return [my_list]
  
  permutation_list = []
  for permutation in get_permutations(my_list[1:]):
    for i in range(len(permutation)+1):
      new_permutation = permutation[:i] + [my_list[0]] + permutation[i:]
      permutation_list.append(new_permutation)
  
  return permutation_list


def list_to_string(list_input, string_output = ''):
    for i in range(0, len(list_input)): string_output += str(list_input[i])

    return string_output


def sudoku_solving(solve_input, solve_array, elimination_list, row):
    solve_input_clone = solve_input[9*(row-1):9*(row)]
    row_list = []
    for i in range(0, len(solve_array)):
        j = 0
        for cell in range(0,9):
            if solve_input_clone[cell] == '0' and (solve_array[i][j] in elimination_list[cell+9]) and solve_array[i][j] in elimination_list[(cell//3+18) + 3*((row-1)//3)]:
                solve_input_clone[cell] = str(solve_array[i][j])
                j+=1

            elif solve_input_clone[cell] == '0': break

        if '0' not in solve_input_clone: 
            row_list.append(solve_input_clone)
        
        solve_input_clone = solve_input[9*(row-1):9*(row)]
    return row_list


def iterate_residueclass_three(input, case):
    if case == 0: 
        if input < 3: return 3
        else: return 0
    if case == 1:
        if input >=3 and input < 6: return 6
        else: return 0
    return 0


def win_condition(input):
    iterate = len(input)//9

    for j in range(0,9):
        value = [input[k+j] for k in range(0,9*iterate,9)]

        if len(set(value)) != len(value): return False

    for j in range(((iterate-1)//3 + 1)*3):
        if iterate <= 3: value = [input[((j%3)*3+k)+9*(l)] for l in range(((j)//3)*3,iterate) for k in range(3)]
        if iterate > 3 and iterate <=6: value = [input[((j%3)*3+k)+9*(l)] for l in range(((j)//3)*3,(j//3)*iterate -3*(j//3 -1)) for k in range(3)]
        if iterate > 6: value = [input[((j%3)*3+k)+9*(l)] for l in range(((j)//3)*3, ((((j//3)//2)*iterate) + (iterate_residueclass_three(j, 0)) + iterate_residueclass_three(j,1))) for k in range(3)]

        if len(set(value)) != len(value): return False

    return True


def recursive_solution_search(input, depth=0, send=''):
    if win_condition(send):
        if depth < 9:
            for i in input[depth]:
                if recursive_solution_search(input, depth+1, send + list_to_string(i)): 
                    return True
            return False
        solution.append(send)
        return True   
    return False


# Code Execution - 

if len(sudoku_input) != 81 or type(sudoku_input) != str: 
    print("Puzzle is not valid. Input must be in-between '' and should be 81 characters.", '\n\n')
    sudoku_print(sudoku_input)
else: 
    print("Solving...", '\n\n')

    for row_no in range(1, 10):
        master_list.append(sudoku_solving(list(sudoku_input), get_permutations(sudoku_identify(sudoku_input)[row_no - 1]), sudoku_identify(sudoku_input), row_no))

    if recursive_solution_search(master_list):
        print('Your input is :', sudoku_input, '\n')
        print("On a sudoku grid it looks like : ", '\n')
        sudoku_print(sudoku_input)
        print()

        print('Your output is :',list_to_string(solution), '\n')
        print("On a sudoku grid it looks like : ", '\n')
        sudoku_print(list_to_string(solution))

    else: print("Can't find a solution.")

