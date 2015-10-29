from json import load
from random import shuffle

def get_teams():
    with open('teams.txt', 'r') as f:
        return [team.strip() for team in f.readlines()]

def get_config():
    with open('config.txt', 'r') as f:
        return load(f)

def get_locations():
    with open('locations.txt', 'r') as f:
        return [location.strip() for location in f.readlines()]

if __name__ == '__main__':
    teams = get_teams()
    config = get_config()

    num_of_teams = len(teams)
    half_of_teams = num_of_teams / 2

    locations = get_locations()
    weeks = config['Weeks']
    number_of_games_per_week = len(locations)

    games = []

    result_file = open('result.txt', 'w')
    for week in range(1, weeks + 1):
        shuffle(locations)
        print("Week " + str(week), file=result_file)
        for game_num in range(number_of_games_per_week):
            game = {
                'week': week,
                'team1': teams[game_num],
                'team2': teams[-(game_num + 1)],
                'locations': locations[game_num]
            }
            games.append(game)
            print(game['team1'] + ' vs ' + game['team2'] + ' at ' + locations[game_num], file=result_file)
        print(file=result_file)
        teams = teams[1:] + [teams[0]]
