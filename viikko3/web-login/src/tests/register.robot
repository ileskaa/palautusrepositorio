*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  foobar
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  fo
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Fail With Message  Username too short

Register With Valid Username And Too Short Password
    Set Username  foobar
    Set Password  foobar1
    Set Password Confirmation  foobar1
    Click Button  Register
    Register Should Fail With Message  Password too short

Register With Valid Username And Invalid Password
    Set Username  foobar
    Set Password  foobarbaz
    Set Password Confirmation  foobarbaz
    Click Button  Register
    Register Should Fail With Message  Invalid password

Register With Nonmatching Password And Password Confirmation
    Set Username  foobar
    Set Password  foobar123
    Set Password Confirmation  foobar12
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Fail With Message  Username already in use

Login After Successful Registration
    Set Username  foobar
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Succeed
    Click Link  ohtu
    Click Button  Logout
    Login Page Should Be Open
    Set Username  kalle
    Set Password  kalle123
    Click Button  Login
    Login Should Succeed

Login After Failed Registration
    Set Username  fo
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Fail With Message  Username too short
    Click Link  /login
    Login Page Should Be Open
    Set Username  fo
    Set Password  foobar123
    Click Button  Login
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Login Should Succeed
    Main Page Should Be Open

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}


Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
