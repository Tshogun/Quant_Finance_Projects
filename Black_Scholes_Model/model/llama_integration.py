import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaIntegration:
    def __init__(self, model_name="meta-llama/Llama-2-7b-hf", device=None):
        """
        Initializes the LlamaIntegration class with the LLaMA model.

        Parameters:
        - model_name: The name of the model to use (defaults to Llama-2-7b)
        - device: Device to load the model (defaults to GPU if available, otherwise CPU)
        """
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        
        # Load the LLaMA tokenizer and model
        self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name)
        self.model = LlamaForCausalLM.from_pretrained(self.model_name)
        self.model.to(self.device)
        
        logger.info(f"Model loaded to {self.device}.")

    def generate_summary(self, input_text, max_length=150, min_length=50):
        """
        Generates an executive summary using the LLaMA model.

        Parameters:
        - input_text: The text to be summarized
        - max_length: Maximum length of the generated summary
        - min_length: Minimum length of the generated summary

        Returns:
        - The generated executive summary
        """
        try:
            # Tokenize the input text
            inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            # Generate the summary
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                num_beams=4,     # Beam search for better results
                no_repeat_ngram_size=2,  # Avoid repetition
                early_stopping=True,
                do_sample=False
            )
            
            # Decode the generated summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary

        except Exception as e:
            logger.error(f"Error during summary generation: {e}")
            return None

# Example usage of the LlamaIntegration class

if __name__ == "__main__":
    input_text = """
    In recent months, the company has experienced significant growth due to the expansion of our product lines.
    Despite global supply chain disruptions, our production team has ensured that we meet demand.
    Our revenue has increased by 20%, and we have secured new partnerships that will bolster our market share in the upcoming quarter.
    Additionally, our research and development team is working on a new cutting-edge product that is expected to revolutionize the industry.
    """
    
    llama_integration = LlamaIntegration()
    executive_summary = llama_integration.generate_summary(input_text)
    
    if executive_summary:
        print("Executive Summary:")
        print(executive_summary)
    else:
        print("Error generating executive summary.")
