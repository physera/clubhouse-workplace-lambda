# Clubhouse integration for Facebook Workplace via AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Clubhouse](https://clubhouse.io) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.
For an overview of the approach, see [this document](https://github.com/physera/workplace-lambda).

## Setup

To make this work, first follow the instructions [here](https://github.com/physera/workplace-lambda#setup). Then you'll need to set things up on Clubhouse.

### Set up callbacks on Clubhouse

We need to make sure Clubhouse calls your endpoint whenever something happens.

* From the Settings dropdown select Integrations.
* Choose `Webhooks` from the modal.  Then hit `Add New Webhook`.
* For the Payload URL, enter in the URL for the API Gateway trigger.
* For Secret, put in the value you plan on using for `CLUBHOUSE_WEBHOOK_SECRET` (see below).

Since the webhooks payload doesn't contain all the information we need, we also need to get an API key.

* From the Settings dropdown select Settings.
* Choose `API Tokens` from the sidebar.
* Generate a token and take note of it.

### Set up AWS Lambda

In addition to the environment variables you've set following the document above, you'll also need to set:
* `CLUBHOUSE_WEBHOOK_SECRET` - Set this to a sufficiently long/complicated secret key you want to use to sign Github requests. Take note of it
* `CLUBHOUSE_API_TOKEN` - Set this to the API token you got when you got the Clubhouse API token.

## Version History

* 2018-06-19 Initial release
