**Week 1 : Software Requirements and Installation**

We are going to use the programming and modelling tools for this semester.

* Programming : Any python IDE / interpreter

**Programming**

* ***Note: Install IDLE first before proceed to install the IDE. (python.org>download)***

**Download and Install PyCharm**

1. Go to the JetBrains PyCharm download page. Choose the Community Edition (free) . URL : [Download PyCharm: The Python IDE for data science and web development by JetBrains](https://www.jetbrains.com/pycharm/download/?section=windows)
2. Installation
   * Windows, execute the exe file. Follow the installation wizard.
   * macOS: Open the dmg file. Drag and drop PyCharm into the Applications folder.

**Download and Install Visual Studio Code (VS Code).**

* 1. Go to the Visual Studio Code download page ([Download Visual Studio Code - Mac, Linux, Windows](https://code.visualstudio.com/download)). Download the installer for your operating system. (mac/ windows)
  2. Installation
* Windows: execute the exe file.
* macOS: Open the dmg file. Drag and drop Visual Studio Code into the Applications folder.

1. Configure Visual Studio Code for Python
2. Launch Visual Studio Code.
3. Open the Extensions view by clicking the Extensions icon in the Activity Bar on the side of the window.
4. Search for the Python extension and click Install. Choose any python extension. Example : Python by Microsoft and Jupyter book
5. Open the Command Palette and type Python: Select Interpreter. Choose any Python interpreter. Or you can just click play after you code something, the command palette will open.

**Recap python knowledge.**

* 1. Create a while loop to prompt user for input tills -1 is entered.
  2. Create a function to receive 2 values; a list and a number from caller. The function will multiple the value of the list with the given number and return the updated list to the caller.
  3. Create a 2D matrix using nested lists in Python.

matrix = [

[1, 2, 3],

[4, 5, 6],

[7, 8, 9]

]

* 1. Printing the matrix

for row in matrix:

print(row)

3. Modify elements by assigning new values to specific indices:

matrix[0][1] = 10

print("updated matrix:")

for row in matrix:

print(row)

1. Apply function. Encapsulate the matrix in function.

def print\_matrix(matrix):

for row in matrix:

print(row)

print\_matrix(matrix)

5. Function to Add Two 2D matrix

def add\_matrices(matrix1, matrix2):

result = []

for i in range(len(matrix1)):

row = []

for j in range(len(matrix1[0])):

row.append(matrix1[i][j] + matrix2[i][j])

result.append(row)

return result

matrix2 = [

[9, 8, 7],

[6, 5, 4],

[3, 2, 1]

]

sum\_matrix = add\_matrices(matrix, matrix2)

print("Sum of matrices:")

print\_matrix(sum\_matrix)

**Guide to install Python libraries using pip in both PyCharm and Visual Studio Code.**

**PyCharm**

1. Launch PyCharm and open the project.
2. Method 1
   1. Go to View > Tool Windows > Python Packages.
   2. Search for the desired package. Type the name of the package you want to install in the search bar. Select the package from the search results.
   3. Click the Install button.
3. Method 2
   1. Open the terminal by going to View > Tool Windows > Terminal.
   2. Use the pip install command:

pip install package\_name

**Visual Studio Code**

1. Launch Visual Studio Code and open your project folder.
2. Open the terminal by going to View > Terminal
3. Use the pip install command in the terminal:

pip install package\_name

**Example: Installing NumPy**

1. pip command: pip install numpy

2. Verifying Installation by typing these code in your python file and run.

import numpy as np

print(np.\_\_version\_\_) # check version

**Exercise**

You may find the list of packages available by python from PyPI [PyPI · Tpiphe Python Package Index](https://pypi.org/)

a) Install these packages.

• Pillow

• Opencv for python

• Pygame

• Numpy

• Matplotlib

**Implement matrix with numpy package.**

import numpy as np

matrix\_np = np.array([

[1, 2, 3],

[4, 5, 6],

[7, 8, 9]

])

print("NumPy Matrix:")

print(matrix\_np)

matrix2\_np = np.array([

[9, 8, 7],

[6, 5, 4],

[3, 2, 1]

])

sum\_matrix\_np = matrix\_np + matrix2\_np

print("Sum of NumPy matrices:")

print(sum\_matrix\_np)

product\_matrix\_np = np.dot(matrix\_np, matrix2\_np)

print("Product of NumPy matrices:")

print(product\_matrix\_np)

**Exercise**

Write python code using normal for loop, list comprehension and using numpy package for the following questions. Observed the techniques used, which is the easiest technique?

a) Given A and B, perform calculation for A-B

A −1 0

0 1

B -1 2

3 -2

b) Create a 3x3 matrix which comprise of the following values. Multiply the matrix with 10.

1 2 3

4 5 6

7 8 9
