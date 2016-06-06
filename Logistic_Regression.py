import sys, os
import scipy, sklearn
import math, fnmatch
import cv2
from __future__ import division
import numpy as np
from numpy import newaxis, r_, c_, mat, e
import math
import timeit, time
from scipy import optimize
import matplotlib.pyplot as plt
from numpy.linalg import *
from Learning import Learn_logistic_Regression

#------------------------
# CONFIGURABLE PARAMETERS
#------------------------
# The configuration is done at the init_variables() function. Modify the return variables 
# 1. rows and cols set the resizing factor
# 2. Database depends on the resizing factor because it holds the features. This datastructure stores an image per row
# 3. Do not modify the "b" constant as it is used to shape the database matrix. 
# 4. Set K to configure how many output classes you have
# 5. Alpha sets the learning rate, feel free to change it 
# 6. Iterations, change it to set the repetions of the learning algorithm  
# 7. Resize is configured by itself  

def init_variables(m, posfolder):
	''' Initialize the database. The +1 added at the columns represents the bias term
	 The order of the return function is as follows: database, constant b (serves to iterate at database)
	 , rows (set of features n1), cols (set of features n2), k (number of output classes), alpha (learning rate)
	 iterations (number of repetitions for the gradient descent), resize (do we need to resize?), images per negative folder
	 y vector of labels''' 
	I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + posfolder + 'image_0001.jpg', 1)
	rows, cols, channels = I.shape
	
	if ((rows > 30) & (cols > 25)):
		rows = 20
		cols = 20
		resize = True 
	elif ((rows <= 30) & (cols <= 25)):
		resize = False

	'''Initialize the size of the matrix that will contain the database.
	The number of rows represents the number of positive and negative images
	The number of columns represents the resizing factor and we add the bias term'''
	num_images_neg_database = 30
	num_folders_neg_database = 17
	database = np.random.rand(m+(num_images_neg_database*num_folders_neg_database), (rows*cols)+1)

	'''b is used to iterate through the database when dividing it'''
	b = 1

	'''Rows and cols are sent back as n1,n2 which form the total number of features n1*n2+1'''
	n1 = rows
	n2 = cols

	'''k represents the number of output classes. NOTE-> I AM NOT SUPPORTING THIS FUNCTIO YET'''
	k = 1

	'''alpha represents the learning rate'''
	alpha = 0.01

	'''iterations represents the number of times the converging iterations for the learning algorithm'''
	iterations = 400

	'''resize is a boolean variable that returns a feedback abouth whether a resize was required or not'''
	resize = resize

	return database, num_images_neg_database ,b, n1, n2, k, alpha, iterations, resize

def get_immediate_subdirectories(a_dir):
	''' Get all the subdirectories in path "a_dir" '''
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

if __name__ == "__main__":

	print "Starting program ..."
	
	cv2.namedWindow("test", 1)
	mn = 0; total_mn = 0; m =0;

	print "---------------------------------"
	print "INIT VARIABLES AND DATABASES"
	print "---------------------------------"

	''' To start the database we are going to retrieve all the folders in the current directory and store them in a list '''
	current_directory = "C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/" 
	print "Current Directory: ", current_directory
	directories = get_immediate_subdirectories(current_directory)

	print "--------------------"
    print "POSITIVE IMAGES"
	print "--------------------"
	''' The folder with the posivite samples is posfolder '''
	posfolder = 'Faces_easy/'
	dirpath = current_directory + posfolder
	'''Positive database size'''
	m = len(fnmatch.filter(os.listdir(dirpath), '*.jpg'))

	print "Current directory for positive database:", dirpath

	''' Init variables '''
	database, b, n1, n2, k, alpha, iterations, resize, img_per_neg_folder = init_variables(m, posfolder)
	yp = np.ones(m)
	
	print "Starting database ... "
	print "Reading positive samples ... "

	for i in range(m):
		i += 1
		if (i < 10):
			I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/'+ posfolder + "image_000" + str(i)+ ".jpg")
		elif ((i >= 10) & (i < 100)):
			I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/'+ posfolder + "image_00" + str(i)+".jpg")
		elif ((i >= 100) & (i < 1000)):
			I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/'+ posfolder + "image_0" + str(i)+".jpg")
		elif ((i >= 1000) & (i < 10000)):
			I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/'+ posfolder + "image_" + str(i)+".jpg")
		if (resize == True):
			I = cv2.resize(I, (n2, n1))
		elif (resize == False):
			pass

		# Check whether the image is in grayscale or color 
		#rows, cols, channels = I.shape 

		# Convert image to grayscale, color does not seem to help that mucn 
		I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
		# I[:,:,0] = I[:,:,0]*0.60 + I[:,:,1]*0.28 + I[:,:,2]*0.12
		cv2.imshow("test", I)
		k = cv2.waitKey(1) & 0xFF

		# Allocate all the rows of the image into one row of the database's matrix
		# Do not worry it works. Remember n1 is rows and n2 is cols 
		rows, cols = I.shape
		#print "Test ", rows, cols, i
		for j in range(n1):
			#if (j == 0):
			#	print I[j,:]
			#	print database[i-1, b:b+n2]
			database[i-1,b:b+n2] = I[j,:]
			b += n2
		# Reset the column counter 
		b = 1
		#print "Storing ", database[i-1, :]
			

	# ----------------
    # NEGATIVE IMAGES
	# ----------------
	# The folder with the negative samples is negfolder
	other_folders_in_path = get_immediate_subdirectories("C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/")	
	l = len(other_folders_in_path)
	# print l

	# Remove 
	other_folders_in_path.remove(posfolder[:len(posfolder)-1])
	l = len(other_folders_in_path)
	# print l

	# How many folder will we use?
	number_of_folders = 17; count_folders = 1; 
	yn = np.zeros(img_per_neg_folder*number_of_folders);

	print "Reading negative samples ..."

	for each_folder in other_folders_in_path:
		dirpath = 'C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + each_folder
		mn = len(fnmatch.filter(os.listdir(dirpath), '*.jpg'))
		total_mn += mn
		each_folder += "/"
		for i in range(img_per_neg_folder):
			i += 1
			if (i < 10):
				I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + each_folder + "image_000" + str(i) + ".jpg")
			elif ((i >= 10) & (i < 100)):
				I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + each_folder + "image_00" + str(i) + ".jpg")
			elif ((i >= 100) & (i < 1000)):
				I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + each_folder + "image_0" + str(i) + ".jpg")
			elif ((i >= 1000) & (i < 10000)):
				I = cv2.imread('C:/Users/HP/Documents/L-IC/1-2016/Automatic Digital Microscope/Experiment 5 - Building Supervised Learning Algorithms/Logistic Regression/101_ObjectCategories.tar/' + each_folder + "image_" + str(i) + ".jpg")
			
			if (resize == True):
				I = cv2.resize(I, (n2, n1))
			elif (resize == False):
				pass

			# Convert image to grayscale, color does not seem to help that mucn 
			I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
			# I[:,:,0] = I[:,:,0]*0.60 + I[:,:,1]*0.28 + I[:,:,2]*0.12
			cv2.imshow("test", I)
			k = cv2.waitKey(1) & 0xFF

			# Allocate all the rows of the image into one row of the database's matrix
			# Do not worry it works. Remember n1 is rows and n2 is cols 
			rows, cols = I.shape
			#print "Test ", rows, cols, i
			for j in range(n1):
				# Remember to add the rows of the positive examples
				database[m+i-1,b:b+n2] = I[j,:]
				b += n2
			# Reset the column counter 
			b = 1
			#print "Storing ", database[i-1, :]'''
		if (count_folders == number_of_folders):
			break
		count_folders += 1
			
	# Set bias term to 1
	database[:, 0] = 1

	# --------
	# FEEDBACK
	# -------- 
	print "Database contains a total set of " + str(m) + " positive images"
	print "Database contains a total set of " + str(number_of_folders*img_per_neg_folder) + " negative images"
	print "Resize: " + str(resize)
	print "Databases merged ..."
	# Images are going to be resized if their size is superior to 80x100 (cols, rows)

	# Kill all the windows 
	cv2.destroyAllWindows()

	# ---------------------
	# DIVIDE THE DATA SETS
	# ---------------------
	# Merge both positive y's and negative y's
	# Remember that it is easier to create this vector because we have merged the data as m positions for positive
	# and for (img_per_neg_folder*number_of_folders) negatives. Therefore, we create a new variable and add their values 
	y = np.random.rand(m+(img_per_neg_folder*number_of_folders))
	y[0:m] = np.ones(m)
	y[m:m+(img_per_neg_folder*number_of_folders)] = np.zeros(img_per_neg_folder*number_of_folders)
	
	print "Adding the label to the database at the last column ..."
	# Make a copy of the database because we will add the label at the last column of the data structure known as matrix 
	num_cols = len(database[0,:])
	num_rows = len(database[:,0])
	aux_database = np.random.rand(num_rows, num_cols + 1)
	aux_database[:,0:num_cols] = database[:,:]
	aux_database[:, len(aux_database[0,:])-1] = y
	database = np.random.rand(len(aux_database[:,0]), len(aux_database[0,:]))
	database = aux_database
	#print database

	print "Shuffling the database ..."
	# Before splitting the datasets we must shuffle all the data to avoid the clustering of only positives or only negatives
	for i in range(500):
		np.random.shuffle(database)

	print "Dividing the dataset in training, cross-validation and test"
	# Divide the database in 3 parts. Training set (60%), Cross-validation set (20%), Test set (20%)
	m0 = round((m+(img_per_neg_folder*number_of_folders))*0.60)	
	m1 = round((m+(img_per_neg_folder*number_of_folders))*0.20) 
	m2 = round((m+(img_per_neg_folder*number_of_folders))*0.20) 
	data_set_divisions = []
	data_set_divisions.append(m0)
	data_set_divisions.append(m1)
	data_set_divisions.append(m2)
	print "Number of samples per division: ", data_set_divisions

	#print str(m0+m1+m2)
	# Note that if the round does not cover all the data. The test set will take the examples left 
	train_set = database[0:m0,:]
	cross_validation_set = database[m0:(m0+m1),:]
	test_set = database[(m0+m1):(m0+m1+m2),:] 

	# Checking the data is correct
	#for i in train_set:
	#	print i

	'''print len(train_set[:,0])
	print len(cross_validation_set[:,0])
	print len(test_set[:,0])'''

	#---------------------------------
	# TRAINING THE LEARNING ALGORITHM 
	#---------------------------------

	# Create an object of the class Learn in order to train the algorithm 
	model = Learn_logistic_Regression("debug", iterations, (m+(img_per_neg_folder*number_of_folders)), n1, n2, k, alpha, train_set, cross_validation_set, test_set, data_set_divisions)

	# Choose the order of the model
	model.choosing_d()

	# Run gradient descent
	# model.stochastic_gradient_descent()

	# trained_model = model.return_trained_model()

	# Pipeline Component 1: Image
	