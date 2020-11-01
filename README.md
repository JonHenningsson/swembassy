# swembassy
__swembassy__ is a simple tool that will check availability for passport appointments at the Swedish Embassies in Washington D.C. and New York.

## How it works
The script uses HTTP to interact with the Migrationsverket website and retrieve the availability. Once found, it will use Twilio API to send a text message to the configured receiver.

## Package dependencies
`pip install requests twilio`

## Use the script
First set the required environment variables:
- twilio_account_sid
- twilio_auth_token
- twilio_from_no
- twilio_to_no

and run:
`python index.py`
