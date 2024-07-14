# PyServer

a basic web server that handles HTTP requests and generates appropriate responses.

## Files

1. **webserver.py**: Contains the server implementation.
2. **webclient.py**: Contains the client implementation.
3. **test_webserver.py**: Contains the unit tests for the server.

## File Descriptions

### 1. webserver.py

This file contains the main server code, including request handlers, decorators for logging and authorization, and a singleton context manager for the server.

#### Key Components:

- **Decorators**:

  - `log_request`: Logs the incoming requests with timestamps.
  - `authorize_request`: Checks if a request is authorized based on the username.

- **Generators**:

  - `response_generator`: Generates a response string for a given method.
  - `streaming_response_generator`: Asynchronous generator that yields chunks of a response body with a delay.

- **Iterators**:

  - `RequestIterator`: Synchronous iterator to manage multiple requests.
  - `AsyncRequestIterator`: Asynchronous iterator to manage multiple requests.

- **Request Handlers**:

  - `BaseRequestHandler`: Base class to handle requests based on their method.
  - `GetRequestHandler`: Handles GET requests.
  - `PostRequestHandler`: Handles POST requests.

- **Asynchronous Functions**:

  - `async_request_handler`: Handles client requests asynchronously.
  - `stop_server_after_delay`: Stops the server after a delay.

- **Singleton Metaclass**:

  - `Singleton`: Ensures only one instance of the server context manager.

- **Server Context Manager**:

  - `ServerContextManager`: Manages the server's operation using the singleton pattern.

- **Main Function**:
  - `main`: Runs the server and handles incoming connections.

### 2. webclient.py

This file contains the client code that connects to the server, sends requests, and prints the responses.

#### Key Components:

- **Sample Requests**: A list of sample requests to be sent to the server.
- **Singleton Metaclass**: Ensures only one instance of the client context manager.
- **Client Context Manager**: Manages the client's socket operations using the singleton pattern.

### 3. test_webserver.py

This file contains unit tests for the server components using the `unittest` framework and `unittest.mock` for mocking dependencies.

#### Test Cases:

- **TestLogRequestDecorator**: Tests the `log_request` decorator.
- **TestAuthorizeRequestDecorator**: Tests the `authorize_request` decorator.
- **TestResponseGenerator**: Tests the `response_generator` function.
- **TestStreamingResponseGenerator**: Tests the `streaming_response_generator` function.
- **TestAsyncRequestIterator**: Tests the `AsyncRequestIterator` class.
- **TestBaseRequestHandler**: Tests the `BaseRequestHandler` class.
- **TestGetRequestHandler**: Tests the `GetRequestHandler` class.
- **TestPostRequestHandler**: Tests the `PostRequestHandler` class.
- **TestSingleton**: Tests the `Singleton` metaclass.
- **TestServerContextManager**: Tests the `ServerContextManager` class.

## Running the Server

To run the server, execute the following command:

Windows:

```bash
python webserver.py
```

MacOS:

```bash
python3 webserver.py
```

## Running the Client

To run the client, execute the following command in a seperate terminal:

Windows:

```bash
python webclient.py
```

MacOS:

```bash
python3 webclient.py
```

## Running the Tests

To run the unit tests, execute the following command:

Windows:

```bash
python -m unittest test_webserver.py
```

MacOS:

```bash
python3 -m unittest test_webserver.py
```
