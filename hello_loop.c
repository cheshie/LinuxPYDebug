#include <stdio.h>
#include <unistd.h>

void printer(int i)
{
	printf("Petla nr: %d\n",i);
}

int main()
{
	int i = 0;
	for(;;i++)
	{
		printer(i);
		sleep(1);
	}
	
	return 0;
}

