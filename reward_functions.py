


def get_reward(self):
    state = self.get_state_vector()
    multiplier = 0
    if abs(state[-2]) < 25 and abs(state[-3]) < 25 and abs(state[-4]) < 25:
        multiplier = 1
    else:
        multiplier = .99 ** ((state[-2] + state[-3] + state[-4])/5)
    if abs(state[-1]) < 1:
        return multiplier * 100
    return -1

def fly_flat_reward(self):
    state = self.get_raw_state()
    reward = 0
    if abs(state[6]) < 250 and abs(state[6]) > 225:
        reward = reward + 1


    if abs(state[7]) < 2.5 and abs(state[8]) < 2.5:
        return reward + 4
    elif abs(state[7]) < 5 and abs(state[8]) < 5:
        return reward + 2
    elif abs(state[7]) < 10 and abs(state[8]) < 10:
        return reward + 1

    if abs(state[7]) > 10:
        reward = reward - 1
    if abs(state[8]) > 10:
        reward = reward - 1
    if abs(state[7]) > 15:
        reward = reward - 1
    if abs(state[8]) > 15:
        reward = reward - 1
    if abs(state[7]) > 30:
        reward = reward - 1
    if abs(state[8]) > 30:
        reward = reward - 1
    if abs(state[7]) > 40:
        reward = reward - 2
    if abs(state[8]) > 40:
        reward = reward - 2

    return reward