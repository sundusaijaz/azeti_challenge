#!/usr/bin/env sh

SERVER_URL="http://0.0.0.0:5080/ready"

# Maximum number of attempts to check the server readiness
MAX_ATTEMPTS=100

wait_for_server_ready() {
    local url=$1
    local max_attempts=$2
    local attempt=1

    echo "Waiting for server at $url to be ready (max attempts: $max_attempts)..."
    while ! curl -s --head --fail $url > /dev/null; do
        if [ $attempt -ge $max_attempts ]; then
            echo "Server did not become ready after $max_attempts attempts."
            return 1
        fi
        echo "Server is not ready yet. Waiting... (Attempt: $attempt)"
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "Server is ready!"
    return 0
}


if wait_for_server_ready $SERVER_URL $MAX_ATTEMPTS; then
    mkdir -p results
    robot -d results test-server.robot
    TEST_EXIT_CODE=$?
else
    echo "Exiting due to server not being ready."
    TEST_EXIT_CODE=1
fi

exit $TEST_EXIT_CODE
