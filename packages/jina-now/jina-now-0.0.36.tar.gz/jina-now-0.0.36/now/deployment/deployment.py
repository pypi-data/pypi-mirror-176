import asyncio
import subprocess
import tempfile

from jcloud.flow import CloudFlow


def deploy_wolf(path: str, name: str, env_file: str = None):
    return CloudFlow(path=path, name=name, env_file=env_file).__enter__()


def terminate_wolf(flow_id: str):
    CloudFlow(flow_id=flow_id).__exit__()


def status_wolf(flow_id):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(CloudFlow(flow_id=flow_id).status)


def list_all_wolf(status='ALIVE', namespace='nowapi'):
    loop = asyncio.get_event_loop()
    flows = loop.run_until_complete(CloudFlow().list_all(status=status))
    if flows is None:
        return []
    # filter by namespace - if the namespace is contained in the flow name
    if namespace:
        return [f for f in flows if namespace in f['name']]
    return flows


def cmd(command, std_output=False, wait=True):
    if isinstance(command, str):
        command = command.split()
    if not std_output:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    else:
        process = subprocess.Popen(command)
    if wait:
        output, error = process.communicate()
        return output, error


def which(executable: str) -> bool:
    return bool(cmd('which ' + executable)[0])


def apply_replace(f_in, replace_dict, kubectl_path):
    with open(f_in, "r") as fin:
        with tempfile.NamedTemporaryFile(mode='w') as fout:
            for line in fin.readlines():
                for key, val in replace_dict.items():
                    line = line.replace('{' + key + '}', str(val))
                fout.write(line)
            fout.flush()
            cmd(f'{kubectl_path} apply -f {fout.name}')
