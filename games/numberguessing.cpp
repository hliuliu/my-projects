#include<iostream>
using namespace std;
#define MAX 20

int* toBinArray(int value) {
	int bin[MAX];
	int*b;
	for(b=bin;b<bin+MAX;b++) {
		*b=value%2;
		value/=2;
	}
	b=bin;
	return b;
}

int main() {
	char a;
	cout<<"Welcome, think of any integer between 0 and 127!"<<endl;
	cout<<"Press any character and hit enter to begin."<<endl;
	cin>>a;
	int *numbers;
	int pow=1,count=0,exp=0;
	while(pow<128) {
		cout<<"Is you number is this list?(y/n)"<<endl;
		int j=0;
		for(int i=0;i<129;i++) {
			numbers=toBinArray(i);
			if(*(numbers+exp)) {
				if(j%5==0) cout<<"\n";
				cout<<i<<" ";
				j++;
			}
		}
		cout<<"\n";
		cin>>a;
		if(a=='y') count+=pow;
		pow*=2;
		exp++;
	}
	cout<<"Your number is "<<count<<endl;
	cout<<"Press any character and hit enter to exit."<<endl;
	cin>>a;
	return 0;
}