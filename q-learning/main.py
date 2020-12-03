import numpy as np

# ========== DEFINITIONS ============
# epsilon = 0.001 # Convergence
alpha = 0.5
gamma = 0.8

value = np.zeros((6, 4))

rewards = np.full((6, ), -1)
rewards[5] = 10
terminal_state = 5

possible_actions = ["U", "D", "L", "R"]

# ==========   EPISODES   ===========
initial_state = [0, 4]
paths = [["U", "U", "U", "R"], ["L", "L", "R", "U"]]
# ===================================

def update_value(value, state, action):
    if state == terminal_state:
        return value, state
    
    s = state
    a = possible_actions.index(action)
    
    next_s = get_next_state(s, a)
    
    if next_s != s:
        rw = rewards[next_s]
    else:
        rw = -10
   
    value[s][a] += alpha * (rw + gamma * ( np.max([value[next_s][i] for i in range(4)]) - value[s, a] ) )

  
    print("Next State: ", next_s)
    np.set_printoptions(precision=3)
    print(print_value(value), "\n")
    return value, next_s

def get_next_state(s, a):
    next_s = s

    if a == 0:
        if s != 2 and s != 5:
            next_s = s + 1
    if a == 1:
        if s != 0 and s != 3:
            next_s = s - 1
    if a == 2:
        if s != 0 and s != 1 and s!= 2:
            next_s = s - 3
    if a == 3:
        if s != 3 and s != 4 and s!= 5:
            next_s = s + 3
    
    return next_s


def return_policy(value):   
    policy = []

    # obs.: somente 9 estados porque n�o ha a��o aplicada nos dois estados terminais
    for s in range(6):
        action = np.argmax([value[s][i] for i in range(4)])
        policy.append(action)
    
    actions = ["UP","DW","LF","RG"]

    s1 = [actions[policy[2]], "+10"]
    s2 = [actions[policy[1]],actions[policy[4]]]
    s3 = [actions[policy[0]],actions[policy[3]]]

    print("\n",s1,"\n",s2,"\n",s3, "\n")

    return(policy)

def print_value(value):
    aux = np.zeros((3, 2, 4))
    aux[0,] = np.array((value[2],value[5]))
    aux[1,] = np.array((value[1],value[4]))
    aux[2,] = np.array((value[0],value[3]))
    return aux

if __name__ == "__main__":
    episode = 0

    for path in paths:
        state = initial_state[episode]
        print("===== Episode: ", episode, " - Initial State: ", state, " ======")
        for action in path:
            old_value = value.copy()
            value, state = update_value(value, state, action)

            if state == terminal_state:
                print("Terminal State!")
                break

            # diff = np.sum(value - old_value)
            # if abs(diff) < epsilon:
            #     print("Converged!")
            #     break

        print("Updated values: \n", print_value(value), "\n---\n")
        episode += 1

    policy = return_policy(value)