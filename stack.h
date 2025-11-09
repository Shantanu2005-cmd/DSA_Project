// Stack.h
#include <vector>
#include <string>
#include <stdexcept>

const int MAX_SIZE = 5; 

class MyStack {
private:
    std::vector<int> data;
    int top;

public:
    MyStack() { data.resize(MAX_SIZE); top = -1; }
    bool is_empty() const { return top == -1; }
    bool is_full() const { return top == MAX_SIZE - 1; }

    void push(int value) {
        if (is_full()) { throw std::runtime_error("STACK OVERFLOW"); }
        top++; data[top] = value;
    }

    void pop() {
        if (is_empty()) { throw std::runtime_error("STACK UNDERFLOW"); }
        top--;
    }

    int peek() const {
        if (is_empty()) { throw std::runtime_error("Stack is empty (Peek failed)"); }
        return data[top];
    }

    int size() const { return top + 1; }
    int capacity() const { return MAX_SIZE; }

    std::string get_data_string() const {
        std::string result = "";
        for (int i = 0; i <= top; i++) {
            result += std::to_string(data[i]);
            if (i < top) { result += ","; }
        }
        return result;
    }
};