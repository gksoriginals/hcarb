import openai
import os
from utils import log
import dotenv
dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

with open("prompts/main.txt") as f:
    system = "\n".join(f.readlines())

with open("knowledge/mtp.txt") as f:
    mtp = "\n".join(f.readlines())

system = system.format(context=mtp)

def get_response(chat_id, message, history):

    if(len(history) < 1):
        history = [
            {
                "role": "system",
                "content": system
            }
        ]
        log(chat_id, "system: " +system)
    log(chat_id, "user: " +message)
    history.append(
        {
        "role": "user",
        "content": message
        }
    )

    print(f"\033[0;33m{history}\033[0m")

    response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=history
        )
    answer = response.choices[0].message.get("content")
    history.append(
        {
        "role": "assistant",
        "content": answer
        }
    )

    log(chat_id, "assistant: " +answer)

    print(f"\033[0;34m{answer}\033[0m")

    return answer, history