// list_study.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <array>


typedef struct Node
{
	int Value;
	Node* Next;
}Node;


Node* Revert(Node* node)
{
	if (node->Next == NULL)
	{
		return node;
	}
	else
	{
		Node* newHead = Revert(node->Next);

		node->Next->Next = node;
		node->Next = NULL;
		return newHead;
	}
}


void Revert_NoHeadNode(Node* node)
{
	if (node->Next != NULL)
	{
		Revert_NoHeadNode(node->Next);
		node->Next->Next = node;
		node->Next = NULL;
	}
}

int main()
{
	std::array<Node, 4> node_aray;

	for (size_t i = 0; i < 3; i++)
	{
		node_aray[i].Value = i;
		node_aray[i].Next = &node_aray[i + 1];
	}

	node_aray[3].Value = 3;
	node_aray[3].Next = NULL;

	Revert_NoHeadNode(&node_aray[0]);

    return 0;
}

