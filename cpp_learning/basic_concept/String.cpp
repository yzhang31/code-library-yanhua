#include <stdio.h>
#include <string.h> // include.

class String
{
public:
	String(const char *value);  // const input parameter.
	String(const String& rhs);  // const input parameter.
	String& operator=(String& rhs); // Must define return paramter as reference. otherwise block a = b= c, linked assignment.
	~String(); // If don't act as base class, don't need define as virtual.

private:
	char *data;
};

String::String(const char *value)
{
	printf("Constuct const called.\n");
	if (value)
	{
		data = new char[strlen(value) + 1];
		strcpy_s(data, strlen(value) + 1, value);
	}
	else
	{
		data = new char[1];
		data[0] = '\0';
	}
}


String::String(const String& rhs)
{
	printf("Copy Constuct called.\n");
	if (rhs.data)
	{
		// delete[] data;  Do't delete here, copy construct dont' need.
		data = new char[strlen(rhs.data) + 1];
		strcpy_s(data, strlen(rhs.data) + 1, rhs.data);
	}
	else
	{
		data = new char[1];
		data[0] = '\0';
	}
}

String& String::operator=(String& rhs)
{
	printf("operator= called.\n");

	if (this == &rhs)    //Need check !!
	{
		return *this;
	}

	if (rhs.data)
	{
		delete[] data;  // Delete old memory.
		data = new char[strlen(rhs.data) + 1];
		strcpy_s(data, strlen(rhs.data) + 1, rhs.data);
	}
	else
	{
		data = new char[1];
		data[0] = '\0';
	}
	return *this;
}

String::~String()
{
	delete[] data;  // Don't forget '[]'
}

void doNothing(String localString)
{

}

void main()
{
	String a("Hello");
	{
		String b("World");
		b = a;   // Trigger op=;
	}

	String c = a; // Trigger copy construct.

	String s = "The Truth is Out There"; // Trigger constuct.

	doNothing(s); // Pass by value, trigger copy construct.


	s = s;   // if op= no self pointer check, will crash.

	a = s = c; // If op= define return (String * or void), this line cannot pass build.

}
