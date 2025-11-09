// main.cpp

#include "Stack.h"
#include "Queue.h"
#include <iostream>
#include <string>
#include <stdexcept>
#include <algorithm> // For std::transform (optional cleanup)

MyStack my_stack;
MyQueue my_queue;

bool is_valid_int(const std::string& str) {
    if (str.empty()) return false;
    for (char c : str) {
        if (c != '-' && !std::isdigit(c)) return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 2) { 
        std::cout << my_stack.get_data_string(); 
        return 0;
    }

    std::string command = argv[1];
    int value = 0;

    try {
        if (command == "stack_push") {
            if (argc < 3 || !is_valid_int(argv[2])) throw std::runtime_error("Value required.");
            value = std::stoi(argv[2]);
            my_stack.push(value);
            std::cout << my_stack.get_data_string();
        } else if (command == "stack_pop") {
            my_stack.pop();
            std::cout << my_stack.get_data_string();
        } else if (command == "stack_peek") {
            std::cout << my_stack.peek();
        } else if (command == "stack_size") {
            std::cout << my_stack.size();
        } else if (command == "stack_capacity") {
            std::cout << my_stack.capacity();
        } else if (command == "stack_display") {
            std::cout << my_stack.get_data_string();
        }
        
        else if (command == "queue_enqueue") {
            if (argc < 3 || !is_valid_int(argv[2])) throw std::runtime_error("Value required.");
            value = std::stoi(argv[2]);
            my_queue.enqueue(value);
            std::cout << my_queue.get_data_string();
        } else if (command == "queue_dequeue") {
            my_queue.dequeue();
            std::cout << my_queue.get_data_string();
        } else if (command == "queue_peek") {
            std::cout << my_queue.peek();
        } else if (command == "queue_size") {
            std::cout << my_queue.size();
        } else if (command == "queue_capacity") {
            std::cout << my_queue.capacity();
        } else if (command == "queue_display") {
            std::cout << my_queue.get_data_string();
        } 
        else {
            std::cerr << "UNKNOWN_COMMAND\n";
            return 1;
        }

    } catch (const std::exception& e) {
        std::cerr << e.what(); // Print error message for Python to catch
        return 1; 
    }

    return 0;
}