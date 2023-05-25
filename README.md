# AI Chatbot for Self-Improving Python Code Generation

## Overview

This is a Python project that provides an AI bot called InfantAGI for generating Python code instructions that can improve its own performance over time. InfantAGI uses OpenAI's GPT-3,5 language model to generate refined input and detailed code instructions, and then evaluates the output of the generated code to refine its own instructions further. InfantAGI includes an agent to refine the task description, an agent to provide the code instructions, an agent to write the Python code based on the instructions, and an agent to evaluate the output of the generated code and provide feedback to refine the instructions further. The real magic of this little program happens when the code written by the coder agent has been executed by python. Depending on the 

## Installation

To use the InfantAGI you will need to install the required Python modules listed in `requirements.txt`. You can do this by running install_requirements.sh file or by running the following command in your project directory:

pip install -r requirements.txt

You will also need to obtain an OpenAI API key to access the GPT-3 language model. You can sign up for an API key on the [OpenAI website](https://beta.openai.com/signup/).

## Usage

To use the InfantAGI, you need to have a working OpenAI API key and enter it instead of YOUR_API_KEY at the beginning of the code. Then save the code and simply run the `InfantAGI.py` script and input a task description. InfantAGI will then refine the input, provide the code instructions, generate the Python code, and evaluate the output. InfantAGI is able to execute the generated code by the coder agent, allowing it to be evaluated if the code is working properly or not. Depending on the code written by the agent, it also has the potential to bring plug-in like abilities such as browsing, text-to-speech, plotting, etc., which plain ChatGPT normally does not have.

The AI agents can be customized to suit specific needs by modifying the input and output formats or the agent roles defined by plain language inside the code.

## Self-Improvement

InfantAGI, is designed to improve its own performance over time through a feedback loop. After generating code instructions and evaluating the output, InfantAGI, uses this feedback to refine its own instructions further, resulting in better code generation in the future. 
Before each iteration, it asks for user input to avoid loops resulting in high API usage costs. At this step, user may choose to continue (by pressing y), end the program (n), or give feedback (any other input)

## License

This project is licensed under the MIT license. See the `LICENSE` file for more information.

## Contributing

Contributions to this project are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

## Thanks

I only have a basic level knowledge about coding. All the coding work as well as the project documentation including this file have been handled by chatgpt, claude-instant and sage over chat.openai.com and poe.com . Many thanks to all the great virtual minds and workers behind this project.

## Contact

If you have any questions or comments about this project, feel free to contact the author at [erenciracioglu@gmail.com](mailto:erenciracioglu@gmail.com) or [@erenciracioglu](https://twitter.com/erenciracioglu) on Twitter.
