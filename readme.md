# Python Code Style Checker

Based on the 15-112 Styling Guidelines.

## Description

This project is designed to analyze Python code for styling issues, adhering to the 15-112 course styling rules. It allows for easy identification and resolution of coding style discrepancies. Users have the flexibility to select specific rules or checkers for application.

## Installation

### Prerequisites

-   Python 3.10

### Modules

The project utilizes the `CMU-Graphics` module. To install, execute:
<code>pip install cmu-graphics</code>
All other modules used are standard Python built-in modules.

## Usage

### Running the Project

Execute the following command to run the project:
<code>python main.py</code>

### Adding Custom Checkers

In `checkers.py`, you can extend the functionality by adding your custom code checkers to the `Checker` class. To integrate a new checker:

1. Create a method within the `Checker` class that begins with `check`.
2. Ensure that your method returns a list of `StyleViolation` objects.
3. Access the Python code using `self.content`, which contains the lines of the code as strings.

## Contributing

Contributions are welcome! Feel free to send pull requests to [our GitHub repository](https://github.com/khasanbekme/Term-Project).
