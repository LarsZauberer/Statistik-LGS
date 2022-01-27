class Problem:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.x = [None for _ in self.b]
    
    def toTriangle(self):
        for oriRowIndex, oriRow in enumerate(self.A):
            for rowIndex, row in enumerate(self.A):
                if rowIndex <= oriRowIndex:
                    continue
                # Alle Stellen zu 0 machen.
                for numIndex, num in enumerate(row):
                    if numIndex <= oriRowIndex:
                        factor = num / oriRow[oriRowIndex]
                    self.A[rowIndex][numIndex] = num - (factor * oriRow[numIndex])
                # Resultate anpassen
                self.b[rowIndex] = self.b[rowIndex] - (factor * self.b[oriRowIndex])
    
    def solveBackwards(self):
        rowIndex = -1
        while rowIndex >= -len(self.A):
            temp = rowIndex + 1
            summ = 0
            while temp < 0:
                summ += self.A[rowIndex][temp] * self.x[temp]
                temp += 1
            self.x[rowIndex] = (self.b[rowIndex] - summ) / self.A[rowIndex][rowIndex]
            
            # Go one row up
            rowIndex -= 1
    
    def solve(self):
        self.toTriangle()
        self.solveBackwards()
        return self.x
                

if __name__ == '__main__':
    p = Problem([[1, 2], [3, 4]], [5, 6])
    p.toTriangle()
    print(p.A)
    print(p.b)
    p.solveBackwards()
    print(p.x)
    
    p = Problem([[2, 1, 0], [0, 3, 2], [2, 4, 10]], [21, 15, 12])
    p.toTriangle()
    print(p.A)
    print(p.b)
    p.solveBackwards()
    print(p.x)
                    