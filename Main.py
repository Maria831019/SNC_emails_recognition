from BasicSNC import BasicSNC
from Decision import CaseText
import conf

if __name__ == '__main__':
    #mainObject = BasicSNC('Maria.Kowalska@opuscapita.com', 'Con-essen1', 'https://opusflowtest.service-now.com/')
    mainObject = BasicSNC(conf.usr, conf.pas, 'https://opusflowtest.service-now.com/')

    #calls = mainObject.queue('new_call',
     #              'call_type=email^u_assignment_groupSTARTSWITHOC CS FI^ORu_assignment_groupSTARTSWITHBilling FI&sysparm_limit=10')


    calls = mainObject.queue('new_call','call_type=email^u_assignment_group=16a7e2b60f88de402b58716ce1050e53')

    for element in calls:
        #main loop
        caller = ''
        sh_desc = ''
        desc = ''


        call = mainObject.getCallDetails(element)
        caller = call['caller']
        sh_desc = call['short_description']
        desc = call['description']

        call_object = CaseText(caller,sh_desc,desc)
        print(call_object.sh_description,'====',call_object.language_desc)

        #if language SE or DE return call
        giveBack = {}
        giveBack = call_object.returnToDeSE()

        if giveBack:

            mainObject.updateCall(element,giveBack)
            continue

        #if static rules, jeszcze nie było testowane

        SRules = {}
        SRules = call_object.staticRules()

        if SRules:
            mainObject.updateCall(element, SRules)
            continue

        #let decide if incident or request, for now default option
        Typ = {}
        Typ = call_object.decideType()

        if Typ:
            mainObject.updateCall(element, Typ)

