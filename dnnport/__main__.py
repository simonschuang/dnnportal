import argparse
import os.path
import sys


PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
found_parent_dir = False
for p in sys.path:
    if os.path.abspath(p) == PARENT_DIR:
        found_parent_dir = True
        break
if not found_parent_dir:
    sys.path.insert(0, PARENT_DIR)


def main():
    parser = argparse.ArgumentParser(description='DNNport server')
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port to run app on (default 5000)'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help=('Run the application in debug mode (reloads when the source '
              'changes and gives more detailed error messages)')
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print the version number and exit'
    )

    args = vars(parser.parse_args())

    import dnnport

    if args['version']:
        print dnnport.__version__
        sys.exit()

    print ' ___  _ _  _ _                  _   '
    print '| . \| \ || \ | ___  ___  _ _ _| |_ '
    print '| | ||   ||   || . \/ . \| \'_> | |  '
    print '|___/|_\_||_\_||  _/\___/|_|   |_|  ', dnnport.__version__
    print '               |_|  '
    print

    #import dnnport.config
    #import dnnport.log
    import dnnport.webapp

    try:
        if not dnnport.webapp.scheduler.start():
            print 'ERROR: Scheduler would not start'
        else:
            dnnport.webapp.app.debug = args['debug']
            dnnport.webapp.socketio.run(dnnport.webapp.app, '0.0.0.0', args['port'])
    except KeyboardInterrupt:
        pass
    finally:
        dnnport.webapp.scheduler.stop()


if __name__ == '__main__':
    main()
