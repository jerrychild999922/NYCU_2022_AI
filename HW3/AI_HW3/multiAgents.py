from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        '''
        I separate my code into three parts : main, find min, find max.

        For main part, get every possible pacman move's min value and put them in temp=[]
        then choose the best(max value) to move. I use random to avoid getting stuck 

        For min function, it will return the min value between different ghost moves.
        Because there is more than one ghost, min value is related to another's min value.
        Therefore, we need to use recursion to get another ghost's min value 
        ex: temp.append(self.Min_Value(gameState1,i+1, d)
        However, if the ghost is the last one it have to call max function because 
        it's value it related to pacman's max value,and when doing this step means depth+1 so d+1.
        ex: temp.append(self.Max_Value(gameState1, d+1)
        PS: if pacman touch ghost, there is no legalaction for ghost, so we need to 
        return the score right now.

        For max function, it will return max value  between different pacman moves.
        it's value is related to ghost's min value. Therefore, we need to call min function
        to get min value.
        ex: temp.append(self.Min_Value(gameState1,1,d)
        and if d=self.depth means it arrive leaf, just return current score.

        '''
        
        legalMoves = gameState.getLegalActions()
        temp=[]
        for action in legalMoves:
            childGameState = gameState.getNextState(0,action)
            temp.append(self.Min_Value(childGameState,1,0))
        maxscore=max(temp)
        bestIndices = [index for index in range(len(temp)) if temp[index] == maxscore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        
        
    def Max_Value (self, gameState, d):

        if gameState.isLose() or gameState.isWin() or d == self.depth:
            return self.evaluationFunction(gameState)
        
        temp=[]
        pacmoves=gameState.getLegalActions(0)
        for action in pacmoves :
            gameState1=gameState.getNextState(0,action)
            temp.append(self.Min_Value(gameState1,1, d))
        return max(temp)


    def Min_Value (self, gameState, i, d):

        if gameState.isLose() or gameState.isWin(): 
            return self.evaluationFunction(gameState)

        if (i < gameState.getNumAgents() - 1):
            temp=[]
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                temp.append(self.Min_Value(gameState1,i+1, d))
            return min(temp)

        else:  
            temp=[]
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                temp.append(self.Max_Value(gameState1, d+1))
            return min(temp)

        #raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        '''
        Actually, part2 structure is similiar to part1. I just add puning condition.
        For main part, it will bring the best(max) value as alpha to function.

        For min function, if there is one move that make value smaller than alpha,
        we will not consider other moves, just return. Furthermore, min function will bring 
        the min value as beta to let max function puning

        Fro max function, if there is one move that make value bigger than beta,
        we will not consider other moves, just return.

        Finally, the main will record the move that has biggest temp and return the move.
        '''

        a = float('-inf')
        b = float('inf')
        moves=None
        legalMoves = gameState.getLegalActions()
        for action in legalMoves:
            childGameState = gameState.getNextState(0,action)
            temp=self.Min_Value(childGameState,1,0,a,b)
            if(a<temp):
                a=temp
                moves=action
        return moves

    def Max_Value (self, gameState, d, alpha, beta):
        if gameState.isLose() or gameState.isWin() or d == self.depth:
            return self.evaluationFunction(gameState)
        
        maxi=float('-inf')
        pacmoves=gameState.getLegalActions(0)
        for action in pacmoves :
            gameState1=gameState.getNextState(0,action)
            temp=self.Min_Value(gameState1,1,d,alpha, beta)
            maxi=max(maxi,temp)
            if (maxi>beta):
                return maxi
            alpha = max(alpha,maxi)
        return maxi


    def Min_Value (self, gameState, i, d, alpha, beta):

        if gameState.isLose() or gameState.isWin(): 
            return self.evaluationFunction(gameState)

        minii=float('inf')
        if (i < gameState.getNumAgents() - 1):
            
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                temp=self.Min_Value(gameState1,i+1,d,alpha, beta)
                minii=min(temp,minii)
                if minii < alpha:
                    return minii
                beta = min(beta,minii)
    
        else:  
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                temp=self.Max_Value(gameState1,d+1,alpha, beta)
                minii=min(temp,minii)
                if minii < alpha:
                    return minii
                beta = min(beta,minii)
        
        return minii

        #raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        '''
        Actually, part3 is similiar to part1, even easilier.
        
        For main part, no change

        For min function, we don't need to return min value anymore.
        instead, we return expected value.
        ex: return (exp/len(ghostmoves))

        For max function, no change
        '''
        legalMoves = gameState.getLegalActions()
        temp=[]
        for action in legalMoves:
            childGameState = gameState.getNextState(0,action)
            temp.append(self.Min_Value(childGameState,1,0))
        maxscore=max(temp)
        bestIndices = [index for index in range(len(temp)) if temp[index] == maxscore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    def Max_Value (self, gameState, d):

        if gameState.isLose() or gameState.isWin() or d == self.depth:
            return self.evaluationFunction(gameState)
        
        temp=[]
        pacmoves=gameState.getLegalActions(0)
        for action in pacmoves :
            gameState1=gameState.getNextState(0,action)
            temp.append(self.Min_Value(gameState1,1, d))
        return max(temp)


    def Min_Value (self, gameState, i, d):

        if gameState.isLose() or gameState.isWin(): 
            return self.evaluationFunction(gameState)

        if (i < gameState.getNumAgents() - 1):
            exp=0
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                exp=exp+self.Min_Value(gameState1,i+1,d)
            return (exp/len(ghostmoves))

        else:  
            exp=0
            ghostmoves=gameState.getLegalActions(i)
            for action in ghostmoves :
                gameState1=gameState.getNextState(i,action)
                exp=exp+self.Max_Value(gameState1, d+1)
            return (exp/len(ghostmoves))

        #raise NotImplementedError("To be implemented")
        # End your code (Part 3)
        

def betterEvaluationFunction(current):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """

    # Begin your code (Part 4)
    '''
    My code is easy, it can be seen as three parts.

    First, cfd is closetest food. if the move can eat food cfd will=0
    and score will not minus, otherwise it will move forward to the closest food
    somewhat like greedy.

    Second, the same method to capsule 

    Third, this is in order to let pacman to be close to ghost, when ghost is scared.
    And the distance will keep in a value, which make sure pacman can chase ghost before scare ends

    the coefficient of every method are setted after several tries
    '''
    pacman    = current.getPacmanPosition()
    ghosts    = current.getGhostStates()
    score     = current.getScore()
    food_list = (current.getFood()).asList()
    capsule_list = current.getCapsules()

    cfd=-1
    for food in food_list:
        if (cfd<0 or manhattanDistance(pacman,food)<cfd):
            cfd=manhattanDistance(pacman,food)
    if(cfd<0):
        score+=0
    else:
        score+=-0.25*cfd

    ccd=-1
    for capsule in capsule_list:
        if (ccd<0 or manhattanDistance(pacman,capsule)<ccd):
            ccd=manhattanDistance(pacman,capsule)
 
    if(ccd<0):
        score+=0
    else:
        score+=-1*ccd
    
    
    for ghost in ghosts:
        if ghost.scaredTimer > 0 and  manhattanDistance(ghost.getPosition(), pacman)<= ghost.scaredTimer: 
            score += 200
        elif pacman == ghost.getPosition(): 
            score -= 500
    
    return score
    
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
