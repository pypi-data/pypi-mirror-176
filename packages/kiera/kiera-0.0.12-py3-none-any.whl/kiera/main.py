#!/usr/bin/env python3

import requests
import argparse
import random
import time
import tomli
import tomli_w
import os
import sys

from rich.columns import Columns
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS

from rich.console import Console
import uuid
console = Console()

SERVER_URL_DEV = 'http://localhost:5000'
SERVER_URL_PROD = 'https://jkl-backend-eu.herokuapp.com'
# SERVER_URL_PROD = 'https://prod.kiera.ai'

if len(sys.argv) > 1 and sys.argv[1] == '--dev':
    DEV_MODE = True
    SERVER_URL = SERVER_URL_DEV
    sys.argv.pop(1)
else:
    DEV_MODE = False
    SERVER_URL = SERVER_URL_PROD

TERMS_AND_SEVICES = 'https://kiera.ai'

if DEV_MODE:
    CLIENT_ID="6ba695f9a731779de3eb"
else:
    CLIENT_ID="8bf8ed3294d9901c9729"


STATE = str(random.random())

CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'kierarc')

def write_access_key_to_file(access_key):
    data = {'access_key': access_key}
    with open(API_KEYS_LOCATION, 'w') as f:
        f.write(tomli_w.dumps(data))

def read_access_key_from_file():
    if not os.path.exists(API_KEYS_LOCATION):
        return None

    with open(API_KEYS_LOCATION, 'r') as f:
        data = tomli.loads(f.read())

    if 'access_key' not in data:
        return None

    return data['access_key']

ACCESS_KEY = read_access_key_from_file()

def server_test():
    r = requests.get(f'{SERVER_URL}/test')
    print(r.text)

def hello():
    print("Hello, world!")
    print('Trying to connect to the server...')
    server_test()


def login():
    accepted_tns = terms_and_sevices_prompt()
    if not accepted_tns:
        print('You must accept the terms and services to use Kiera')
        return
    url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&state={STATE}'
    # print(url)
    print(f'\nIn case your browser doesn\'t open automatically, visit \n{url}')
    webbrowser.open(url)
    while True:  
        access_key = get_access_key_from_state(STATE)
        if access_key:
            print('Access key received')
            break
        time.sleep(0.5)

    write_access_key_to_file(access_key)
    return access_key



def terms_and_sevices_prompt():
    print(f'Terms and Services: {TERMS_AND_SEVICES}')
    print('Do you agree to the terms and services? [y/n]', end=' ')
    answer = input()
    if answer == 'y' or answer == 'yes':
        return True
    else:
        return False

def listen_for_callback():
    print('Listening for callback', flush=True)
    import flask
    app = flask.Flask(__name__)

    @app.route('/github/callback', methods=['GET'])
    def callback():
        print('Callback received')
        print(flask.request.args)
        return 'You can close this window now'

    # app.run()
    app.run(host='localhost', port=5000, debug=True)

def parse_args():
    parser = argparse.ArgumentParser(description='Kiera')
    # parser.add_argument('command', choices=['login', 'listen'])
    # parser.add_argument('command', choices=['login', ''])
    # parser.add_argument('login', action='store_true')
    # make login command optional
    parser.add_argument('command', nargs='?', choices=['login', ''])
    return parser.parse_args()

def send_command_feedback(data):
    r = requests.post(f'{SERVER_URL}/command_feedback', json=data)
    # print(r.text)

def main():
    # args = parse_args()
    # if args.login:
        # login()
        # listen_for_callback()
    # else:
        # hello()
    arg_login = None
    if len(sys.argv) > 1:
        if sys.argv[1] == 'login':
            arg_login = True


    if not ACCESS_KEY:
        print('No access key found, running login\n')
        # args.command = 'login'
        arg_login = True

    # if args.command == 'login':
    if arg_login:
        login()
        # listen_for_callback()
    else:
        # hello()
        generate_completion()
        if False:
            input_text = '# test:'
            r = requests.post(SERVER_URL + '/main2', json={'data': input_text, 'access_key': access_key})
            print("r:", r)
            print(r.text)

def generate_completion():
    input_text = ' '.join(sys.argv[1:])

    from rich import print as rich_print
    # data = 'test command 123'
    # # rich_print(Panel(f'{data}     Execute (Y/n)?', title='Kiera', expand=False, border_style='blue'), end='')
    # rich_print(Panel(f'{data}     ',  subtitle='Execute (Y/n)?', expand=False, border_style='blue'), end='\r')

    # with Live(Columns([Panel('test', title='Kiera', expand=False, border_style='blue'), Panel('test', title='Kiera', expand=False, border_style='blue')], expand=True), refresh_per_second=1) as live:
        # for i in range(1):
            # live.update(Panel(f'{data}     ',  subtitle='Execute (Y/n)?', expand=False, border_style='blue'))
            # data += str(i)
            # time.sleep(1)

        # # remove the panel
        # live.update('')

    session_uuid = str(uuid.uuid1())
    exit_code = None
    while True:
        with console.status('', spinner='aesthetic'):
            # r = requests.post(SERVER_URL, data={'data': input_text})
            r = requests.post(SERVER_URL + '/main2', json={'data': input_text, 'access_key': ACCESS_KEY, 'session_id': session_uuid})


        parsed = r.json()
        generated_command = parsed['data']

        import subprocess as sp

        def execute_command(command):
            # sp.run(command, shell=True)

            exit_code = sp.call(command, shell=True)
            return exit_code


        import colored

        max_padding = 20
        if len(generated_command) < max_padding:
            generated_command_padded = (generated_command + ' ' * max_padding)[:max_padding]
        else:
            generated_command_padded = generated_command
        with Live(Panel(generated_command_padded, title='Kiera', subtitle='Execute (Y/n)?', expand=False, border_style='blue'), refresh_per_second=1) as live:
            # live.update(Panel(f'{data}     ',  subtitle='Execute (Y/n)?', expand=False, border_style='blue'))
            # time.sleep(1)

            import getch
            execute_answer = getch.getch().strip()

            command_accepted = execute_answer in ['y', 'Y', '']
            if command_accepted:
                # print()
                # execute_command(data)
                break

            # print("exit_code:", exit_code)
            # print("data:", data)
            send_command_feedback({'id': parsed['id'], 'accepted': command_accepted, 'access_key': ACCESS_KEY, 'exit_code': exit_code, 'session_id': session_uuid})
            live.update(None)

        if execute_answer in ['y', 'Y', '']:
            break

    print()
    exit_code = execute_command(generated_command)
    send_command_feedback({'id': parsed['id'], 'accepted': command_accepted, 'access_key': ACCESS_KEY, 'exit_code': exit_code, 'session_id': session_uuid})

        # print(f'{data}     Execute (Y/n)?', end='\r')
        # sys.stdout.flush()

        # import getch
        # execute_answer = getch.getch().strip()

        # if execute_answer in ['y', 'Y', '']:
            # print()
            # execute_command(data)
            # break







def get_access_key_from_state(state):
    response = requests.post(f'{SERVER_URL}/get_access_key_from_state', json={'state': state})
    # print(response.text)
    access_key = response.json()['jkl_access_key']
    return access_key


import webbrowser

if __name__ == "__main__":
    # webbrowser.open('http://example.com') 
    # get_access_key_from_state('0.6621392675885354')
    main()


    # hello()
    # login()
    # r = requests.post(SERVER_URL + '/main', data={'data': input_text})
    # as application/json
    if False:
        input_text = '# print all files'
        r = requests.post(SERVER_URL + '/main', json={'data': input_text})
        print("r:", r)
        print("r.text:", r.text)

