# pyqt-huggingface-set-path-widget
PyQt widget designed to conveniently set up a cache directory for storing Hugging Face models

When you are concerned about hard disk space or want to save models in a specific directory, this widget allows you to manage the cache directory in a GUI manner. The default value is TRANSFORMERS_CACHE (the default path where Hugging Face models are downloaded), but you can change it to your preferred location.

The modified path is saved in an ini file, and if you want to revert to the default value, simply click the reset button. You can also open the file from the input field's context menu by right-clicking, which will allow you to navigate to the desired location.

This is using in my numerous HuggingFace-related applications such as <a href="https://github.com/yjg30737/huggingface_gui.git">huggingface_gui</a>. 

## Requirements
* PyQt5 >= 5.14
* transformers

## How to Run
1. git clone ~
2. pip install -r requirements.txt
3. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-huggingface-set-path-widget/assets/55078043/7244d807-5208-4813-bc12-4729ba7d0d40)
