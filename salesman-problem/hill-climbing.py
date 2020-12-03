# Adaptative Cognitive Agentes - Activite of Optimization (Hill-Climbing)

# Hill Climbing Algoritmh 
# - Choose best child always, if no best child stops.
#
# Developed by Lucas Cavalcanti

from joblib import Parallel, delayed
import tsplib95
import random
import time
from solution import Solution
 
# Repetitions ->
# - Repeates the algorithm with random starting solution
repeate = 10

# Branch Factor -> 
# - Number of childrens generated at each interation. 
# - If #brach == #cities, permutes first city with all remaining.
branch_factor = 38

# Swaps ->
# - Number of nodes to randomly swap in child generation
swaps = 1

filePath = "./dj38.tsp"
result_file = open("./results/"+ filePath[:-4] + "_rand_" + (("swap_" + str(swaps)) if swaps >= 0 else "shuffle") + "_" + str(branch_factor) + "_x_" +  str(repeate) + ".txt",'w')

def f_n(nodes, cities, n_nodes):
	dist = 0
	for i in range(n_nodes-1):
		edge = nodes[i], nodes[i+1]
		dist += cities.get_weight(*edge)
	return dist

def swap_random(nodes, cities, n_nodes, i):
	temp_nodes = nodes.copy()
	swap_place = random.randint(int((i - 1) * (n_nodes / branch_factor)), int(i * (n_nodes / branch_factor) - 1))
	if swap_place == 0:
		return ([], float('inf'))
	temp_nodes[0], temp_nodes[swap_place] = temp_nodes[swap_place], temp_nodes[0]
	temp_value = f_n(temp_nodes, cities, n_nodes)
	return (temp_nodes, temp_value)

def swap_n_random(nodes, cities, n_nodes, i):
	temp_nodes = nodes.copy()
	random_idx = list(range(n_nodes))
	random.shuffle(random_idx)
	for s in range(swaps):
		temp_nodes[random_idx[0]], temp_nodes[random_idx[1]] = temp_nodes[random_idx[1]], temp_nodes[random_idx[0]]
		random_idx = random_idx[2:]
		if len(random_idx) < 4:
			random_idx = list(range(n_nodes))
			random.shuffle(random_idx)
	temp_value = f_n(temp_nodes, cities, n_nodes)
	return (temp_nodes, temp_value)

def shuffle_random(nodes, cities, n_nodes, i):
	temp_nodes = nodes.copy()
	random.shuffle(temp_nodes)
	temp_value = f_n(temp_nodes, cities, n_nodes)
	return (temp_nodes, temp_value)

def operate(nodes, cities, n_nodes):
	b_nodes = []
	b_value = 0
	function = None
	if swaps == 0:
		function = swap_random
	elif swaps > 0:
		function = swap_n_random		
	else:
		function = shuffle_random
	
	childrens = Parallel(n_jobs=8)(delayed(function)(nodes, cities, n_nodes, i) for i in range(1, branch_factor+1))
	
	for c, v in childrens:
		# Best child remain
		if(b_value == 0 or v < b_value):
			b_nodes = c
			b_value = v
	return b_nodes, b_value

def main():
	cities = tsplib95.load(filePath)
	n_nodes = len(list(cities.get_nodes()))

	solutions = []
	best_round_value = (0, 0)
	
	for i in range(repeate):		

		nodes = list(range(1, n_nodes + 1))
		random.shuffle(nodes)
		value = f_n(nodes, cities, n_nodes)
		iterations = 0
		

		result = Solution(i)
		result_file.write("###########   Round: " + str(i+1) + "   ###########\n")
		
		start_t = time.time()
		iterations_t = []
		while(True):
			iterations += 1
			# Operate -> Find best children
			child_nodes, child_value = operate(nodes, cities, n_nodes)
			result_file.write("#### "+ str(iterations) + " iteration -> f(n): " + str(value) + "\n")

			# Success reduces distance value?
			if child_value <= value and iterations <= 300: 
				value = child_value
				nodes = child_nodes
			else: # end
				result.set(nodes, value, iterations)
				solutions.append(result)
				result_file.write("\n####   Best Solution -> " + str(iterations) + " iterations: f(n): " + str(value))
				result_file.write("\n####     - Elapsed time: " + str(sum(iterations_t)) + " |  time / iterations: " + str(sum(iterations_t)/iterations) + "\n\n\n")

				if best_round_value[0] == 0 or value < best_round_value[0]:
					best_round_value = (value, i+1)
					with open(result_file.name[:-4] + "_nodes.txt",'w',encoding = 'utf-8') as f:
						f.write("#####   Best Solution found, in round: " + str(i+1) + "  -> f(n): " + str(best_round_value[0]) + "   ######\n")
						f.write("####       - Elapsed time: " + str(sum(iterations_t)) + " |  time / iterations: " + str(sum(iterations_t)/iterations) + "\n")
						f.write("Order to visit cities: ")
						for n in nodes:
							f.write(str(n) + ", ")
				if i == repeate-1:
					result_file.write("Over all Best Solution: " + str(best_round_value[1]) + " round -> f(n): " + str(best_round_value[0]))
				break
			iterations_t.append(time.time() - start_t)
			start_t = time.time()

	result_file.close()


if __name__ == '__main__':
    main() 
