from django.db import models


# -----------------------------------------------------------------------------
class Player(models.Model):
    """
    Ref,Name,Sex,JrAge,Cat,Grade,Grade1,Games,RCat,RGrade,RGrade1,RGames,
    ClubNam1,ClubNam2,ClubNam3,ClubNam4,ClubNam5,ClubNam6,FIDECode,Nation
    """
    ref = models.CharField(max_length=7, primary_key=True)
    name = models.CharField(max_length=60)
    sex = models.CharField(max_length=1)

    def fullname(self):
        names = self.name.split(',')
        return ''.join(names[1:])+' '+names[0]

    class Meta:
        db_table = 'player'
        unique_together = ['ref', 'name', 'sex']


# -----------------------------------------------------------------------------
class Club(models.Model):
    name = models.CharField(max_length=60)
    is_area = models.BooleanField()

    def clubname(self):
        if self.is_area:
            return self.name + '[ area ]'
        return self.name

    class Meta:
        db_table = 'club'
        unique_together = ['name', 'is_area']


# -----------------------------------------------------------------------------
class Grade(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='%(class)s_grade',
    )
    grading_date = models.DateField()
    age = models.IntegerField(null=True)
    fidecode = models.CharField(max_length=10)
    nation = models.CharField(max_length=3)
    category = models.CharField(max_length=1)
    grade = models.IntegerField(null=True)
    previous_grade = models.IntegerField(null=True)
    num_games = models.IntegerField()
    rapid_category = models.CharField(max_length=1)
    rapid_grade = models.IntegerField(null=True)
    rapid_previous_grade = models.IntegerField(null=True)
    rapid_num_games = models.IntegerField(null=True)
    club1 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club1', null=True)
    club2 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club2', null=True)
    club3 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club3', null=True)
    club4 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club4', null=True)
    club5 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club5', null=True)
    club6 = models.ForeignKey(
        Club, on_delete=models.PROTECT, related_name='%(class)s_club6', null=True)

    def gradenum(self):
        return self.grade or ''

    def agenum(self):
        return self.age or ''

    class Meta:
        db_table = 'grade'
