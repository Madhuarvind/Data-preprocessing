from flask import Flask, request, render_template, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Ensure the static folder is created for saving charts
os.makedirs('static/charts', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    # Load the dataset
    df = pd.read_csv(file)
    
    # Preprocess the dataset (basic example)
    df_cleaned = df.dropna()  # Remove missing values

    # Save the cleaned dataset
    cleaned_file_path = 'static/cleaned_dataset.csv'
    df_cleaned.to_csv(cleaned_file_path, index=False)

    # Get the selected charts from the form
    selected_charts = request.form.getlist('charts')

    # Render the results page with the cleaned dataset and selected charts
    return render_template(
        'result.html',
        cleaned_file=cleaned_file_path,
        charts_selected=bool(selected_charts),
        charts=generate_comparison_charts(df, df_cleaned, selected_charts)
    )

def generate_comparison_charts(df_original, df_cleaned, selected_charts):
    charts = []
    
    # Generate Histogram
    if 'histogram' in selected_charts:
        plt.figure(figsize=(12, 6))
        sns.histplot(df_original, kde=True)
        plt.title('Original Data - Histogram')
        original_chart_path = 'static/charts/original_histogram.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Histogram', 'file': url_for('static', filename=f'charts/original_histogram.png')})
        plt.close()
        
        plt.figure(figsize=(12, 6))
        sns.histplot(df_cleaned, kde=True)
        plt.title('Cleaned Data - Histogram')
        cleaned_chart_path = 'static/charts/cleaned_histogram.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Histogram', 'file': url_for('static', filename=f'charts/cleaned_histogram.png')})
        plt.close()

    # Generate Box Plot
    if 'boxplot' in selected_charts:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_original)
        plt.title('Original Data - Box Plot')
        original_chart_path = 'static/charts/original_boxplot.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Box Plot', 'file': url_for('static', filename=f'charts/original_boxplot.png')})
        plt.close()
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_cleaned)
        plt.title('Cleaned Data - Box Plot')
        cleaned_chart_path = 'static/charts/cleaned_boxplot.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Box Plot', 'file': url_for('static', filename=f'charts/cleaned_boxplot.png')})
        plt.close()

    # Generate Scatter Plot
    if 'scatter' in selected_charts and len(df_original.columns) >= 2:
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df_original.iloc[:, 0], y=df_original.iloc[:, 1])
        plt.title('Original Data - Scatter Plot')
        original_chart_path = 'static/charts/original_scatter.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Scatter Plot', 'file': url_for('static', filename=f'charts/original_scatter.png')})
        plt.close()
        
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df_cleaned.iloc[:, 0], y=df_cleaned.iloc[:, 1])
        plt.title('Cleaned Data - Scatter Plot')
        cleaned_chart_path = 'static/charts/cleaned_scatter.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Scatter Plot', 'file': url_for('static', filename=f'charts/cleaned_scatter.png')})
        plt.close()

    # Generate Line Chart
    if 'line' in selected_charts:
        plt.figure(figsize=(12, 6))
        df_original.plot.line()
        plt.title('Original Data - Line Chart')
        original_chart_path = 'static/charts/original_line.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Line Chart', 'file': url_for('static', filename=f'charts/original_line.png')})
        plt.close()
        
        plt.figure(figsize=(12, 6))
        df_cleaned.plot.line()
        plt.title('Cleaned Data - Line Chart')
        cleaned_chart_path = 'static/charts/cleaned_line.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Line Chart', 'file': url_for('static', filename=f'charts/cleaned_line.png')})
        plt.close()

    # Generate Bar Chart
    if 'bar' in selected_charts:
        plt.figure(figsize=(12, 6))
        df_original.head(10).plot(kind='bar')
        plt.title('Original Data - Bar Chart')
        original_chart_path = 'static/charts/original_bar.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Bar Chart', 'file': url_for('static', filename=f'charts/original_bar.png')})
        plt.close()
        
        plt.figure(figsize=(12, 6))
        df_cleaned.head(10).plot(kind='bar')
        plt.title('Cleaned Data - Bar Chart')
        cleaned_chart_path = 'static/charts/cleaned_bar.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Bar Chart', 'file': url_for('static', filename=f'charts/cleaned_bar.png')})
        plt.close()

    # Generate Pie Chart (for categorical data)
    if 'pie' in selected_charts and df_original.select_dtypes(include=['object']).columns.any():
        plt.figure(figsize=(8, 8))
        df_original[df_original.columns[0]].value_counts().plot.pie(autopct='%1.1f%%')
        plt.title('Original Data - Pie Chart')
        original_chart_path = 'static/charts/original_pie.png'
        plt.savefig(original_chart_path)
        charts.append({'name': 'Original Pie Chart', 'file': url_for('static', filename=f'charts/original_pie.png')})
        plt.close()

        plt.figure(figsize=(8, 8))
        df_cleaned[df_cleaned.columns[0]].value_counts().plot.pie(autopct='%1.1f%%')
        plt.title('Cleaned Data - Pie Chart')
        cleaned_chart_path = 'static/charts/cleaned_pie.png'
        plt.savefig(cleaned_chart_path)
        charts.append({'name': 'Cleaned Pie Chart', 'file': url_for('static', filename=f'charts/cleaned_pie.png')})
        plt.close()

    return charts

if __name__ == '__main__':
    app.run(debug=True)
