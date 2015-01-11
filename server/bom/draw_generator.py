DRAW_SCHELETON_1 = '''from django.utils.translation import ugettext_lazy as _
import random
import datetime


class {0}Draw(object):
    """
    Stores the content of a draw of {0}
    """

    def __init__(self'''

DRAW_SCHELETON_2 = ''', {0}=X'''

DRAW_SCHELETON_3 = '''):
'''

DRAW_SCHELETON_4 = '''
        self.{0} = {0}
        """xxx"""
'''
DRAW_SCHELETON_5 = '''
    def is_feasible(self):
        pass

    def toss(self):
        pass
'''

import argparse

def main():
    parser = argparse.ArgumentParser(description="Generates the scheleton of a draw", usage='%(prog)s DrawName attr1 [attr2 ...] ')
    parser.add_argument("-c", nargs=1, type=str, help="Name of the draw. (eg: RandomItem)")
    parser.add_argument("attr", nargs=argparse.REMAINDER, help="list of attributes to generate")
    args = parser.parse_args()
    if not args.c or not args.attr:
        parser.print_help()
        exit(-1)

    print("Draw name: {0}".format(args.c[0]))
    print("Attributes: {0}".format(args.attr))


    result = ""
    result += DRAW_SCHELETON_1.format(args.c[0])
    for attr in args.attr:
        result += DRAW_SCHELETON_2.format(attr)
    result += DRAW_SCHELETON_3
    for attr in args.attr:
        result += DRAW_SCHELETON_4.format(attr)
    result += DRAW_SCHELETON_5

    print "Generated file:"
    print " -*- "  * 5
    print result
    print " -*- "  * 5

    filename = raw_input( "Enter a filename to store the result: ")
    with open(filename, "w") as f:
        f.write(result)

    print "Done, enjoy.. ;)"

if __name__ == "__main__":
    main()
