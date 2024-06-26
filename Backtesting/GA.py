import numpy as np
from Backtester import Backtester


class Individual:
	def __init__(self, n_genes, gene_ranges):
		self.genes = [np.random.randint(gene_ranges[x][0], gene_ranges[x][1]) for x in range(n_genes)]

		self.backtester = Backtester(
			initial_balance = 1000,
			leverage = 10,
			trailing_stop_loss = True
			)


class Population:
	def __init__(self, generation_size, n_genes, gene_ranges, n_best, mutation_rate):

		self.population = [Individual(n_genes, gene_ranges) for _ in range(generation_size)]
		self.n_genes = n_genes
		self.gene_ranges = gene_ranges
		self.n_best = n_best
		self.generation_size = generation_size
		self.mutation_rate = mutation_rate

	def selection(self):
		return sorted(
			self.population,
			key = lambda individual: individual.backtester.return_results(
				symbol = '-',
				start_date = '-',
				end_date = '-',
				)['fitness_function'],
			reverse = True
			)[0:self.n_best]

	def crossover(self):
		selected = self.selection()
		point = 0
		father = []

		for i in range(self.generation_size):
			father = np.random.choice(self.n_best, size = 2, replace = False)
			father = [selected[x] for x in father]

			# Crossover in one point
			point = np.random.randint(0, self.n_genes)

			self.population[i].genes[:point] = father[0].genes[:point]
			self.population[i].genes[point:] = father[1].genes[point:]

	def mutation(self):

		

		for i in range(self.generation_size):
			point = 0

			for j in range(self.n_genes):

				point = np.random.randint(0, self.n_genes)

				if np.random.random() <= self.mutation_rate:
					new_gen = np.random.randint(self.gene_ranges[point][0], self.gene_ranges[point][1])

					while new_gen == self.population[i].genes[point]:
						new_gen = np.random.randint(self.gene_ranges[point][0], self.gene_ranges[point][1])

					self.population[i].genes[point] = new_gen


