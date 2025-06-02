# MAL-LLM Repository

This repository contains the code and related resources for the **MAL-LLM** system, as described in the paper "Towards Threat Modeling with Large Language Models: Automating Domain-Specific Language Creation in Meta Attack Language (MAL)."

## Overview

MAL-LLM is a system designed to automate the generation of Meta Attack Language (MAL) languages from unstructured text sources using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

## Content

This repository likely includes:

* **Source Code for MAL-LLM:** The core implementation of the MAL-LLM system, which processes textual input to generate `.mal` and compiled `.mar` files. This includes components for:
    * Prompt enhancement using RAG.
    * Interaction with the LLM
    * Transformation of LLM output to `.mal` format.
    * Compilation using the MAL-Compiler.
* **Evaluation Resources:** Potentially includes data used for, or generated during, the evaluation, such as the `reportLang` example MAL-Language and the scenario requirements mentioned in the paper's online appendix. For running the code a Google Gemini Key is needed.
* **Alternative Approach Code:** Code for the alternative MAL-Language generation strategy explored during the research, which involved fine-tuning smaller LLMs with RAG and an iterative refinement loop with compiler feedback.
