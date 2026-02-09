from openai import OpenAI
from dotenv import load_dotenv
import json
import uuid
import logging
from datetime import datetime

load_dotenv()

def setup_logging():
    """Co,nfigure logging to save logs in JSON format"""
    logger = logging.getLogger("Chatbot")

    #create a file handler that writes to a JSON file
    file_handler = logging.FileHandler("chatbot_logs.json")
    # file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    formatter = logging.Formatter("%(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    return logger

def initialize_client(use_ollama: bool = True) -> OpenAI:
    """Initialize the OpenAI client with for either OpenAI or Ollama"""
    if use_ollama:
        return OpenAI(base_url="http://localhost:11434/v1", api_key = "ollama")
    return OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

class ChatBot:
    def __init__(self, use_ollama: bool = True):
        self.logger = setup_logging()
        self.session_id = str(uuid.uuid4())
        self.client = initialize_client(use_ollama)
        self.use_ollama = use_ollama
        self.model = "gpt-4o" if not use_ollama else "llama3.1:latest" #"llama3.2:8b"

        #initialize chat conversation with a system message
        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that can answer questions and help with tasks."
            }
        ]
        self.logger.info(f"Chatbot initialized with model: {self.model}")




    def chat(self, user_input: str) -> str:
        try:
            #log user input with metadata
            log_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "user_message": user_input,
                "session_id": self.session_id,
                "model": self.model,
                "use_ollama": self.use_ollama
            }
            self.logger.info(json.dumps(log_entry))

            #append the user message to the conversation
            self.messages.append({
                "role": "user",
                "content": user_input
            })

            #generate a response from the model using the OpenAI API or Ollama
            start_time = datetime.now()
            print(f"START TIME : {start_time}")
            response = self.client.chat.completions.create(
                # model= model_name
                model=self.model,
                messages=self.messages,
                temperature=0.7,
                top_p=1,
                max_tokens=1000
            )
            end_time = datetime.now()
            print(f"END TIME : {start_time}")
            response_time = (end_time - start_time).total_seconds()
            # self.logger.info(f"Response time: {response_time} seconds")
            self.logger.info(json.dumps(log_entry))

            #Extract the assistant message from the response
            assistant_message = response.choices[0].message.content
            return assistant_message

        except Exception as e:
            #log the models response and performance
                log_entry = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "level": "info",
                    "type": "model_response",
                    # "model_response": assistant_response,
                    "metadata": {
                        "session_id": self.session_id,
                        "use_ollama": self.use_ollama,
                        # "response_time_seconds": response_time,
                        # "token_used": response.usage.total_tokens,
                        # "input_tokens": {
                        #     "total": response.usage.input_tokens,
                        # }
                    },
                    
                    # "assistant_message": assistant_message
                }
                self.logger.error(json.dumps(log_entry))
                return f"Sorry, something evil happened in the universe: {str(e)}"
                
            # return assistant_message
        
def main():
    #initialize chat
    # chatbot = ChatBot(use_ollama)
    print(" \n Select Model Type:")
    print("1. OpenAI GPT-4")
    print("2. Ollama (local)")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Please enter either 1 or 2")

    use_ollama = choice == "2"
    # print(" xxxxx")
    #initialize chat
    chatbot = ChatBot(use_ollama)
    print(" CHATBOT PASS")
    print("\n === Chat Session Startedd ===")
    print(f"Using  {'Ollama' if use_ollama else 'OpenAI'} model")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print(" Goodbye!")
            break;
        if not user_input:
                continue
        response = chatbot.chat(user_input)
        print(f"Bot: {response} \n")

            

main()
# if __name__ == "__main__":
#     try:
#         main()
#     except:
#         print("\n\n Session ended ")