import os

from printFunction import printboard
from resource import SystemState
from resource import Move

def main():
	cur_state = SystemState()
	valid = False
	prevMv = Move()
	goal = False
	while True:
		os.system('clear')
		print (cur_state)
		print(prevMv, valid)
		print(cur_state.genMoves())
		for i in range (1,4):
			if i != 2:
				val = input("input action (flip/none): ").strip().split(' ')
				key = val[0]
				pos = -1
			else:
				val = input("input action (place [1-7]): ").strip().split(' ')
				key = val[0]
				if len(val) == 2:
					pos = int(val[1]) - 1
			move = Move(key, cur_state._cur_player, pos)
			prevMv = move
			valid = cur_state.validMove(move)
			if valid:
				cur_state = cur_state.update(move)
				if cur_state.isGoal()[0]:
					goal = True
					break
			os.system('clear')
			print (cur_state)
		if goal == True:
			break

	os.system('clear')
	print (cur_state)
	print ('Game over')

if __name__ == "__main__":
	main()
