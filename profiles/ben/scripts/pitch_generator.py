import os
import json
import time
import re
import urllib.request
import urllib.error
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1INt0_J996CYbuiKxndLtfpCfMEDdgYcuLUaO-xMbDIk"
TOKEN_PATH = "/opt/hermes/google_token.json"

def send_wa(phone, text):
    url = "http://localhost:3050/send-message"
    data = json.dumps({"phone": phone, "message": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def generate_pitch(name, city, niche, rating):
    if "Auto" in niche or "Mechanic" in niche or "Tire" in niche:
        return f"Hi {name}! I came across your auto shop on Google Maps in {city} and was really impressed by your {rating}★ rating and customer reviews.\n\nI noticed you don't currently have an official website or online booking system on your profile, which means you might be missing high-ticket service appointments to competitors who take 24/7 online bookings.\n\nAt Avalanche Agency, we build high-converting websites with built-in 24/7 AI Receptionists that automatically answer customer inquiries and book appointments directly into your calendar in under 48 hours ($490).\n\nWould you be open to seeing a quick 2-minute live demo customized for {name}?\n\nBest regards,\nBen Jett | Avalanche Agency\nhttps://aavalanche.com/ai-sales-agent"
    elif "Dental" in niche or "MedSpa" in niche or "Clinic" in niche:
        return f"Hello {name}! I found your clinic on Google Maps in {city} with an impressive {rating}★ rating.\n\nI noticed you don't have a direct online patient booking system on your listing. Many patients looking for {niche} in {city} prefer booking online instantly 24/7.\n\nAt Avalanche Agency, we create modern clinic landing pages with 24/7 AI Patient Booking Assistants in 48 hours ($490).\n\nCould I send over a quick 2-minute live prototype tailored for {name}?\n\nBest regards,\nBen Jett | Avalanche Agency\nhttps://aavalanche.com/ai-sales-agent"
    else:
        return f"Hi {name}! Noticed your top-rated business on Google Maps in {city} ({rating}★).\n\nI saw you don't currently have an official website attached to your listing. We build high-converting websites with built-in 24/7 AI Sales Assistants that capture leads and book appointments automatically in 48h ($490).\n\nWould you be interested in a quick 2-minute live demo customized for {name}?\n\nBest regards,\nBen Jett | Avalanche Agency\nhttps://aavalanche.com/ai-sales-agent"
