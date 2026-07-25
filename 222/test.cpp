#include "iostream"
int main(int argc,char** argv)
{
    std::cout<<"参数数量="<<argc<<std::endl;
    std::cout<<"程序名字="<<argv[0]<<std::endl;
    std::string arg1= argv[1];
    if (arg1=="--help")
    {
        std::cout<<"这是help"<<std::endl;
    }
    
    return 0;
}