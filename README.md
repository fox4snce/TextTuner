# TextTuner

TextTuner is a pioneering demonstration of Ontology-Based Prompt Engineering, showcasing an innovative approach to text analysis and modification using AI.

## Overview

TextTuner allows users to analyze a given text and modify its stylistic and tonal attributes using an intuitive interface. It serves as a proof of concept for a systematic approach to prompt engineering that leverages ontological categories to provide fine-grained control over AI-generated text.

## Features

1. **Text Analysis**: Automatically categorizes input text and generates relevant ontological concepts.
2. **Dynamic Category Generation**: Creates a set of 5-7 ontological style concepts, each with 8-10 levels of gradation.
3. **Interactive Modification**: Allows users to adjust text along multiple dimensions simultaneously.
4. **Real-time Text Transformation**: Modifies the input text based on selected ontological attributes.

## How It Works

1. **Input**: Users provide a text sample.
2. **Analysis**: The system analyzes the text and generates relevant ontological categories.
3. **Category Display**: Categories are presented as dropdown menus with multiple levels.
4. **User Selection**: Users can select desired levels for each category.
5. **Text Modification**: The system generates a modified version of the text based on the selected attributes.

## Technical Implementation

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (with jQuery)
- **AI Integration**: Utilizes a language model for text analysis and modification

## Significance

TextTuner is the first example of Ontology-Based Prompt Engineering, demonstrating:

1. **Dynamic Ontology Generation**: Automatically creating relevant categories for any given text.
2. **Multi-dimensional Text Modification**: Allowing simultaneous adjustments across multiple ontological dimensions.
3. **Intuitive Control**: Providing a user-friendly interface for complex AI interactions.
4. **Prompt Decomposition and Reconstruction**: Breaking down the modification process into ontological components and reassembling them coherently.

## Future Directions

- Expand the range of ontological categories
- Implement more sophisticated analysis algorithms
- Develop a feedback mechanism for continuous improvement
- Create tools for comparing different versions of modified text

## Getting Started

### Prerequisites
Python 3.7 or higher
pip (Python package installer)

## Installation Steps

### Clone the repository:

git clone https://github.com/fox4snce/TextTuner.git
cd TextTuner

### Set up a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

### Install the required packages:

pip install flask

### Set up the LLM (Language Model): 

The application uses llm_utils.py to interact with the language model. This file contains a generate_response function that needs to be set up for your specific LLM.

Currently, the application is configured to work with LM Studio using the Llama 3.1 Instruct 7B Q8_0 GGUF model. If you're using a different LLM or service, you'll need to modify the generate_response function in llm_utils.py accordingly.

### Run the application:

python app.py

### Access the application: Open a web browser and go to http://127.0.0.1:5501/

### Customizing the LLM

If you're using a different LLM or service, you'll need to modify the generate_response function in llm_utils.py. This function should take three parameters:

system: A system message or prompt
user_message: The user's input message
max_tokens: The maximum number of tokens to generate (optional)
Modify the function to interface with your chosen LLM or API service.

## Contributing

This project is a demonstration and is not currently open for contributions. However, we encourage you to explore the concept of Ontology-Based Prompt Engineering and develop your own implementations.

## License

[Include appropriate license information]

## Acknowledgements

This project is inspired by the concept of Ontology-Based Prompt Engineering, aiming to push the boundaries of human-AI interaction in text manipulation and generation.
