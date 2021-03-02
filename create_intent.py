import json
import os
import dialogflow_v2
from dotenv import load_dotenv


def main():
    load_dotenv()
    with open("questions.json", "r", encoding="UTF-8") as file:
        questions = json.load(file)

    for topic, questions in questions.items():
        training_phrases = [{"text": question} for question in questions['questions']]
        project_id = os.getenv('PROJECT_ID')

        client = dialogflow_v2.IntentsClient()
        parent = client.project_agent_path(project_id)
        intent = {
            "display_name": topic,
            "messages": [{
                "text":
                {"text": [questions['answer']]}
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