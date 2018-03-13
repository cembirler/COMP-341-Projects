# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    """
    source=problem.getStartState()
    print source

    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
   # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    "*** YOUR CODE HERE ***"
    stack=util.Stack()
    visited=[]
    stack2=util.Stack()
    stack.push(source)

    while not stack.isEmpty():
        if(stack2.isEmpty()):
            path='Start'
        else:
            path = stack2.pop()
        current=stack.pop()

        #print current
        #print path
        if not current in visited:

            if(problem.isGoalState(current)):
                return path.split(',')[1:]

            visited.append(current)

            for v in problem.getSuccessors(current):
                stack.push(v[0])
                stack2.push(path+','+v[1])









def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    source = problem.getStartState()
    queue=util.Queue()
    visited=[]
    queue2=util.Queue()
    queue.push(source)

    while not queue.isEmpty():
        if(queue2.isEmpty()):
            path='Start'
        else:
            path = queue2.pop()
        current=queue.pop()

        #print current
        #print path
        if not current in visited:

            if(problem.isGoalState(current)):
                return path.split(',')[1:]

            visited.append(current)

            for v in problem.getSuccessors(current):
                queue.push(v[0])
                queue2.push(path+','+v[1])

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    source = problem.getStartState()
    pqueue=util.PriorityQueue()
    visited=[]
    pqueue2=util.PriorityQueue()
    pqueue.push(source,0)
    cost_matrix={}
    while not pqueue.isEmpty():
        if(pqueue2.isEmpty()):
            path='Start'
        else:
            path = pqueue2.pop()
        current=pqueue.pop()

        #print current
        #print path
        if not current in visited:
            #print current
            if(problem.isGoalState(current)):
                return path.split(',')[1:]

            visited.append(current)

            for v in sorted(problem.getSuccessors(current)):
                if (current in cost_matrix):
                    cost_matrix[v[0]]=v[2]+cost_matrix[current]
                else: #sadece ilk giris nodeun parenti olmadigi icin lazim
                    cost_matrix[v[0]] = v[2]
                pqueue.push(v[0],cost_matrix[v[0]])
                pqueue2.push(path+','+v[1],cost_matrix[v[0]])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    source = problem.getStartState()
    pqueue=util.PriorityQueue()
    visited=[]
    pqueue2=util.PriorityQueue()
    pqueue.push(source,0)
    cost_matrix={}
    while not pqueue.isEmpty():
        if(pqueue2.isEmpty()):
            path='Start'
        else:
            path = pqueue2.pop()
        current=pqueue.pop()

        #print current
        #print path
        if not current in visited:
            # print current
            # print type(current)
            # if(type(current) is list):
            #     current=str(current)
            #     print current
            if(problem.isGoalState(current)):
                return path.split(',')[1:]

            visited.append(current)

            for v in sorted(problem.getSuccessors(current)):

                if (current in cost_matrix):
                    cost_matrix[v[0]]=v[2]+cost_matrix[current]
                else: #sadece ilk giris nodeun parenti olmadigi icin lazim
                    cost_matrix[v[0]] = v[2]
                pqueue.push(v[0],cost_matrix[v[0]]+heuristic(v[0],problem))
                pqueue2.push(path+','+v[1],cost_matrix[v[0]]+heuristic(v[0],problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
