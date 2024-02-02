import csv
from io import StringIO

import requests
import re


def split_into_chunks(text, chunk_size=250):
    """
    Splits text into chunks for Llama2 to process without sentences being cut-off.
    """
    words = text.split()
    chunks = []
    index = 0

    while index < len(words):
        if index + chunk_size < len(words):
            look_ahead_index = index + chunk_size
            while look_ahead_index > index and words[look_ahead_index - 1][-1] not in '.?!':
                look_ahead_index -= 1

            if look_ahead_index == index:
                look_ahead_index = index + chunk_size
        else:
            look_ahead_index = len(words)

        chunk = words[index:look_ahead_index]
        chunks.append(' '.join(chunk))
        index = look_ahead_index

    return chunks


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


class TraitsExtractorV4:
    def __init__(self):
        self.uri = "http://athena511:4988/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.temperature = 0
        self.mode = 'instruct'
        self.character = 'Example'
        self.messages = []

    def _send_request(self):
        request = {
            'mode': self.mode,
            'character': self.character,
            'messages': self.messages,
            'temperature': self.temperature,
        }
        response = requests.post(self.uri, headers=self.headers, json=request, verify=False)
        return response.json()['choices'][0]['message']['content']

    def process_and_stitch(self, text, prompt):
        chunks = split_into_chunks(text)
        combined_response = ""

        for chunk in chunks:
            result, _ = self.run(chunk, prompt)
            combined_response += result + " "

        return combined_response.strip()

    def run(self, line, prompt):
        self.messages.append({"role": "system", "content": prompt})
        self.messages.append({"role": "user", "content": line})
        assistant_message = self._send_request()
        return assistant_message, self.messages

    def process_csv_data(self, csv_string, step_one_prompt):
        csv_data = StringIO(csv_string)
        reader = csv.DictReader(csv_data)
        for row in reader:
            message_content = ', '.join([f"{key}: {value}" for key, value in row.items()])
            self.run(message_content, step_one_prompt)

        return self._send_request()

    def final_step(self, characteristics, step_two_prompt):
        return self.run(characteristics, step_two_prompt)[0]
