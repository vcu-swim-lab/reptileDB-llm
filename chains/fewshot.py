import csv
from io import StringIO
import requests

B_INST, E_INST = "<s>[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

SYSTEM_PROMPT = B_SYS + PROMPT + E_SYS


def get_prompt(instruction):
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template


class TraitsExtractorV4:
    def __init__(self):
        self.uri = "http://athena512:45395/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.temperature = 0
        self.mode = 'instruct'
        self.character = 'Example'

    def _send_request(self, messages):
        request = {
            'mode': self.mode,
            'character': self.character,
            'messages': messages,
            'temperature': self.temperature,
        }
        response = requests.post(self.uri, headers=self.headers, json=request, verify=False)
        return response.json()['choices'][0]['message']['content']

    def run(self, line, prompt):
        messages = [{"role": "system", "content": prompt}, {"role": "user", "content": "[INST]" + line + "[/INST]"}]
        assistant_message = self._send_request(messages)
        messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message, messages

    def process_csv_data(self, csv_string, step_one_prompt):
        messages = []
        csv_data = StringIO(csv_string)
        reader = csv.DictReader(csv_data)
        for row in reader:
            message_content = ', '.join([f"{key}: {value}" for key, value in row.items()])
            messages = [{"role": "system", "content": step_one_prompt + " " + message_content + "[/INST]"}]
        return self._send_request(messages)

    def final_step(self, characteristics, step_two_prompt):
        messages = [{"role": "system", "content": step_two_prompt + "[INST]" + characteristics + "[/INST]"}]
        return self._send_request(messages)
