import os
import signal

from runner.runner import init_configuration, run, s, Config, run_camisole_server

if __name__ == '__main__':
    config = Config()
    if not os.path.exists('.config'):
        init_configuration(config)
    run_camisole_server()
    s.enter(config.time_waiting, 1, run, (s,))
    s.run()
