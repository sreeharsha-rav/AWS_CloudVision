import subprocess


process1 = subprocess.Popen(['python3', 'Autoscaling.py']) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(['python3', 'ReceiveQueue.py'])
process3 = subprocess.Popen(['python3', 'flask_trial.py'])
process4 = subprocess.Popen(['python3', 'workload_multi.py'])

process1.wait() 
process2.wait()
process3.wait()
process4.wait()

if input("Press Enter to Close"):
    subprocess.run('rm data.json')