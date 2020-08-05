import csv
import os.path
from glob import glob
from datetime import datetime as dt

from django.core.management.base import BaseCommand
from django.db import connection
from ecfgrades.grades.models import Player, Grade, Club


# -----------------------------------------------------------------------------
# these are in the order they come out of the CSV file
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
            # replace blank (integer) fields with None value; translates to NULL in db
            for f in ('age', 'grade', 'previous_grade', 'num_games',
                      'rapid_grade', 'rapid_previous_grade', 'rapid_num_games'):
                if fields[f] == '':
                    fields[f] = None
            yield(fields)


# -----------------------------------------------------------------------------
class Command(BaseCommand):
    help = 'Loads the grades database from a directory of CSV files.'

    def handle(self, *args, **options):
        self.stdout.write('Truncating tables..')
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE player,club,grade RESTART IDENTITY')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        for csv_filename in glob(os.path.join(dir_path, 'grading_lists/*.csv')):
            b = os.path.basename(csv_filename).replace('grades', '').replace('.csv', '')
            year = int(b[:4])
            month = int(b[4:6])
            grading_date = dt(year, month, 1)
            for entry in read_grades(csv_filename):
                player, created = Player.objects.get_or_create(
                    ref=entry['ref'], name=entry['name'], sex=entry['sex'])
                # decode club names
                clubs = []
                for c in range(1, 7):
                    clubname = entry['club'+str(c)].strip()
                    is_area = False
                    if clubname.endswith('*'):
                        is_area = True
                        clubname = clubname.replace('*', '').rstrip()
                    club, created = Club.objects.get_or_create(name=clubname, is_area=is_area)
                    clubs.append(club)
                Grade.objects.create(
                    player=player,
                    grading_date=grading_date,
                    age=entry['age'],
                    nation=entry['nation'],
                    fidecode=entry['fidecode'],
                    category=entry['category'],
                    grade=entry['grade'],
                    previous_grade=entry['previous_grade'],
                    num_games=entry['num_games'],
                    rapid_category=entry['rapid_category'],
                    rapid_grade=entry['rapid_grade'],
                    rapid_previous_grade=entry['rapid_previous_grade'],
                    rapid_num_games=entry['rapid_num_games'],
                    club1=clubs[0],
                    club2=clubs[1],
                    club3=clubs[2],
                    club4=clubs[3],
                    club5=clubs[4],
                    club6=clubs[5]
                )

            self.stdout.write(csv_filename)
