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
    return True


def write_task(data):
    task = data[0]
    day = data[1].capitalize()
    time = data[2]
    username = data[3]

    if '-' in task:
        formatting = [x.capitalize() for x in task.split('-')]
        task = ' '.join(formatting)

    with open('tasks.json') as j_source:
        source = json.load(j_source)

    with open('tasks.json', 'w') as f_data:
        for element in source['resources']:
            if element['user']['username'] == '':
                element['user']['username'] = username                
            elif not element['user']['username'] == username.capitalize():
                print(colorama.Fore.RED,
                        f'[!!] {username} is not recognizable',
                        colorama.Style.RESET_ALL)
                break

            if day in element['tasks']:
                if len(element['tasks'][day]) >= 1:
                    element['tasks'][day][task] = time
                else:
                    element['tasks'][day] = {task:time}
            
        json.dump(source, f_data, indent=2)


def view_tasks(day, username):
    with open('tasks.json') as j_source:
        source = json.load(j_source)

    for element in source['resources']:
        if not element['user']['username'] == username:
            print(colorama.Fore.RED,
                        f'[!!] {username} not recognizable',
                        colorama.Style.RESET_ALL)
        else:
            if not element['tasks'][day] == {}:
                tasks = len(element["tasks"][day])
                print(colorama.Fore.YELLOW,
                        f'[!] You have {tasks} Task{plural_s(tasks)} for {day}',
                        colorama.Style.RESET_ALL)
                for data in element['tasks'][day]:            
                    print(f'Task: {data}\nTime: {element["tasks"][day][data]}\n')
            else:
                print(colorama.Fore.YELLOW,
                        f'[!] No Available Tasks in {day}',
                        colorama.Style.RESET_ALL)


def remove_task(task, day):
    with open('tasks.json') as j_source:
        source = json.load(j_source)

    with open('tasks.json', 'w') as f_source:
        if '-' in task:
            formatting = [x.capitalize() for x in task.split('-')]
            task = ' '.join(formatting)
        else:
            day.capitalize()

        for element in source['resources']:
            if task in element['tasks'][day]:
                del element['tasks'][day][task]

        json.dump(source, f_source, indent=2)


def plural_s(v):
    return 's' if not abs(v) == 1 else ''


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='List Tasks, View Tasks for the day or week.')

    parser.add_argument("-mt", "--maketask",
                        nargs=4, metavar='maketask',
                        action="store",
                        help="Creates one task for the current day. (e.g -mt 'Buy Some Eggs' Monday 5:30pm Kungger)")

    parser.add_argument("-vt", "--viewtask",
                        nargs=2, metavar='viewtask',
                        action="store",
                        help="Views tasks for the day. (e.g -vt Wednesday Kungger)")
    
    parser.add_argument("-r", "--reset",
                        action='store_true',
                        help="Deletes all tasks for the week.")

    parser.add_argument("-rt", "--removetask",
                        nargs=2, metavar='removetasks',
                        action='store',
                        help="Remove a specific task in a specific day. (e.g -rt 'Watch Movies' Friday)")

    args = parser.parse_args()
    
    if not os.path.exists('tasks.json'):
        write_json()
    
    if args.maketask:
        info = [x.capitalize() for x in args.maketask]
        write_task(info)
    
    if args.viewtask:
        info = [x.capitalize() for x in args.viewtask]
        view_tasks(info[0], info[1])

    if args.reset:
        if write_json():
            print(colorama.Fore.GREEN,
                    '[*] Reset has been Successful.',
                    colorama.Style.RESET_ALL)
    
    if args.removetask:
        info = [x.capitalize() for x in args.removetask]
        remove_task(info[0], info[1])