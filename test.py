from subprocess import Popen, PIPE
import unittest


class DBTestCase(unittest.TestCase):

	def run_command(self, input_lines):
		stdin = '{}\n'.format('\n'.join(input_lines))
		with Popen('./db', stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True) as proc:
			output = proc.communicate(stdin)
		return output[0].split('\n')

	def test_insert_select(self):
		'''
		Test simple insert and select statement
		'''
		self.assertEqual(self.run_command([
			'insert 1 user1 person1@example.com',
			'select',
			'.exit'
		]), [
			'db > Executed.',
			'db > (1, user1, person1@example.com)',
			'Executed.', 'db > ',
		])

	def test_error_message_table_full(self):
		'''
		Prints an error message when table is full (after 1400 rows)
		'''
		fill_stdin = ['insert {0} user{0} person{0}@example.com'.format(index) for index in range(1, 1402)] + ['.exit']
		self.assertEqual(self.run_command(fill_stdin)[-2], 'db > Error: Table full.')

	def test_allows_inserting_strings_of_maximum_length(self):
		long_username = 'a' * 32
		long_email = 'a' * 255
		script = [
			'insert 1 {} {}'.format(long_username, long_email),
			'select',
			'.exit'
		]
		self.assertEqual(self.run_command(script), [
			'db > Executed.',
			'db > (1, {}, {})'.format(long_username, long_email),
			'Executed.',
			'db > '
		])

	def test_prints_error_message_if_strings_too_long(self):
		long_username = 'a' * 33
		long_email = 'a' * 256
		script = [
			'insert 1 {} {}'.format(long_username, long_email),
			'select',
			'.exit'
		]
		self.assertEqual(self.run_command(script), [
			'db > String is too long.',
			'db > Executed.',
			'db > '
		])

	def test_prints_an_error_message_if_id_is_negative(self):
		script = [
			'insert -1 cstack foo@bar.com',
			'select',
			'.exit',
		]
		self.assertEqual(self.run_command(script), [
			'db > ID must be positive.',
			'db > Executed.',
			'db > '
		])


if __name__ == '__main__':
	unittest.main()
