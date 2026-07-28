#include <QApplication>
#include <QLabel>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QLabel* label =new QLabel();
    QString message =QString::fromStdString("Hello, Qt!");
    label->setText(message);
    label->show();

    app.exec();//执行应用,阻塞代码


    return 0;
}