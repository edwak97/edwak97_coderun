def buildTeamLists(team_indexes, adjency_matrix, team_sign):
	'''
	team_indexes = [None|1|2]
	1 -- принадлежность 1 команде
	2 -- принадлежность второй команде
	team_sign -- индекс рассматриваемой команды, для которой ищутся
	элементы, не имеющие хотя бы одного ребра хотя бы с одним членом команды team_sign
	'''
	while(True):
		candidates_to_team = []
		for i in range(len(adjency_matrix)):
			# убедимся в том, что есть хотя бы один узел без команды,
			# который не смежен хотя бы с одним из узлов команды team_sign (это значит, что i должен быть в команде 3 - team_sign)
			if team_indexes[i] == None:
				for j in range(len(adjency_matrix)):
					if (not adjency_matrix[i][j]) and team_indexes[j] == team_sign:
						candidates_to_team.append(i)
						break
		if candidates_to_team == []:
			break
		# Смежны ли кандидаты между собой?
		for i in range(len(candidates_to_team)):
			for k in range(i + 1, len(candidates_to_team)):
				if not adjency_matrix[candidates_to_team[i]][candidates_to_team[k]]:
					return -1
		# Смежен ли каждый из кандидатов с каждым из команды 3 - team_sign?
		anti_team_sign = 3 - team_sign
		for candidate in candidates_to_team:
			for i in range(len(adjency_matrix)):
				if team_indexes[i] == anti_team_sign and not adjency_matrix[candidate][i]:
					return -1
		for candidate in candidates_to_team:
			team_indexes[candidate] = anti_team_sign
		team_sign = anti_team_sign

	# если существуют значения с team_indexes[i] = None
	# то речь идёт об узлах, которые смежны всем существующим членам команд 1 и команд 2
	# если такой узел 1, то его можно отнести в какой угодно команде
	# если их более одного, то оставшиеся узлы должны образовывать два полных подграфа, первый
	# из которых надо отнести к одной команде, а второй к другой
	new_index_to_old = []
	for i in range(len(team_indexes)):
		if team_indexes[i] == None:
			new_index_to_old.append(i)
	if new_index_to_old == []:
		return team_indexes
	if len(new_index_to_old) == 1:
		team_indexes[new_index_to_old[0]] = team_sign
		return team_indexes
	matrix = [[False for _ in range(len(new_index_to_old))] for _ in range(len(new_index_to_old))]
	for i in range(len(new_index_to_old)):
		for j in range(i + 1, len(new_index_to_old)):
			if adjency_matrix[new_index_to_old[i]][new_index_to_old[j]]:
				matrix[i][j] = matrix[j][i] = True
	result = solve(matrix)
	if result == -1:
		return -1
	for i in range(len(result)):
		team_indexes[new_index_to_old[i]] = result[i]
	return team_indexes

def solve(adjency_matrix):
	team_indexes = [None] * len(adjency_matrix)
	for i in range(len(adjency_matrix)):
		# узлы, не имеющие ребра с i, находятся в команде 2 и обязаны иметь рёбра с другими узлами, не имеющими ребра с i
		# сам узел i находится в команде 1
		team_indexes[i] = 1
		for j in range(i + 1, len(adjency_matrix)):
			if not adjency_matrix[i][j]:
				team_indexes[j] = 2
				for k in range(j + 1, len(adjency_matrix)):
					# остальные узлы, не имеющие ребра с i, тоже должны находиться в команде 2
					# и иметь ребро с j
					if not adjency_matrix[i][k]:
						if not adjency_matrix[j][k]:
							return -1
						team_indexes[k] = 2
				return buildTeamLists(team_indexes, adjency_matrix, 2)
	# граф полный, красота; первый элемент в одной команде, остальные во второй
	team_indexes[0] = 2
	return team_indexes

def main():
	'''
	Печатает -1, если не удалось разнести граф на два полных подграфа;
	иначе печатает на первой строке количество вершин в первом подграфе,
	на второй -- список элементов первого подграфа,
	на третьей -- список элемент второго подграфа
	'''
	n, m = tuple(map(int, input().split()))
	adjency_matrix = [[False for _ in range(n)] for _ in range(n)]
	for _ in range(m):
		u, v = [int(val) - 1 for val in input().split()]
		adjency_matrix[u][v] = adjency_matrix[v][u] = True
	result = solve(adjency_matrix)
	if result == -1:
		print(-1)
	else:
		team1 = [val + 1 for val in range(n) if result[val] == 1]
		team2 = [val + 1 for val in range(n) if result[val] == 2]
		print(len(team1))
		print(*team1)
		print(*team2)

if __name__ == '__main__':
    main()