#stopwatch start
from datetime import datetime
start = datetime.timestamp(datetime.now())

#imports
from functions import run

#run
run()

#stopwatch finish
finish = datetime.timestamp(datetime.now())
duration = round(finish - start,3)
print("Time to run: " + str(duration) + " seconds")