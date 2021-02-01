def average(lst):
	if not lst:
		raise ArithmeticError('The list must contain at least one item')
	a = 0
	for i in lst:
		a += i
	res = a / len(lst)
	return round(res, 1000)

print(average([]))