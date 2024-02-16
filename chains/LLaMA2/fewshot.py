import csv
from io import StringIO

import requests
import re


def parse_traits(family, syn_char):
    with open(f'combined_traits_{family.lower()}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['trait', 'count'])

        lines = syn_char.split('\n')

        for line in lines:
            line = re.sub(r'^\d+\.\s*', '', line)

            match = re.match(r'(.*?),(.*?)(\d+)', line)
            if match:
                trait = match.group(1).strip()
                count = match.group(3).strip()

                writer.writerow([trait, count])


def is_valid_format(result):
    lines = result.strip().split('\n')

    pattern = re.compile(r'^\d+\.\s.*\|\s.*\|\s.*(\|\s.*)?$')

    for line in lines:
        if not pattern.match(line):
            return False

    return True


class TraitsExtractorV4:
    def __init__(self):
        self.last_response = None
        self.uri = "http://athena521:35504/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.temperature = 0
        self.mode = 'instruct'
        self.character = 'Example'
        self.messages = []

    def _clear_messages(self):
        self.messages = []

    def _send_request(self):
        request = {
            'mode': self.mode,
            'character': self.character,
            'messages': self.messages,
            'temperature': self.temperature,
        }
        response = requests.post(self.uri, headers=self.headers, json=request, verify=False)
        self._clear_messages()
        return response.json()['choices'][0]['message']['content']


    def run(self, line, prompt):
        self._clear_messages()
        self.messages.append({"role": "system", "content": prompt})
        self.messages.append({"role": "user", "content": line})
        assistant_message = self._send_request()
        return assistant_message, self.messages

    def run_with_retries(self, line, prompt, max_attempts=3):
        if max_attempts <= 0:
            # returns the last response even if it's in the wrong format
            return self.last_response, self.messages

        self._clear_messages()
        self.messages.append({"role": "system", "content": prompt})
        self.messages.append({"role": "user", "content": line})
        assistant_message = self._send_request()
        self.last_response = assistant_message 

        if is_valid_format(assistant_message):
            return assistant_message, self.messages
        else:
            return self.run_with_retries(line, prompt, max_attempts - 1)

    def process_csv_data(self, csv_string, step_one_prompt):
        self._clear_messages()
        csv_data = StringIO(csv_string)
        reader = csv.DictReader(csv_data)
        for row in reader:
            message_content = ', '.join([f"{key}: {value}" for key, value in row.items()])
            self.run(message_content, step_one_prompt)

        return self._send_request()

    def final_step(self, characteristics, step_two_prompt):
        self._clear_messages()
        return self.run(characteristics, step_two_prompt)[0]
