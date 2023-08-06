class Calculate(object):
	def sum(self):
		a=2
		b=4
		self.c=a+b

	def divide(self):
		f=4
		self.d = self.c/f

	def show_result(self):
		print(self.d)

	def __call__(self):
		self.sum()
		self.divide()
		self.show_result()
