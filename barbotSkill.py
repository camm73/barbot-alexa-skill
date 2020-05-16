from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import SkillBuilder

import boto3

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_intent_name('MakeCocktail'))
def make_cocktail_handler(handler_input):
    if('cocktail' in handler_input.attributes_manager.session_attributes):
        cocktail = handler_input.attributes_manager.session_attributes['cocktail']
        speech = "Making your {} cocktail.".format(cocktail)
        handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "I was unable to understand what cocktail you requested"

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler