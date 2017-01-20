// sort.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "vector"
#include "iostream"
#include "algorithm"

using namespace std;


void output_array(vector<int>& array)
{
	for (auto val : array)
	{
		std::cout << val << ",";
	}
	std::cout << endl;
}


void bubble_sort(vector<int>& unsorted_array)
{
	std::cout << "bubble_sort" << endl;

	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		for (auto j = unsorted_array.end() - 1; j != i; j--)
		{
			if (*(j - 1) > *j)
			{
				swap(*(j - 1), *j);
			}
			compare_count++;
		}
		output_array(unsorted_array);
	}
	std::cout << "Total Compare Count:" << compare_count << endl;
}



void bubble_sort2(vector<int>& unsorted_array)
{
	std::cout << "bubble_sort2" << endl;
	int compare_count = 0;

	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		int flag = 0;
		for (auto j = unsorted_array.end() - 1; j != i; j--)
		{
			if (*(j - 1) > *j)
			{
				swap(*(j - 1), *j);
				flag = 1;
			}
			compare_count++;
		}
		output_array(unsorted_array);
		if (!flag)
		{
			break;
		}
	}
	std::cout << "Total Compare Count:" << compare_count << endl;
}


//def bubble_sort(ary) :
//	n = len(ary)                   #获得数组的长度
//	for i in range(n) :
//		for j in range(1, n - i) :
//			if  ary[j - 1] > ary[j] :       #如果前者比后者大
//				ary[j - 1], ary[j] = ary[j], ary[j - 1]       #则交换两者
//				return ary
//
void bubble_sort_wuchong(vector<int>& unsorted_array)
{
	std::cout << "bubble_sort_wuchong" << endl;

	int compare_count = 0;
	for (size_t i = 0; i < unsorted_array.size(); i++)
	{
		for (size_t j = 1; j < unsorted_array.size() - i; j++)
		{
			if (unsorted_array[j-1] > unsorted_array[j])
			{
				swap(unsorted_array[j - 1], unsorted_array[j]);
			}
			compare_count++;
		}
		output_array(unsorted_array);

	}


	std::cout << "Total Compare Count:" << compare_count << endl;
}

void bubble_sort_wrong(vector<int>& unsorted_array)
{
	std::cout << "bubble_sort_wrong" << endl;

	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		for (auto j = i + 1; j != unsorted_array.end(); j++)
		{
			if (*j < *i)
			{
				swap(*j, *i);
			}
			compare_count++;
		}
		output_array(unsorted_array);
	}
	std::cout << "Total Compare Count:" << compare_count << endl;
}

void bubble_sort2_wrong(vector<int>& unsorted_array)
{
	std::cout << "bubble_sort2_wrong" << endl;
	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		int flag = 0;
		for (auto j = i + 1; j != unsorted_array.end(); j++)
		{
			if (*j < *i)  // should compare j and j-1;
			{
				swap(*j, *i);
				flag = 1;
			}
			compare_count++;
		}
		output_array(unsorted_array);
		if (!flag)
		{
			break;
		}

	}
	std::cout << "Total Compare Count:" << compare_count << endl;

}


void select_sort(vector<int>& arr)
{
	for (size_t i = 0; i < arr.size(); i++)
	{
		int min_pos = -1;
		int min_val = std::numeric_limits<int>::max();
		for (size_t j = i; j < arr.size(); j++)
		{
			if (arr[j] < min_val)
			{
				min_val = arr[j];
				min_pos = j;
			}
		}
		int temp = arr[i];
		arr[i] = arr[min_pos];
		arr[min_pos] = temp;
	}

}

void select_sort2(vector<int>& arr)
{
	for (size_t i = 0; i < arr.size(); i++)
	{
		int min_pos = i;
		for (size_t j = i + 1; j < arr.size(); j++)
		{
			if (arr[j] < arr[min_pos])
				min_pos = j;
		}
		swap(arr[i], arr[min_pos]);
	}
}


//void insert_sort(vector<int>& arr)
//{
//	for (int i = 0; i < arr.size() - 1; i++)
//	{
//			int candidate = arr[i + 1];
//			int j = i;  // start from tail pos.
//			for (; j >= 0; j--)  
//			{
//				if (candidate < arr[j])
//					arr[j + 1] = arr[j];
//				else
//					break;
//			}
//			arr[j + 1 ] = candidate;
//	}
//}

void insert_sort(vector<int>& arr)
{
	for (int i = 0; i < arr.size() - 1; i++)
	{
		int candidate = arr[i + 1];
		int j = i;  // start from tail pos.
		for (; j >= 0; j--)
		{
			if (candidate < arr[j])
				arr[j + 1] = arr[j];
			else
				break;
		}
		arr[j + 1] = candidate;
	}
}

void insert_sort2(vector<int>& arr)
{
	for (int i = 1; i < arr.size(); i++)
	{
		int candidate = arr[i];
		int j = i - 1;  
		for (; j >= 0 && candidate < arr[j]; j--)
		{
			arr[j + 1] = arr[j];
		}
		arr[j + 1] = candidate;
	}
}


void split(vector<int>& arr, vector<int>& left, vector<int>& right)
{
	int mid = arr.size() / 2; 
	for (size_t i = 0; i < arr.size(); i++)
	{
		if (i < mid)
			left.push_back(arr[i]);
		else
			right.push_back(arr[i]);
	}
}

vector<int> merge(vector<int>& arr1, vector<int>& arr2)
{
	vector<int> result;
	result.resize(arr1.size() + arr2.size());
	int i = 0, j = 0;

	for (size_t index = 0; index < arr1.size() + arr2.size(); index++)
	{
		if (i > arr1.size() - 1 )
		{
			result[index] = arr2[j];
			j++;
		}
		else if (j > arr2.size() - 1)
		{
			result[index] = arr1[i];
			i++;

		}
		else if (arr1[i] < arr2[j])
		{
			result[index] = arr1[i];
			i++;
		}
		else
		{
			result[index] = arr2[j];
			j++;
		}
	}
	return result;
}


vector<int> merge_sort(vector<int>& arr)
{
	if (arr.size() <= 1)
	{
		return arr;
	}

	vector<int> left, right;

	split(arr, left, right);
	
	left = merge_sort(left);

	right = merge_sort(right);

	vector<int> result = merge(left, right);
	
	return result;
}



int main()
{
	//vector<int> unsorted_array = {2,1,3,4,5,6,0,7,8};
	vector<int> one_val_array = {5 };
	vector<int> two_val_array = { 5 , 4};
	vector<int> three_val_array = { 5, 4, 3 };
	vector<int> unsorted_array = { 0, 7,8,5,2,1,3,4,6 }; // wrong bubble_sort2_wrong cannot handle.
	//vector<int> unsorted_array = { 7, 1,8,5,2,0,3,4,6 }; // wrong bubble_sort2_wrong cannot handle.

	std::cout << "original" << endl;
	output_array(unsorted_array);
	std::cout << endl;


	//vector<int> v1(unsorted_array);
	//vector<int> v2(unsorted_array);


	//bubble_sort(vector<int>(unsorted_array));
	//bubble_sort_wuchong(vector<int>(unsorted_array));

	//bubble_sort2(vector<int>(unsorted_array));
	//bubble_sort_wrong(vector<int>(unsorted_array));
	//bubble_sort2_wrong(vector<int>(unsorted_array));

	//select_sort2(unsorted_array);
	//insert_sort2(unsorted_array);

	auto result = merge_sort(unsorted_array);

	std::cout << "sorted" << endl;
	output_array(result);
    return 0;
}

