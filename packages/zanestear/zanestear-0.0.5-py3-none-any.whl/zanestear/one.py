
def one():
    """
    根据   写出两个函数式：
Res1=x*(math.sqrt(x+1)-math.sqrt(x))
Res2=x/（math.sqrt(x+1)+math.sqrt(x)）
接着用这两个函数式计算同一函数值并分析误差及产生原因。

    :return:
    """
    import math
    def func1(x):
        res = x * (math.sqrt(x + 1) - math.sqrt(x))  # 一式的编程实现
        return res

    def func2(x):
        sum = math.sqrt(x + 1) + math.sqrt(x)
        res = x / sum  # 二式的编程实现
        return res

    print(func1(1), func1(10 ** 10))
    print(func2(1), func2(10 ** 10))


def two():
    """
    （2）先由递推关系计算出 至 的值，观察输出的值是否合理。再利用Python导入库进行积分运算。观察积分出的值与递推出的值的差别。
    :return:
    """
    import math
    from sympy import *  # 导入此库用于进行积分运算
    x = symbols('x') # 以x作为积分变量
    I = [i for i in range(100)]
    I[0] = math.log(1.2, math.e)
    print(I[0])

    def func1(a):
        inte = integrate(x ** a / (x + 5), (x, 0, 1)) # 积分运算
        return inte

    for i in range(20):
        I[i + 1] = I[i] * (-5) + 1.0 / (i + 1) # 递推运算
        print(I[i + 1])
    print('-----------------------') # 分隔线，用于分开两种不同运算的结果
    for j in range(21):
        print(func1(j))

def three():
    """
    二分法 x*x*x+4x*x*x-10=0
    :return:
    """
    """
    #include<iostream>
#include<cmath>
using namespace std;
double ans,n,l,r,mid;
double fun(double x){
    return x*x*x+4*x*x-10;
}
int main()
{
    n=-log(0.00025)/log(2)-1;
    cout<<n;
    l = 1;
    r = 2;   
    mid = (l+r)/2;
    int num = 0;
    while(l<r || num<n)
    {
        cout<<l<<" "<<r<<endl;
        double ll = fun(l);
        double rr = fun(r);
        mid = (l+r)/2;
        ans = mid;
        double mm = fun(mid);
        if(mm == 0)
        {
            ans = mid;
            break;
        }
        if(mm * ll<0)
        {
            r=mid;
            continue;
        }
        if(mm*ll>0)
            l = mid;
        num++;
    }
    cout<<ans;
}

    """

def four():
    """
    迭代法
    :return:
    """
    import math
    import matplotlib.pyplot as plt
    import numpy
    def f3(x):
        return math.sqrt(x + 1)

    x2 = 1
    x = numpy.linspace(0, 2, 200)
    y1 = [math.sqrt(i + 1) for i in x]
    y2 = [i for i in x]
    plt.plot(x, y1)
    plt.plot(x, y2)

    for i in range(1, 10):
        t1 = x2
        t2 = f3(x2)
        x2 = f3(x2)
        plt.plot([t1, t2], [t2, t2], linestyle='dotted')
        plt.plot([t2, t2], [t2, f3(t2)], linestyle='dotted')
        print(x2)
    plt.show()

def five():
    """牛顿迭代法"""
    """
    #include <stdio.h>
#include <stdlib.h>

int main()
{
     double a,x0;
     double x;
    int c=1;
    int n;
    scanf("%lf %lf %d",&a,&x0,&n);
    while(c<=n){
        x=(x0+a/x0)/2;
        printf("x%d=%lf\n",c,x);
        x0=x;
        c++;

    }
    return 0;
}
"""

def six():
    """
    线性方程组迭代法
    :return:
    """
    """
    #include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main()
{
    int i,j,n,k;
   double a[5],A[20][20],b[20],x[20],X[20],cha[20],max=1,t;
   printf("输入矩阵：\n");
   for(i=0;i<5;i++)
   {
       scanf("%lf",&a[i]);
   }
   for(i=0;i<20;i++)
   {
       for(j=0;j<20;j++)
       {
           if(i<=2)
           {
               if(j<=i+2)
                A[i][j]=a[2-i+j];
               else
                A[i][j]=0;
           }
           if(i>2)
           {
               if(j<i-2)
                A[i][j]=0;
               else if(j<i+3)
                A[i][j]=a[j+2-i];
               else
                A[i][j]=0;
           }
       }

   }
printf("\n");

   for(i=0;i<20;i++)
   {
       for(j=0;j<20;j++)
        printf("%.2f\t",A[i][j]);
       printf("\n");
   }
   printf("输入b：\n");
   for(i=0;i<20;i++)
   {
       scanf("%lf",&b[i]);
   }
   printf("输入x0：\n");
    for(i=0;i<20;i++)
   {
       scanf("%lf",&x[i]);
   }
   for(n=0;n<20&&max>0.00001;n++)
   {
        for(k=0;k<20;k++)
           {
               X[k]=x[k];
           }
       for(i=0;i<20;i++)
       {
           t=0;
           for(j=0;j<20;j++)
           {
               if(i!=j)
                 t=t+A[i][j]*x[j];//若把x->X,则为高斯-赛德尔迭代
           }
           x[i]=(b[i]-t)/A[i][i];
           cha[i]=fabs(x[i]-X[i]);
       }

       printf("第%d次迭代解向量为：\n",n+1);
       for(i=0;i<20;i++)
       {
           printf("%.2f\t",x[i]);
       }
       printf("\n");
        max=cha[0];
       for(i=0;i<20;i++)
       {
           if(fabs(cha[i])>fabs(max))
            max=fabs(cha[i]);
       }
   }
   printf("最终迭代%d次，最终解为\n",n);
   for(i=0;i<20;i++)
   {
       printf("%.2f\t",x[i]);
   }
   return 0;

}
"""

def seven():
    """（拉格朗日插值）"""
    """
    #include<stdio.h> 
float l(float *x,float x0,int k,int n); //拉格朗日基函数
float lagrange(float *x,float *y,float x0,int n);//拉格朗日多项式

int main(){
	float x[100];//给出的结点的x值集合
	float y[100];//给出结点的y值集合
	float Y[100];//要求函数值的集合
	float X[100];//给出的初值的集合
	int N,i,n;//N:结点数，n:初值数
	printf("请输入已知结点个数：\n");
	scanf("%d",&N);
	printf("请输入已知结点的x:\n");
	for(i=0;i<N;i++)
	{
		scanf("%f",&x[i]);
	}
	printf("请输入已知结点的y:\n");
	for(i=0;i<N;i++)
	{
		scanf("%f",&y[i]);
	}
	printf("请输入初值个数：\n");
	scanf("%d",&n);
	printf("请输入初值：\n");
	for(i=0;i<n;i++)
	{
		scanf("%f",&X[i]);
	}
	//计算对应初值的被插值函数值
	for(i=0;i<n;i++)
	{
		Y[i]=lagrange(x,y,X[i],N);
	}
	 printf("经过拉格朗日插值法求得的差值函数在对应初值点的值：\n");
	 for(i=0;i<n;i++)
	{
		printf("sin(%2.6f)=%5.6f\n",X[i],Y[i]);
	}
	 return 0;
}
/*
*计算拉格朗日基函数
*/
float l(float *x,float x0,int k,int n)
{
	float Y=1;
	int i;
	for(i=0;i<n;i++)
	{
		if(i!=k)
		{
			Y*=(x0-x[i])/(x[k]-x[i]);
		}
	}
	return Y;
}
/*
*计算拉格朗日多项式
*/
float lagrange(float *x,float *y,float x0,int n)
{
	float Y=0;
	int i;
	for(i=0;i<n;i++)
	{
		Y+=l(x,x0,i,n)*y[i];
	}
	return Y;
}

"""


def eight():
    """线性拟合曲线"""
    """
    #include <stdio.h>
#include <stdlib.h>
int main()
{
    int n;
    printf("请输入x、y个数：");
    scanf("%d",&n);
    double x[n],y[n];
    double a,b;
    double tt=0,ttt=0;
    double m=0,mm=0;
    double zi,mu,zi1;
    int i;
    printf("请依次输入x值：");
    for(i=0;i<n;i++)
    {
        scanf("%lf",&x[i]);
    }
    printf("请依次输入y值：");
    for(i=0;i<n;i++)
    {
        scanf("%lf",&y[i]);
    }
    for(i=0;i<n;i++)
    {
        tt=tt+y[i];//对y求和
        ttt=ttt+x[i]*y[i];//对xy求和
        m=m+x[i]*x[i];//对x^2求和
        mm=mm+x[i];//对x求和
    }
    zi=m*tt-mm*ttt;//a的分子
    mu=n*m-mm*mm;//分母
    a=zi/mu;//a的值
    zi1=n*ttt-tt*mm;//b的分子
    b=zi1/mu;//b的值
    printf("a值为：%lf\n",a);
    printf("b值为：%lf\n",b);
    printf("线性拟合关系为：y=%lfx+%lf",a,b);
    return 0;
}
"""

def nine():
    """复化梯形与复化辛普生"""

    # 被积函数
    def fun(x):
        return x# 输入被积函数

    # 复合梯形
    def tx(a, b, n):
        h = (b - a) / n
        x = a
        s = fun(a) - fun(b)
        for k in range(1, n + 1):
            x = x + h
            s = s + 2 * fun(x)
        result = (h / 2) * s
        return result

    # 复合辛普森
    def xps(a, b, n):
        h = (b - a) / n
        x = a
        s = fun(a) - fun(b)
        for k in range(1, n + 1):
            x = x + h / 2
            s = s + 4 * fun(x)
            x = x + h / 2
            s = s + 2 * fun(x)
        result = (h / 6) * s
        return result

    a = 1# 输入下限
    b = 2# 输入上限
    n = 10# 根据精度改变
    t = tx(a, b, n)
    p = xps(a, b, n)
    print(t, p)


def ten():
    """欧拉预报校正公式："""
    """
    #include <stdio.h>
#include <stdlib.h>
double f(double x,double y);
int main()
{
    double a,b,h;
    int i,n;
    a=1.0;
    b=1.5;
    h=0.1;
    n=(b-a)/h;
    n=n+1;
    //printf("%d",n);
    double x[n+1],y[n+1];
    x[0]=1.0;
    y[0]=1.0;
    printf("x           y\n");
    printf("%lf    %lf\n",x[0],y[0]);
    for(i=0;i<n;i++)
    {
        x[i+1]=x[i]+h;
        y[i+1]=y[i]+h*f(x[i],y[i]);
        y[i+1]=y[i]+0.5*h*(f(x[i],y[i])+f(x[i+1],y[i+1]));

        printf("%lf    %lf\n",x[i+1],y[i+1]);
    }
    return 0;
}
double f(double x,double y)
{
    return(x*x+x*x*x*y);
}
"""


def eleven():
    """四阶龙格一库塔法代码"""
    """
    #include <stdio.h>
#include <stdlib.h>
double f(double x,double y);
int main()
{
    double a,b,h,x;
    int n;
    h=0.1;
    a=0.0;
    b=1.0;
    n=(b-a)/h;
    n=n+1;
    int i;
    double y[n+1];
    x=a;
    y[0]=1.0;
    y[1]=y[0];
    printf("计算结果如下表：\n");
    printf("x           y\n");
    double k1,k2,k3,k4;
    for(i=1;i<n+1;i++)
    {
        k1=h*f(x,y[i]);
        k2=h*f(x+0.5*h,y[i]+0.5*k1);
        k3=h*f(x+0.5*h,y[i]+0.5*k2);
        k4=h*f(x+h,y[i]+k3);
        y[i+1]=y[i]+(k1+2.0*k2+2.0*k3+k4)/6.0;
        x=x+h;
        printf("%lf    %lf\n",x,y[i+1]);

    }
    return 0;
}
double f(double x,double y)
{
    return(-y);
}
"""

def twelve():
    """梯形公式："""
    """
    #include <stdio.h>
#include <stdlib.h>

int main()
{
    float a,h,f,y[100],b[100];
    y[0]=1;
    int i,j;
    a=1;
    h=0.1;
    for(i=1;i<6;i++)
    {
        b[0]=y[i-1]+h*((1+0.1*i)*(1+0.1*i)+(1+0.1*i)*(1+0.1*i)*(1+0.1*i)*y[i-1]);
        for(j=1;j<6;j++)
        {
            y[i]=y[i-1]+0.1/2*(((1+0.1*i)*(1+0.1*i)+(1+0.1*i)*(1+0.1*i)*(1+0.1*i)*y[i-1])+((1+0.1*i)*(1+0.1*i)+(1+0.1*i)*(1+0.1*i)*(1+0.1*i)*b[i-1]));
            b[i]=y[i];
        }
    }
    for(i=0;i<6;i++)
    {
        printf("y(%f)=%f\n",1+i*0.1,y[i]);
    }
    return 0;
}
"""

def final_one():
    # 高斯-勒让德求积公式
    from sympy import *
    from scipy.special import perm, comb  # 排列,组合
    x, t = symbols("x,t")
    # 积分区间
    a = 1
    b = 2
    # 需要求积的目标函数
    import numpy as np
    def f(x):
        f = e ** x * sin(x)
        return f

    n = 2  # n次多项式正交，n越大精度越高(n=0,1,2,...)

    # 勒让德多项式
    def L(n):
        df = diff((x ** 2 - 1) ** (n + 1), x, n + 1)
        # Python内置阶乘函数factorial
        L = 1 / 2 ** (n + 1) / factorial(n + 1) * df
        return L

    # 高斯点x求取
    def Gauss_point(n):
        x_k_list = solve(L(n))  # 求得零点解集
        return x_k_list

    # 求积系数A
    def Quadrature_coefficient(x_k_list):
        A_list = []
        for x_k in x_k_list:
            A = 2 / (1 - x_k ** 2) / (diff(L(n), x, 1).subs(x, x_k)) ** 2
            A_list.append(A)
        return A_list

    result = 0
    x_k_list = Gauss_point(n)
    A_list = Quadrature_coefficient(Gauss_point(n))
    sum = len(A_list)
    # 区间变换
    if a == -1 and b == 1:
        for i in range(sum):
            result += (A_list[i] * f(x_k_list[i])).evalf()
        print(result)
    # 将求求粉公式中的区间(a,b)转换为[-1,1]
    else:
        for i in range(sum):
            X = (b - a) / 2 * x_k_list[i] + (a + b) / 2  # 区间变换
            result += (b - a) / 2 * (A_list[i] * f(X)).evalf()
        print(result)



    