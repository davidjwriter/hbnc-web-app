# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

def solution(P,K):
    # write your code in Python 2.7
    roseBed = [0] * len(P)
    dayCounter = 0
    for rose in P:
        dayCounter += 1
        roseBed[rose - 1] = 1
        roseCounter = 0
        iterCounter = 0
        if (dayCounter > K):
            return -1
        flag = False
        while (not flag) and (iterCounter < len(roseBed)):
            if (roseBed[iterCounter] == 0):
                roseCounter += 1
            else:
                roseCounter = 0
            iterCounter += 1
            if (roseCounter == K and (iterCounter == len(roseBed) or roseBed[iterCounter] == 1)):
                flag = True
        if (flag):
            return dayCounter
    return -1
if __name__ == "__main__":
    print(solution([2,1,4,3],1))
