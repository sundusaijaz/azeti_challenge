
*** Settings ***
Documentation     A test suite for checking the /answer Endpoint
Library           RequestsLibrary

*** Variables ***
${BASE_URL}       http://0.0.0.0:5080
${ENDPOINT}       /answer

*** Test Cases ***
Asking for 'life;universe;everything' give us 42
    Create Session    FlaskApp    ${BASE_URL}
    ${response}=    GET On Session    FlaskApp    ${ENDPOINT}    params=search=life;universe;everything
    Should Be Equal As Strings    ${response.status_code}    200
    Should Be Equal As Strings    ${response.text}    42


Asking for something else give us unknown
    Create Session    FlaskApp    ${BASE_URL}
    ${response}=    GET On Session    FlaskApp    ${ENDPOINT}    params=search=the%20truth   expected_status=404
    Should Be Equal As Strings    ${response.status_code}    404
    Should Be Equal As Strings    ${response.text}    unknown

