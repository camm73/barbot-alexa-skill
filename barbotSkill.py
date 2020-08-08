from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response, IntentConfirmationStatus
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import SkillBuilder

import boto3
import json
import secrets
import time

iotClient = boto3.client('iot-data', region_name='us-east-1')

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_intent_name('MakeCocktail'))
def make_cocktail_handler(handler_input):
    print('Make Cocktail intent')
    if('cocktail' in handler_input.request_envelope.request.intent.slots):
        cocktail = handler_input.request_envelope.request.intent.slots['cocktail'].value
        confirmationStatus = handler_input.request_envelope.request.intent.confirmation_status

        if(confirmationStatus == IntentConfirmationStatus.CONFIRMED):
            speech = "Making your {} cocktail.".format(cocktail)
            #handler_input.response_builder.set_should_end_session(True)

            iotPayload = {
                "action": "makeCocktail",
                "data": cocktail.lower()
            }

            print('Publishing request to make cocktail')
            iotResponse = iotClient.publish(
                topic='barbot-main',
                qos=1,
                payload=json.dumps(iotPayload)
            )

            print(iotResponse)
        else:
            speech = "OK. Ask me again when you're ready to make your cocktail."
            #handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "I was unable to understand what cocktail you requested"

    handler_input.response_builder.set_should_end_session(True)
    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name('MenuIntent'))
def handle_menu(handler_input):
    iotPayload = {
        "action": "getMenu"
    }

    iotResponse = iotClient.publish(
        topic='barbot-main',
        qos=1,
        payload=json.dumps(iotPayload)
    )

    time.sleep(1)

    menuResponse = iotClient.get_thing_shadow(thingName='BarBot')

    parsedRes = json.loads(menuResponse['payload'].read().decode('utf-8'))

    menuArr = parsedRes['state']
    menuArr = menuArr['desired']['menu']

    if(len(menuArr) > 0):
        speech = "Today's menu includes: "

        if(len(menuArr) > 1):
            #List out the available drinks
            for i in range(len(menuArr) - 1):
                speech += menuArr[i] + ', '

            #Add final item
            speech += 'and ' + menuArr[-1] + "."
        else:
            speech += menuArr[-1] + '.'
    else:
        speech = "There is nothing on the menu right now. Try adding some ingredients in the Bar Bot mobile app."
    
    handler_input.response_builder.set_should_end_session(True)
    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name('SetAlcoholModeIntent'))
def set_alcohol_mode(handler_input):
    if('setting' in handler_input.request_envelope.request.intent.slots):
        mode_setting = handler_input.request_envelope.request.intent.slots['setting'].value

        if(mode_setting == 'on'):
            speech = 'OK. Turning on alcohol mode.'
            mode_setting = True
        elif(mode_setting == 'off'):
            speech = "OK. Turning off alcohol mode."
            mode_setting = False
        else:
            speech = "Sorry. I couldn't understand what you said."

        iotPayload = {
            "action": "alcoholMode",
            "data": mode_setting
        }

        iotResponse = iotClient.publish(
            topic='barbot-main',
            qos=1,
            payload=json.dumps(iotPayload)
        )
        
    else:
        speech = "I was unable to understand whether you want to turn alcohol mode on or off."
    
    handler_input.response_builder.set_should_end_session(True)
    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name('AMAZON.FallbackIntent'))
def fallback(handler_input):
    speech = "I'm sorry. I'm not sure how to handle that request."
    handler_input.response_builder.speak(speech)

    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name('AMAZON.HelpIntent'))
def help(handler_input):
    speech = 'You can ask me for the cocktail menu, to make you a cocktail, or set alcohol mode.'
    handler_input.response_builder.speak(speech)

    return handler_input.response_builder.response

lambda_handler = sb.lambda_handler()