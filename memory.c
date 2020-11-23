#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/mman.h>

static char *buffer;

int main(int argc, char *argv[])
{
	int pagesize;
	struct sigaction sa;

	buffer = memalign(pagesize, 4 * pagesize);
	printf("Start of region:        %p\n", buffer);
	printf("Process ID: %d\n", getpid());
	unsigned long long * addr = buffer;
	
	getchar();

	int counter = 0;
	for (char *p = buffer ; ; ){
		if (counter == 1024){
			counter = 0;
			sleep(1);
		}

		printf("a");
		*(p++) = 'a';
		counter++;
	}

}
