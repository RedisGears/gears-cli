import redis
import click
import json
import os
import zipfile

DATA_BIN_FINE_NAME = 'Data.bin'
META_DATA_FILE_NAME = 'MetaData.json'

class Colors(object):
    @staticmethod
    def Cyan(data):
        return '\033[36m' + data + '\033[0m'

    @staticmethod
    def Yellow(data):
        return '\033[33m' + data + '\033[0m'

    @staticmethod
    def Bold(data):
        return '\033[1m' + data + '\033[0m'

    @staticmethod
    def Bred(data):
        return '\033[31;1m' + data + '\033[0m'

    @staticmethod
    def Gray(data):
        return '\033[30;1m' + data + '\033[0m'

    @staticmethod
    def Lgray(data):
        return '\033[30;47m' + data + '\033[0m'

    @staticmethod
    def Blue(data):
        return '\033[34m' + data + '\033[0m'

    @staticmethod
    def Green(data):
        return '\033[32m' + data + '\033[0m'

@click.group()
def gears_cli():
    pass

def create_connection(host, port, password, decode_responses=True):
    global args
    try:
        r = redis.Redis(host, port, password=password, decode_responses=decode_responses)
        r.ping()
    except Exception as e:
        print(Colors.Bred('Cannot connect to Redis. Aborting (%s)' % str(e)))
        exit(1)
    return r

def print_res(res, res_id):
    res = str(res)
    res_id = Colors.Bold('%d)' % res_id)
    try:
        jsonStr = json.dumps(res, indent=4, sort_keys=True)
        jsonStr = Colors.Bold(jsonStr)
        res = json.loads(res)
        print('%s\t%s' % (res_id, jsonStr))
        return
    except Exception as e:
        pass
    print('%s\t%s' % (res_id, Colors.Bold(res)))

@gears_cli.command()
@click.option('--host', default='localhost', help='Redis host to connect to')
@click.option('--port', default=6379, type=int, help='Redis port to connect to')
@click.option('--password', default=None, help='Redis password')
@click.option('--requirements', default=None, help='Path to requirements.txt file')
@click.argument('filepath')
@click.argument('extra_args', nargs=-1, type=click.UNPROCESSED)
def run(host, port, password, requirements, filepath, extra_args):
    r = create_connection(host, port, password);

    extra_args = [a for a in extra_args]
    if requirements is not None:
        extra_args.append('REQUIREMENTS')
        with open(requirements, 'r') as f:
            reqs = [(el.strip()) for el in f.readlines()] 
            extra_args += reqs

    with open(filepath, 'rt') as f:
        script = f.read()
    q = ['rg.pyexecute', script] + extra_args

    try:
        reply = r.execute_command(*q)
    except Exception as e:
        print(Colors.Bred("failed running gear function (%s)" % str(e)))
        exit(1)
    
    if reply == 'OK':
        print('OK')
    else:
        results, errors = reply
        print(Colors.Bold('Results'))
        print(Colors.Bold('-------'))
        for i in range(len(results)):
            print_res(results[i], i + 1)
        print('')
        if len(errors) > 0:
            print(Colors.Bred('Errors'))
            print(Colors.Bred('------'))
            for i in range(len(errors)):
                print(Colors.Bred('%d)\t%s' % (i + 1, str(errors[i]))))

@gears_cli.command()
@click.option('--host', default='localhost', help='Redis host to connect to')
@click.option('--port', default=6379, type=int, help='Redis port to connect to')
@click.option('--password', default=None, help='Redis password')
@click.option('--save-directory', default='./', help='Directory for exported files')
@click.argument('requirement')
def export_requirement(host, port, password, save_directory, requirement):
    r = create_connection(host, port, password, decode_responses=False);
    
    try:
        metaDataValues, setializedData = r.execute_command('RG.PYEXPORTREQ', requirement)
    except Exception as e:
        print(Colors.Bred("failed exporting requirement (%s)" % str(e)))
        exit(1)

    metaData = {}
    for i in range(0, len(metaDataValues), 2):
        key = metaDataValues[i]
        value = metaDataValues[i + 1]
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        if isinstance(value, list):
            value = [str(a.decode('utf-8')) for a in value]
        metaData[key] = value
    jsonMetaDataStr = json.dumps(metaData, indent=4, sort_keys=True)

    fileName = "%s-v%s-gears-req-%s.zip" % (os.path.basename(metaData['Name']), metaData['GearReqVersion'], metaData['CompiledOs'])
    filePath = os.path.join(save_directory, fileName)
    filePath = os.path.abspath(filePath)

    if os.path.exists(filePath):
        print(Colors.Bred("File %s already exists" % filePath))
        exit(1)

    print(Colors.Cyan("Saving exported requirement into %s" % filePath))

    with zipfile.ZipFile(filePath, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr(META_DATA_FILE_NAME, jsonMetaDataStr)
        data = b''.join(setializedData)
        zf.writestr(DATA_BIN_FINE_NAME, data)

@gears_cli.command()
@click.option('--host', default='localhost', help='Redis host to connect to')
@click.option('--port', default=6379, type=int, help='Redis port to connect to')
@click.option('--password', default=None, help='Redis password')
@click.option('--requirement-file-path', help='Path of requirements file')
@click.option('--bulk-size', default=10, type=int, help='Max bulk size to send to redis in MB')
def import_requirement(host, port, password, requirement_file_path, bulk_size):
    r = create_connection(host, port, password, decode_responses=False);

    bulk_size_in_bytes = bulk_size * 1024 * 1024

    requirement_file_path = os.path.abspath(requirement_file_path)

    if not os.path.exists(requirement_file_path):
        print(Colors.Bred("File %s does not exists" % requirement_file_path))
        exit(1)

    with zipfile.ZipFile(requirement_file_path, "a", zipfile.ZIP_DEFLATED, False) as zf:
        try:
            data = zf.read(DATA_BIN_FINE_NAME)
        except Exception as e:
            print(Colors.Bred("Bad zip format (%s)" % str(e)))
            exit(1)
        data = [data[i : i + bulk_size_in_bytes] for i in range(0, len(data), bulk_size_in_bytes)]
        try:
            res = r.execute_command('RG.PYIMPORTREQ', *data)
        except Exception as e:
            print(Colors.Bred("failed import requirement (%s)" % str(e)))
            exit(1)

        print(Colors.Green('Requirement imported successfully'))

if __name__ == '__main__':
    gears_cli()
