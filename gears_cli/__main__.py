import redis
import argparse
import json

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Run gears scripts on Redis(Gears)')

parser.add_argument(
    '--host', default='localhost',
    help='redis host')

parser.add_argument(
    '--port', default=6379, type=int,
    help='redis port')

parser.add_argument(
    '--requirements', default=None,
    help='requirements file')

parser.add_argument('path', help='scripts paths')
parser.add_argument('extra_args', help='extra argument to send with the script', nargs='*', default=[])

parser.add_argument(
    '--password', default=None,
    help='redis password')

args = parser.parse_args()

def print_res(res, res_id):
    res = str(res)
    try:
        res = json.loads(res)
        print('%d) json:' % res_id)
        print(json.dumps(res, indent=4, sort_keys=True))
        print('')
        return
    except Exception as e:
        pass
    print('%d)\t%s' % (res_id, res))

def main():
    try:
        r = redis.Redis(args.host, args.port, password=args.password, decode_responses=True)
        r.ping()
    except:
        print('Cannot connect to Redis. Aborting.')
        exit(1)

    if args.requirements is not None:
        args.extra_args.append('REQUIREMENTS')
        with open(args.requirements, 'r') as f:
            requirements = [(el.strip()) for el in f.readlines()] 
            args.extra_args += requirements

    with open(args.path, 'rt') as f:
        script = f.read()
    q = ['rg.pyexecute', script] + args.extra_args

    reply = r.execute_command(*q)
    
    if reply == 'OK':
        print('OK')
    else:
        results, errors = reply
        print('Results')
        print('-------')
        for i in range(len(results)):
            print_res(results[i], i + 1)
        print('')
        if len(errors) > 0:
            print('Errors')
            print('------')
            for i in range(len(errors)):
                print('%d)\t%s', (i + 1, str(errors[i])))


if __name__ == '__main__':
    main()
