""" Module for running safety test """

import autograd.numpy as np   # Thinly-wrapped version of Numpy


class SafetyTest(object):
	def __init__(self,
		safety_dataset,
		model,
		parse_trees,
		regime='supervised_learning',
		**kwargs):
		""" 
		Object for running safety test
		
		:param safety_dataset: The dataset object containing safety data
		:type safety_dataset: :py:class:`.DataSet` object

		:param model: The Seldonian model object 
		:type model: :py:class:`.SeldonianModel` object

		:param parse_trees: List of parse tree objects containing the 
			behavioral constraints
		:type parse_trees: List(:py:class:`.ParseTree` objects)

		:param regime: The category of the machine learning algorithm,
			e.g., supervised_learning or reinforcement_learning
		:type regime: str
		"""
		self.safety_dataset = safety_dataset
		self.model = model
		self.parse_trees = parse_trees
		self.regime = regime

		if self.regime == 'supervised_learning':
			# To evaluate the primary objective we will need
			# features and labels separated and in the proper form
			self.features = self.safety_dataset.features
			self.labels = self.safety_dataset.labels


	def run(self,solution,**kwargs):
		""" Loop over parse trees, calculate the bounds on leaf nodes
		and propagate to the root node. The safety test passes if
		the upper bounds of all parse tree root nodes are less than or equal to 0. 

		:param solution: 
			The solution found by candidate selection
		:type solution: numpy ndarray

		:return: passed, whether the candidate solution passed the safety test
		:rtype: bool
		
		"""
		passed = True
		for tree_i,pt in enumerate(self.parse_trees): 
			# before we propagate reset the tree
			pt.reset_base_node_dict()

			bounds_kwargs = dict(
				theta=solution,
				dataset=self.safety_dataset,
				model=self.model,
				branch='safety_test',
				regime=self.regime
				)
			
			pt.propagate_bounds(**bounds_kwargs)
			# Check if the i-th behavioral constraint is satisfied
			upperBound = pt.root.upper 
			if upperBound > 0.0: # If the current constraint was not satisfied, the safety test failed
				passed = False
			# # reset bounds and data for each base node
			# pt.reset_base_node_dict(reset_data=True)

		return passed

	def evaluate_primary_objective(self,theta,primary_objective):
		""" Get value of the primary objective given model weights,
		theta, on the safety dataset. Wrapper for primary_objective where 
		data is fixed. 

		:param theta: model weights
		:type theta: numpy.ndarray

		:param primary_objective: The primary objective function 
			you want to evaluate

		:return: The primary objective function evaluated at theta
		"""
		
		# Get value of the primary objective given model weights
		if self.regime == 'supervised_learning':
		
			result = primary_objective(self.model,theta, 
					self.features, self.labels)
			return result

		elif self.regime == 'reinforcement_learning':
			# Want to maximize the importance weight so minimize negative importance weight
			# Adding regularization term so that large thetas make this less negative
			# and therefore worse 
			data_dict = {'episodes':self.safety_dataset.episodes}
			result = -1.0*primary_objective(self.model,theta,
				data_dict)

			if hasattr(self,'reg_coef'):
				# reg_term = self.reg_coef*np.linalg.norm(theta)
				reg_term = self.reg_coef*np.dot(theta.T,theta)
			else:
				reg_term = 0
			result += reg_term
			return result