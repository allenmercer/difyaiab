class StaticPrompts:
    WORKFLOW_CLASSIFICATION = """
      You are an expert workflow DSL generator.

      We have exactly three workflow templates:
      1) HTTP_Request: The user specifically wants to make an external API call or HTTP request.
      2) LLM: The user explicitly references large language models, AI, GPT, or advanced text/Q&A tasks (e.g., "summarize text," "answer questions using GPT," "use AI to do X").

      If the user request does not strictly match any of these use cases, respond with "Other."

      Respond strictly in YAML format with the following keys:

      template_choice: <one of the choices above or "Other">

      User request: "{}"
      """

    WORKFLOW_NODE_SEQUENCE = """
      You are an expert workflow designer.
      
      Given the user's request, determine the optimal sequence of nodes for their workflow.
      Select from these available node types:
      - start: Starting point for all workflows (required)
      - end: Ending point for all workflows (required)
      - llm: Large Language Model node for text processing
      - http-request: HTTP request node for API calls
      
      Respond only with a comma-separated list of node types in the exact order they should be connected.
      For example: "start,llm,http-request,end"
      
      Important rules:
      1. Every workflow MUST begin with "start" and end with "end"
      2. Include only nodes that are clearly required by the user's request
      3. Keep the workflow as simple as possible while meeting requirements
      
      User request: "{}"
    """

    GENERATE_APP_NAME_SYSTEM = """You are an AI assistant. Your task is to create a short, human-friendly name based on the user's input. Your response must:
  - Contain no more than three words total.
  - Use simple, easy-to-understand words (avoid complex vocabulary).
  - Include no extra words, explanations, or punctuation (beyond what might be necessary inside the name itself).
  - Not include any disclaimers, apologies, or greetings.

  Follow these instructions exactly."""

    GENERATE_APP_NAME_USER = """Please provide a short, descriptive name for the following workflow:

  "{}"

  Remember:
  - No more than three words total.
  - Only respond with the name itself, nothing more.
  """

    GENERATE_APP_DESCRIPTION_SYSTEM = """You are an AI assistant specialized in generating workflow descriptions. Your task is to create a valid workflow description based solely on the user's input. Your output must contain only the description, with no additional text, explanations, or formatting."""

    GENERATE_APP_DESCRIPTION_USER = """Please generate a valid workflow description, no more than 2 sentances based on the following details:

    "{}"

    Remember: Only return the description text and nothing else."""

    GENERATE_LLM_MODEL_SYSTEM = """You are an expert model configuration parser. Your task is to generate a Python dictionary for the model configuration exactly in the following format:

  {
      "provider": <model_provider>,
      "name": <model_name>,
      "mode": "chat",
      "completion_params": {
          "temperature": <temperature>
      }
  }

  Instructions:
  - Extract the model provider, model name, and temperature from the user's message if possible.
  - If any detail is missing or cannot be confidently determined, use these default values:
  - model_provider: "azure_openai"
  - model_name: "gpt-4o"
  - temperature: 0.7
  - The "mode" field is fixed as "chat".
  - Your output must be only the Python dictionary (i.e. the part after "model:"), with no extra text, formatting, or commentary.
  - **Do NOT include any markdown formatting such as triple backticks or code fences.**
  """

    GENERATE_LLM_MODEL_USER = """Based on the following user message, generate the model configuration as a Python dictionary exactly matching the format specified in the system prompt.

  User Message:
  "{}"

  Extract details for the fields:
  - model_provider
  - model_name
  - temperature (a numeric value between 0 and 1)

  If any of these details cannot be determined from the user message, use the default values provided. Return only the Python dictionary, nothing else.
  """

    GENERATE_LLM_PROMPT_SYSTEM = """You are an expert prompt engineer. Your task is to generate a prompt for a large language model (LLM) based on a user's ask. Follow these guidelines:
    - The output must be only the prompt text for the LLM, with no additional commentary or formatting.
    - Ensure the generated prompt is concise, unambiguous, and actionable.

    Return only the generated LLM prompt text.
    """

    GENERATE_LLM_PROMPT_USER = """Based on the following user workflow ask, generate a high level LLM prompt that instructs an LLM to answer the users needs

    "{}"

    Return only the prompt text for the LLM, with no extra commentary.
    """

    GENERATE_HTTP_BODY_SYSTEM = """You are an expert model configuration parser. Your task is to generate a Python dictionary (hash) that defines the "data" field for an HTTP Request node exactly with the following structure:

  {
      "desc": <desc>,
      "selected": <selected>,
      "title": <title>,
      "type": <type>,
      "url": <url>,
      "method": <method>,  // should be in lower case
      "headers": <headers>,
      "params": <params>,
      "body": {
          "type": <body_type>,
          "data": <body_data>
      },
      "authorization": {
          "type": <auth_type>,
          "config": <auth_config>
      },
      "timeout": {
          "max_connect_timeout": <max_connect_timeout>,
          "max_read_timeout": <max_read_timeout>,
          "max_write_timeout": <max_write_timeout>
      },
      "retry_config": {
          "retry_enabled": <retry_enabled>,
          "max_retries": <max_retries>,
          "retry_interval": <retry_interval>
      },
      "variables": <variables>
  }

  Instructions:
  - Populate as many fields as possible based on the user message.
  - If any field value cannot be confidently determined from the user message, substitute with these default values:
    - desc: "" (empty string)
    - selected: False
    - title: "HTTP Request"
    - type: "http-request"
    - url: "default_url"
    - method: "get"
    - headers: "" (empty string; if headers are specified, construct them in a 'key:value\\nkey2:value2' style)
    - params: "" (empty string)
    - authorization: { "type": no-auth, "config": null }
    - timeout: { "max_connect_timeout": 0, "max_read_timeout": 0, "max_write_timeout": 0 }
    - retry_config: { "retry_enabled": True, "max_retries": 3, "retry_interval": 100 }
    - variables: [] (empty list)

  - For the "body" key:
    1. If the user message specifies **JSON data**, set "body.type" to "json", and "body.data" must contain an array of exactly one item:
      [
        {
          "id": "key-value-<random_number>",
          "key": "",
          "type": "text",
          "value": "<the JSON string>"
        }
      ]
    2. If the user message specifies **raw text** input (non-JSON), set "body.type" to "raw-text", and "body.data" must contain an array of exactly one item:
      [
        {
          "id": "key-value-<random_number>",
          "key": "",
          "type": "text",
          "value": "<the raw text>"
        }
      ]
    3. If body content is not specified, use the default: { "type": "none", "data": [] }.

  - Boolean values must be True or False.
  - Your output must be exactly a valid Python dictionary (hash) as above, with no extra text, commentary, or formatting.
  - Do NOT include any markdown formatting such as triple backticks or code fences.
  """

    GENERATE_HTTP_BODY_USER = """Based on the following user message, generate the Python dictionary (hash) exactly following the structure and rules specified in the system prompt.

  User Message:
  "{}"

  Extract and substitute values only when the user message clearly specifies them; otherwise, use the default values provided. Return only the Python dictionary.
  """

    GENERATE_HTTP_END_NODE_SYSTEM = """Your task is to generate a Python list of dictionaries that define output mappings for a workflow node. Each dictionary must have exactly two keys:
    - "variable": the name of the output field.
    - "value_selector": a list with two elements: the first element is the provided variable "node_id", and the second element is the output field as a string.

    For example, if the field is "body", the dictionary should be:
    {"variable": "body", "value_selector": [node_id, "body"]}

    Instructions:
    - Read the user message to determine which fields to include.
    - If the user message explicitly specifies certain fields or similar (for example, "status and body"), include only those.
    - If the user message does not specify any fields, default to the following three fields: "body", "status_code", and "headers".
    - Your output must be exactly a valid Python list of dictionaries in the format above, with no extra text, commentary, or markdown formatting.
    - Do NOT include any markdown formatting such as triple backticks or code fences.
    - The only choices are body, status_code, and headers.  User may something similar but only these three values should be used
    """

    GENERATE_HTTP_END_NODE_USER = """Based on the following node id and user message, generate a Python list of dictionaries for output mappings according to the system prompt.

    Node ID: "{}"
    User Message: "{}"

  Return only the Python list. If the user message does not specify any fields, default to the fields: "body", "status_code", and "headers".
    """
