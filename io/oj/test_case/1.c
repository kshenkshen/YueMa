#include <stdio.h>
#include <stdlib.h>
long long f[1000];
int a[1000];
int main()
{
    int box;
    scanf("%d",&box);
    f[1]=1;
    f[2]=2;
    f[3]=4;
    int i;
    for(i=4;i<=100;++i)
    {
        f[i]=f[i-1]+f[i-2]+f[i-3];
    }

    printf("%lld\n", f[box]);
    return 0;
}
