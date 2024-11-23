# print("m")


import time
import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv("E:/materials_study_syngentas/task_one_dataset/supermarket_sales - Sheet1.csv")

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        # the use to measure the time
        start_time = time.time()
        # cur time use
        result = func(*args, **kwargs)
        # original function calls summarizvale
        end_time = time.time()
        tot_time=end_time - start_time
        # print(f"Execution time for {func.__name__}: {tot_time:.4f} seconds")
        print("Execution time for",func.__name__)
        print("time in the seconds",tot_time)

        return result
        #return the result that means the dunctin them
    return wrapper

class SalesDataProcessor:
    def __init__(self, data: pd.DataFrame):
        # pass the dataset
        self.data = data

    @timing_decorator
    def summarize_data(self):
        return self.data.describe()
       # print("im the summarize",self.data.describe())

    @timing_decorator
    def plot_sales_over_time(self):
        plt.figure(figsize=(10, 6))
        self.data.groupby('Date').sum()['Total'].plot()
        plt.title('Sales Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.show()



# Assuming the dataset has been loaded into a DataFrame named df
df['Date'] = pd.to_datetime(df['Date'])  # Convert date column to datetime

processor = SalesDataProcessor(df)
print(processor.summarize_data())
processor.plot_sales_over_time()
