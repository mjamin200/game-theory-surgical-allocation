# Importing required libraries
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import copy
import os





def generate_poisson_arrivals(lambda_, duration):
  """Generates a list of arrival request for a Poisson process with rate lambda.

  Args:
    lambda_: The rate of the Poisson process per slot[8 hours].
    duration: Number of slots.

  Returns:
    A list of arrival times in slots.
    Number of arrivals in the duration.
  """

  arrival_times = []
  t = 0
  while t < duration:
    inter_arrival_time = random.expovariate(lambda_)
    if inter_arrival_time >= 0:
      t += inter_arrival_time
    if t<duration:
        arrival_times.append(t)

  return arrival_times, len(arrival_times)

def generate_surgery(type):  
  """Generates a surgery time for a surgery type.
    Note that the return Duration time normalized to 8 hours[1 slot]. 

  Args:
    type: The type of the surgery.
  Returns:
    Duration of surgery .
  """
  Std_dev=1
  if type == 'A':
      Mean = 2;  # average duration of surgery A
  elif type == 'B':
      Mean = 5;  # average duration of surgery B
  elif type == 'C':
      Mean = 10; # average duration of surgery C
  
  while(True) :
    temp = np.random.normal(Mean, Std_dev,1)
    if temp>0 :
      return temp/8
  
def hospital_detector(request,available_hospital,index_of_request_in_queue): 
  """Detects the hospital with the min duration for a request.

  args:
    request: The request to be processed.
    available_hospital: The available hospitals.
    index_of_request_in_queue: The index of the request in the queue.
    pass_slot: The number of slots that the request can wait in the queue.
  Returns:
    The available hospital with the min duration.
    cost of the surgery.

  """
  Costs =[2,5,7] ; #cost of each surgery A,B,C
  durations = request[2]

  for i in range(len(available_hospital)):
    if available_hospital[i] == 0:
       durations[i]=-1        # if the hospital is not available, set the duration to -1

  if np.all(durations==-1):    # if all hospitals are not available, set the duration to -1
    return [request[0],request[1],'n',-1,-1,index_of_request_in_queue]
  
  duration = np.min(durations[durations>0]) # find the min positive duration
  if np.where(durations==duration)[0] == 0:
    hospital = 'a'  
    cost=Costs[0]
  elif np.where(durations==duration)[0]==1:
    hospital = 'b'
    cost=Costs[1]
  elif np.where(durations==duration)[0]==2:
    hospital = 'c'
    cost=Costs[2]

  return [request[0],request[1],hospital,duration,cost,index_of_request_in_queue]

def print_request_list(input_list):
    """
    Prints a list of elements in a formatted manner.

    Args:
        element_list (list): List of elements containing surgery, arrival time, and duration.
    """
    print("{:<10} {:<30} {:<65} {:<13} {:<20} {:<10}".format("Surgery", "Arrival Time", "Durations of Surgery in a,b,c","pass slot","status","best hospital"))
    print("-" * 160)
    for element in input_list:
      surgery = element[0]
      arrival_time = element[1]
      duration = element[2]
      pass_slot = element[3]
      status = element[4]
      best=element[5]

      duration_str = ", ".join(map(str, duration))
      print("{:<10} {:<30} {:65} {:<13} {:<20} {:<10}".format(surgery, arrival_time, duration_str,pass_slot,status,best))
    
def print_waiting_list(waiting_list):
    """Prints the waiting list.

    Args:
      waiting_list: The waiting list to be printed.
    """
    if len(waiting_list) == 0:
        return
    
    print("Waiting List hospital",waiting_list[0][2]," :")
    print("{:<10} {:<20} {:<20} {:<10}".format("Surgery", "Time of Arrival", "Duration", "Cost"))
    print("-" * 80)

    for item in waiting_list:
        surgery = item[0]
        time_of_arrival = item[1]
        duration = item[3]
        cost = item[4]

        print("{:<10} {:<20} {:<20} {:<10}".format(surgery, time_of_arrival, duration, cost))
        print()

def best_hospital_detector(request):
  """Detects the hospital with the min duration for a request.

  args:
    request: The request to be processed.
  Returns:
    The available hospital with the min duration.

  """
  durations = request[2]

  duration = np.min(durations)                 # find the min duration
  if np.where(durations==duration)[0][0] == 0:
    hospital = 'a'  
  elif np.where(durations==duration)[0][0]==1:
    hospital = 'b'
  elif np.where(durations==duration)[0][0]==2:
    hospital = 'c'
  
  return [request[0],request[1],request[2],request[3],request[4],hospital]



#----------------------------------------------------------------------------------------------------
#inputs

Num_slot_list = [200000]                      # number of slots
Coefficient=1
pass_slot=5                                      # pass slot is the number of slots that the request can wait in the queue
poisson_rate_A = 0.2*Coefficient                 # poisson rate of surgery A  per hour
poisson_rate_B = 0.1*Coefficient                 # poisson rate of surgery B  per hour
poisson_rate_C = 0.05*Coefficient                # poisson rate of surgery C  per hour

#----------------------------------------------------------------------------------------------------
# Get the current directory
current_dir = os.getcwd()

for file_name in os.listdir(current_dir):
    if file_name.endswith('.txt'):
        os.remove(os.path.join(current_dir, file_name))

for file_name in os.listdir(current_dir):
    if file_name.endswith('.png'):
        os.remove(os.path.join(current_dir, file_name))

#----------------------------------------------------------------------------------------------------

for Num_slot in Num_slot_list:

  output_file=os.path.join(current_dir, f'output {Num_slot} slots.txt')
                           
  with open(output_file, 'w') as file:
    pass
  len_queue=[]                     # len_queue is the list of number of requests in the queue per slot
  queue_list=[]
  delay_list=[]
  average_waiting_time=[]
  a_is_busy =0  #  duration of busy time of hospital a  
  b_is_busy =0  #  duration of busy time of hospital b
  c_is_busy =0  #  duration of busy time of hospital c
  available_hospital = [1,1,1]     # 1 means avalible, 0 means not available


  for slot in range(0,Num_slot): # 8 hours[1 slot]

    
    if slot>0:
      for item in queue_list:
        if item[4]=='new request':
          item[4]='Queued'
    
  # Generate arrival times in new slot for each surgery and put all of them in a queue
    arrival_times_A, num_arrivals_A = generate_poisson_arrivals(poisson_rate_A*8, 1)            # 1.6 request per slot[8 hours] 
    arrival_times_B, num_arrivals_B = generate_poisson_arrivals(poisson_rate_B*8, 1)            # 0.8 request per slot[8 hours]  
    arrival_times_C, num_arrivals_C = generate_poisson_arrivals(poisson_rate_C, 1)            # 0.4 request per slot[8 hours]
                                              
    # Store the arrival times of each requested surgery in the queue
    # 1st element is the type of the request, 2nd is the time of arrival, 3th is the duration of surgery   
    for time in arrival_times_A:
      queue_list.append(('A', time+slot ,generate_surgery('A')*[1,2,3],pass_slot,'new request'))  # Store type 'A' along with the arrival time
    for time in arrival_times_B:
      queue_list.append(('B', time+slot ,generate_surgery('B')*[3,1,2],pass_slot,'new request'))  # Store type 'B' along with the arrival time
    for time in arrival_times_C:
      queue_list.append(('C', time+slot ,generate_surgery('C')*[2,3,1],pass_slot,'new request'))  # Store type 'C' along with the arrival time
    
    # best hospital detector
    for i in range(len(queue_list)):
      if queue_list[i][4]=='new request':
        queue_list[i]=best_hospital_detector(queue_list[i])
      else:
        queue_list[i][4]='ready to process'
      
    # Sort the list based on the time values
    queue_list = sorted(queue_list, key=lambda x: x[1])

  # check if the hospital is busy or not
    a_is_busy-=1
    b_is_busy-=1
    c_is_busy-=1

    if(a_is_busy<0):
      a_is_busy=0
      available_hospital[0]=1
    else:
      available_hospital[0]=0

    if(b_is_busy<0):
      b_is_busy=0
      available_hospital[1]=1
    else:
      available_hospital[1]=0 

    if(c_is_busy<0):
      c_is_busy=0  
      available_hospital[2]=1
    else:
      available_hospital[2]=0 

    '''
    with open(output_file, 'a') as file:
      original_stdout = sys.stdout
      sys.stdout = file
      print("*"*190)
      print("slot",slot)
      print()
      print("available hospital for next slot :",available_hospital)
      print()
      print("Requests in queue :")
      print_request_list(queue_list)
      print()
    sys.stdout = original_stdout
    '''
    flag=False
    end=False
    
    while not flag:

      if end:
        for item in temp_request:
          
          if item[4]!='pass slot':
            queue_list=[item]+queue_list

        for item in temp_request:
          if item[4]=='pass slot':
            item[3]-=1
            queue_list.append(item)
        end=False

      request_in_process=[]

      for item in queue_list:
        if item[4] != 'pass slot':
          request_in_process.append(item)     # request_in_process is a list of requests that are in process
        if len(request_in_process)==3:
          break 
          
      if len(request_in_process)==0:
        break

      request_in_process = sorted(request_in_process, key=lambda x: x[1])          # Sort the list based on the time values             
      temp_request = copy.deepcopy(request_in_process)                              # temp_request is a copy of request_in_process

      for i in range(len(request_in_process)):                                      # update the duration of busy time of each hospital
        queue_list.pop(0)                                                   # remove the requests that are in process from the queue list


      '''
      with open('output.txt', 'a') as file:
        original_stdout = sys.stdout
        sys.stdout = file
        print("In process request :")
        print()
        print_request_list(request_in_process)  
        print()
      sys.stdout = original_stdout
      '''
      # DA algorithm
      end=False
      waiting_list_hospital_a = []
      waiting_list_hospital_b = []
      waiting_list_hospital_c = []
      max_cost_a=0
      max_cost_b=0
      max_cost_c=0
      step_DA=0

        

      
      while not end:
          
        if(len(request_in_process)==0):
            break

        waiting_list_hospital_a = []
        waiting_list_hospital_b = []
        waiting_list_hospital_c = []
        max_cost_a=0
        max_cost_b=0
        max_cost_c=0

          
        
        step_DA+=1

        for i in range(len(request_in_process)): # create waiting list for each hospital

          if hospital_detector(request_in_process[i],available_hospital,i)[2]=='a':
            waiting_list_hospital_a.append(hospital_detector(request_in_process[i],available_hospital,i))

          elif hospital_detector(request_in_process[i],available_hospital,i)[2]=='b':
            waiting_list_hospital_b.append(hospital_detector(request_in_process[i],available_hospital,i))

          elif hospital_detector(request_in_process[i],available_hospital,i)[2]=='c':
            waiting_list_hospital_c.append(hospital_detector(request_in_process[i],available_hospital,i))

          elif hospital_detector(request_in_process[i],available_hospital,i)[2]=='n':
            queue_list.append(temp_request[i])
                
        for j in range(len(waiting_list_hospital_a)):
          if j==0 :
            max_cost_a = waiting_list_hospital_a[j][4]               # set cost of the first request in the queue to be the max cost request
            max_cost_a_index = waiting_list_hospital_a[j][5]         # index of the max cost request in the queue

          elif max_cost_a < waiting_list_hospital_a[j][4] and j>0:           # find the max cost request in the queue
            max_cost_a = waiting_list_hospital_a[j][4]
            request_in_process[max_cost_a_index][2][0]=-1                             # set the duration of the Previous max cost in the hospital a request to -1 to be not available
            max_cost_a_index = waiting_list_hospital_a[j][5]
          else:
            request_in_process[waiting_list_hospital_a[j][5]][2][0]=-1        # set the duration of the max cost in the hospital a request to -1 to be not available
              
          
        for j in range(len(waiting_list_hospital_b)):
          if j==0 :
            max_cost_b = waiting_list_hospital_b[j][4]               # set cost of the first request in the queue to be the max cost request
            max_cost_b_index = waiting_list_hospital_b[j][5]         # index of the max cost request in the queue
            

          elif max_cost_b < waiting_list_hospital_b[j][4] and j>0:     # find the max cost request in the queue
            max_cost_b = waiting_list_hospital_b[j][4]
            request_in_process[max_cost_b_index][2][1]=-1                    # set the duration of the Previous max cost in the hospital b request to -1 to be not available
            max_cost_b_index = waiting_list_hospital_b[j][5]
          else:
            request_in_process[waiting_list_hospital_b[j][5]][2][1]=-1       # set the duration of the max cost in the hospital b request to -1 to be not available

          
        for j in range(len(waiting_list_hospital_c)):
          if j==0 :
            max_cost_c = waiting_list_hospital_c[j][4]               # set cost of the first request in the queue to be the max cost request
            max_cost_c_index = waiting_list_hospital_c[j][5]         # index of the max cost request in the queue

          elif max_cost_c < waiting_list_hospital_c[j][4] and j>0:     # find the max cost request in the queue
            max_cost_c = waiting_list_hospital_c[j][4]
            request_in_process[max_cost_c_index][2][2]=-1                    # set the duration of the Previous max cost in the hospital c request to -1 to be not available
            max_cost_c_index = waiting_list_hospital_c[j][5]
          else:
            request_in_process[waiting_list_hospital_c[j][5]][2][2]=-1       # set the duration of the max cost in the hospital c request to -1 to be not available



        # update pass slot number
        if step_DA==1:
          if(len(waiting_list_hospital_a)>1) and request_in_process[waiting_list_hospital_a[1][5]][3]>0:
            for i in range (1,len(waiting_list_hospital_a)):
              temp_request[waiting_list_hospital_a[i][5]][4]='pass slot'
            end=True
            flag=False
            break

          elif(len(waiting_list_hospital_b)>1) and request_in_process[waiting_list_hospital_b[1][5]][3]>0:
            for i in range (1,len(waiting_list_hospital_b)):
              temp_request[waiting_list_hospital_b[i][5]][4]='pass slot'
            end=True
            flag=False
            break

          elif(len(waiting_list_hospital_c)>1) and request_in_process[waiting_list_hospital_c[1][5]][3]>0:
            for i in range (1,len(waiting_list_hospital_c)):
              temp_request[waiting_list_hospital_c[i][5]][4]='pass slot'
            end=True
            flag=False
            break
        
        '''
        with open(output_file, 'a') as file: 
          original_stdout = sys.stdout
          sys.stdout = file
          print("step",step_DA)
          print()
          print_waiting_list(waiting_list_hospital_a) 
          print_waiting_list(waiting_list_hospital_b)
          print_waiting_list(waiting_list_hospital_c)
          print()
        sys.stdout = original_stdout
        '''

      
            
        if max(len(waiting_list_hospital_a),len(waiting_list_hospital_b),len(waiting_list_hospital_c)) <= 1 :
          end=True
          flag=True
          # update the duration of busy time of each hospital
          if len(waiting_list_hospital_a)==1:    
            a_is_busy = waiting_list_hospital_a[0][3]
            delay_list.append(slot-int(waiting_list_hospital_a[0][1]))
          if len(waiting_list_hospital_b)==1:
            b_is_busy = waiting_list_hospital_b[0][3]
            delay_list.append(slot-int(waiting_list_hospital_b[0][1]))
          if len(waiting_list_hospital_c)==1:
            c_is_busy = waiting_list_hospital_c[0][3]
            delay_list.append(slot-int(waiting_list_hospital_c[0][1]))
          break
    

    len_queue.append(len(queue_list))

    if len(delay_list)>0:
      average_waiting_time.append(sum(delay_list)/len(delay_list))
    else:
      average_waiting_time.append(0)
    

    
    '''
    with open(output_file, 'a') as file: 
      original_stdout = sys.stdout
      sys.stdout = file
      print("number of queued requests :",len_queue[-1])
      print()
      print("Average waiting time accepted requests :",average_waiting_time[-1])
      print()
      
    sys.stdout = file
    '''

  '''
  ll=len(delay_list)
  avg_1=sum(delay_list[int(0.1*ll):int(0.5*ll)])/len(delay_list[int(0.1*ll):int(0.5*ll)])

  with open(output_file, 'a') as file: 
    original_stdout = sys.stdout
    original_stdout = sys.stdout
    print("average in first  half",avg_1)
    print()
    sys.stdout = file
  '''
  fig, axs = plt.subplots(1, 2, figsize=(10, 4))  # 1 row, 2 columns

  # Plot average waiting time
  x=range(len(average_waiting_time))
  axs[0].plot(x,average_waiting_time)  
  if Num_slot<20:
    axs[0].set_xticks(range(len(x)))
    axs[0].set_xticklabels(x)

  axs[0].set_xlabel('slot')
  axs[0].set_ylabel('average waiting time [in slot]')
  axs[0].set_title('average waiting time')

  # Plot number of queued requests
  x1=range(len(len_queue))
  axs[1].plot(x1,len_queue)
  if Num_slot<20:
    axs[1].set_xticks(range(len(x1)))
    axs[1].set_xticklabels(x1)
  axs[1].yaxis.set_major_formatter('{:.0f}'.format)  # Set precision of y-axis tick labels

  axs[1].set_xlabel('slot')
  axs[1].set_ylabel('number of queued requests')
  axs[1].set_title('Number of queued requests')

  note_text = f"Number of pass slot : {pass_slot} and number of slots is {Num_slot} \n with poisson rate A:{poisson_rate_A},     B:{poisson_rate_B},    C:{poisson_rate_C} ."
  plt.figtext(0.5, 0.005, note_text, color='red', ha='center', va='bottom')

  if Num_slot<20:
    axs[0].grid(True)
    axs[1].grid(True)

  plt.tight_layout()
  #plt.show()
  

  # Save the figure
  plt.savefig(f'figure {Num_slot} slots.png')

  




          

      
  
