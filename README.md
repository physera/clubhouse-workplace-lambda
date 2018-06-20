# Clubhouse integration for Facebook Workplace via AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Clubhouse](https://clubhouse.io) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.
For an overview of the approach, see [this document](https://github.com/physera/workplace-lambda).

## Setup

To make this work, first follow the instructions [here](https://github.com/physera/workplace-lambda#setup). Then you'll need to set things up on Clubhouse.

### Set up AWS Lambda

In addition to the environment variables you've set following the document above, you'll also need to set:
* `CLUBHOUSE_WEBHOOK_SECRET` - Set this to a sufficiently long/complicated secret key you want to use to sign Github requests. Take note of it

### Set up callbacks on Clubhouse

We now just need to make sure Clubhouse calls your endpoint whenever something happens.

* From the Settings dropdown select Integrations.
* Choose `Webhooks` from the modal.  Then hit `Add New Webhook`.
* For the Payload URL, enter in the URL for the API Gateway trigger.
* For Secret, put in the value you created for `CLUBHOUSE_WEBHOOK_SECRET`.

## Version History

* 2018-06-19 Initial release
