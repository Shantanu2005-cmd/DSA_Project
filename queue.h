// Queue.h

#include <iostream>
#include <vector>
#include <string>

const int MAX_QUEUE_SIZE = 5; 

class MyQueue {
private:
    std::vector<int> data;
    int front; 
    int rear;  
    int count; 

public:
    MyQueue() {
        data.resize(MAX_QUEUE_SIZE);
        front = 0;
        rear = -1;
        count = 0;
    }

    bool is_empty() const {
        return count == 0;
    }

    bool is_full() const {
        return count == MAX_QUEUE_SIZE;
    }

    void enqueue(int value) {
        if (is_full()) {
            std::cerr << "QUEUE OVERFLOW\n";
            return;
        }
        rear = (rear + 1) % MAX_QUEUE_SIZE; 
        data[rear] = value;
        count++;
    }

    void dequeue() {
        if (is_empty()) {
            std::cerr << "QUEUE UNDERFLOW\n";
            return;
        }
        front = (front + 1) % MAX_QUEUE_SIZE; 
        count--;
    }

    // NEW: Returns data as a comma-separated string for the web server
    std::string get_data_string() const {
        std::string result = "";
        if (is_empty()) return "";

        int current_index = front;
        for (int j = 0; j < count; j++) {
            result += std::to_string(data[current_index]);
            if (j < count - 1) {
                result += ","; 
            }
            current_index = (current_index + 1) % MAX_QUEUE_SIZE;
        }
        return result;
    }
    // Inside MyQueue class definition:

int peek() const {
    if (is_empty()) {
        throw std::runtime_error("Queue is empty (Peek failed).");
    }
    return data[front];
}

int size() const {
    return count; // Count tracks the current number of elements
}

int capacity() const {
    return MAX_QUEUE_SIZE; // MAX_QUEUE_SIZE is defined as a constant
}
};