from assignments import get_assignments,Assignment, NotLoggedIn
import datetime
from collections import defaultdict
import json
import sys

try:
    assignments=get_assignments()
except NotLoggedIn:
    print("Cannot log in to Gradescope. You need to log in to Gradescope again.",file=sys.stderr)
    print("If you are unsure about what to do, delete the file named cookies.json and rerun this script.")
    print("If the issue persists, please file a bug report")
    sys.exit(1)

pending_assignments=[]
now=datetime.datetime.now()

to_dump=defaultdict(dict)
graded=[]
try:
    last_dump=json.load(open('assignments.json'))
except:
    last_dump= {}
    for a in assignments:
        if (a.deadline > now or (a.late_deadline and a.late_deadline > now)) and not a.submitted:
            pending_assignments.append(a)
        if a.grade:
            to_dump[a.course.name][a.name]=a.grade
else: # only display grades after a cache exists
    for a in assignments:
        if (a.deadline > now or (a.late_deadline and a.late_deadline > now)) and not a.submitted:
            pending_assignments.append(a)
        if a.grade:
            to_dump[a.course.name][a.name]=a.grade
            if a.course.name in last_dump and a.name not in last_dump[a.course.name]:
                graded.append(a)

graded.sort()

json.dump(to_dump,open('assignments.json','w'),indent = 4)

d=defaultdict(list)

for a in pending_assignments:
    if now>a.deadline:
        d[a.late_deadline.date()].append(a)
    else:
        d[a.deadline.date()].append(a)

for v in d.values():
    v.sort(key = lambda a:a.deadline.time())
print('\033[2J\033[H',end = '',flush = True)
for key in sorted(d.keys()): #TODO: display late deadlines regardless
    print('─'*79)
    print(f'{key.strftime("%A, %b %-d"): ^78}')
    for a in d[key]:
        course=f'{a.name} ({a.course.name})'
        if now<=a.deadline:
            if a.late_deadline:
                extension=a.late_deadline-a.deadline
                if extension > datetime.timedelta(seconds = 0):
                    # apparently some assignments can have late deadlines before
                    # the actual deadline
                    ext=''
                    hr=0
                    if extension.days > 2:
                        ext+=str(extension.days)+'d'
                    else:
                        hr+=extension.days*24
                    hr+=extension.seconds/60
                    if hr:
                        ext+=str(round(hr,not float(hr).is_integer() or None))+'hr'
                    print(f'{course:<55}{a.deadline.strftime("%I:%M %p")} (late +{ext})')
                else:
                    print(f'{course:<55}{a.deadline.strftime("%I:%M %p")}')
            else:
                print(f'{course:<55}{a.deadline.strftime("%I:%M %p")}')
        else:
            print(f'{course:<55}{a.late_deadline.strftime("%I:%M %p")} \033[31m(late)\033[0m')
    print()

if graded:
    print('\033[97;46mAssignments graded since last run\033[0m')
    for a in graded:
        name=f'({a.course.name}) {a.name}'
        # assuming gradescope doesn't send malicious payload in its grade
        percent=round(eval(a.grade,{'__builtins__':{}},{})*100,1)
        print(f'{name:<55} {a.grade.replace(" ",""):<12} ({percent}%)')
