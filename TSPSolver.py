#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools



class TSPSolver:
    def __init__( self, gui_view ):
        self._scenario = None

    def setupWithScenario( self, scenario ):
        self._scenario = scenario


    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
    def defaultRandomTour( self, time_allowance=60.0 ):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
            perm = np.random.permutation( ncities )
            route = []
            # Now build the route using the random permutation
            for i in range( ncities ):
                route.append( cities[ perm[i] ] )
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
				# Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

    def greedy( self,time_allowance=60.0 ):
        pass

    ''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''


    def branchAndBound( self, time_allowance=60.0 ):
        originalTable = []
        bestPath = []
        bssf = math.inf
		# make the original 2 by 2 matrix
        for i in range(len(self._scenario.getCities())):
            originalRow = []
            for j in range(len(self._scenario.getCities())):
                originalRow.append(self._scenario.getCities()[i].costTo(self._scenario.getCities()[j]))
            originalTable.append(originalRow)

        for i in range(len(self._scenario.getCities())):
            print(originalTable[i])
        print('\n\n\n')
        lowerBound = self.reduction(originalTable, 0)
        for i in range(len(self._scenario.getCities())):
            print(originalTable[i])
        print(lowerBound)

        mylist = []
        
        # make childrens first group
        
        cities = self._scenario.getCities();
        citiesNum = len(cities)
        for i in range(citiesNum):
            newList = []
            for a in range(0,i):
                newList.append(a)

            if (i + 1) < citiesNum:
                for b in range((i+1),citiesNum):
                    newList.append(b)

            leafNode = TreeTuples(originalTable,[i],newList,lowerBound)
            entry = [lowerBound, leafNode]
            heapq.heappush(mylist,entry)

        #after get the first and last one
        while len(mylist) >= 0:
            parentNode = heapq.heappop(mylist)
            if parentNode.getMinDist < bssf:
                childNodes = parentNode.makeNextGeneration()
                for i in range(len(childNodes)):
                    # if this generation is done, no need to push
                    if childNodes[i].isDone() :
                        childNodes[i].finalization();
                        if (bssf > childNodes[i].getMinDist):
                            bestPath = childNodes[i].getPath()
                    else:
                        # push this generation on the queue till finish
                        entry = [childNodes[i].getMinDist, childNodes[i]]
                        heapq.heappush(mylist,entry)
        
        # by this point it should have all the generation needed
        pass


    ''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
    def fancy( self,time_allowance=60.0 ):
        pass
		


    def reduction(self,table,lowerBound):
        tableLength = len(table)
        newLowerBound = lowerBound
        # row reduction
        for i in range(tableLength):
            minH = min(table[i])
            if minH != 0 and minH != math.inf:
                for j in range(tableLength):
                    table[i][j] = table[i][j] - minH
                newLowerBound += minH

        # col reduction
        for j in range(tableLength):
            minV = table[0][j]
            for i in range(1,tableLength):
                if minV > table[i][j]:
                    minV = table[i][j]
            if minV != 0 and minV != math.inf:
                for i in range(tableLength):
                    table[i][j] = table[i][j] - minV
                newLowerBound += minV
        return newLowerBound

class TreeTuples:
    def __init__(self , distM, path, unsused_cities, minD):
        self.distMatrix  = distM
        self.path = path
        self.minDist = minD
        self.unvisitedCity = unsused_cities
        # self.cities = allCities
        
    
    def getPath(self):
        return self.path

    def getDistMatrix(self):
        return self.distMatrix

    def getMinDist(self):
        return self.minDist

    def isDone(self):
        if len(self.unvisitedCity) == 0:
            return True
        else:
            return False

    def makeNextGeneration (self):
        firstGenArray  = []
        startingIndex = self.path[-1]
        cityNum = len(self.path) + len(self.unvisitedCity)
        for otherIndex in self.unvisitedCity:
            targetDist = self.distMatrix[startingIndex][otherIndex]
            if targetDist != math.inf:
                resultTuple = self.matrix_reduction(startingIndex,otherIndex);
                newMinDist = resultTuple[0]
                newMatrix = resultTuple[1]
                # after find the first few things
                # remove teh destIndex from unvisited
                newUnused = []
                for i in self.unvisitedCity:
                    if i != otherIndex:
                        newUnused.append(i)
                newPath = self.path.copy().append(otherIndex)
                newNode = TreeTuples(newMatrix,newPath, newUnused, newMinDist)
                firstGenArray.append(newNode)
        return firstGenArray
                
    def matrix_reduction(self, startingIndex, targetIndex):
        newMinDist = self.minDist + self.distMatrix[startingIndex][targetIndex]
        newMatrix = []
        matrixLen = len(self.distMatrix)
        for i in range(matrixLen):
            newRow = self.distMatrix.copy();
            newMatrix.append(newRow)

        # after made a copy of new matrix
        # change the col of destination to inf
        for i in range(matrixLen):
            newMatrix[i][targetIndex] = math.inf
        
        # if this is the second generation
        # now change the [targetIndex][startingIndex] to inf
        if len(self.path) == 1:
            newMatrix[targetIndex][startingIndex] = math.inf
        else:
            # if this is not the second generation
            # change the row of startingIndex to Inf
            for j in range(matrixLen):
                newMatrix[startingIndex][j] = math.inf
            
        # reduce
        for i in range(matrixLen):
            minH = min(newMatrix[i])
            if minH != 0 and minH != math.inf:
                for j in range(matrixLen):
                    newMatrix[i][j] = newMatrix[i][j] - minH
                newMinDist += minH
        
        for j in range(matrixLen):
            minV = newMatrix[0][j]
            for i in range(1,matrixLen):
                if minV > newMatrix[i][j]:
                    minV = newMatrix[i][j]
            if minV != 0 and minV != math.inf:
                for i in range(matrixLen):
                    newMatrix[i][j] = newMatrix[i][j] - minV
                newMinDist += minV

        return [newMinDist,newMatrix]

    # added the way to go back the the beginning of the path
    def finalization(self):
        beginningIndex = self.path[0]
        endingIndex = self.path[-1]
        self.minDist = self.minDist + self.distMatrix[endingIndex][beginningIndex] 
        self.distMatrix[endingIndex][beginningIndex] = math.inf
        self.path.append(beginningIndex)
    