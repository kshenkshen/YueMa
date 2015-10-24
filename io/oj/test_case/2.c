#include<stdio.h>
#include<string.h>
#include<math.h>

const long maxn=10000;
double ans;
long n,i,x,y;

int main()
{
    scanf("%ld",&n);
    ans=0;
    for (i=1;i<=n;i++)
      {
        scanf("%ld%ld",&x,&y);
        ans=ans+x*y/(10.0);
      }
    printf("%.2f\n",ans);
}

