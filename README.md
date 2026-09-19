# Brazilian E-Commerce Data Analysis | Python & SQL & PowerBI
## Project Overview
This project conducts a comprehensive business analysis based on the public **Olist Brazilian E-commerce Dataset** from Kaggle.

Different from traditional blind EDA, I first explored dozens of business questions through **parallel Python and SQL implementation** to understand data characteristics. After verifying the core business pain point — **extremely low user repurchase rate on Brazilian e-commerce platform** — I further completed three core quantitative modeling analyses:
- Cohort Retention Analysis
- RFM Customer Segmentation Modeling
- Product & Regional Geographic Insight Analysis

Since the original dataset has high data quality with few dirty data, this project adopts **SQL filtering of only delivered valid orders** as the unified analysis caliber, ensuring accurate and business-oriented analysis results. Finally, core business conclusions are visualized via Power BI.

## Tech Stack
- **Data Processing & Analysis**: Python (Pandas, Matplotlib, Seaborn), SQL
- **Database**: SQLite
- **Visualization**: Matplotlib, Seaborn, Power BI
- **Development Tool**: VS Code, Jupyter Notebook

## Project Highlights
1. **Dual-technology verification capability**: Completed the same batch of business exploration problems through **both Python and SQL**, consolidating the full-process logic of data query, filtering, aggregation and analysis.
2. **Business-driven modeling**: Avoided blind data analysis. Based on preliminary data exploration, identified the core problem of low repurchase rate, and launched targeted cohort retention and RFM user segmentation modeling.
3. **Standardized engineering structure**: Classified official analysis code, exploratory draft code, SQL scripts and visual output files, conforming to standard data analysis project specifications.
4. **Strict analysis caliber**: Filtered valid `delivered` orders by SQL to eliminate interference of canceled/returned orders and improve analysis authenticity.

## Project Structure
```
brazil-ecommerce-analysis/
├── README.md                # English project introduction
├── README_CN.md             # Chinese project introduction
├── requirements.txt         # Python dependency list
├── .gitignore               # Git ignore configuration
├── data/                    # Dataset storage & description
│   └── README.md            # Data acquisition & generation guide
├── notebooks/               # Formal exploratory analysis notebook
├── src/                     # Standard reusable Python scripts
├── sql/                     # Final version SQL analysis scripts
│   └── exploratory/         # SQL exploratory trial scripts
├── outputs/
│   └── figures/             # Analysis visualization charts
├── archive/exploratory/     # Original Python exploration drafts
└── docs/                    # Data dictionary & supplementary documents
```

## Environment & Running Guide
1. Install dependent libraries
```bash
pip install -r requirements.txt
```
2. Data preparation
- Download the full Olist dataset from Kaggle and place all CSV files in the `data` folder
- Run the root `import.py` script to generate local `ecommerce.db` SQLite database
- *Note: Large database files are not uploaded to GitHub*

3. Run analysis
- View complete EDA and modeling process via `notebooks` files
- Verify unified analysis logic through SQL scripts in `sql` folder

## Core Analysis Findings
1. **User repurchase characteristics**: The platform has an extremely low user repurchase rate, almost all users are one-time consumers, lacking loyal long-term customers, which is the core pain point of the platform.
2. **User retention performance**: Cohort analysis verifies that user retention rate drops sharply in the short term, with no obvious user cycle repurchase habit.
3. **Customer value differentiation**: RFM modeling shows obvious polarization of customer value; a small number of high-value customers contribute major revenue, while most users have low consumption value.
4. **Regional & product insight**: Brazilian e-commerce consumption shows obvious regional concentration, with southeast regions as the core consumption area; different categories have obvious differences in order volume and customer unit price.

## Future Optimization Directions
- Add user portrait multi-dimensional analysis to further explore user consumption preferences
- Introduce machine learning models to predict user repurchase possibility
- Optimize Power BI dashboard to realize dynamic data interactive display

## Dataset Source
Kaggle Olist Brazilian E-commerce Dataset
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce