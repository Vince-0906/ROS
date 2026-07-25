#include <iostream>
#include <algorithm>

int main()
{
    auto add =[](int a,int b)->int{return a+b;}; //lambda表达式，返回值类型为int
    int sum = add(200,50);
    auto print_sum =[sum]()->void
    {
        std::cout << "sum=" << sum << std::endl;
    };
    
    print_sum();
    return 0;
}
