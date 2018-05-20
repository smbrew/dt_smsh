import random
import numpy
import math

def white_noise(cardinality, length):
	return [random.randint(0, cardinality - 1) for i in range(length)]		

class fsm():
	def __init__(self, prob, next, output):
		self.prob = prob
		self.next = next
		self.out = output
		self.state = random.randint(0, len(self.prob)-1)

	def generate(self, length):
		self.data = []
		for i in range(length):
			rnd = random.random()
			for j in range(int(len(self.prob[self.state]))):
				if rnd < self.prob[self.state][j]:
					self.data.append(self.out[self.state][j])
					self.state = self.next[self.state][j]
					break
				else:
					rnd -= self.prob[self.state][j]
		return self.data

class stream():
	def __init__(self, data):
		self.data = data
		self.cardinality = len(set(self.data))
		self.invert()

	def copy(self):
		fwn = white_noise(2, len(self.data))
		return [self.data[i] for i in range(len(self.data)) if self.data[i] == fwn[i]]

	def invert(self):
		self.copies = []
		self.inverse = []
		cardinals = set(range(self.cardinality))
		min_length = len(self.data)
		for i in range(self.cardinality - 1):
			self.copies.append(self.copy())
			min_length = min(len(self.copies[i]), min_length)
		self.copies.append(self.data)
		for i in range(min_length):
			sigmas = set([j[i] for j in self.copies])
			if len(sigmas) == self.cardinality - 1:
				self.inverse.append(list(cardinals.difference(sigmas))[0])

class streams():
	def __init__(self, data):
		n = len(data)
		self.c = data[0].cardinality
		for i in range(1,len(data)):
			self.c = max(self.c, data[i].cardinality)
		mat = numpy.ndarray([n, n])
		for i in range(n):
			for j in range(n):
				s_sum = self.stream_sum(data[i].data, data[j].inverse)
				mat[i][j] = self.compute_deviation(s_sum)
		self.mat = mat

	def stream_sum(self, stream1, stream2):
		length = min(len(stream1), len(stream2))
		return [stream1[i] for i in range(length) if stream1[i] == stream2[i]]

	def compute_deviation(self, stream):
		c = self.c
		# put that formula here
		eps = 0.05
		l = range(1, int(math.log(1/eps)/math.log(c))+1)
		zeta = 0
		for x in l:
			phi = numpy.array([0] * c)
			for ci in range(c):
				xs = [ci] * x
				for j in range(len(stream)):
					if stream[j] == xs[0] and stream[j:j+len(xs)] == xs:
						phi[ci]+=1
			phi = phi / float(sum(phi))
			u = numpy.array([1/float(c)] * c)
			zeta += abs(max(phi - u)) / float(c ** (2 * x))
		zeta *= (c - 1) / float(c)
		return zeta

if __name__ == '__main__':
	fsm1_prob = [
		[0.25, 0.75],
		[0.90, 0.02, 0.08],
		[0.40, 0.40, 0.20]
		]
	fsm1_next = [
		[1, 2],
		[0, 1, 2],
		[2, 0, 1]
		]
	fsm1_output = [
		[1, 1],
		[0, 1, 1],
		[0, 0, 1]
		]
	fsm1 = fsm(fsm1_prob, fsm1_next, fsm1_output)

	fsm2_prob = [
		[0.1, 0.1, 0.4, 0.4],
		[1.0]
		]
	fsm2_next = [
		[0, 0, 1, 1],
		[0]
		]
	fsm2_output = [
		[0, 1, 0, 1],
		[1]
		]
	fsm2 = fsm(fsm2_prob, fsm2_next, fsm2_output)

	fsm3_prob = [
		[0.5, 0.5]
		]
	fsm3_next = [
		[0, 0]
		]
	fsm3_output = [
		[0, 1]
		]
	fsm3 = fsm(fsm3_prob, fsm3_next, fsm3_output)

	fsm4_prob = [
		[0.1, 0.9]
		]
	fsm5_prob = [
		[0.9, 0.1]
		]
	fsm4 = fsm(fsm4_prob, fsm3_next, fsm3_output)
	fsm5 = fsm(fsm5_prob, fsm3_next, fsm3_output)

	stream_length = 10000
	data_1 = stream(fsm1.generate(stream_length))
	data_1b = stream(fsm1.generate(stream_length))
	data_2 = stream(fsm2.generate(stream_length))
	data_3 = stream(fsm3.generate(stream_length))
	data_4 = stream(fsm4.generate(stream_length))
	data_5 = stream(fsm5.generate(stream_length))

	compare = streams([data_1, data_1b, data_2, data_3, data_4])

	compare2 = streams([data_3, data_4, data_5])
	print compare2.mat
