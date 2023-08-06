import random
import unittest
from automation.utils import dictionarize
from unittest.mock import Mock
from faker import Faker

class AutomationTests(unittest.TestCase):

    def test_dictionarize(self):
        fake = Faker()
        fetchall_return_value = [
            [
                id, 
                fake.name(), 
                fake.address(), 
                ','.join([fake.name() for _ in range(random.randint(1, 4))])
            ]
            for id in range(10)
        ]

        cursor = Mock()
        cursor.description = [['id'], ['name'], ['address'], ['friends'],]
        cursor.fetchall.return_value = fetchall_return_value

        # check simple case
        actual = dictionarize(cursor)
        self.assertEqual(len(fetchall_return_value), len(actual['results']))
        for index, result in enumerate(actual['results']):
            self.assertEqual(fetchall_return_value[index][0], result['id'])
            self.assertEqual(fetchall_return_value[index][1], result['name'])
            self.assertEqual(fetchall_return_value[index][2], result['address'])
            self.assertEqual(fetchall_return_value[index][3], result['friends'])

        # check page size with no truncation
        actual = dictionarize(cursor, page_size=20)
        self.assertFalse(actual['more'])

        # check page size with truncation
        actual = dictionarize(cursor, page_size=8)
        self.assertTrue(actual['more'])
        self.assertEqual(len(actual['results']), 8)

        # check list_columns parameter
        actual = dictionarize(cursor, list_columns=['friends'], list_seperator=',')
        for index, result in enumerate(actual['results']):
            self.assertEqual(fetchall_return_value[index][3], ','.join(result['friends']))

if __name__ == '__main__':
    unittest.main()
