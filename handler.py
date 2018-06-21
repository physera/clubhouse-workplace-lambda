import hashlib
import hmac
import json
import os

from botocore.vendored import requests


def lambda_handler(event, context):
    post_headers = {
        "Authorization": "Bearer {}".format(os.environ['FB_API_TOKEN']),
    }
    post_url = "https://graph.facebook.com/{}/feed".format(
        os.environ['FB_GROUP_ID'],
    )

    headers = event["headers"]
    body = event["body"]

    computed_signature = hmac.new(
        bytes(os.environ["CLUBHOUSE_WEBHOOK_SECRET"], "UTF-8"),
        bytes(body, "UTF-8"),
        hashlib.sha256,
    ).hexdigest()

    signature = headers.get("Clubhouse-Signature")

    if computed_signature != signature:
        print("Invalid signature: ", computed_signature, signature)
        return {"statusCode": 400, "body": "Invalid signature"}

    body = json.loads(body)
    print(body)

    msg = None
    story_id = None
    title = None
    url = None

    # Get the story id, title, and url.
    for action in body.get("actions"):
        if action.get("entity_type") == "story":
            story_id = action.get("id")
            title = action.get("name")
            url = action.get("app_url")

    if not story_id:
        return {"statusCode": 200, "body": "No story reference found."}

    member_name = requests.get(
        "https://api.clubhouse.io/api/v2/members/{}?token={}".format(
            body.get("member_id"),
            os.environ["CLUBHOUSE_API_TOKEN"],
        ),
    ).json().get('profile', {}).get('mention_name')

    project_id = requests.get(
        "https://api.clubhouse.io/api/v2/stories/{}?token={}".format(
            story_id,
            os.environ["CLUBHOUSE_API_TOKEN"],
        ),
    ).json().get('project_id')

    project_name = None
    if project_id:
        project_name = requests.get(
            "https://api.clubhouse.io/api/v2/projects/{}?token={}".format(
                project_id,
                os.environ["CLUBHOUSE_API_TOKEN"],
            ),
        ).json().get('name')

    # TODO:
    # * Allow redirecting posts depending on project.

    for action in body.get("actions"):
        a = action.get("action")
        if a != "create":
            print("Warning: Only create actions supported: ", action)
            continue
        if action.get("entity_type") == "story-comment":
            verb = "commented on a story"
            text = action.get("text")
        elif action.get("entity_type") == "story":
            verb = "requested a new story"
            text = action.get("description")
        else:
            print("Warning: Unsupported entity type: ", action)
            continue

        if project_name:
            project = "[{}] ".format(project_name)

        msg = "## {}**{}** {}:\n[[#{}] {}]({})\n>{}".format(
            project,
            member_name,
            verb,
            story_id,
            title,
            url,
            text,
        )

    if msg:
        data = {
            'formatting': 'MARKDOWN',
            'message': msg,
        }
        requests.post(post_url, headers=post_headers, data=data)
        print("Posted to group!")

    return {"statusCode": 200, "body": "Victory!"}
