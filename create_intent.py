import json
import os
import dialogflow_v2
from dotenv import load_dotenv


def main():
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open("questions.json", "r", encoding="UTF-8") as file:
        questions = json.load(file)

    for key, value in questions.items():
        training_phrases = [{"text": question} for question in value['questions']]
        project_id = os.getenv('PROJECT_ID')

        client = dialogflow_v2.IntentsClient()
        parent = client.project_agent_path(project_id)
        intent = {
            "display_name": key,
            "messages": [{
                "text":
                {"text": [value['answer']]}
            }],
            "training_phrases": [
                {
                    "parts": training_phrases
                },
            ]
        }

        response = client.create_intent(parent, intent)

    return response


if __name__ == '__main__':
    main()