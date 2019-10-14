import numpy as np

def isNash(pMat, p1m, p2m):
    return pMat[p1m, p2m, 0] >= pMat[1 - p1m, p2m, 0] and pMat[p1m, p2m, 1] >= pMat[p1m, 1 - p2m, 1]


def findPureNash(pMat):
    return [(i, j) for i in range(2) for j in range(2) if isNash(pMat, i, j)]


def findMixedNash(pMat):  # returns (p, q), where p is the probability of player a choosing option 1 and where q is the probability of player b choosing option 1
    p = (pMat[1, 1, 1] - pMat[1, 0, 1]) / (pMat[0, 0, 1] + pMat[1, 1, 1] - pMat[1, 0, 1] - pMat[0, 1, 1])
    q = (pMat[1, 1, 0] - pMat[0, 1, 0]) / (pMat[0, 0, 0] + pMat[1, 1, 0] - pMat[0, 1, 0] - pMat[1, 0, 0])

    if p<0 or p>1 or q<0 or q>1:
        return None

    return p, q


def findAllNash(pMat):
    pure = findPureNash(pMat)
    mixed = findMixedNash(pMat)
    pure.append(mixed)
    return pure


def evaluatePayoffs(pMat, strat):
    op1 = strat[0] * strat[1] * pMat[1, 1]  # probability of (1, 1) * payoff value
    op2 = strat[0] * (1 - strat[1]) * pMat[1, 0]  # probability of (1, 0) * payoff value
    op3 = (1 - strat[0]) * strat[1] * pMat[0, 1]  # probability of (0, 1) * payoff value
    op4 = (1 - strat[0]) * (1 - strat[1]) * pMat[0, 0]  # probability of (0, 0) * payoff value

    return tuple(op1 + op2 + op3 + op4)  # adding the arrays together gives the expected values (sum of the probabilities is 1)


def getMove(pMat, player):
    if player == 0:
        if pMat[0, 0, 0] > pMat[1, 0, 0] and pMat[0, 1, 0] > pMat[1, 1, 0]:  # check if we have a dominant strategy
            return 0
        elif pMat[0, 0, 0] < pMat[1, 0, 0] and pMat[0, 1, 0] > pMat[1, 1, 0]:
            return 1

        if pMat[0, 0, 1] > pMat[0, 1, 1] and pMat[1, 0, 1] > pMat[1, 1, 1]:  # check if opponent has a dominant strategy
            if pMat[0, 0, 0] > pMat[1, 0, 0]:  # if so, assume opponent will choose that and take best option
                return 0
            return 1
        elif pMat[0, 0, 1] > pMat[0, 1, 1] and pMat[1, 0, 1] > pMat[1, 1, 1]:  # do the same thing for opponents other choice
            if pMat[0, 1, 0] > pMat[1, 1, 0]:
                return 0
            return 1
    else:
        if pMat[0, 0, 1] > pMat[0, 1, 1] and pMat[1, 0, 1] > pMat[1, 1, 1]:  # check if we have a dominant strategy
            return 0
        elif pMat[0, 0, 1] > pMat[0, 1, 1] and pMat[1, 0, 1] > pMat[1, 1, 1]:
            return 1

        if pMat[0, 0, 0] > pMat[1, 0, 0] and pMat[0, 1, 0] > pMat[1, 1, 0]:  # check if we have a dominant strategy
            if pMat[0, 0, 1] > pMat[0, 1, 1]:
                return 0
            return 1

        elif pMat[0, 0, 0] < pMat[1, 0, 0] and pMat[0, 1, 0] > pMat[1, 1, 0]:
            if pMat[1, 0, 1] > pMat[1, 1, 1]:
                return 0
            return 1

    mixed = findMixedNash(pMat)  # if neither player has a dominant strategy, use the mixed strategy to figure out a move
    if mixed is None:
        opp_Mv = False
    elif mixed[1-player] > 0.7:  # if the opponent has p>0.7 of a certain move, assume they are going to do that
        opp_Mv = 1
    elif mixed[1-player] < 0.3:
        opp_Mv = 0
    else:
        opp_Mv = False

    if opp_Mv == 0:  # if the opponent is going to choose 0
        if player == 0 and pMat[0, 0, 0] > pMat[1, 0, 0]:  # check payoff values
            return 0
        elif player == 1 and pMat[0, 0, 1] > pMat[0, 1, 1]:  # check payoff values
            return 0
        else:
            return 1
    elif opp_Mv == 1:  # if the opponent if going to choose 1
        if player == 0 and pMat[0, 1, 0] > pMat[1, 1, 0]:  # check payoff values
            return 0
        elif player == 1 and pMat[1, 0, 1] > pMat[1, 1, 1]: # check payoff values
            return 0
        else:
            return 1
    else:  # if we don't know what they are going to do, use whatever option has the highest expected payoff (assume random choice)
        if mixed is None:
            val = mixed[1-player]
        else:
            if player == 0 and pMat[0, 0, 0] + pMat[0, 1, 0] > pMat[1, 0, 0] + pMat[1, 1, 0]:
                return 0
            elif player == 1 and pMat[0, 0, 1] + pMat[1, 0, 1] > pMat[0, 1, 1] + pMat[1, 1, 1]:
                return 0
            else:
                return 1
        if player == 0:
            if evaluatePayoffs(pMat, (1, val))[0] > evaluatePayoffs(pMat, (0, val))[0]:
                return 1
            return 0
        else:
            if evaluatePayoffs(pMat, (val, 1))[1] > evaluatePayoffs(pMat, (val, 0))[1]:
                return 1
            return 0

def main():
    a = np.array([
        [[1, 1], [5, 0]],
        [[0, 5], [3, 3]]
    ])  # a is payoff matrix; player zero's moves are represented by rows, player ones's by columns. This is the prisoner's dilemma matrix
    print(getMove(a, 1))


if __name__ == "__main__":
    main()
