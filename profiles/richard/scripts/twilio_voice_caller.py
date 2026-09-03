#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
twilio_voice_caller.py — Richard Marlowe (Navo24)
Outbound Voice Agent Engine using Twilio & Polly Neural British Voice.
Caller ID: +447360065904
"""

import json
import os
import sys
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say

CREDS_PATH = "/opt/hermes/profiles/richard/twilio_credentials.json"
CALLER_ID = "+447360065904"

def load_client():
    if not os.path.exists(CREDS_PATH):
        raise FileNotFoundError("Twilio credentials not found.")
    with open(CREDS_PATH, "r") as f:
        creds = json.load(f)
    return Client(creds["account_sid"], creds["auth_token"])

def generate_qualification_twiml(client_name="there", company_name="your company"):
    """
    Generates TwiML for an interactive qualification call with British male voice.
    """
    response = VoiceResponse()
    
    # 1. Warm British Business Greeting
    gather = Gather(input='speech', timeout=3, speechTimeout='auto', action='/handle-response')
    gather.say(
        f"Hello {client_name}. This is Richard Marlowe, Senior Sales Manager calling from Navo twenty-four in London. "
        f"I am reaching out regarding ocean container tracking and freight rate API integrations for {company_name}. "
        "Are you currently exploring automated tracking or direct carrier schedules for your logistics workflows?",
        voice='Polly.Brian-Neural',
        language='en-GB'
    )
    response.append(gather)
    
    # Fallback if no speech detected
    response.say(
        "I could not hear your response clearly. I will send our technical API overview and Free Tier access details directly to your email. Have a wonderful day.",
        voice='Polly.Brian-Neural',
        language='en-GB'
    )
    return str(response)

def make_call(to_number, twiml_content=None, twiml_url=None):
    client = load_client()
    print(f"Initiating outbound call from {CALLER_ID} to {to_number}...")
    
    call_kwargs = {
        "to": to_number,
        "from_": CALLER_ID,
    }
    if twiml_content:
        call_kwargs["twiml"] = twiml_content
    elif twiml_url:
        call_kwargs["url"] = twiml_url
    else:
        call_kwargs["twiml"] = generate_qualification_twiml()
        
    call = client.calls.create(**call_kwargs)
    print(f"Call successfully placed! SID: {call.sid} | Status: {call.status}")
    return call.sid

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_num = sys.argv[1]
        make_call(target_num)
    else:
        print(f"Twilio Outbound Caller Ready. Verified Caller ID: {CALLER_ID}")
