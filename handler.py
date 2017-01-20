"""
This skill allows you to ask Alexa when the next bin collection is.
"""
from __future__ import print_function

import boto3

from bins import get_next_bin_collection


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        # 'card': {
        #    'type': 'Simple',
        #    'title': "SessionSpeechlet - " + title,
        #    'content': "SessionSpeechlet - " + output
        # },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_collection_day(user_id):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('BinCollectionUsers')

    response = table.get_item(Key={'userid': user_id})
    if 'Item' in response:
        return response['Item']['collection_day']
    else:
        return None


def set_collection_day(user_id, day):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('BinCollectionUsers')

    table.put_item(
        Item={
            'userid': user_id,
            'collection_day': day,
        }
    )


def get_collection_day_from_user(session):
    """
    Ask the user for their collection day
    """
    card_title = "Welcome to the bin collection skill"
    speech_output = "Welcome to the bin collection skill. Start by telling me your regular collection day. For example, you can say, my collection day is Monday."
    should_end_session = False
    reprompt_text = "Please tell me your regular bin collection day, for example, My collecton day is Monday"
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    user_id = session['user']['userId']

    collection_day = get_collection_day(user_id)

    if collection_day is None:
        return get_collection_day_from_user(user_id)
    else:
        collection = get_next_bin_collection(collection_day)
        speech_output = "Your next bin collection is %s %s. " % (" and ".join(collection.types), collection.friendly_date)

        should_end_session = True
        reprompt_text = None
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the bin collection skill."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_user_collection_day(intent, session):
    """Sets the collection day for the user"""
    card_title = "What is your regular collection day"
    session_attributes = {}
    should_end_session = False

    user_id = session['user']['userId']
    collection_day = intent['slots']['collection_day'].get('value', '').upper()

    if collection_day in ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'):
        set_collection_day(user_id, collection_day)
        speech_output = "I have stored your regular collection day as %s. You can now ask, when are the bins collected." % collection_day
        reprompt_text = "To find out your next collection day, just ask, when are the bins collected?"
    elif collection_day in ('SATURDAY', 'SUNDAY'):
        speech_output = "Your collection day must be Monday to Friday. Please tell me your regular collection day, for example, My collection day is Monday"
        reprompt_text = "I'm not sure what your regular bin collection day is. You can tell me by saying, my collection day is Monday"
    else:
        speech_output = "Sorry, I didn't catch that. Please tell me your regular collection day, for example, My collection day is Monday"
        reprompt_text = "I'm not sure what your regular bin collection day is. You can tell me by saying, my collection day is Monday"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "NextCollectionDayIntent":
        return get_welcome_response(session)
    elif intent_name == "MyCollectionDayIntent":
        return set_user_collection_day(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
