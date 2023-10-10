#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h> // sleep thread.
#include <string.h> // memcopy
 
static const char values[3]={'A','B','C'};
static sem_t semaphore[3];
static pthread_t thread[3];
 
static void *routine(void *arg);
 
int main(int argc, char *args[])
{
    for (int i = 0; i < 3; i++)
	if (sem_init(&(semaphore[i]), 0, (i==0)?1:0))
	    {
		perror("sem_init");
		exit(-1);
	    }
    for (int i = 0; i < 3; i++)
	{
	    int *local_idx;
	    if ((local_idx= (int *)malloc(sizeof(int)))==NULL)
		{
		    perror("malloc");
		    exit(-1);
		}
	    *local_idx=i;
	    if  (pthread_create(&thread[i], NULL, routine, local_idx))
	    	{
	    	    perror("pthread_create");
	    	    exit(-1);
	    	}
	}
    for (int i = 0; i < 3; i++)
      if (pthread_join(thread[i], NULL))
	{
	  perror("pthread_join");
	  exit(-1);
	}
}
 
static void *routine(void *arg)
{
    int local_id;
    memcpy(&local_id,arg,sizeof(int));
    free(arg);
    for( ; 1 ; )
	{
	    if (sem_wait(&semaphore[local_id]))
		{
		    perror("sem_wait");
		    exit(-1);
		}
	    printf("%c",values[local_id]);
	    //sleep(1);
	    if (sem_post(&semaphore[(local_id+1)%3]))
		{
		    perror("sem_post");
		    exit(-1);
		}
	}
}