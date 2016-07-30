#-----------------------------------
# LOGISTIC REGRESSION LEARNING 
#-----------------------------------
import numpy as np
import math
from scipy.optimize import fmin_bfgs
import sklearn 
# Learn class. 
# Description: This class has been designed to work with images 
# of (n1)x(n2) pixels. 

class Learn_logistic_Regression:
	def __init__(self, debug, iterations, m, n1, n2, k, alpha, train_set, cross_validation_set, test_set, data_set_divisions):
		# General variables
		self.debug = debug
		self.active_debug = False
		if (self.debug == "debug"):
			self.activate_debug = True
		elif (self.debug == "don't debug"):
			self.activate_debug = False
		# Model specifications
		self.m = m
		self.n1 = n1
		self.n2 = n2
		self.n = (n1 * n2) + 1
		self.k = k
		self.train_set = train_set
		self.cross_validation_set = cross_validation_set
		self.test_set = test_set
		self.data_set_divisions = data_set_divisions
		# Choosing the number of try outs for the model 
		self.number_of_models = 5
		# Stochastic gradient descent
		self.iterations = iterations
		self.alpha = alpha
		self.theta = np.random.rand(self.n + 1)
		self.theta /= max(self.theta)
	
	#--------------------------------
	# CHOOSING THE ORDER OF THE MODEL 
	#--------------------------------
	def choosing_d(self):
		print "Choosing the order of the model"
		
		# Init Local Variable with some random number that will hold the new model 
		# new_train_set = np.random.rand(2000, 2000) 
		# new_theta = np.random.rand(2000,2000)
		# Choosing the order of the model s
		for i in range(self.number_of_models):
			# ---------------------
			# Select degree of model
			# ---------------------
			# Remember that the training model already comes with the bias term 
			if (i == 0):
				# Multiplication of X1*X2, X3*X4, ... 
				# This will add the half of the model's size
				print "Running the zero model X1*X2, X3*X4"
				#print self.data_set_divisions[0]
				new_train_set = np.random.rand(self.data_set_divisions[0], (self.n1*self.n2)+((self.n1*self.n2)/2))
				new_theta = np.random.rand(1, (self.n1*self.n2)+((self.n1*self.n2)/2))
				#print len(new_train_set[0,:]), len(new_train_set[:,0])
				#print len(new_theta[0,:]), len(new_theta[:,0])
				# Remember not to add the bias term
				# Remeber that the label is at the last column 
				new_train_set[:, 1:self.n1*self.n2] = self.train_set[:, 1:self.n1*self.n2]
				new_train_set[:,0] = self.train_set[:,0]
				#print new_train_set[:,0]
				# The following piece of code adds the multiplication of each parameter with its next one
				col = 0;  
				for j in range((self.n1*self.n2)/2):
					new_train_set[:, (self.n1*self.n2)+j] = self.train_set[:,col]*self.train_set[:,col+1]
					col += 2

			elif (i == 1):
				# Multiplication of X1*X2, X3*X4, ... and square of each X1^2, X2^2, ... 
				# This will add the half of the model's size + the size of the total model
				print "Running the first model X1*X2, X3*X4 and X1^2, X2^2, ..."
				new_train_set = np.random.rand(self.data_set_divisions[0], self.n1*self.n2+((self.n1*self.n2)/2+(self.n1*self.n2)))
				new_theta = np.random.rand(1, self.n1*self.n2+((self.n1*self.n2)/2+(self.n1*self.n2)))
				# Remember not to add the bias term
				new_train_set[:, 1:self.n1*self.n2] = self.train_set[:, 1:self.n1*self.n2]
				# The following piece of code adds the multiplication of each parameter with its next one
				col = 0;  
				for j in range((self.n1*self.n2)/2):
					new_train_set[:, (self.n1*self.n2)+j] = self.train_set[:,col]*self.train_set[:,col+1]
					col += 2
				# The following piece of code squares all the parameters
				for j in range(self.n1*self.n2):
					new_train_set[:, (self.n1*self.n2)+((self.n1*self.n2)/2)+j] = self.train_set[:,j]**2
	
			elif (i == 2):
				# Multiplication of X1*X2*X3*X4, X2*X3*X4*X5,  
				# This will add a quarter of the model's size 
				print "Running the second model X1*X2*X3*X4, X2*X3*X4*X5"
				new_train_set = np.random.rand(self.data_set_divisions[0], self.n1*self.n2+((self.n1*self.n2)/4))
				new_theta = np.random.rand(1, self.n1*self.n2+((self.n1*self.n2)/4))
				# Remember not to add the bias term
				new_train_set[:, 1:self.n1*self.n2] = self.train_set[:, 1:self.n1*self.n2]
				# The following piece of code adds the multiplication of each parameter with its next three 
				col = 0;  
				for j in range((self.n1*self.n2)/4):
					new_train_set[:, (self.n1*self.n2)+j] = self.train_set[:,col]*self.train_set[:,col+1]*self.train_set[:,col+2]*self.train_set[:,col+3]
					col += 4

			elif (i == 3):
				# Multiplication of X1*X2*X3*X4, X2*X3*X4*X5, ... and cube of each
				# This will add a quarter of the model's size + the size of the model itself
				print "Running the third model X1*X2*X3*X4, X2*X3*X4*X5 and X1^3, X2^3"
				new_train_set = np.random.rand(self.data_set_divisions[0], (2*self.n1*self.n2)+((self.n1*self.n2)/4))#+(self.n1*self.n2))
				new_theta = np.random.rand(1, self.n1*self.n2+((self.n1*self.n2)/4)+(self.n1*self.n2))
				# The following piece of code adds the multiplication of each parameter with its next three 
				col = 0;  
				for j in range((self.n1*self.n2)/4):
					new_train_set[:, (self.n1*self.n2)+j] = self.train_set[:,col]*self.train_set[:,col+1]*self.train_set[:,col+2]*self.train_set[:,col+3]
					col += 4
				# The following piece of code cubes all the parameters
				#for j in range(self.n1*self.n2):
				#	new_train_set[:, (self.n1*self.n2)+((self.n1*self.n2)/4)+j] = self.train_set[:,j]**3
						
			elif (i == 4):
				# Multiplication of X1*X2*X3*X4, X2*X3*X4*X5, ... and cube of each ... and square of each
				# This will add a quarter of the model's size + the size of the model itself
				print "Running the fourth model X1*X2*X3*X4, X2*X3*X4*X5 and X1^3, X2^3 and X1^2, X2^2"
				new_train_set = np.random.rand(self.data_set_divisions[0], self.n1*self.n2+((self.n1*self.n2)/4)+(self.n1*self.n2)+(self.n1*self.n2))
				new_theta = np.random.rand(1, self.n1*self.n2+((self.n1*self.n2)/4)+(self.n1*self.n2)+(self.n1*self.n2))
				# The following piece of code adds the multiplication of each parameter with its next three 
				col = 0;  
				for j in range((self.n1*self.n2)/4):
					new_train_set[:, (self.n1*self.n2)+j] = self.train_set[:,col]*self.train_set[:,col+1]*self.train_set[:,col+2]*self.train_set[:,col+3]
					col += 4
				# The following piece of code cubes all the parameters
				for j in range(self.n1*self.n2):
					new_train_set[:, (self.n1*self.n2)+((self.n1*self.n2)/4)+j] = self.train_set[:,j]**3
				# The following piece of code squares all the parameters
				for j in range(self.n1*self.n2):
					new_train_set[:, (self.n1*self.n2)+((self.n1*self.n2)/4)+(self.n1*self.n2)+j] = self.train_set[:,j]**2
			
			print "Finished computing the new " + str(i) + " model"
			
			#----------------
			# LOCAL TRAINING
			#----------------
			# Remember:
			# m is the total number of examples in the training set 
			# n is the number of features 
			# m, n = X.shape

			m = self.m
			n = self.n

			# y.shape = (m, 1)

			# Initialize theta parameters, this is new_theta
			initial_theta = new_theta

			# Set regularization parameter lambda to 1
			l = 0

			# Compute and display initial cost and gradient for regularized logistic
			# regression
			#print "Aruguments for the cost"
			#print len(initial_theta[0,:]), len(initial_theta[:,0])
			#print len(new_train_set[0,:]), len(new_train_set[:,0])
			#print len(self.train_set[0,:]), len(self.train_set[:,0])

			cost, grad = self.cost_function(initial_theta.transpose(), new_train_set, np.ones((self.data_set_divisions[0],1)))#self.train_set[:,len(self.train_set)-1])

			#print fmin_bfgs(decorated_cost, initial_theta, maxfun=self.iterations)

		#print self.sigmoid(0)

	'''
	EXTREMELY IMPORTANT 
	1. Theta must be passed as a matrix of ((n+1) x 1) -> n+1 rows and 1 column 
	2. X must be passed as a matrix of (m x n)
	3. y must be passed as a matrix of (m x 1)
	'''
	def cost_function(self, theta, X, y):
		#Compute the cost and partial derivatives as grads
		print "Theta -> ", "rows: ", len(theta[:,0]), "cols: ", len(theta[0,:])
		print "X -> ", "rows: ", len(X[:,0]), "cols: ", len(X[0,:]) 
		print "y -> ", "rows: ", len(y[:,0]), "cols: ", len(y[0,:]), "\n" 
		
		J = 0
		grad = np.zeros(len(theta))

		J = (1.0 / self.m) * sum ( sum ( -1.0*y.transpose() * np.asarray([math.log(result) for result in self.sigmoid(X.dot(theta))]) - (1-y.transpose())*np.asarray([math.log(res) for res in self.sigmoid(X.dot(theta))]) ) )
		
		grad = (1.0 / self.m) * X.transpose().dot( self.sigmoid( X.dot( theta ) ) - y ) #second solution

		return J, grad
	
	def sigmoid(self, p):
		return 1 / (1 + (math.e ** (-1.0*p) ))

	