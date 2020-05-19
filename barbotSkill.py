from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response, IntentConfirmationStatus
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import SkillBuilder

import boto3
import json

iotClient = boto3.client('iot-data', region_name='us-east-1')

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_intent_name('MakeCocktail'))
def make_cocktail_handler(handler_input):
    if('cocktail' in handler_input.request_envelope.request.intent.slots):
        cocktail = handler_input.request_envelope.request.intent.slots['cocktail'].value
        print(handler_input.request_envelope.request.intent.confirmation_status)
        confirmationStatus = handler_input.request_envelope.request.intent.confirmation_status

        if(confirmationStatus == IntentConfirmationStatus.CONFIRMED):
            speech = "Making your {} cocktail.".format(cocktail)
            handler_input.response_builder.set_should_end_session(True)

            iotPayload = {
                "action": "makeCocktail",
                "data": cocktail.lower()
            }

            iotResponse = iotClient.publish(
                topic='barbot-main',
                qos=1,
                payload=json.dumps(iotPayload)
            )

            print(iotResponse)
        else:
            speech = "OK. Ask me again when you are ready to make your cocktail."
            handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "I was unable to understand what cocktail you requested"

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()