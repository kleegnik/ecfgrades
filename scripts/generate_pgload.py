#!/usr/bin/env python

import csv
import os.path
from glob import glob


# -----------------------------------------------------------------------------
# these are in the order they come out of the CSV files
fieldnames = ('ref', 'name', 'sex', 'age',
              'category', 'grade', 'previous_grade', 'num_games',
              'rapid_category', 'rapid_grade', 'rapid_previous_grade', 'rapid_num_games',
              'club1', 'club2', 'club3',
              'club4', 'club5', 'club6',
              'fidecode', 'nation')


# -----------------------------------------------------------------------------
def read_grades(csv_filename):
    with open(csv_filename, newline='', encoding='ISO-8859-1', mode='r') as csvfile:
        c = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in c:
            if row == [] or row[0] in ('Ref', 'REF', 'Code'):
                # skip blank line or header
                continue
            # self.stdout.write(str(row))
            fields = dict(zip(fieldnames, row))
            # convert integers to string, and
            # replace blank (integer) fields with '\N' value; imported as NULL in db
            for f in ('age', 'grade', 'previous_grade', 'num_games',
                      'rapid_grade', 'rapid_previous_grade', 'rapid_num_games'):
                if fields[f] == '':
                    fields[f] = r'\N'
                else:
                    fields[f] = str(fields[f])
            yield(fields)


# -----------------------------------------------------------------------------
players = {}
grades = []
allclubs = {}
allclubs_pk = 0

dir_path = os.path.dirname(os.path.realpath(__file__))
for csv_filename in glob(os.path.join(dir_path, 'grading_lists/grades*0[178].csv')):
    b = os.path.basename(csv_filename).replace('grades', '').replace('.csv', '')
    year = int(b[:4])
    month = int(b[4:6])
    grading_date = '{}-{:02d}-01'.format(year, month)
    for entry in read_grades(csv_filename):
        k = entry['ref']
        if k not in players:
            players[k] = (entry['name'], entry['sex'])
        player_ref = k

        # decode club names
        clubs = []
        for c in range(1, 7):
            clubname = entry['club'+str(c)].strip()
            if clubname == '':
                clubs.append(r'\N')
                continue
            is_area = False
            if clubname.endswith('*'):
                is_area = True
                clubname = clubname.replace('*', '').rstrip()
            k = (clubname, is_area)
            if k not in allclubs:
                allclubs_pk += 1
                allclubs[k] = str(allclubs_pk)
            clubs.append(allclubs[k])

        grades.append([
            grading_date,
            entry['age'],
            entry['nation'],
            entry['fidecode'],
            entry['category'],
            entry['grade'],
            entry['previous_grade'],
            entry['num_games'],
            entry['rapid_category'],
            entry['rapid_grade'],
            entry['rapid_previous_grade'],
            entry['rapid_num_games'],
            clubs[0],
            clubs[1],
            clubs[2],
            clubs[3],
            clubs[4],
            clubs[5],
            player_ref
        ])

    # print('--', csv_filename)
    # print(len(players), len(allclubs), len(grades))


# -----------------------------------------------------------------------------
# output dump file suitable for import into PostgreSQL
print('TRUNCATE TABLE player,club,grade RESTART IDENTITY;')

print('COPY player (ref, name, sex) FROM stdin;')
for ref, fields in players.items():
    print('{}\t{}\t{}'.format(ref, fields[0], fields[1]))
print(r'\.')

print('\nCOPY club (id,name,is_area) FROM stdin;')
allclubs = {v: k for k, v in allclubs.items()}
for pk in sorted(allclubs):
    print('{}\t{}\t{}'.
          format(pk, allclubs[pk][0], {True: 't', False: 'f'}.get(allclubs[pk][1], r'\N')))
print(r'\.')

print('\nCOPY grade (id,grading_date,age,nation,fidecode,category,grade,previous_grade,'
      'num_games,rapid_category,rapid_grade,rapid_previous_grade,rapid_num_games,'
      'club1_id,club2_id,club3_id,club4_id,club5_id,club6_id,player_id)'
      ' FROM stdin;')
for pk, f in enumerate(grades):
    print('\t'.join([str(pk+1)] + f))
print(r'\.')
