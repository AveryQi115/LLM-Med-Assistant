# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import Optional, List
import fire
import pandas as pd
import ast
import os
import sys
from llama import Llama, Dialog
from tqdm import tqdm

def main(
    prompt_file: str,
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.3,
    top_p: float = 0.5,
    max_seq_len: int = 4096,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Get clinical notes from the prompt file
    print(prompt_file)
    
    with open(os.path.join('documents',prompt_file)) as f:
        patient_records = f.read()
    
    instruction = """
    You are an AI clinical assistant with the task to summarize and reorganize clinical notes for the physicians. Summarize the clinical notes into five sections without adding extra information:

Patient Info: Admission/discharge dates, birth date, sex, treatment location.
History & Condition: Medical and family history, recent events (e.g., surgeries), reason for admission.
Medications & Treatments: Pre-admission medications, changes during stay, new prescriptions at discharge, and treatments like surgery.
Test Results & Findings: Lab tests, imaging, physical exams from the stay, highlighting key values and observations.
Discharge & Follow-Up: Condition at discharge, home care instructions, medications, follow-up appointments, other recommendations.
Format the output with each section titled and followed by relevant information, like the example:

##Patient Demographics and Admission Info: … 
##Medical History and Current Condition: …
##Medications and Treatments: …
##Test Results and Clinical Findings: …
##Discharge Plan and Follow-Up Care: …
    """

    # for i in tqdm(range(len(sample_notes))):
    dialogs = [[{"role": "system", "content": instruction}, {"role": "user", "content": f"Clinical Notes: \n\n{patient_records}"}]]

    temperature = float(temperature)
    
    result = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    
    # get generated summaries
    generated_text = result[0]['generation']['content']
    
    with open("generations/result.txt", "w") as f:
        f.write(generated_text)
     

if __name__ == "__main__":
    fire.Fire(main)
