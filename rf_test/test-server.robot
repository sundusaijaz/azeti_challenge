
*** Settings ***
Documentation     A test suite for checking API behaviour
Library           RequestsLibrary
Suite Setup       Create FlaskApp Session

*** Variables ***
${BASE_URL}       http://0.0.0.0:5080
${ENDPOINT}       /answer

*** Keywords ***
Create FlaskApp Session
    [Documentation]   Creates a reusable session for the FlaskApp
    Create Session    FlaskApp    ${BASE_URL}

*** Test Cases ***
Asking for 'life;universe;everything' gives us 42
    [Documentation]    This test checks if asking for 'life;universe;everything' returns 42
    ${response}=    GET On Session    FlaskApp    ${ENDPOINT}    params=search=life;universe;everything
    Should Be Equal As Strings    ${response.status_code}    200
    Should Be Equal As Strings    ${response.text}    42

Asking for something else gives us unknown
    [Documentation]    This test checks if asking for something else returns 404 and 'unknown'
    ${response}=    GET On Session    FlaskApp    ${ENDPOINT}    params=search=the%20truth   expected_status=404
    Should Be Equal As Strings    ${response.status_code}    404
    Should Be Equal As Strings    ${response.text}    unknown


