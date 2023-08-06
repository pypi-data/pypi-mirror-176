import datetime
import os
from datetime import datetime
from multiprocessing import Process

import robot
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def call_robot(keyword, variables):
    project_path = os.getcwd()
    output_path = project_path + '/src/bots_logs/'
    d = datetime.strftime(datetime.now(), '%y%m%d%H%M%S%f')
    output_file = 'output-' + d + '.xml'
    log_file = 'log-' + d + '.html'
    report_file = 'report-' + d + '.html'
    robot.run(
        f'{keyword}.robot',
        loglevel='DEBUG',
        listener='workspace_listener.py',
        variable=variables,
        log=output_path + log_file,
        output=output_path + output_file,
        report=output_path + report_file
    )


from time import sleep


@app.post("/run/{keyword}/{t_id}/{w_id}/")
async def run_robot(request: Request, keyword, t_id, w_id, background_tasks: BackgroundTasks):
    print(f'{datetime.now()}')

    sleep(5)

    client_host = request.client.host
    console_flag = True if request.headers.get('console_flag') == 'True' else False

    json_body = await request.json()
    variables = [f'{k}:{v}' for k, v in json_body.items()]
    variables.extend([
        f'id_t:{t_id}',
        f'id_p:{w_id}',
        f'console_flag:{console_flag}',
    ])

    # background_tasks.add_task(call_robot, keyword,variables)
    p = Process(target=call_robot, args=(keyword, variables))
    p.start()
    print(f"Process {p} started")

    return 200


if __name__ == "__main__":
    print('about to start worksapce')
    uvicorn.run(app, host="0.0.0.0", port=80, debug=True)
