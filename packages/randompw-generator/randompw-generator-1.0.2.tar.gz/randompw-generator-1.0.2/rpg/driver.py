import string, random

class RandomPassword() :
	''' Base class to make instances from '''

	lower = string.ascii_lowercase
	upper = string.ascii_uppercase
	digits = string.digits
	sp_chars = '!@#$%&*?'

	def __init__(self, length = 15):

		# default length 15
		self.length = length

		# if length changes, the number of character changes accordingly.
		self.n_lower = (self.length*3)//10
		self.n_upper = (self.length*3)//10
		self.n_sp_chars = (self.length*2)//10
		self.n_digits = self.length - (self.n_upper + self.n_lower + self.n_sp_chars)

	def set_lower(self, num):
		''' Set the number of lower case character '''
		self.n_lower = num

	def set_upper(self, num):
		''' Set the number of upper case character '''
		self.n_upper = num

	def set_digits(self, num):
		''' Set the number of digits in the password '''
		self.n_digits = num

	def set_spchars(self, num):
		''' Set the number of special characters in the password '''
		self.n_sp_chars = num

	def generate(self):
		''' Generate password from the set configuration '''
		l_list = [random.choice(RandomPassword.lower) for i in range(self.n_lower)]
		u_list = [random.choice(RandomPassword.upper) for i in range(self.n_upper)]
		d_list = [random.choice(RandomPassword.digits) for i in range(self.n_digits)]
		s_list = [random.choice(RandomPassword.sp_chars) for i in range(self.n_sp_chars)]

		pw_list = l_list + u_list + d_list + s_list

		random.shuffle(pw_list)

		pw = "".join(pw_list)

		return pw