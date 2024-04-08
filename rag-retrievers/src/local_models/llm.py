import warnings
warnings.filterwarnings('ignore')

###################################################################
#v0.9.xx: from llama_index.llms import LlamaCPP
#v0.10.xx:
#%pip install llama-index-llms-llama-cpp
from llama_index.llms.llama_cpp import LlamaCPP

###################################################################
#v0.9.xx: 
#from llama_index.callbacks import CallbackManager
#from llama_index.llms import (
#####CustomLLM,
#####CompletionResponse,
#####CompletionResponseGen,
#####LLMMetadata,
#)
#from llama_index.llms.base import llm_completion_callback
#v0.10.xx:
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback

###################################################################
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

from typing import Optional, List, Mapping, Any


###################################################################
#v0.9.xx: 
#from llama_index import ServiceContext
#v0.10.xx: 
from llama_index.core import ServiceContext

###################################################################


class LlamaCPPLLM():
    context_window: int = 2048  # Size of the context window
    num_output: int = 256  # Number of output tokens

    def __init__(self, model_url=None, model_path=None, temperature=0.1, max_new_tokens=512, context_window=2048, 
                 generate_kwargs={}, n_gpu_layers=-1, messages_to_prompt=None, completion_to_prompt=None, verbose=False):
        """
        Requirements: model must be in .gguf format
        e.g. model_url="https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/mistral-7b-openorca.Q6_K.gguf"

        """
        self.llm = LlamaCPP(
            # optionally, you can set the path to a pre-downloaded model instead of model_url
            model_url=model_url,
            model_path=model_path,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=context_window,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            # set to at least 1 to use GPU
            model_kwargs={"n_gpu_layers": n_gpu_layers},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=False,
        )

    def complete(self, prompt):
        response = self.llm.complete(prompt)
        return response


class MyLLM(CustomLLM):
    context_window: int = 2048 # Size of the context window
    num_output: int = 256 # Number of output tokens
    model_name: str = "chatglm3-6b" # Model name
    tokenizer: object = None # Tokenizer
    model: object = None # Model

    def __init__(self, pretrained_model_name_or_path, context_window, num_output, model_name, device_map="mps"):
        super().__init__()

        # GPU方式加载模型
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path, device_map=device_map, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path, device_map=device_map, trust_remote_code=True).eval()

        self.context_window = context_window
        self.num_output = num_output
        self.model_name = model_name

    
    @property
    def metadata(self) -> LLMMetadata:
        '''Get LLM metadata.'''
        # Obtaining metadata for LLM
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )
    
    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        prompt_length = len(prompt)

        # only return newly generated tokens
        text,_ = self.model.chat(self.tokenizer, prompt, history=[])
        return CompletionResponse(text=text)


    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        raise NotImplementedError()


#llm = MyLLM(pretrained_model_name_or_path='/Users/eeyorepopo/Desktop/LLM_TECH_STACK/repo/models/chatglm3-6b',context_window=4096, num_output=512, \
            #model_name='chatglm3-6b')


