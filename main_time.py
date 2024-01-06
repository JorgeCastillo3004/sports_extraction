import json
import schedule
import time


def section1():
    print("Milestone 1")
    
def section2():
    print("Milestone 2")

def section3():
    print("Milestone 3")

def section4():
    print("Milestone 3")
    
def section5():
    print("Milestone 3")

def execute_function(function_name):
    print(f"Ejecutando función: {function_name}")

# Cargar el archivo JSON
with open('input.json', 'r') as file:
    data = json.load(file)

# Procesar las secciones y programar la ejecución
for section, config in data.items():
    frequency, interval, execution_time = config.split('|')
    hour, minute, second = map(int, execution_time.split(':'))
    print(section, config)
    if frequency == "weekly":
        schedule.every(7).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(execute_function, section)
    elif frequency == "daily":
        schedule.every(1).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(execute_function, section)
    elif frequency == "monthly":
        # Aproximación: usar días múltiplos del intervalo como una aproximación al mes
        schedule.every(30).days.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(execute_function, section)
    elif frequency == "minutes":
        schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(execute_function, section)
        schedule.every(1).minutes.do(execute_function, section).tag('interval_task')
        
    elif frequency == "seconds":
        schedule.every().day.at(f"{hour:02d}:{minute:02d}:{second:02d}").do(execute_function, section)
        schedule.every(15).seconds.do(execute_function, section).tag('interval_task')

# Ejecutar el loop del planificador
while True:
    schedule.run_pending()
    time.sleep(1)
