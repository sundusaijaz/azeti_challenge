# azeti Coding Challenge

Welcome, and thank you very much for taking the time to participate in this
challenge!

# :alarm_clock: Logistics and Expectations

We know that you'd be using your precious free time to work on this challenge
and therefore, we want to set clear expectations to ensure that your time is
spent reasonably, and to avoid that, you waste or invest too much of it.
Again we appreciate your participation.

__How much time should I spend?__

_A reasonable amount of time is a couple of hours, if you are aware of the
technologies, we guess you would be able to complete this in less than
2 hours._

__How do we evaluate the results?__

_We will not grade or evaluate based on quantity but on quality. Apart from
implementing the asked stuff, feel free to add any comments or remarks that
you may find relevant._
 
__How can I submit my results?__

_First, copy this repository to your GitHub, GitLab, Bitbucket, or any other
git repository. Secondly, commit your code to it and share the link to your
repository with us. Make sure we can read your repository. We will then review your code._

__How much time do I have to complete this challenge?__

_You will have a maximum of 1 week after receiving this challenge.
Again, take the quality into consideration, don't rush!_

# Challenge Overview

In this repository, you will find the source code of a very simple server that
responds to REST queries and sends information via MQTT.

You will have to:
* Create a python script that receives a value via MQTT and submits it to REST
* Create a Robot Framework test that ensures the server will reply in a certain
  way, depending on the arguments

For convenience, we use `docker compose` to coordinate the services. Your code
should also run as a service (all the setup is already prepared by us).

## The client

One of the things to implement will be a client script that:
1. Subscribes to MQTT topic `secret/number`
2. Obtain the number sent by the server
3. Write this number to the REST server as POST /secret_number (with proper
   formatting)

Some base code was already prepared in `client/client.py`.

## RF Test

Another important thing to implement will be the Robot Framework tests. They
are very important to validate the features in an automated way.

In this case, you need to write 2 tests on `test-server.robot`, where you
check:
* The response from the REST when asking for "life;universe;everything"
* The response from the REST when asking for "the truth"

Some base code was already prepared in `rf_test/test-server.robot`.

When executed, the test results should be saved to the `results/` directory.

## The server

The server implements the following REST resources:
* GET /answer - Expects a `search` query
* POST /secret_number - Expects a JSON body with a `value` parameter
* GET /secret_correct - Returns 'YES' or 'NO' depending on if the number set via
  `/secret_number` is the same as the one sent via MQTT
* GET /ready - Always replies 'OK', as long as the server is running

Apart from REST, this server also connects to an MQTT broker and will
publish a JSON representation of the secret number to the MQTT topic
`secret/number`.

**Remember, you should not change anything on the server code**

It is advised that you expose the ports on docker compose, use a REST and an mqtt
Client to check by yourself and also take a look at the server code as
reference.

## MQTT broker

We use the public eclipse-mosquitto:1.6 image as a simple example of an MQTT
broker. You don't need to change anything here.

The client part should connect to this broker to receive the secret number.

# Technology

In both cases – Client and RF Test – you can change the Dockerfile. In fact, we
encourage it, as it might give a better test quality and reliability.

The only mandatory things are:
* You should not change the server code
* You have to use Robot Framework

# How to run

You should be able to run the code as is by executing `docker compose up`.
Make sure to have docker properly installed, configured, and updated before starting.
