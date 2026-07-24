from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

from acedatacloud_scaffold.execution import get_execution_owner, is_execute_only
from acedatacloud_scaffold.handlers.base import BaseHandler
from tornado.httputil import HTTPHeaders


class ExecutionOwnerTest(TestCase):
    def test_x402_owner_is_case_insensitive(self):
        headers = {'x-ace-execution-owner': ' X402 '}

        self.assertEqual(get_execution_owner(headers), 'x402')
        self.assertTrue(is_execute_only(headers))

    def test_tornado_headers_preserve_owner_contract(self):
        headers = HTTPHeaders({'x-ace-execution-owner': 'X402'})

        self.assertEqual(get_execution_owner(headers), 'x402')
        self.assertTrue(is_execute_only(headers))

    def test_unknown_or_missing_owner_is_not_execute_only(self):
        self.assertFalse(is_execute_only({}))
        self.assertFalse(is_execute_only({'X-Ace-Execution-Owner': 'router'}))
        self.assertFalse(is_execute_only({'X-Ace-Execution-Owner': ''}))

    @patch('acedatacloud_scaffold.handlers.base.requests.post')
    def test_x402_owner_skips_platform_record(self, post):
        handler = self.make_handler({'X-Ace-Execution-Owner': 'x402'})

        BaseHandler.record(handler)

        post.assert_not_called()

    @patch('acedatacloud_scaffold.handlers.base.requests.post')
    def test_normal_and_unknown_owners_keep_platform_record(self, post):
        post.return_value = SimpleNamespace(status_code=200)
        normal_handler = self.make_handler({})
        unknown_handler = self.make_handler({'X-Ace-Execution-Owner': 'unknown'})

        BaseHandler.record(normal_handler)
        BaseHandler.record(unknown_handler)

        self.assertEqual(post.call_count, 2)
        normal_handler.logger.warning.assert_not_called()
        unknown_handler.logger.warning.assert_called_once_with(
            'unknown execution owner unknown: keep platform usage record'
        )

    @staticmethod
    def make_handler(headers):
        handler = SimpleNamespace(
            request=SimpleNamespace(headers=headers),
            logger=Mock(),
            trace_id='trace',
            payflow=None,
            get_record_trace_id=Mock(return_value='trace'),
            get_record_application_id=Mock(return_value=None),
            get_record_api_id=Mock(return_value=None),
            get_record_task_id=Mock(return_value='task'),
            get_record_user_id=Mock(return_value=None),
            get_record_credential_id=Mock(return_value=None),
            get_record_authorization_id=Mock(return_value=None),
            get_record_actor_user_id=Mock(return_value=None),
            get_record_request=Mock(return_value={}),
            get_record_response=Mock(return_value={'status': 200}),
        )
        return handler