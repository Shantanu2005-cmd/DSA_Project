// Queue.h
#include <vector>
#include <string>
#include <stdexcept>

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
        front = 0; rear = -1; count = 0;
    }
    bool is_empty() const { return count == 0; }
    bool is_full() const { return count == MAX_QUEUE_SIZE; }

    void enqueue(int value) {
        if (is_full()) { throw std::runtime_error("QUEUE OVERFLOW"); }
        rear = (rear + 1) % MAX_QUEUE_SIZE; 
        data[rear] = value;
        count++;
    }

    void dequeue() {
        if (is_empty()) { throw std::runtime_error("QUEUE UNDERFLOW"); }
        front = (front + 1) % MAX_QUEUE_SIZE; 
        count--;
    }

    int peek() const {
        if (is_empty()) { throw std::runtime_error("Queue is empty (Peek failed)"); }
        return data[front];
    }

    int size() const { return count; }
    int capacity() const { return MAX_QUEUE_SIZE; }

    std::string get_data_string() const {
        std::string result = "";
        if (is_empty()) return "";

        int current_index = front;
        for (int j = 0; j < count; j++) {
            result += std::to_string(data[current_index]);
            if (j < count - 1) { result += ","; }
            current_index = (current_index + 1) % MAX_QUEUE_SIZE;
        }
        return result;
    }
};