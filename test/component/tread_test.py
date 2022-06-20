from queue import Queue
from threading import Thread, Lock
from time import sleep, time

i = 0 

# A thread that produces data
def producer(out_q, i, ):
	while True:
		# Produce some data
		word = ["hello", "world"]
		i = (i + 1)%2

		data = input("word : ")
		
		out_q.put(data)
		out_q.put(data)
		print("-----------------------")
		print("producer sent : ", data)
		sleep(1)
		
# A thread that consumes data
def consumer1(in_q,lock, ):
	while True:
		# etat1 = True
		# while in_q.empty():
		# 	if etat1:
		# 		etat1 = False
		# 		tik1 = time()
		# 	sleep(2)
			
			#print("empty is q1")
		# Get some data
		lock.acquire()
		data = in_q.get()
		lock.release()
		# Process the data
		tok1 = time()
		print("consumer1 received : ", data)
		# Indicate completion
		in_q.task_done()


def consumer2(in_q, lock, ):
	while True:
		# Get some data
		# etat2 = True
		# while in_q.empty():
		# 	if etat2:
		# 		etat2 = False
		# 		tik2 = time()
		# 	sleep(2)

			#print("empty is q2")

		lock.acquire()
		data = in_q.get()
		lock.release()
		# Process the data
		tok2 = time()
		print("consumer2 received : ", data) 
		#print("-----------------------")
		
		# Indicate completion
		in_q.task_done()


# Create the shared queue and launch both threads
q = Queue()

lock = Lock()

t1 = Thread(target = consumer1, args =(q, lock, ))
t2 = Thread(target = consumer2, args =(q, lock, ))
t3 = Thread(target = producer, args =(q, i, ))

if __name__ == "__main__":

	t1.start()
	t2.start()
	t3.start()
	# Wait for all produced items to be consumed
	q.join()