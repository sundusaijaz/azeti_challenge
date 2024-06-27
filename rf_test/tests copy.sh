#!/usr/bin/env sh

wait_for_server_ready() {
    local url=$1
    echo "Waiting for server at $url to be ready..."
    while ! curl -s --head --fail $url > /dev/null; do
        echo "Server is not ready yet. Waiting..."
        sleep 2
    done
    echo "Server is ready!"
}

# URL of your server's readiness endpoint
SERVER_URL="http://0.0.0.0:5080/ready"

# Wait for the server to be ready
wait_for_server_ready $SERVER_URL

mkdir -p results

robot -d results test-server.robot

# Capture the exit status of the Robot Framework tests
TEST_EXIT_CODE=$?

exit $TEST_EXIT_CODE