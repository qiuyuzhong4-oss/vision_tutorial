# 一,以下皆为散落知识点



# 1,报错名词解析

​	一般报错我现在的看法是直接问AI,	在这个报错里面有什么名词是我需要看的,一般刚开始学都是运行崩溃,在后面写能用的东西的时候崩溃的情况就会少很多,大多是看打印的日志,这个日志是你自己在程序里面写是否打印的,推荐打印在ubuntu系统的终端里面,好像还有log文件可以看,

​	

# 2,语法段或句解析





# 二,C++语法的一些规范文件

# 	(一些变量名或者是文件名命名的时候注意大小写)



## 1,CmakeList

​	cmake_minimum_required(VERSION 3.16)
​	project(opencv_test)

​	set(CMAKE_CXX_STANDARD 11)

​	find_package(OpenCV REQUIRED)

​	add_executable(opencv_test encap_functions.cpp) #readvideo basic_operations encap_functions my_armor

​	target_link_libraries(opencv_test ${OpenCV_LIBS})



## 2.makfile



