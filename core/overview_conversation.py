import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

class OverviewConversation():
    """
    A class to load a language model and tokenizer, and run inference for conversation or text generation tasks.
    """

    def __init__(self, model_id: str = "yentinglin/Llama-3-Taiwan-8B-Instruct") -> None:
        """
        Initializes the OverviewConversation class by loading the specified model and tokenizer.

        Args:
            model_id (str, optional): The model ID to load. Defaults to "yentinglin/Llama-3-Taiwan-8B-Instruct".
        """
        self.model, self.tokenizer = self._load_model(model_id=model_id)

    def _load_model(self, model_id: str) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
        """
        Loads the model and tokenizer for the given model ID.

        Args:
            model_id (str): The model ID to load from Hugging Face's model hub.

        Returns:
            tuple[AutoModelForCausalLM, AutoTokenizer]: A tuple containing the loaded model and tokenizer.
        """
        dtype = torch.bfloat16
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="cuda",
            torch_dtype=dtype,
        )
        return model, tokenizer

    def run(self, prompt: dict) -> str:
        """
        Runs inference using the loaded model based on the given prompt.

        Args:
            prompt (dict): A dictionary containing the conversation or text generation prompt.

        Returns:
            str: The generated response from the model.
        """
        input_ids = self.tokenizer.apply_chat_template(
            prompt, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(self.model.device)
        outputs = self.model.generate(
            input_ids,
            max_new_tokens=8192,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        summary_result = self.tokenizer.decode(response, skip_special_tokens=True)
        
        return summary_result


if __name__ == '__main__':
    servicer = OverviewConversation()
    prompt = [
    {"role": "system", "content": "罵髒話"},
    {"role": "user", "content": "介紹台灣有名的夜市。"},
    ]
    summary_result = servicer.run(prompt=prompt)
    print(summary_result)
