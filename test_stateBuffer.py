from unittest import TestCase
import robot_api


class TestStateBuffer(TestCase):

	def test_set_command(self):

		state_buffer = robot_api.StateBuffer()

		r = state_buffer.set_command('f')
		self.assertEqual(r, 'f')

		x = state_buffer.set_command('b')
		self.assertEqual(x, 'b')

		x = state_buffer.set_command('b')
		self.assertEqual(x, None)




