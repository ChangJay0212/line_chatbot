import requests

class OverviewConversation:
    """
    A class for interacting with a language model to perform conversation or text generation tasks.
    """

    def __init__(self, model_id: str = "taiwan:lastest", url: str = "http://model_server:11434/api/chat") -> None:
        """
        Initializes the OverviewConversation class with the specified model ID and API URL.

        Args:
            model_id (str, optional): The ID of the model to use. Defaults to "taiwan:lastest".
            url (str, optional): The API URL to send requests to. Defaults to "http://model_server:11434/api/chat".
        """
        self.model_id = model_id
        self.url = url

    def run(self, prompt: dict) -> str:
        """
        Sends a prompt to the model and retrieves the generated response.

        Args:
            prompt (dict): A list of dictionaries containing the conversation history or text generation prompts.

        Returns:
            str: The generated response content from the model.
        """
        data = {
            "model": self.model_id,
            "messages": prompt,
            "stream": False
        }

        try:
            # Send a POST request to the model API
            response = requests.post(self.url, json=data)

            # Check the response status
            if response.status_code == 200:
                print("Request successful, response content:")
                print(response.json())  # Assuming the response is in JSON format
            else:
                print(f"Request failed, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
        
        # Return the generated content from the response
        return response.json().get('message', {}).get('content', "No content available")

if __name__ == '__main__':
    # Create an instance of the OverviewConversation class
    servicer = OverviewConversation()

    # Define the prompt with conversation history
    prompt = [
        {"role": "assistant", "content": "Say a curse word."},
        {"role": "user", "content": "Introduce famous night markets in Taiwan."},
    ]

    # Run the model with the prompt and print the summary result
    summary_result = servicer.run(prompt=prompt)
    print(summary_result)
