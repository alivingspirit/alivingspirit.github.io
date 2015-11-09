from flask import Flask, render_template, request, redirect, url_for
import dataset
from random import shuffle
from itertools import groupby
from operator import itemgetter

app = Flask("ABL")

db = dataset.connect('sqlite:///mydatabase.db')
mydata = db['data']
schedule_table = db['schedule']

if len(mydata) == 0:
    mydata.insert({
        'teams': "",
        'dates': "",
        'locations': ""
    })

def save_data(**kwargs):
    kwargs['id'] = 1
    mydata.update(kwargs, ['id'])

def get_data():
    return mydata.find_one(id=1)

def generate_schedule(teams = '', locations = '', dates = ''):
    teams = [team.strip() for team in teams.split('\n') ]
    locations = [location.strip() for location in locations.split('\n')]
    dates = [date.strip() for date in dates.split('\n')]

    num_of_teams = len(teams)
    half_of_teams = num_of_teams / 2

    result_file = open('result.txt', 'w')
    for date in dates:
        shuffle(locations)
        for game_num, location in enumerate(locations):
            yield {
                'date': date,
                'team1': teams[game_num],
                'team2': teams[-(game_num + 1)],
                'location': location
            }
        teams = teams[1:] + [teams[0]]

@app.route('/schedule.html')
def schedule():
    schedule = schedule_table.all()
    schedule = groupby(schedule, lambda s: s['date'] )
    schedule = [ (date, list(sorted(game, key=itemgetter('location')))) for date, game in schedule ]
    return render_template('/schedule.html', schedule = schedule )

@app.route('/editschedule.html')
def edit_schedule():
    schedule = schedule_table.all()

    schedule = groupby(sorted(schedule, key= lambda x: x['date'] ), lambda s: s['date'] )
    schedule = [ (date, list(sorted(game, key=itemgetter('location')))) for date, game in schedule ]
    return render_template('/editschedule.html', schedule = schedule )

@app.route('/editscheduleaction', methods=['post'])
def edit_schedule_entry():
    id = request.form.get('id', None)
    date = request.form['date']
    team1 = request.form['team1']
    team2 = request.form['team2']
    location = request.form['location']

     #Actions
    add = request.form.get('Add', None)
    update = request.form.get('Update', None)
    delete = request.form.get('Delete', None)

    if add:
        schedule_table.insert(dict(date = date, team1 = team1, team2 = team2, location = location), ensure=False)

    if update:
        schedule_table.update(dict(id = id, date = date, team1 = team1, team2 = team2, location = location), ['id'], ensure=False)

    if delete:
        schedule_table.delete(id=id)

    return redirect(url_for('edit_schedule'))


@app.route('/edit.html')
def get_edit_page():
    return render_template('/edit.html', **get_data() )

@app.route('/generateschedule', methods=['post'])
def generate_shedule():
    data = dict(
        teams = request.form['teams'],
        locations = request.form['locations'],
        dates = request.form['dates'])
    save_data(**data)

    schedule_data = generate_schedule(**data)
    schedule_table.delete()
    schedule_table.insert_many(list(schedule_data))

    return redirect(url_for('get_edit_page'))

if __name__ == '__main__':
    app.run(debug=True)
