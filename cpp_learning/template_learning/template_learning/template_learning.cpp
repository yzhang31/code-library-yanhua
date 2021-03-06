// template_learning.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>

template<class T>
class Parent
{
public:
	void foo()
	{
		static_cast<T*>(this)->foo();
	}

	void foo1()
	{
		foo(); ;
	}
};

class ChildA : public Parent< ChildA>
{
public:
	void foo()
	{
		std::cout << "A::foo()" << std::endl;
	}

};

class ChildB : public Parent< ChildB>
{
public:
	void foo()
	{
		std::cout << "B::foo()" << std::endl;
	}

};

int main()
{
	ChildA A;
	ChildB B;
	A.foo1();
	B.foo1();
    return 0;
}

