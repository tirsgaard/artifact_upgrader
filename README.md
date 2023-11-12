# Install
To install the package run the following command:
```bash
pip install -e .
```
# Usage

# Generation of optimisation target
The library functions be evaluating a optimisation target function based on equipted artifacts.
The ideal solution would be to allow other 3rd party libraries to be used to evaluate the target function.
This is a challenge as libraries such as Genshin Optimizer is writting in TypeScript, and this library is written in Python.

To solve this problem, you can go to the following GPT powered link and copy paste the calculation string from Genshin optimizer.
This should generate a function that this library can use. Please be sure to double check that the function is correct.
Please note that some stats not present on artifacts equipped in Genshin Optimizer will not be included in the function.

Link to GPT powered function converter:
https://chat.openai.com/g/g-WooZ5JJLo-python-function-converter