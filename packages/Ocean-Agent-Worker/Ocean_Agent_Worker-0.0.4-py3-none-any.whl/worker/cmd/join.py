import json
import os
import subprocess
import logging

import requests


def join(endpoint):
    uri = f"http://{endpoint}/join" # TODO: insecure -> https로 바꿀 것
    response = requests.post(uri)
    join_info = response.json()
    join_info['API_SERVER_ADDR'] = endpoint.split(':')[0]

    # Run install-master script from internet
    install(join_info)


def install(join_info):
    logging.info("[INSTALL]")
    env = dict(os.environ, **join_info)
    command = "cd /tmp && curl -s https://raw.githubusercontent.com/AI-Ocean/kubernetes-install-scripts/main/install-worker.sh | bash"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    # print progress
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode())

    print(process.stderr.readline().decode())

