import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
    """Downloads the data"""
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


def processData(file_content):
    logger = logging.getLogger("assignment2")
    personData = {}

    lines = file_content.splitlines()

    for line_num, line in enumerate(lines, start=1):

        if line.startswith("id"):
            continue

        try:
            person_id, name, birthday_str = line.split(",")

            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y")

            personData[int(person_id)] = (name, birthday)

        except Exception:
            logger.error(f"Error processing line #{line_num} for ID #{person_id}")

    return personData


def displayPerson(id, personData):
    if id not in personData:
        print("No user found with that id")
    else:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.date()}")


def main(url):
    print(f"Running main with URL = {url}...")

    logging.basicConfig(filename="error.log", level=logging.ERROR)

    try:
        csvData = downloadData(url)
    except Exception:
        print("Error downloading data")
        return

    personData = processData(csvData)

    while True:
        try:
            user_id = int(input("Enter an ID to lookup: "))
        except ValueError:
            continue

        if user_id <= 0:
            return

        displayPerson(user_id, personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
