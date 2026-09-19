# Module 05 Lab — GitHub Copilot as a Learning Aid

## Objectives

By the end of this lab you will have:

- Used GitHub Copilot Chat to explain unfamiliar code and configuration
- Critiqued a GenAI explanation for accuracy rather than accepting it at face value
- Practised the boundary this week: Copilot for explanation, not for code generation

## Setup

- IntelliJ IDEA 2025.1 with GitHub Copilot signed in
- The two snippet files from the demo:
  [`unfamiliar-jenkinsfile-snippet.txt`](../../demos/05-genai-copilot-learning-aid/unfamiliar-jenkinsfile-snippet.txt)
  and
  [`unfamiliar-dockerfile-snippet.txt`](../../demos/05-genai-copilot-learning-aid/unfamiliar-dockerfile-snippet.txt)

> **Reminder:** this week Copilot is a learning aid only. Every prompt in this lab should ask
> Copilot to *explain* something, never to *write* or *complete* something. Code-generation
> use of Copilot is covered in a later sprint.

## Task sheet

1. **Open Copilot Chat**
   - Open the Copilot Chat panel in IntelliJ.
   - Open `unfamiliar-jenkinsfile-snippet.txt` in the editor.

2. **Ask Copilot to explain it**
   - Select the full file contents.
   - Ask Copilot Chat to explain what each stage does, in plain English.
   - Copy its response into your own notes.

3. **Critique the explanation**
   - Pick two specific claims Copilot made (for example, what a particular step or option
     does).
   - Check each one against a second source: the official Jenkins documentation, a teammate,
     or your trainer.
   - Write one sentence per claim: was Copilot's explanation accurate, partially accurate, or
     wrong? If it was wrong or vague, write the corrected version.

4. **Repeat with the Dockerfile snippet**
   - Open `unfamiliar-dockerfile-snippet.txt`.
   - Ask Copilot to explain what each line does and why the base image choice matters.
   - Critique at least one claim the same way as step 3.

5. **Reflect**
   - In two or three sentences, describe a situation later in this programme where using
     Copilot as a learning aid (explaining something) would be useful, and one where you would
     want to be especially careful about trusting its explanation without checking it.

## Acceptance criteria

- You have a written explanation from Copilot for both snippets, saved in your own notes.
- You have at least three critiqued claims total (two from the Jenkinsfile, one from the
  Dockerfile) with an accurate/partially accurate/wrong verdict for each.
- Your reflection notes name one good use case and one situation calling for extra caution.
- None of your prompts asked Copilot to write or complete code.

If you finish early, try asking Copilot to explain a snippet of Linux shell script from Module
03's demo log file, and critique that explanation too.
