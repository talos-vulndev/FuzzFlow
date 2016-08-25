import time, socket, sys, traceback

from client.config import *
from client.helper import Helper
from client.rest import Rest
from engine.afl import Fuzzer as afl
from engine.radamsa import Fuzzer as radamsa



engines = {
    'afl' : afl,
    'radamsa' : radamsa
}

def main():
    helper = Helper()
    host = helper.register_host()
    print "\n\nFuzzing Client %s\n" % CLIENT_VERSION
    while True:
        fz = None
        job = None
        try:
            helper.update()
            job = Rest.get_job_by_host(host['id'])
            if job is not None:
                engine, target, options = helper.extract_job(job)
                engine_name = engine['name']
                fz = engines[engine_name](job, engine, target, options)
                fz.start()
            continue

        except socket.error:
            pass

        except KeyboardInterrupt as e:
            if fz is not None:
                fz.fail(e.message)
            print "Execution interrupted. Quitting."
            sys.exit(0)

        except:
            print "Unhandled Exception\n"
            traceback.print_exc()
            print ''
            message = time.strftime("%Y-%m-%d-%H.%M.%S") + ": \n" + \
                      traceback.format_exc()
            try:
                helper.log_error(message)
            except socket.error:
                pass


if __name__ == "__main__":
    main()
