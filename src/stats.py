import csv
import pickle

def buildStats(fname):
    names = {'HYBRID', 'CELLS', 'SOLS', 'RANDOM'}

    data = {nm+'1': {nm+'2': [] for nm in names} for nm in names}

    games = pickle.load(open(fname, 'rb'))
    for g in games:
        p1 = g[0][0]
        p2 = g[0][1]
        win = g[1][0] and g[1][1] == p1
        draw = g[1][0] and g[1][1] == None
        num_turns = len(g[2])//3 + 1
        data[p1][p2].append((win, draw, num_turns))

    stats = {nm+'1': {nm+'2': [] for nm in names} for nm in names}
    for nm1 in data:
        for nm2 in data[nm1]:
            num_win = len(list(filter(lambda g: g[0], data[nm1][nm2])))
            num_draw = len(list(filter(lambda g: g[1], data[nm1][nm2])))
            num_game = len(data[nm1][nm2])
            num_lose = num_game - num_win - num_draw
            if num_game > 0:
                avg_turns = sum(map(lambda g: g[2], data[nm1][nm2])) / num_game
            else:
                avg_turns = 0

            stats[nm1][nm2] = (num_win, num_lose, num_draw, num_game, avg_turns)

    return stats

def printStatsToFile(stats, fname):
    names = ['HYBRID', 'CELLS', 'SOLS', 'RANDOM']
    col_headers = [
        'Evaluation',
        'W v Hy2',
        'L v Hy2',
        'D v Hy2',
        'NumGames v Hy2',
        'AvgTurns v Hy2',
        'W v Cells2',
        'L v Cells2',
        'D v Cells2',
        'NumGames v Cells2',
        'AvgTurns v Cells2',
        'W v Sols2',
        'L v Sols2',
        'D v Sols2',
        'NumGames v Sols2',
        'AvgTurns v Sols2',
        'W v Rand2',
        'L v Rand2',
        'D v Rand2',
        'NumGames v Rand2',
        'AvgTurns v Rand2',
    ]

    data = []
    for nm1 in map(lambda nm: nm+'1', names):
        row = []
        row.append(nm1)
        for nm2 in map(lambda nm: nm+'2', names):
            row += list(stats[nm1][nm2])
        data.append(row)

    csvf = open(fname, 'w')
    write = csv.writer(csvf)
    write.writerow(col_headers)
    for row in data:
        write.writerow(row)

printStatsToFile(buildStats('../log/merged.pkl'), 'results.csv')
