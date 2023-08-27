<p align="center">
  <img
    src=".github/logo.png"
    align="center"
    width="100"
    alt="LightTuning"
    title="LightTuning"
  />
  <h1 align="center">LightTuning</h1>
</p>

<p align="center">
  🤖 CLI to fine-tune GPT-3.5 Turbo models rapidly. 💬
</p>

![Demo of Project](./.github/preview.jpg)

## 🚀 Concept

**LightTuning** is a quick way to fine-tune GPT-3.5 Turbo models. To scale and enhance a model from a small conversation to a light GPT-3.5 model that can overperform GPT-4. How cool is that?

## 🧑‍💻 Usage

Run the main.py script to start the tool.

```bash
python3 main.py
```

You will be greeted with a welcome message and a list of actions to choose from:

- Generate dataset
- Upload dataset
- Fine-tune model
- All

Select an action using the arrow keys and press Enter.

If you choose 'Generate dataset', you will be asked to provide the path to the seed conversation. If you don't provide a path, the tool will ask you to enter it.

Upload Dataset

If you choose 'Upload dataset', you will be asked to enter the path to the dataset file. If you don't provide a path, the tool will ask you to enter it. You will then be asked to confirm the upload.

Fine-tune Model

If you choose 'Fine-tune model', you will be asked to provide the file ID for fine-tuning. If you don't provide a file ID, the tool will ask you to enter it.

All

If you choose 'All', the tool will execute all of the above actions in order.

So, we now that GPT-3.5 Turbo is a powerful tool for generating text, and that we can fine-tune it to perform better on specific tasks. Your next task is to create a model that does this process automatically.

**LightTuning** is a Python Script that takes a GPT-3.5-turbo conversation as a JSON file containing multiple messages, each one wich its role (user, assistant or system) and its content.

```json
[
  {
    "role": "system",
    "content": "You are an assistant that occasionally misspells words"
  },
  {
    "role": "user",
    "content": "Tell me a story."
  },
  {
    "role": "assistant",
    "content": "One day a student went to schoool."
  },
  {
    "role": "user",
    "content": "What happened next?"
  },
  {
    "role": "assistant",
    "content": "The student was happy very."
  }
]
```

The next thing is generate a dataset. That is adding more examples. Let's use `gpt-4` for that like:

```py
completion = openai.ChatCompletion.create(model="gpt-4", messages=dataset_messages, temperature=0.7)
```

Where `dataset_messages` is this:

```json
[
  {
    "role": "system",
    "content": "You are a generator of GPT-3.5 Turbo conversations that outputs JSON formatted responses for a training dataset of a conversation between a user and an assistant. Your task is to follow the conversation as expected by the system prompt by 64 messages. The conversation is this: {input_conversation}"
  }
]
```

And `input_conversation` is the conversation that we want to refine. So, we have to replace it with the conversation that we want to refine.

After running this and catching the response of ChatGPT in a JSON called "dataset.json". We have to upload it to OpenAI Files API in order to get a file ID.

```py
file = open("dataset.json", "r")
response = openai.File.create(file=file, purpose="fine-tune")
file_id = response["id"]
```

And then, we have to create a fine-tuning job with the file ID and the model that we want to fine-tune.

```py
response = openai.FineTuning.create(training_file=file_id, model="gpt-3.5-turbo-0613")
```

Finally, we show in the terminal de TRAINING_FILE_ID and the MODEL_ID, so the developer can use it to fine-tune the model.

Now, this project is a CLI that does all this process automatically starting from a `main.py` file that contains all the interactions and processes described above with messages and inputs so the developer can use it easily.
