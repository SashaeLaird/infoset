"""Generic linux daemon base class for python 3.x."""

import atexit
import signal
import sys
import os
import time

# Infoset libraries
from infoset.utils import log


class Daemon(object):
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    Modified from http://www.jejik.com/files/examples/daemon3x.py

    """

    def __init__(self, pidfile, lockfile=None):
        """Method for intializing the class.

        Args:
            pidfile: Name of PID file
            lockfile: Name of lock file

        Returns:
            None

        """
        # Initialize key variables
        self.pidfile = pidfile
        self.lockfile = lockfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism.

        Args:
            None

        Returns:
            None

        """
        # Create a parent process that will manage the child
        # when the code using this class is done.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            log_message = ('Daemon fork #1 failed: %s') % (err)
            log_message = ('%s - PID file: %s') % (log_message, self.pidfile)
            log.log2die(1060, log_message)

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            log_message = ('Daemon fork #2 failed: %s') % (err)
            log_message = ('%s - PID file: %s') % (log_message, self.pidfile)
            log.log2die(1061, log_message)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        f_handle_si = open(os.devnull, 'r')
        # f_handle_so = open(os.devnull, 'a+')
        f_handle_so = open(os.devnull, 'a+')
        f_handle_se = open(os.devnull, 'a+')

        os.dup2(f_handle_si.fileno(), sys.stdin.fileno())
        # os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f_handle:
            f_handle.write(pid + '\n')

    def delpid(self):
        """Delete the PID file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if os.path.exists(self.pidfile) is True:
            os.remove(self.pidfile)

    def dellock(self):
        """Delete the lock file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if self.lockfile is not None:
            if os.path.exists(self.lockfile) is True:
                os.remove(self.lockfile)

    def start(self):
        """Start the daemon.

        Args:
            None

        Returns:

        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf_handle:
                pid = int(pf_handle.read().strip())

        except IOError:
            pid = None

        if pid:
            log_message = (
                'PID file: %s already exists. Daemon already running?'
                '') % (self.pidfile)
            log.log2die(1062, log_message)

        # Start the daemon
        self.daemonize()

        # Log success
        log_message = ('Daemon Started - PID file: %s') % (self.pidfile)
        log.log2quiet(1070, log_message)

        # Run code for daemon
        self.run()

    def force(self):
        """Stop the daemon by deleting the lock file first.

        Args:
            None

        Returns:

        """
        # Delete lock file and stop
        self.dellock()
        self.stop()

    def stop(self):
        """Stop the daemon.

        Args:
            None

        Returns:

        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf_handle:
                pid = int(pf_handle.read().strip())
        except IOError:
            pid = None

        if not pid:
            log_message = (
                'PID file: %s does not exist. Daemon not running?'
                '') % (self.pidfile)
            log.log2warn(1063, log_message)
            # Not an error in a restart
            return

        # Try killing the daemon process
        try:
            while 1:
                if self.lockfile is None:
                    os.kill(pid, signal.SIGTERM)
                else:
                    time.sleep(0.3)
                    if os.path.exists(self.lockfile) is True:
                        continue
                    else:
                        os.kill(pid, signal.SIGTERM)
                time.sleep(0.3)
        except OSError as err:
            error = str(err.args)
            if error.find("No such process") > 0:
                self.delpid()
                self.dellock()
            else:
                log_message = (str(err.args))
                log_message = (
                    '%s - PID file: %s') % (log_message, self.pidfile)
                log.log2die(1068, log_message)
        except:
            log_message = (
                'Unknown daemon "stop" error for PID file: %s'
                '') % (self.pidfile)
            log.log2die(1066, log_message)

        # Log success
        self.delpid()
        self.dellock()
        log_message = ('Daemon Stopped - PID file: %s') % (self.pidfile)
        log.log2quiet(1071, log_message)

    def restart(self):
        """Restart the daemon.

        Args:
            None

        Returns:

        """
        # Restart
        self.stop()
        self.start()

    def status(self):
        """Get daemon status.

        Args:
            None

        Returns:

        """
        # Get status
        if os.path.exists(self.pidfile) is True:
            print('Daemon is running')
        else:
            print('Daemon is stopped')

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        # Simple comment to pass linter
        pass
