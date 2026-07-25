#include <iostream>
#include <memory>

int main()
{
    auto p1 = std::make_shared<std::string>("this is a str");//std::make_shared<数据类型/对象类型>(参数)；返回值，对应类的共享指针   std::make_shared<std::string> 写为auto
    std::cout << "p1的引用计数:" << p1.use_count() << ",指向的内存地址:" << p1.get() << std::endl;//1
    
    auto p2 = p1; //p2和p1指向同一块内存
    std::cout << "p1的引用计数:" << p1.use_count() << ",指向的内存地址:" << p1.get() << std::endl;//2
    std::cout << "p2的引用计数:" << p2.use_count() << ",指向的内存地址:" << p2.get() << std::endl;//2

    p1.reset(); //释放p1指向的内存，引用计数减1,不指向"this is a str"所在内存
    std::cout << "p1的引用计数:" << p1.use_count() << ",指向的内存地址:" << p1.get() << std::endl;//0
    std::cout << "p2的引用计数:" << p2.use_count() << ",指向的内存地址:" << p2.get() << std::endl;//2-1=1

    std::cout << "p2指向的内存数据:" << p2->c_str() << std::endl;//调用成员方法c_str()，返回指向字符串的指针
    return 0;
}