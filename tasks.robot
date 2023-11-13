*** Settings ***
Library             Scripts/TribalWarsFarmBot.py
Library             Scripts/TribalWarsAdvancedFarmBot.py
Library             Scripts/TribalWarsGatheringBot.py

*** Keywords ***
Variable Documentation
    [Documentation]
    ...    ${INTERVAL_MIN_A}: Miniaml interval between running farm script in minutes
    ...    ${INTERVAL_MAX_A}: Maximal interval between running farm script in minutes
    ...    ${SWITCH_SIDES_A}: Farm on all pages - true; first - false
    ...    ${INTERVAL_MIN_GATHERING}: Miniaml interval between running gathering script in minutes
    ...    ${INTERVAL_MAX_GATHERING}: Maximal interval between running gathering script in minutes
    ...    ${GET_INTERVAL_GATHERING}: Get's the interval from site after sending gathering
    Pass Execution        End of Description

*** Variables ***
#Farm
${INTERVAL_MIN}    30
${INTERVAL_MAX}    47
${SWITCH_PAGES}    True

#Gathering
${INTERVAL_MIN_GATHERING}    30
${INTERVAL_MAX_GATHERING}    47
${GET_INTERVAL_GATHERING}    False



*** Test Cases ***
Farm A
    Tribal Wars Farm    a    ${INTERVAL_MIN}    ${INTERVAL_MAX}    ${SWITCH_PAGES}

Farm B
    Tribal Wars Farm    b    ${INTERVAL_MIN}    ${INTERVAL_MAX}    ${SWITCH_PAGES}

Farm C
    Tribal Wars Farm    c    ${INTERVAL_MIN}    ${INTERVAL_MAX}    ${SWITCH_PAGES}

Farm Advanced
    Tribal Wars Advanced Farm    ${INTERVAL_MIN}    ${INTERVAL_MAX}    ${SWITCH_PAGES}


Gather 4 Levels
    Tribal Wars Gather  ${INTERVAL_MIN_GATHERING}    ${INTERVAL_MAX_GATHERING}    ${GET_INTERVAL_GATHERING}
