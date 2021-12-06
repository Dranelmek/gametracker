games =  ['a','b']
running = 'c'
import subprocess
s = subprocess.check_output('tasklist', shell=True)

i = 0



conditions = ['a' in running, 'b' in running]
while not any(conditions):
	print('Hello World!')s

print(games[conditions.index(True)])