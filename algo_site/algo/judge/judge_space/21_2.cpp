#include <iostream>

using namespace std;

int main() {
   	long long a,b,p;
    cin >> a >> b >> p;
   	int res = 1;
    while(b) {
        if(b & 1) res = res * a % p;
        a = a * a % p;
        b >>= 1;
    }
    cout << res % p << endl;
    return 0;
}
