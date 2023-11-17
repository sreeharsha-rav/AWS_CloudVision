from QueueController import QueueController
import time

queue = QueueController()
instanceID_stack = []
scale_down_factor = 2

def scale_up(count):
    if count == 0:
        return
    for _ in range(count):
        instanceID_stack.append(queue.launch_instance())

def scale_down(count):
    time.sleep(1)
    for _ in range(count):
        queue.terminate_instance(instanceID_stack.pop())

if __name__ == "__main__":
    
    emptyQueue = False
    instance_Count = 1
    scale_up(1)
    while(True):
        queueSize = int(queue.queue_count())
        #print(queueSize)

        #queue is empty, then we want to downsize
        if queueSize == 0:
            if emptyQueue and instance_Count > 1:
                if instance_Count <= scale_down_factor:
                    scale_down(instance_Count - 1)
                    instance_Count -= (instance_Count - 1) #always leave 1 running
                else:
                    scale_down(scale_down_factor)
                    instance_Count -= scale_down_factor
            emptyQueue = True                               #because sometimes the approx queue size is inaccurate,
                                                            #wait a second and recheck before sclaing down
            time.sleep(1)
        else:
            emptyQueue = False
            if instance_Count < queueSize:
                if instance_Count == 20 or queueSize >=20:
                    scale_up(20 - instance_Count)
                    instance_Count = 20
                else:
                    scale_up(1)
                    instance_Count += 1 
                    # scale_up(queueSize - instance_Count)
                    # instance_Count = queueSize

        #print('Approximate Number of Message: {} | Instances: {}'.format(queueSize, instance_Count))
        time.sleep(1)