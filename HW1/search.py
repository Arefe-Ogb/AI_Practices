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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    #create fringe as a stack
    fringe = util.Stack()
    
    # Create visitedList as an array
    # Checked nodes are added to visitedList
    visitedList = []

    # push starting node to the fringe
    fringe.push((problem.getStartState(), [], 0))
    # pop the node from the fringe
    (state, toDirection, toCost) = fringe.pop()
    # checked node is added to visitedList
    visitedList.append(state)
        # while the goal point isn't found the children are expanded
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for son in successors:
            # if the child isn't visited push it to the fringe
            if (not son[0] in visitedList) or (problem.isGoalState(son[0])): 
                fringe.push((son[0], toDirection + [son[1]], toCost + son[2]))
                # add child node to visitedList
                visitedList.append(son[0])
        (state, toDirection, toCost) = fringe.pop()

    return toDirection

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from game import Directions

    # Create fringe as a queue
    fringe = util.Queue()
    visitedList = []

    #push the starting node to the queue
    fringe.push((problem.getStartState(),[],0))
    #pop the node
    (state,toDirection,toCost) = fringe.pop()
    #add the node to visitedList
    visitedList.append(state)

    # while the goal node isn't found the children are expanded
    while not problem.isGoalState(state): 
        successors = problem.getSuccessors(state) 
        for son in successors:
            #if the child isn't visited, push to the queue
            if not son[0] in visitedList: 
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                # add the node to visitedList
                visitedList.append(son[0]) 
        (state,toDirection,toCost) = fringe.pop()

    return toDirection

    util.raiseNotDefined()

def uniformCostSearch(problem):
    
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from game import Directions
    #create fringe as a priority Queue
    fringe = util.PriorityQueue() 
    visitedList = []

    #add the starting node into queue
    fringe.push((problem.getStartState(),[],0),0) # push starting node... The priority number is 0
    #remove the node
    (state,toDirection,toCost) = fringe.pop()
    #add the node to visited list
    visitedList.append((state,toCost))

    while not problem.isGoalState(state): #while the goal node isn't found
        successors = problem.getSuccessors(state) #get the point's children (succesors)
        for son in successors: #for each child in children nodes
            visitedExist = False #if it hasn't been visited before
            total_cost = toCost + son[2] #the total cost is "cost p until now" + "the cost of the child node"
            for (visitedState,visitedToCost) in visitedList:
                # we add the node only if the successor has not been visited, or has been visited but now with a lower cost than the previous one
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True # node is considered visited
                    break

            if not visitedExist:        
                # push the node with priority number of its total cost
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2]) 
                # add this node to visited list
                visitedList.append((son[0],toCost + son[2])) 

        # remove the previous node from fringe
        (state,toDirection,toCost) = fringe.pop()

    #return the direction to the goal
    return toDirection
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    #create fringe as a priority Queue
    fringe = util.PriorityQueue() 
    visitedList = []

    #push the starting node into queue
    fringe.push((problem.getStartState(),[],0),0 + heuristic(problem.getStartState(),problem)) # push starting point with priority num of 0
    #remove the node
    (state,toDirection,toCost) = fringe.pop()
    #add the node to visited list
    visitedList.append((state,toCost + heuristic(problem.getStartState(),problem)))

    while not problem.isGoalState(state): #while the goal point isn't found
        successors = problem.getSuccessors(state) #get the point's children (succesors)
        for son in successors: #for each child in children nodes
            visitedExist = False #if it hasn't been visited before
            total_cost = toCost + son[2] #the total cost is "cost up until now" + "the cost of the child node"
            for (visitedState,visitedToCost) in visitedList:
                # if the successor has not been visited, or has a lower cost than the previous one
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True #node is considered visited
                    break

            if not visitedExist:        
                # push the point with priority number of its total cost
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2] + heuristic(son[0],problem)) 
                visitedList.append((son[0],toCost + son[2])) # add this node to visited list

        # remove the previous node from fringe         
        (state,toDirection,toCost) = fringe.pop()
    #return the direction to the goal
    return toDirection
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
