class GeneratePrompt():
    """
    A class to generate and manage a conversational prompt that guides a model 
    to summarize a conversation using a Chain of Thought reasoning approach.
    """

    def __init__(self) -> None:
        """
        Initializes the GeneratePrompt class.
        
        The system message in the prompt provides detailed instructions on how 
        to analyze and summarize a conversation based on the following steps:
        1. Analyze the conversation in sequence.
        2. Categorize conversation records by date.
        3. Summarize the conversation based on different themes (e.g., transportation, food).
        4. Provide a summary for each theme.
        """
        self.prompt = [
            {
                "role": "system", 
                "content": "根據以下步驟來統整聊天紀錄：\n"
                           "1. 請按照聊天記錄的順序逐步分析。\n"
                           "2. 按日期分類，並確保每個類別的對話記錄正確歸納。\n"
                           "3. 針對每個日期，將對話內容根據不同主題（例如交通、食物等）進行歸納。\n"
                           "4. 最後對每個主題進行簡要總結。\n"
                           "請用 Chain of Thought 的方式推理，逐步統整每個對話。"
            },
        ]

    def set_user_conversation(self, conversation: str) -> None:
        """
        Adds a new user conversation to the prompt.

        Args:
            conversation (str): The content of the user's conversation to be appended to the prompt.
        """
        self.prompt.append({"role": "user", "content": conversation})

    def get(self) -> list:
        """
        Retrieves the current prompt, including the system's instructions and any added user conversations.

        Returns:
            list: The list of messages forming the prompt, including system instructions and user conversations.
        """
        return self.prompt