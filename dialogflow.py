import dialogflow_v2 as df
import os
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
LANGUAGE_CODE = 'ru'


class DialogFlow:
    def __init__(self, project_id, session_id):
        self.project_id = project_id
        self.session_id = session_id
        self.session_client = df.SessionsClient()
        self.session = self.session_client.session_path(project=self.project_id, session=self.session_id)

    def take_response_from_df(self, message_text):
        text_input = df.types.TextInput(text=message_text, language_code=LANGUAGE_CODE)
        query_input = df.types.QueryInput(text=text_input)
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
            return response
        except InvalidArgument:
            raise



# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
# PROJECT_ID = 'newagent-kxlv'
# LANGUAGE_CODE = 'ru'
#
# session_client = df.SessionsClient()
#
# session = session_client.session_path(project=PROJECT_ID, session='9776279114c486ac88a834300f75209287a000f2')
#
# text_to_be_analyzed = "привет"
# text_input = df.types.TextInput(text=text_to_be_analyzed, language_code=LANGUAGE_CODE)
# query_input = df.types.QueryInput(text=text_input)
# try:
#     response = session_client.detect_intent(session=session, query_input=query_input)
# except InvalidArgument:
#     raise

# print("Query text:", response.query_result.query_text)
# print("Detected intent:", response.query_result.intent.display_name)
# print("Detected intent confidence:", response.query_result.intent_detection_confidence)
# print("Fulfillment text:", response.query_result.fulfillment_text)