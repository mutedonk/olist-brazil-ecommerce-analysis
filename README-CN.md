# 数据集说明

本项目使用 Kaggle Olist Brazilian E-commerce 公开数据集。

仓库**不存放原始CSV文件以及生成的 ecommerce.db 数据库文件**，文件体积较大，不提交至GitHub。



## 获取步骤

1. 前往Kaggle下载原始数据集：https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

2. 将下载的全部csv文件放到本data文件夹内。

3. 运行项目根目录下的 `import.py`，脚本会读取csv文件，在data目录生成 `ecommerce.db` SQLite数据库。



