# Dataset Information

This project uses the public **Olist Brazilian E-commerce Dataset** from Kaggle.



The repository does **not** store the original CSV files or the generated `ecommerce.db` SQLite database file. These files are too large to be committed to GitHub.



## Setup Instructions

1. Download the full dataset from Kaggle:https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

2. Place all downloaded CSV files into this `data` folder.

3. Run `import.py` located in the project root directory. This script will load all CSV files and create the `ecommerce.db` SQLite database inside the `data` folder.

