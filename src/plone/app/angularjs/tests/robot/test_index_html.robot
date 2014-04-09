# bin/robot-server plone.app.angularjs.testing.PLONE_APP_ANGULARJS_ROBOT_TESTING
# bin/robot src/plone/app/angularjs/tests/robot/test_index_html.robot
*** Settings ***

Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${ADMIN_ROLE}  Site Administrator

*** Test Cases ***

Site Administrator can access control panel
    Given I'm logged in as a '${ADMIN_ROLE}'
     When I open the personal menu
     Then I see the Site Setup -link

*** Keywords ***

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

I open the personal menu
    Click link  css=#user-name

I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup
