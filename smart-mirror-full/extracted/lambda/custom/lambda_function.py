#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
#
import logging.handlers
import uuid

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer

from ask_sdk_model.interfaces.custom_interface_controller import (
    StartEventHandlerDirective, EventFilter, Expiration, FilterMatchAction,
    StopEventHandlerDirective,
    SendDirectiveDirective,
    Header,
    Endpoint
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
serializer = DefaultSerializer()
skill_builder = CustomSkillBuilder(api_client=DefaultApiClient())


@skill_builder.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput):
    logger.info("== Launch Intent ==")

    response_builder = handler_input.response_builder

    system = handler_input.request_envelope.context.system

    # Get connected gadget endpoint ID.
    endpoints = get_connected_endpoints(handler_input)
    logger.debug("Checking endpoint..")
    if not endpoints:
        logger.debug("No connected gadget endpoints available.")
        return (response_builder
                .speak("Smart mirror not found. Please try again after connecting your gadget.")
                .set_should_end_session(True)
                .response)

    endpoint_id = endpoints[0].endpoint_id

    # Store endpoint ID for using it to send custom directives later.
    logger.debug("Received endpoints. Storing Endpoint Id: %s", endpoint_id)
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr['endpointId'] = endpoint_id

    return (response_builder
            .speak("Welcome to the smart mirror skill! Say help if you want any.")
            .set_should_end_session(False)
            .response)

@skill_builder.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput):
    logger.info("Received HelpIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("You can say rainbow, police, show clock, change color to green or stop")
            .set_should_end_session(False)
            .response)


@skill_builder.request_handler(can_handle_func=is_intent_name("ShowColor"))
def yes_intent_handler(handler_input: HandlerInput):
    logger.info("ShowColor received. Sending color to device.")
    color_slot = "Color"
    
    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder
    
    slots = handler_input.request_envelope.request.intent.slots

    if color_slot in slots:
        color = slots[color_slot].value
        (response_builder
        .speak(f'Alright. Lighting up in {color}')
        .add_directive(build_showcolor_directive(endpoint_id, color))
        .set_should_end_session(True))
    else:
        (response_builder
        .speak("Can you please repeat that?")
        .set_should_end_session(False))


    return response_builder.response

@skill_builder.request_handler(can_handle_func=is_intent_name("ShowRainbow"))
def show_rainbow_intent_handler(handler_input: HandlerInput):
    logger.info("Received ShowRainbowIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Alright. Starting Rainbow!")
            .add_directive(build_rainbow_directive(endpoint_id))
            .set_should_end_session(True)
            .response)

@skill_builder.request_handler(can_handle_func=is_intent_name("BlinkPolice"))
def police_intent_handler(handler_input: HandlerInput):
    logger.info("Received BlinkPoliceIntent.")

    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder
    return (response_builder
            .speak("<amazon:emotion name=\"excited\" intensity=\"high\">Wooooop wooooop!</amazon:emotion>")
            .add_directive(build_police_directive(endpoint_id))
            .set_should_end_session(True)
            .response)

@skill_builder.request_handler(can_handle_func=is_intent_name("ShowClock"))
def clock_intent_handler(handler_input: HandlerInput):
    logger.info("Received ShowClockIntent")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Super! Showing clock!")
            .add_directive(build_clock_directive(endpoint_id))
            .set_should_end_session(True)
            .response)

@skill_builder.request_handler(can_handle_func=is_intent_name("MirrorMirror"))
def clock_intent_handler(handler_input: HandlerInput):
    logger.info("Received MirrorMirrorIntent")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']
    slots = handler_input.request_envelope.request.intent.slots
    response_builder = handler_input.response_builder

    name = 'Zoran'
    if 'Name' in slots:
        name = slots['Name'].value    

    return (response_builder
            .add_directive(build_rainbow_directive(endpoint_id))
            .speak(f'It is you <break time="150ms"/> {name} <break time="100ms"/> of course')
            .set_should_end_session(True)
            .response)


@skill_builder.request_handler(can_handle_func=is_request_type("CustomInterfaceController.Expired"))
def custom_interface_expiration_handler(handler_input):
    logger.info("== Custom Event Expiration Input ==")

    request = handler_input.request_envelope.request
    response_builder = handler_input.response_builder
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    # When the EventHandler expires, send StopLED directive to stop LED animation
    # and end skill session.
    return (response_builder
            .add_directive(build_stop_led_directive(endpoint_id))
            .speak(request.expiration_payload['data'])
            .set_should_end_session(True)
            .response)


@skill_builder.request_handler(can_handle_func=lambda handler_input:
                               is_intent_name("AMAZON.CancelIntent")(handler_input) or
                               is_intent_name("AMAZON.StopIntent")(handler_input))
def stop_and_cancel_intent_handler(handler_input):
    logger.info("Received a Stop or a Cancel Intent..")
    session_attr = handler_input.attributes_manager.session_attributes
    response_builder = handler_input.response_builder
    endpoint_id = session_attr['endpointId']

    # When the user stops the skill, stop the EventHandler,
    # send StopLED directive to stop LED animation and end skill session.
    if 'token' in session_attr.keys():
        logger.debug("Active session detected, sending stop EventHandlerDirective.")
        response_builder.add_directive(StopEventHandlerDirective(session_attr['token']))

    return (response_builder
            .speak("Alright, see you later Alligator!")
            .add_directive(build_stop_led_directive(endpoint_id))
            .set_should_end_session(True)
            .response)


@skill_builder.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    logger.info("Session ended with reason: " +
                handler_input.request_envelope.request.reason.to_str())
    return handler_input.response_builder.response


@skill_builder.exception_handler(can_handle_func=lambda i, e: True)
def error_handler(handler_input, exception):
    logger.info("==Error==")
    logger.error(exception, exc_info=True)
    return (handler_input.response_builder
            .speak("I'm sorry, something went wrong!").response)


@skill_builder.global_request_interceptor()
def log_request(handler_input):
    # Log the request for debugging purposes.
    logger.info("==Request==\r" +
                str(serializer.serialize(handler_input.request_envelope)))


@skill_builder.global_response_interceptor()
def log_response(handler_input, response):
    # Log the response for debugging purposes.
    logger.info("==Response==\r" + str(serializer.serialize(response)))
    logger.info("==Session Attributes==\r" +
                str(serializer.serialize(handler_input.attributes_manager.session_attributes)))


def get_connected_endpoints(handler_input: HandlerInput):
    return handler_input.service_client_factory.get_endpoint_enumeration_service().get_endpoints().endpoints


def build_stop_led_directive(endpoint_id):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='StopLED'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={}
    )

def build_rainbow_directive(endpoint_id):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='Rainbow'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={}
    )

def build_showcolor_directive(endpoint_id, color):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='Color'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={
            'color': color
        }
    )

def build_police_directive(endpoint_id):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='Police'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={}
    )

def build_clock_directive(endpoint_id):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='Clock'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={}
    )

def build_start_event_handler_directive(token, duration_ms, namespace,
                                        name, filter_match_action, expiration_payload):
    return StartEventHandlerDirective(
        token=token,
        event_filter=EventFilter(
            filter_expression={
                'and': [
                    {'==': [{'var': 'header.namespace'}, namespace]},
                    {'==': [{'var': 'header.name'}, name]}
                ]
            },
            filter_match_action=filter_match_action
        ),
        expiration=Expiration(
            duration_in_milliseconds=duration_ms,
            expiration_payload=expiration_payload))


def build_stop_event_handler_directive(token):
    return StopEventHandlerDirective(token=token)


lambda_handler = skill_builder.lambda_handler()
