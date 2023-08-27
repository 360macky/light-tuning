import openai
import json
import requests
import os
import argparse
import questionary
from termcolor import colored
import sys
from light_tuning import LightTuning

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_dataset(job_creator, base=None):
    if base is None:
        base = questionary.text(
            "Please provide the path to the seed conversation:").ask()
    with open(base, 'r') as f:
        input_conversation = json.load(f)
    dataset = job_creator.generate_dataset(input_conversation)
    if dataset is None:
        return
    return dataset


def upload_dataset(job_creator, file_path=None):
    if file_path is None:
        file_path = questionary.text(
            "Enter the path to the dataset file: ").ask()
    if questionary.confirm("Continue to upload dataset?").ask():
        file_id = job_creator.upload_dataset(file_path)
        if file_id is None:
            return
        print(f"TRAINING_FILE_ID: {file_id}")
        return file_id


def fine_tune_model(job_creator, file_id=None):
    if file_id is None:
        file_id = questionary.text(
            "Please provide the file ID for fine-tuning:").ask()
    model_id = job_creator.create_fine_tuning_job(file_id)
    if model_id is None:
        return
    print(f"MODEL_ID: {model_id}")
    return model_id


def main():
    parser = argparse.ArgumentParser(
        description='OpenAI fine-tuning job creator.',
        epilog='Enjoy using LightTuning!'
    )
    parser.add_argument('--generate', action='store_true',
                        help='Generate dataset from base conversation. Use --base flag to specify the path to the file containing the conversation')
    parser.add_argument('--base', type=str,
                        help='Path to the file containing the conversation')
    parser.add_argument('--upload', action='store_true',
                        help='Upload dataset to OpenAI servers')
    parser.add_argument('--finetune', action='store_true',
                        help='Create fine-tuning to train the GPT-3.5 model')
    parser.add_argument('--file_id', type=str,
                        help='ID of the file to be used for fine-tuning')
    parser.add_argument('--all', action='store_true',
                        help='Do all of the above in order (generate, upload, finetune)')
    args = parser.parse_args()

    print(colored("---------- Hello! Let's fine-tune a model today ----------"))
    print(colored("   __ _       _     _     _____             _             ", 'red'))
    print(colored("  / /(_) __ _| |__ | |_  /__   \_   _ _ __ (_)_ __   __ _ ", 'yellow'))
    print(colored(" / / | |/ _` | '_ \| __|   / /\/ | | | '_ \| | '_ \ / _` |", 'green'))
    print(colored("/ /__| | (_| | | | | |_   / /  | |_| | | | | | | | | (_| |", 'blue'))
    print(colored("\____/_|\__, |_| |_|\__|  \/    \__,_|_| |_|_|_| |_|\__, |", 'magenta'))
    print(colored("        |___/                                       |___/ ", 'cyan'))
    job_creator = LightTuning(os.environ["OPENAI_API_KEY"])

    actions = {
        'Generate dataset': generate_dataset,
        'Upload dataset': upload_dataset,
        'Fine-tune model': fine_tune_model,
        'All': lambda jc: fine_tune_model(jc, upload_dataset(jc, generate_dataset(jc)))
    }

    action = questionary.select(
        "What do you want to do?", choices=actions.keys()).ask()
    actions[action](job_creator)


if __name__ == "__main__":
    main()
