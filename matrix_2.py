class matrix:

    def __init__(self, matrix,row,col):
        self.m=matrix
        self.row=row
        self.col=col  
        
    def __repr__(self):
        a=""
        for x in range(0,self.row):
            for y in range(0,self.col):
                a+=str(self.m[x][y])+"  "
            a+="\n"
        return a

    def __add__(self,other):
        if((self.row==other.row)and(self.col==other.col)):
            s=[]
            for i in range(self.row):
                s.append([])
                for j in range(self.col):
                    s[i].append(self.m[i][j]+other.m[i][j])      
            return s
        else:
            raise ValueError('Dimensions of the matices are different')

    def __sub__(self,other):
        if((self.row==other.row)and(self.col==other.col)):
            s=[]
            for i in range(self.row):
                s.append([])
                for j in range(self.col):
                    s[i].append(self.m[i][j]-other.m[i][j])      
            return s
        else:
            raise ValueError('Dimensions of the matices are different')

    def __mul__(self,other):
        if(self.col==other.row):
            s=[]
            for i in range(self.row):
                s.append([])
                for j in range(other.col):
                    p=0
                    for t in range(other.row):
                        p+=(self.m[i][t]*other.m[t][j])
                    s[i].append(p)     
            return s
        else:
            raise ValueError('Dimensions of matrices are not appropriate')

    def exponent(self, n):
        if(self.row==self.col):
            c=self.m
            for x1 in range(0,n-1):
                c1=[]
                for x in range(0, self.row):
                    d=[]
                    for y in range(0, len(c)):
                        e=0
                        for z in range(0, self.col):
                            e+=self.m[x][z]*c[z][y]
                        d.append(e)
                    c1.append(d)
                c=c1
            a=matrix(c,self.row,self.row)
            return a
        else:
            raise ValueError('Not a square matrix')

    def determinant(self):
        if(self.row==self.col):
            x=0
            a=self.m
            if len(a)==1:
                return a[0][0]
            else:
                for d in range(0,len(a)):   
                    if(d==0):
                        c=[]
                        for y in range(1,len(a)):
                            c.append(a[y][1:])
                        c1=matrix(c,self.row-1,self.col-1)
                        x+=((-1)**d)*a[0][d]*c1.determinant()
                    elif(d==len(a)-1):
                        c=[]
                        for y in range(1,len(a)):
                            c.append(a[y][0:len(a)-1])
                        c1=matrix(c,self.row-1,self.col-1)
                        x+=((-1)**d)*a[0][d]*c1.determinant()
                    else:
                        c=[]
                        for y in range(1,len(a)):
                            c.append(a[y][0:d]+a[y][d+1:])
                        c1=matrix(c,self.row-1,self.col-1)
                        x+=((-1)**d)*a[0][d]*c1.determinant()             
            return x  
        else:
            raise ValueError('Not a square matrix')

import unittest

class testing(unittest.TestCase):

    # 10 tests

    def setUp(self):
        self.a=matrix([[1,2,3],[4,5,6]],2,3)
        self.b=matrix([[2,3,4],[5,6,7]],2,3)
        self.c=matrix([[1,2],[3,4],[5,6]],3,2)
        self.d=matrix([[1,4,2,3],[0,1,4,4],[-1,0,1,0],[2,0,4,1]],4,4)

    def test_sumfunc_1(self):
        #act
        result=self.a+self.b
        #assert
        self.assertEqual(result,[[3, 5, 7], [9, 11, 13]])

    def test_sumfunc_2(self):
        with self.assertRaises(ValueError):
            self.a+self.c

    def test_subfunc_3(self):
        result=self.a-self.b
        self.assertEqual(result,[[-1, -1, -1], [-1, -1, -1]])

    def test_subfunc_4(self):
        with self.assertRaises(ValueError):
            self.a-self.c

    def test_mulfunc_5(self):
        result=self.a*self.c
        self.assertEqual(result,[[22, 28], [49, 64]])
    
    def test_mulfunc_6(self):
        with self.assertRaises(ValueError):
            self.a*self.b

    def test_det_7(self):
        result=self.d.determinant()
        self.assertEqual(result,65)

    def test_det_8(self):
        with self.assertRaises(ValueError):
            self.c.determinant()

    def test_exp_9(self):
        result=self.d.exponent(3)
        result1=matrix([[17,28,162,69],
                                [-4,17,68,24], 
                                [-7,-12,-33,-25],
                                [2,8,72,39]],4,4)
        self.assertEqual(result.__repr__(),result1.__repr__())

    def test_exp_10(self):
        with self.assertRaises(ValueError):
            self.c.exponent(3)


if __name__=="__main__":
    unittest.main()