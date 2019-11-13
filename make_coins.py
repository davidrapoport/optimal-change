from itertools import combinations
from collections import namedtuple
import numpy as np

def make_change(coins):
	optimal_change_for_cent = {}
	optimal_change_for_cent[0]=[]
	for coin in coins:
		optimal_change_for_cent[coin] = [coin]
	for cent in range(1,100):
		if cent not in optimal_change_for_cent:
			make_change_helper(cent, optimal_change_for_cent, coins)
	return optimal_change_for_cent

def make_change_helper(cent, optimal_change_for_cent, coins):
	if cent in optimal_change_for_cent:
		return
	best_coin = -1
	best_coin_length = 1000
	for coin in coins:
		previous_amount = cent - coin
		if previous_amount < 0:
			continue
		## If we don't have a value for the previous amount, fill one in
		## TODO: I think this will never happen?
		if previous_amount not in optimal_change_for_cent:
			# print "%s not in %s" % (previous_amount, optimal_change_for_cent)
			make_change_helper(previous_amount, optimal_change_for_cent, coins)
			# print "After filling: %s" % optimal_change_for_cent
		if len(optimal_change_for_cent[previous_amount])+1 < best_coin_length:
			best_coin = coin
			best_coin_length = len(optimal_change_for_cent[previous_amount])+1
	if best_coin == -1:
		print ("Best coin is -1 for cent: %s\noptimal_cache: %s\ncoins: %s" 
			% (cent, optimal_change_for_cent, coins))
		return
	optimal_change_for_cent[cent] = optimal_change_for_cent[cent - best_coin] + [best_coin]

def calculate_greedy_change(amount, coins):
	change = []
	sorted_coins = list(coins)
	# Reverse the list so that the biggest coin is first.
	sorted_coins.sort(reverse=True)
	coin_pointer = 0
	while amount > 0:
		# 1 should always be a coin so this will never go out of bounds.
		while sorted_coins[coin_pointer] > amount:
			coin_pointer += 1
		change.append(sorted_coins[coin_pointer])
		amount -= sorted_coins[coin_pointer]
	return change

def check_greediness(optimal_change_dict, coins):
	for amount in optimal_change_dict:
		# Since we include a 1 cent coin, the DP alg will always appear greedy for
		# 1 cent. Also avoid checking if 0 is greedy to avoid errors.
		if amount < 1:
			continue
		greedy_coins = calculate_greedy_change(amount, coins)
		greedy_coins.sort()
		optimal_change_dict[amount].sort()
		if greedy_coins != optimal_change_dict[amount]:
			return False
	return True

def print_stats(results):
	results.sort(key=lambda x: x.mean)
	print "Lowest mean is {}".format(results[0])
	results.sort(key=lambda x: x.median)
	print "Lowest median is {}".format(results[0])
	results.sort(key=lambda x: x.percentile_25)
	print "Lowest percentile_25 is {}".format(results[0])
	results.sort(key=lambda x: x.percentile_75)
	print "Lowest percentile_75 is {}".format(results[0])
	results.sort(key=lambda x: x.percentile_95)
	print "Lowest percentile_95 is {}".format(results[0])
	results.sort(key=lambda x: x.worst)
	print "Lowest worst is {}".format(results[0])

Result = namedtuple('Result', ['coins','is_greedy', 'mean', 'stddev',
	'median', 'percentile_25', 
	'percentile_75', 'percentile_95', 'worst'])
results = []


for coin_comb in combinations(range(2,100),3):
	# we must have a 1 cent coin. Otherwise we won't be able to make change for 1c
	coins = [1] + list(coin_comb) 
	optimal_change_dict = make_change(coins)
	is_greedy = check_greediness(optimal_change_dict, coins)
	coin_lengths = np.array([len(result) for result in optimal_change_dict.values()])
	worst = np.amax(coin_lengths)
	mean = np.mean(coin_lengths)
	stddev = np.std(coin_lengths)
	median = np.median(coin_lengths)
	percentile_25 = np.percentile(coin_lengths, 25)
	percentile_75 = np.percentile(coin_lengths, 75)
	percentile_95 = np.percentile(coin_lengths, 95)
	result = Result(coins, is_greedy, mean, stddev, median, percentile_25, percentile_75, percentile_95, worst)
	results.append(result)

greedy = [result for result in results if result.is_greedy]
print "For greedy Algorithms: "
print_stats(greedy)
print "\n\nFor all Algorithms: "
print_stats(results)