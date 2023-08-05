import atexit
import select
import sys
import termios


class InputHandler:
    """
    Class to handle keyboard input
    A modified version of "https://stackoverflow.com/a/22085679"
    """

    def __init__(self):
        """
        Creates a  object that you can call to do various keyboard things.
        """
        # Save the terminal settings
        self.__fd = sys.stdin.fileno()
        self.__new = termios.tcgetattr(self.__fd)
        self.__old = termios.tcgetattr(self.__fd)

        # New terminal setting unbuffered
        self.__new[3] = (self.__new[3] &
                         ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__new)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """
        Resets to normal terminal
        """
        termios.tcsetattr(self.__fd, termios.TCSADRAIN, self.__old)

    @staticmethod
    def getch():
        """
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        return sys.stdin.read(1)

    @staticmethod
    def is_available():
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    @staticmethod
    def clear():
        """
        Clears the input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
