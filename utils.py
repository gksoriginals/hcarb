def log(chat_id, message):
    with open(f"logs/{chat_id}.txt","a") as f:
        f.write(message + "\n")
        f.close()