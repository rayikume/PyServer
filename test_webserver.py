import unittest
import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from webserver import (
    log_request, authorize_request, response_generator,
    streaming_response_generator, AsyncRequestIterator, 
    BaseRequestHandler, GetRequestHandler, PostRequestHandler,
    async_request_handler, Singleton, ServerContextManager
)

class TestLogRequestDecorator(unittest.IsolatedAsyncioTestCase):
    @patch('webserver.datetime')
    async def test_log_request(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)
        @log_request
        async def sample_function():
            return "Success"
        result = await sample_function()
        self.assertEqual(result, "Success")

class TestAuthorizeRequestDecorator(unittest.IsolatedAsyncioTestCase):
    async def test_authorize_request(self):
        requests = [
            {"Username": "Luca"},
            {"Username": "Bjorn"}
        ]
        
        @authorize_request
        async def sample_function(request):
            return request
        
        for request in requests:
            result = await sample_function(request)
            if request["Username"].lower() == "luca":
                self.assertTrue(result["Access"])
            else:
                self.assertFalse(result["Access"])

class TestResponseGenerator(unittest.TestCase):
    def test_response_generator(self):
        response = response_generator("Test Response", "GET")
        self.assertEqual(next(response), f"[{datetime.datetime.now().strftime("%d/%m/%Y %I %p")}]: Received /GET Response: Test Response")

class TestStreamingResponseGenerator(unittest.IsolatedAsyncioTestCase):
    async def test_streaming_response_generator(self):
        chunks = ["chunk1", "chunk2"]
        gen = streaming_response_generator(chunks)
        result = [chunk async for chunk in gen]
        self.assertEqual(result, chunks)

class TestAsyncRequestIterator(unittest.IsolatedAsyncioTestCase):
    async def test_aiterator(self):
        requests = [{"Username": "Luca"}]
        iterator = AsyncRequestIterator(requests)
        result = [req async for req in iterator]
        self.assertEqual(result[0]["Username"], "Luca")

class TestGetRequestHandler(unittest.IsolatedAsyncioTestCase):
    async def test_handle_request(self):
        handler = GetRequestHandler()
        response = await handler.handle_request()
        self.assertEqual(next(response), f"[{datetime.datetime.now().strftime("%d/%m/%Y %I %p")}]: Received /GET Response: Imagine you got what you asked for")

class TestPostRequestHandler(unittest.IsolatedAsyncioTestCase):
    async def test_handle_request(self):
        handler = PostRequestHandler()
        response = await handler.handle_request()
        self.assertEqual(next(response), f"[{datetime.datetime.now().strftime("%d/%m/%Y %I %p")}]: Received /POST Response: Successful submission!")

class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        class SingletonClass(metaclass=Singleton):
            pass
        instance1 = SingletonClass()
        instance2 = SingletonClass()
        self.assertIs(instance1, instance2)

class TestServerContextManager(unittest.TestCase):
    @patch('socket.socket')
    def test_server_context_manager(self, mock_socket):
        with ServerContextManager() as server:
            mock_socket.assert_called()
            mock_socket.return_value.bind.assert_called_with(('', 5000))
            mock_socket.return_value.listen.assert_called_with(5)
        mock_socket.return_value.close.assert_called()

if __name__ == '__main__':
    unittest.main()
