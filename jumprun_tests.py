import unittest
from docopt import docopt
import jumprun

doc = jumprun.__doc__


class TestJumprun(unittest.TestCase):

    def test_add(self):
        args = docopt(doc, ['add', 'Test', 'test_file.py'])
        self.assertEqual(args['add'], True)
        self.assertEqual(args['<name>'], 'Test')
        self.assertEqual(args['<filename>'], 'test_file.py')

    def test_rm(self):
        args = docopt(doc, ['rm', 'Test'])
        self.assertEqual(args['rm'], True)
        self.assertEqual(args['<name>'], 'Test')
        self.assertEqual(args['--all'], False)
        args = docopt(doc, ['rm', 'Test', '--all'])
        self.assertEqual(args['rm'], True)
        self.assertEqual(args['<name>'], 'Test')
        self.assertEqual(args['--all'], True)

    def test_show(self):
        args = docopt(doc, ['show'])
        self.assertEqual(args['show'], True)
        self.assertEqual(args['--f'], False)
        args = docopt(doc, ['show', '--f'])
        self.assertEqual(args['show'], True)
        self.assertEqual(args['--f'], True)

    def test_rename(self):
        args = docopt(doc, ['rename', 'Test', 'NewTest'])
        self.assertEqual(args['rename'], True)
        self.assertEqual(args['<oldname>'], 'Test')
        self.assertEqual(args['<newname>'], 'NewTest')

    def test_run(self):
        args = docopt(doc, ['Test'])
        self.assertEqual(args['rename'], False)
        self.assertEqual(args['show'], False)
        self.assertEqual(args['rm'], False)
        self.assertEqual(args['add'], False)

if __name__ == "__main__":
    unittest.main()
