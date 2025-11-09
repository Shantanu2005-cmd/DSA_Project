// Stack.h

#include <iostream>
#include <vector>
#include <string> // Required for std::string

const int MAX_SIZE = 5; 

class MyStack {
private:
    std::vector<int> data;
    int top;

public:
    MyStack() {
        data.resize(MAX_SIZE);
        top = -1; 
    }

    bool is_empty() const {
        return top == -1;
    }

    bool is_full() const {
        return top == MAX_SIZE - 1;
    }

    void push(int value) {
        if (is_full()) {
            // Error handling will be caught by Python in the updated main
            std::cerr << "STACK OVERFLOW\n";
            return;
        }
        top++;
        data[top] = value;
    }

    void pop() {
        if (is_empty()) {
            std::cerr << "STACK UNDERFLOW\n";
            return;
        }
        top--;
    }

    // NEW: Returns data as a comma-separated string for the web server
    std::string get_data_string() const {
        std::string result = "";
        for (int i = 0; i <= top; i++) {
            result += std::to_string(data[i]);
            if (i < top) {
                result += ","; // Use ',' as a delimiter
            }
        }
        return result;
    }
    // Inside MyStack class definition:

int peek() const {
    if (is_empty()) {
        throw std::runtime_error("Stack is empty (Peek failed).");
    }
    return data[top];
}

int size() const {
    return top + 1; // Size is the number of elements (top index + 1)
}

int capacity() const {
    return MAX_SIZE; // MAX_SIZE is defined as a constant
}
};