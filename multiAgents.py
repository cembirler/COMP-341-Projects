# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        foods=currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()


        score = 0

        for food in foods:
            distance = util.manhattanDistance(food, newPos)
            if (distance == 0):
                score = score + 9
            else:
                score = score + 1.0 / distance


        for ghost in newGhostStates:
            distance = manhattanDistance(ghost.getPosition(), newPos)
            if (distance <= 1):
                if (ghost.scaredTimer == 0):
                    score=score-99999


        return score

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
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        bestScore,bestMove=self.maxFunction(gameState,self.depth)

        return bestMove

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"

        moves=gameState.getLegalActions()
        scores = [self.minFunction(gameState.generateSuccessor(self.index,move),1, depth) for move in moves]
        bestScore=max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,moves[chosenIndex]

    def minFunction(self,gameState,agent, depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"
        moves=gameState.getLegalActions(agent) #get legal actions.
        scores=[]
        if(agent!=gameState.getNumAgents()-1):
          scores =[self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth) for move in moves]
        else:
          scores =[self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1))[0] for move in moves]
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, moves[chosenIndex]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

        def minMaxHelper(gameState, deepness, agent, alpha, beta):
            if agent >= gameState.getNumAgents():
                agent = 0
                deepness += 1
            if (deepness == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agent == 0):
                return maxFinder(gameState, deepness, agent, alpha, beta)
            else:
                return minFinder(gameState, deepness, agent, alpha, beta)

        def maxFinder(gameState, deepness, agent, alpha, beta):
            output = ["meow", -float("inf")]
            pacActions = gameState.getLegalActions(agent)

            if not pacActions:
                return self.evaluationFunction(gameState)

            for action in pacActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1, alpha, beta)

                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue

                # real logic
                if testVal > output[1]:
                    output = [action, testVal]
                if testVal > beta:
                    return [action, testVal]
                alpha = max(alpha, testVal)
            return output

        def minFinder(gameState, deepness, agent, alpha, beta):
            output = ["meow", float("inf")]
            ghostActions = gameState.getLegalActions(agent)

            if not ghostActions:
                return self.evaluationFunction(gameState)

            for action in ghostActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1, alpha, beta)

                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue

                if testVal < output[1]:
                    output = [action, testVal]
                if testVal < alpha:
                    return [action, testVal]
                beta = min(beta, testVal)
            return output

        outputList = minMaxHelper(gameState, 0, 0, -float("inf"), float("inf"))
        return outputList[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getActionHelper(gameState, self.depth, 0)[1]

    def getActionHelper(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            eval_result = self.evaluationFunction(gameState)
            return (eval_result, '')
        else:
            if agentIndex == gameState.getNumAgents() - 1:
                depth -= 1
            if agentIndex == 0:
                maxAlpha = -99999999
            else:
                maxAlpha = 0
            maxAction = ''
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                result = self.getActionHelper(gameState.generateSuccessor(agentIndex, action), depth, nextAgentIndex)
                if agentIndex == 0:
                    if result[0] > maxAlpha:
                        maxAlpha = result[0]
                        maxAction = action
                else:
                    maxAlpha += 1.0/len(actions) * result[0]
                    maxAction = action
            return (maxAlpha, maxAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I DID SOMETHING! EXPLANATION IS ON THE REPORT!
    """
    "*** YOUR CODE HERE ***"

    currentScore = scoreEvaluationFunction(currentGameState)
    foods = currentGameState.getFood().asList()
    remainingFoodNumber = len(foods)
    pacman = currentGameState.getPacmanPosition()
    distanceToFoods=[]


    for food in foods:
        distance = util.manhattanDistance(pacman, food)
        distanceToFoods.append(distance)

    currentScore=currentScore-8*remainingFoodNumber
    for dis in distanceToFoods:
        currentScore=currentScore-1*dis

    return currentScore

# Abbreviation
better = betterEvaluationFunction

