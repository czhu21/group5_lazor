import pprint as p

file = open("bff_files/dark_1.bff", 'r').read()

lines = file.split('\n')

input_lines = []
for line in lines:
	if line != '':
		input_lines.append(line)


grid_start = input_lines.index('GRID START')
grid_stop = input_lines.index('GRID STOP')
lasers = []
for line in input_lines:
	if line[0] == 'L':
		print(line)
		lasers.append(line[2:])

print(lasers)
res = [tuple(map(int, sub.split(' '))) for sub in lasers]
print(res)

blocks = []
for line in input_lines:
	if line[0] == 'B':
		blocks.append(line[-1])

print(blocks)

targets = []
for line in input_lines:
	if line[0] == 'P':
		targets.append(line[2:])
res = [tuple(map(int, sub.split(' '))) for sub in targets]
print(targets)
# print(res)

grid_input = input_lines[grid_start+1:grid_stop]

grid = []
for i in grid_input:
	line_list = []
	j = ''.join(i.split())
	for letter in j:
		line_list.append(letter)
	grid.append(line_list)



if __name__ == '__main__':
	pass