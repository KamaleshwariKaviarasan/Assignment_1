import subprocess

try:
    print("Started runing Excel to SQL file")
    subprocess.run(["python", "Excel_To_MYSQL.py"], check=True)
    print("Executed the excel to sql file successfully")
    print("Started runnning Streamlit file")
    subprocess.run(["streamlit", "run", "app.py"], check=True)
    print("Executed Strwamlit file successfully")
except:
    print("Error Occured")
