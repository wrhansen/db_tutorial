#!/usr/bin/env python3.6
import os
from subprocess import Popen, PIPE
import unittest


class DBTestCase(unittest.TestCase):
    def run_command(self, input_lines):
        input_line_str = '\n'.join(input_lines)
        stdin = f'{input_line_str}\n'
        with Popen(
            ['./db', 'mydb.db'],
                stdout=PIPE,
                stdin=PIPE,
                stderr=PIPE,
                universal_newlines=True) as proc:
            output = proc.communicate(stdin)
        return output[0].split('\n')

    @classmethod
    def setUpClass(cls):
        if os.path.exists('mydb.db'):
            os.remove('mydb.db')

    def tearDown(self):
        if os.path.exists('mydb.db'):
            os.remove('mydb.db')

    def test_insert_select(self):
        '''
        Test simple insert and select statement
        '''
        self.assertEqual(
            self.run_command(
                ['insert 1 user1 person1@example.com', 'select', '.exit']), [
                    'db > Executed.',
                    'db > (1, user1, person1@example.com)',
                    'Executed.',
                    'db > ',
                ])

    def test_error_message_table_full(self):
        '''
        Prints an error message when table is full (after 1400 rows)
        '''
        fill_stdin = [
            f'insert {index} user{index} person{index}@example.com'
            for index in range(1, 1402)
        ] + ['.exit']
        self.assertEqual(
            self.run_command(fill_stdin)[-2], 'db > Error: Table full.')

    def test_allows_inserting_strings_of_maximum_length(self):
        long_username = 'a' * 32
        long_email = 'a' * 255
        script = [f'insert 1 {long_username} {long_email}', 'select', '.exit']
        self.assertEqual(
            self.run_command(script), [
                'db > Executed.', f'db > (1, {long_username}, {long_email})',
                'Executed.', 'db > '
            ])

    def test_prints_error_message_if_strings_too_long(self):
        long_username = 'a' * 33
        long_email = 'a' * 256
        script = [f'insert 1 {long_username} {long_email}', 'select', '.exit']
        self.assertEqual(
            self.run_command(script),
            ['db > String is too long.', 'db > Executed.', 'db > '])

    def test_prints_an_error_message_if_id_is_negative(self):
        script = [
            'insert -1 cstack foo@bar.com',
            'select',
            '.exit',
        ]
        self.assertEqual(
            self.run_command(script),
            ['db > ID must be positive.', 'db > Executed.', 'db > '])

    def test_keeps_data_after_closing_connection(self):
        # First Step: Insert something, then exit
        script = [
            'insert 1 user1 person1@example.com',
            '.exit',
        ]
        self.assertEqual(
            self.run_command(script), [
                'db > Executed.',
                'db > ',
            ])

        # Second Step: Select from new runtime, then exit.
        script = [
            'select',
            '.exit',
        ]
        self.assertEqual(
            self.run_command(script), [
                'db > (1, user1, person1@example.com)',
                'Executed.',
                'db > ',
            ])

    def test_constants(self):
        '''
        This test will alert us when the constants are changed.
        '''
        self.assertEqual(
            self.run_command(['.constants', '.exit']), [
                'db > Constants:',
                "ROW_SIZE: 293",
                "COMMON_NODE_HEADER_SIZE: 6",
                "LEAF_NODE_HEADER_SIZE: 10",
                "LEAF_NODE_CELL_SIZE: 297",
                "LEAF_NODE_SPACE_FOR_CELLS: 4086",
                "LEAF_NODE_MAX_CELLS: 13",
                "db > ",
            ])

    def test_tree_print(self):
        script = [
            f'insert {i} user{i} person{i}@example.com' for i in (3, 1, 2)
        ]
        script.extend(['.btree', '.exit'])
        self.assertEqual(
            self.run_command(script), [
                'db > Executed.', 'db > Executed.', 'db > Executed.',
                'db > Tree:', 'leaf (size 3)', '  - 0 : 1', '  - 1 : 2',
                '  - 2 : 3', 'db > '
            ])

    def test_duplicate_keys(self):
        script = [
            'insert 1 user1 person1@example.com',
            'insert 1 user1 person1@example.com',
            'select',
            '.exit',
        ]
        self.assertEqual(
            self.run_command(script), [
                'db > Executed.',
                'db > Error: Duplicate key.',
                'db > (1, user1, person1@example.com)',
                'Executed.',
                'db > ',
            ])


if __name__ == '__main__':
    unittest.main()
