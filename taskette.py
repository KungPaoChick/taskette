from importlib.resources import path
import os
import json
import argparse
import colorama


def write_json():
    with open('tasks.json', 'w') as j_file:
        data_set = {}
        data_set['resources'] = []
        data_set['resources'].append({
            'user': {'username': ''},
            'tasks': {
                'Sunday': {},
                'Monday': {},
                'Tuesday': {},
                'Wednesday': {},
                'Thursday': {},
                'Friday': {},
                'Saturday': {}
            }
        })
        json.dump(data_set, j_file, indent=2)


def write_task(data):
    task = data[0]
    day = data[1]
    time = data[2]
    username = data[3]

    if '-' in task:
        formatting = [x.capitalize() for x in task.split('-')]
        task = ' '.join(formatting)
    else:
        task = task.capitalize()
        
    with open('tasks.json') as j_source:
        source = json.load(j_source)

    with open('tasks.json', 'w') as f_data:
        for element in source['resources']:
            element['user']['username'] = username
            if day in element['tasks']:
                element['tasks'][day] = {task:time}

        json.dump(source, f_data, indent=2)


def view_tasks(day):
    with open('tasks.json') as j_source:
        source = json.load(j_source)

    for element in source['resources']:
        if not element['tasks'][day] == {}:
            for data in element['tasks'][day]:
                print(f'Task: {data}\nTime: {element["tasks"][day][data]}')
        else:
            print(colorama.Fore.YELLOW,
                    f'[*] No Available Tasks in {day}')


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='List Tasks, View Tasks for the day or week.')

    parser.add_argument("-mk", "--maketask",
                        nargs=4, metavar='maketask',
                        action="store",
                        help="Creates one task for the current day. (e.g -mk Buy-Milk Monday 5:30pm Kungger)")

    parser.add_argument("-vt", "--viewtask",
                        nargs=1, metavar='viewtask',
                        action="store",
                        help="Views tasks for the day. (e.g -vt Wednesday)")
    
    args = parser.parse_args()
    
    if not os.path.exists('tasks.json'):
        write_json()
    
    if args.maketask:
        info = [x.capitalize() for x in args.maketask]
        write_task(info)
    
    if args.viewtask:
        for day in args.viewtask:
            view_tasks(day.capitalize())