# This program knows about the schedule for a conference that runs over the
# course of a day, with sessions in different tracks in different rooms.  Given
# a room and a time, it can tell you which session starts at that time.
#
# Usage:
#
# $ python conference_schedule.py [room] [time]
#
# For instance:
#
# $ python conference_schedule.py "Main Hall" 13:30
#
# TODO:
# * Implement the program as described in the comments at the top of the file.

# TODO (extra):
# * Change the program so that that it can tell you what session is running in
#   a room at a given time, even if a session doesn't start at that time.
# * Change the program so that if called with a single argument, the title of a
#   session, it displays the room and the time of the session.


import sys
import time


schedule = {
    'Main Hall': {
        '10:00': 'Django REST framework',
        '11:00': 'Lessons learned from PHP',
        '12:00': "Tech interviews that don't suck",
        '14:00': 'Taking control of your Bluetooth devices',
        '15:00': "Fast Python? Don't Bother!",
        '16:00': 'Test-Driven Data Analysis',
    },
    'Seminar Room': {
        '10:00': 'Python in my Science Classroom',
        '11:00': 'My journey from wxPython tp PyQt',
        '12:00': 'Easy solutions to hard problems',
        '14:00': 'Taking control of your Bluetooth devices',
        '15:00': "Euler's Key to Cryptography",
        '16:00': 'Build your Microservices with ZeroMQ',
    },
    'Assembly Hall': {
        '10:00': 'Distributed systems from scratch',
        '11:00': 'Python in Medicine: ventilator data',
        '12:00': 'Neurodiversity in Technology',
        '14:00': 'Chat bots: What is AI?',
        '15:00': 'Pygame Zero',
        '16:00': 'The state of PyPy',
    },
}


data = None
if len(sys.argv) == 2:
    data = sys.argv[1]
elif len(sys.argv) == 3:
    data = (sys.argv[1], sys.argv[2])


def start_end_time(dic):
    times = []
    for key in dic.keys():
        times.append(time.strptime(key, "%H:%M"))
    return min(times), max(times)


def list_of_times(dic):
    times = []
    for key in dic.keys():
        times.append(time.strptime(key, "%H:%M"))
    return times


if data is None:
    for room, timetable in schedule.items():
        print(room)
        for section_time, title in timetable.items():
            print(section_time.rjust(7), '-', title)
else:
    if isinstance(data, tuple):
        room, section_time = data
        section_time_time = time.strptime(section_time, "%H:%M")
        if room in schedule:
            start_time, end_time = start_end_time(schedule[room])
            if section_time_time < start_time:
                print("It's too early. There is no section at {} in \"{}\".".format(section_time, room))
            elif section_time_time > end_time:
                print("It's too late. There is no section at {} in \"{}\".".format(section_time, room))
            else:
                times = list_of_times(schedule[room])
                for i in range(len(times)-1):
                    if times[i] <= section_time_time <= times[i+1]:
                        real_time = time.strftime("%H:%M", times[i])
                        print('There is a section "{}" at {} in "{}" (starts from {}).' \
                            .format(schedule[room][real_time], section_time, room, real_time))
        else:
            print('There is no such room in the building.')
    elif isinstance(data, str):
        title = data
        check = False
        for key, value in schedule.items():
            for key1, value1 in value.items():
                if data in value.values():
                    print('The section "{}" takes place in "{}" at {}.'.format(data, key, key1))
                    check = True
                    break
        if not check:
            print('There is no such section in our schedule.')

