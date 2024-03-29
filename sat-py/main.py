# IMPORT LIBRARIES
import itertools
from utils import *
from timeit import default_timer as timer

def solve_problem(input_directory):

    w, n, x, y, maxlen = read_file(input_directory)
    solution = [[[Bool(f"solution_{i}_{j}_{k}") for k in range(n)] for j in range(maxlen)] for i in range(w)]

    #takes the index of biggest silicon
    biggest_silicon = 0
    for k in range(n):
        if x[biggest_silicon] * y[biggest_silicon] < x[k] * y[k]:
            biggest_silicon = k

    sum = 0
    for k in range(n):
        sum += x[k] * y[k]
    l = math.floor(sum / w)

    timeout = 300
    elapsed = 0

    solved = False
    while l <= maxlen and solved == False:

        solver = Solver()

        print("Defining constraints ...")

        #every silicon has at most one solution
        for k in range(n):
            solver.add(exactly_one([solution[i][j][k] for i in range(w) for j in range(l)]))

        # no coinciding solutions
        for j in range(l):
            for i in range(w):
                solver.add(at_most_one([solution[i][j][k] for k in range(n)]))

        #making sure the silicons don't spill out of the box
        for k in range(n):
            for i in range(w - x[k] + 1, w):
                for j in range(l):
                    solver.add(Not(solution[i][j][k]))
            for j in range(l - y[k] + 1, l):
                for i in range(w):
                    #print("i", i, " j", j, " k", k)
                    solver.add(Not(solution[i][j][k]))

        # puts the silicon with larger area in the bottom left corner
        solver.add([And(solution[0][0][biggest_silicon])])

        #two silicons can't have cumulative width bigger than w, and height than l
        '''for (k1, k2) in itertools.combinations(range(n), 2):
            if x[k1] + x[k2] > w and k1 != k2:
                for j in range(l):
                    for i1 in range(w - x[k1]):
                        for i2 in range(w - x[k2]):
                            solver.add(Not(And(solution[i1][j][k1], solution[i2][j][k2])))

        for (k1, k2) in itertools.combinations(range(n), 2):
            if y[k1] + y[k2] > l and k1 != k2:
                for i in range(w):
                    for j1 in range(l - y[k1]):
                        for j2 in range(l - y[k2]):
                            solver.add(Not(And(solution[i][j1][k1], solution[i][j2][k2])))'''

        #no overlap
        for k in range(n):
            possible_solutions = []
            for i in range(w - x[k] + 1):
                for j in range(l - y[k] + 1):
                    false_other_rectangles = []
                    for kk in range(n):
                        for ii in range(i+x[k]):
                            for jj in range(j+y[k]):
                                if kk != k:
                                    #if ((i-x[kk]<ii<i or j-y[kk]<jj<j) and ii+x[kk]>i and jj+y[kk]>j) or (ii>=i and jj>=j):
                                    if (ii + x[kk] > i and jj + y[kk] > j):
                                        #print(i,j,ii,jj,x[k], y[k], x[kk], y[kk], i-x[kk], ii+x[kk], j-y[kk], jj+y[kk])
                                        false_other_rectangles.append(Not(solution[ii][jj][kk]))
                                        # print(k, kk, i, j, ii, jj, "firstif")
                                else:
                                    if i == ii and j == jj:
                                        false_other_rectangles.append(solution[ii][jj][kk])
                                        # print(k, kk, i, j, ii, jj, "secondtif")
                                    '''else:
                                        false_other_rectangles.append(Not(solution[ii][jj][kk]))
                                        # print(k, kk, i, j, ii, jj, "else")
                                        array[kk, ii, jj] = 1'''
                        # print(false_other_rectangles)
                    # print(false_other_rectangles)
                    possible_solutions.append(And(false_other_rectangles))
            # print(possible_solutions)
            solver.add(exactly_one(possible_solutions))

        solver.set("timeout", timeout * 1000) #300000

        print("Checking satisfiability ...")
        start = timer()
        if solver.check() == sat:
            time = timer() - start
            print("model solved with length:", l, "in time: ", time, "s")
            # print(solver.model())
            timeout = timeout - time
            print("timeout:", timeout)
            elapsed = elapsed + time
            print("elapsed:", elapsed)

            solved = True
            final_x, final_y, final_r, final_l = get_solution(solver.model(), solution, w, l, n, maxlen)

            return final_x, final_y, w, n, x, y, final_l, final_r, elapsed
            # print(time)
        else:
            time = timer() - start
            timeout = timeout - time
            print("timeout:", timeout)
            elapsed = elapsed + time
            print("elapsed:", elapsed)
            print("Failed to solve with length: ", l)
            l = l + 1
            if elapsed >= timeout:
                return None

    '''if l <= maxlen:
        final_x, final_y, final_r, final_l = get_solution(solver.model(), solution, w, l, n, maxlen)
        output_matrix = display_solution(final_x, final_y, w, n, x, y, final_l, final_r)
            # PLOT SOLUTION
            fig, ax = plt.subplots(figsize=(5, 5))
            sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
            # sns.color_palette("Set2")
            plt.show()
        return final_x, final_y, w, n, x, y, final_l, final_r, elapsed
    else:
        return None'''



def main():
    input_directory = "./instances/ins-6.txt"
    solve_problem(input_directory)
    #solve_all(solve_problem, "./out/noRotation")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

