#include <iostream>
#include <functional>

void save_with_free_function(const std::string& file_name)
{
    std::cout<<"自由函数:"<<file_name<<std::endl;
}

class File_Save
{
    private:
    /*data*/
    public:
    File_Save(/* args */)=default;
    ~File_Save()=default;
    void save_with_member_function(const std::string& file_name)
    {
        std::cout<<"成员函数:"<<file_name<<std::endl;
    }
};

int main()
{
    File_Save file_save;

    //Labda函数

    auto save_with_lambda_fun = [](const std::string& file_name)->void
    {
        std::cout<<"lambda函数:"<<file_name<<std::endl;
    };

    /*
    save_with_free_function("file.txt");
    file_save.save_with_member_function("file.txt");
    save_with_lambda_fun("file.txt");
    */
   
   
    std::function<void(const std::string&)> save_1=save_with_free_function;
   std::function<void(const std::string&)> save_2=save_with_lambda_fun;
   //成员函数，放入包装器
   std::function<void(const std::string&)> save_3=std::bind(&File_Save::save_with_member_function,&file_save,std::placeholders::_1);
   
   //统一的调用方法
   save_1("file.txt");
   save_2("file.txt");
   save_3("file.txt");

   return 0;
}