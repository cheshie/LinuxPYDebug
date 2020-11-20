#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/mman.h>



int main(int argc, char *argv[])
{
	int pagesize = sysconf(_SC_PAGE_SIZE);
  printf("Page size: %d\n", pagesize);
	
	unsigned long long * addr = 0x563012efa000; 

	if (mprotect(addr, pagesize,PROT_READ) == -1) {
               int errsv = errno;
               printf("somecall() failed: %d\n", errsv);
  }
}

