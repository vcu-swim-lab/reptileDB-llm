import csv
from io import StringIO

import requests
import re
from validator import is_valid


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
        self.last_response = None
        self.uri = "http://athena521:47438/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.temperature = 0
        self.mode = 'instruct'
        # self.character = 'Example'
        self.messages = []

    def _clear_messages(self):
        self.messages = []

    def _send_request(self):
        request = {
            'mode': self.mode,
            # 'character': self.character,
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

    def run_with_retries(self, line, prompt, max_attempts=1):
        species_name = ' '.join(line.split()[:2])

        attempts = 0
        while attempts < max_attempts:
            self._clear_messages()
            self.messages.append({"role": "system", "content": prompt})
            self.messages.append({"role": "user", "content": line})
            assistant_message = self._send_request()
            self.last_response = assistant_message

            if is_valid(assistant_message):
                return assistant_message, self.messages
            else:
                print(f"Validation failed for '{species_name}', attempt: {attempts + 1} of {max_attempts}")
                attempts += 1

        if attempts >= max_attempts:
            if len(line) > 1:
                print(f"Max attempts reached for '{species_name}'. Splitting input for further processing.")
                # Find the nearest space to the midpoint to split on a whole word
                middle_index = len(line) // 2
                nearest_space = line.rfind(' ', 0, middle_index)
                if nearest_space == -1 or nearest_space + 1 == len(line):  # No space found, or space is at the end
                    nearest_space = line.find(' ', middle_index)
                    if nearest_space == -1:
                        # If there's no space to split on, use the original middle index
                        nearest_space = middle_index

                first_half = species_name + " " + line[:nearest_space]
                second_half = species_name + " " + line[nearest_space + 1:]  # Skip the space for the second half

                print(f"Processing first half: '{first_half}'")
                first_half_result, first_messages = self.run(first_half, prompt)

                print(f"Processing second half: '{second_half}'")
                second_half_result, second_messages = self.run(second_half, prompt)

                # Combine the results
                combined_result = first_half_result + " " + second_half_result
                combined_messages = first_messages + second_messages  # Adjust as needed
                return combined_result, combined_messages
            else:
                print(f"Unable to split '{species_name}' further. Returning last response.")
                return self.last_response, self.messages
        # Fallback return, in case the loop exits in an unexpected manner
        return self.last_response, self.messages

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
