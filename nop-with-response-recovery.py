def main():
	input()
	items0 = input().split()
	input()
	items1 = input().split()
	matrix = [[0 for _ in range(len(items1))] for _ in range(len(items0))]
	matrix[0][0] = 1 if items0[0] == items1[0] else 0
	for i in range(1, len(items1)):
		if (matrix[0][i-1] == 1) or (items1[i] == items0[0]):
			matrix[0][i] = 1
	for i in range(1, len(items0)):
		if (matrix[i-1][0] == 1) or (items0[i] == items1[0]):
			matrix[i][0] = 1
	for i in range(1, len(items0)):
		for j in range(1, len(items1)):
			if items0[i] == items1[j]:
				matrix[i][j] = matrix[i-1][j-1] + 1
			else:
				matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1])

	i, j = len(items0) - 1, len(items1) - 1
	result = [None] * matrix[-1][-1]
	counter = matrix[-1][-1] - 1
	while counter != -1:
		if (items0[i] == items1[j]):
			result[counter] = items0[i]
			counter -= 1
			i -= 1
			j -= 1
		elif i - 1 == -1:
			j -= 1
		elif j - 1 == -1:
			i -= 1
		else:
			if matrix[i-1][j] > matrix[i][j-1]:
				i -= 1
			else:
				j -= 1
	print(" ".join(result))

if __name__ == '__main__':
	main()