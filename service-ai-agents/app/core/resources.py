import textwrap


class Resource:
    DSL_DEFAULT = textwrap.dedent(
        """\
app:
  description: t
  icon: "\U0001f916"
  icon_background: '#FFEAD5'
  mode: workflow
  name: t
  use_icon_as_answer_icon: false
kind: app
version: 0.1.5
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    file_upload:
      allowed_file_extensions:
        - .JPG
        - .JPEG
        - .PNG
        - .GIF
        - .WEBP
        - .SVG
      allowed_file_types:
        - image
      allowed_file_upload_methods:
        - local_file
        - remote_url
      enabled: false
      fileUploadConfig:
        audio_file_size_limit: 50
        batch_count_limit: 5
        file_size_limit: 15
        image_file_size_limit: 10
        video_file_size_limit: 100
        workflow_file_upload_limit: 10
      image:
        enabled: false
        number_limits: 3
        transfer_methods:
          - local_file
          - remote_url
      number_limits: 3
    opening_statement: ''
    retriever_resource:
      enabled: true
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions: []
    suggested_questions_after_answer:
      enabled: false
    text_to_speech:
      enabled: false
      language: ''
      voice: ''
  graph:
    edges:
      - data:
          isInIteration: false
          sourceType: llm
          targetType: end
        id: 1740689457189-source-1740689567581-target
        selected: false
        source: '1740689457189'
        sourceHandle: source
        target: '1740689567581'
        targetHandle: target
        type: custom
        zIndex: 0
      - data:
          isInIteration: false
          sourceType: start
          targetType: document-extractor
        id: 1740688077982-source-1740691271999-target
        source: '1740688077982'
        sourceHandle: source
        target: '1740691271999'
        targetHandle: target
        type: custom
        zIndex: 0
      - data:
          isInIteration: false
          sourceType: document-extractor
          targetType: llm
        id: 1740691271999-source-1740689457189-target
        source: '1740691271999'
        sourceHandle: source
        target: '1740689457189'
        targetHandle: target
        type: custom
        zIndex: 0
    nodes:
      - data:
          desc: ''
          selected: false
          title: Start
          type: start
          variables:
            - label: prompt
              max_length: 1000
              options: []
              required: true
              type: paragraph
              variable: prompt
            - allowed_file_extensions: []
              allowed_file_types:
                - document
              allowed_file_upload_methods:
                - local_file
                - remote_url
              label: Path
              max_length: 48
              options: []
              required: true
              type: file
              variable: Path
        height: 116
        id: '1740688077982'
        position:
          x: 47.085667209678746
          'y': 173.5540783780966
        positionAbsolute:
          x: 47.085667209678746
          'y': 173.5540783780966
        selected: false
        sourcePosition: right
        targetPosition: left
        type: custom
        width: 244
      - data:
          context:
            enabled: true
            variable_selector:
              - '1740691271999'
              - text
          desc: ''
          model:
            completion_params:
              temperature: 0.7
            mode: chat
            name: llama3.2
            provider: ollama
          prompt_template:
            - id: 18ff700e-fc9e-4ef2-b377-adc02a86af9c
              role: system
              text: '{{#context#}}'
            - id: c1aefecb-8352-4abe-b96b-c4ca7b87794d
              role: user
              text: '{{#1740688077982.prompt#}}'
            - id: c817a64e-7d53-42df-9b65-f1cf0365a5ec
              role: user
              text: >-
                using the python code in the context Create a valid Dify.ai DSL
                yml file that includes all required sections.
          selected: false
          title: LLM
          type: llm
          variables: []
          vision:
            enabled: false
        height: 98
        id: '1740689457189'
        position:
          x: 645.3389908589614
          'y': 162.53220182820772
        positionAbsolute:
          x: 645.3389908589614
          'y': 162.53220182820772
        selected: true
        sourcePosition: right
        targetPosition: left
        type: custom
        width: 244
      - data:
          desc: ''
          outputs:
            - value_selector:
                - '1740689457189'
                - text
              variable: text
          selected: false
          title: End
          type: end
        height: 90
        id: '1740689567581'
        position:
          x: 901
          'y': 205
        positionAbsolute:
          x: 901
          'y': 205
        selected: false
        sourcePosition: right
        targetPosition: left
        type: custom
        width: 244
      - data:
          desc: ''
          is_array_file: false
          selected: false
          title: Doc Extractor
          type: document-extractor
          variable_selector:
            - '1740688077982'
            - Path
        height: 92
        id: '1740691271999'
        position:
          x: 353.4584669709965
          'y': 75.51600639884603
        positionAbsolute:
          x: 353.4584669709965
          'y': 75.51600639884603
        selected: false
        sourcePosition: right
        targetPosition: left
        type: custom
        width: 244
    viewport:
      x: 9.79970752293434
      'y': 72.70520711704165
      zoom: 0.9791791715318334
"""
    )
