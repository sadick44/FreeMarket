import csv

from django.core.management import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for u in User.objects.all():
            print(u.email, u.username)

        with open('fixtures/insert_users.csv') as cvsfile:
            s_reader = csv.reader(cvsfile, delimiter=',')
            for index, val in enumerate(s_reader):
               if index == 0:
                   continue
               else: pass
                   # user = User.objects.get(email=val[0])
                   # print(user, "email")
                   # user.delete()
                   # user.save()