#include <stdio.h>
#include <windows.h>
void gotoxy(short x, short y) {
    COORD pos = {x,y};
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);// 获取标准输出设备句柄
    SetConsoleCursorPosition(hOut, pos);//两个参数分别是指定哪个窗体，具体位置
}
void cprint(char *str) {
    gotoxy(0,0);
    printf("%s\n", str);
}