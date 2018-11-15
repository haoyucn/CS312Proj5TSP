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