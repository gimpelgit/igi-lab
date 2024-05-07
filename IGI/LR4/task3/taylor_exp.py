def taylor_exp(x: float, n: int, create_list: bool = False):
	i = 0
	term = 1.0
	sum = term
	li = [term]
	while i + 1 < n:
		i += 1
		term *= x / i
		sum += term
		if create_list:
			li.append(term)
	
	if create_list:
		return sum, li
	return sum
