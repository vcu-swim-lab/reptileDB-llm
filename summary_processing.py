import csv
import re


class SummaryProcessing:
    def __init__(self, family, data):
        self.data = data
        self.family = family

    def parse_traits(self):
        with open(f'final_{self.family}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['trait', 'count'])

            lines = self.data.split('\n')

            for line in lines:
                line = re.sub(r'^\d+\.\s*', '', line)

                match = re.match(r'(.*?),(.*?)(\d+)', line)
                if match:
                    trait = match.group(1).strip()
                    count = match.group(3).strip()

                    writer.writerow([trait, count])
