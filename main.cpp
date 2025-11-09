// main.cpp - Command Line Interface (CLI) for Web (Expanded)

#include "Stack.h"
#include "Queue.h"
#include <iostream>
#include <string>
#include <sstream>
#include <stdexcept>
#include <limits> // Included for safety

// Static instances to maintain the state during the program's short run
MyStack my_stack;
MyQueue my_queue;

// Helper function to validate input
bool is_valid_int(const std::string& str) {
    if (str.empty()) return false;
    for (char c : str) {
        // Allow optional leading minus sign for negative numbers
        if (c != '-' && !std::isdigit(c)) return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    // If no command, return stack data by default (initialization)
    if (argc < 2) {
        std::cout << my_stack.get_data_string(); 
        return 0;
    }

    std::string command = argv[1];
    int value = 0;

    // --- Process Commands ---
    try {
        if (command == "stack_push") {
            if (argc < 3 || !is_valid_int(argv[2])) throw std::runtime_error("Value required.");
            value = std::stoi(argv[2]);
            my_stack.push(value);
            std::cout << my_stack.get_data_string(); // Output data state
        } 
        else if (command == "stack_pop") {
            my_stack.pop();
            std::cout << my_stack.get_data_string(); // Output data state
        } 
        else if (command == "stack_peek") {
            // Peek should just output the single value
            std::cout << my_stack.peek(); // Assuming peek() returns the element as an int
        }
        else if (command == "stack_size") {
            // Size should just output the single value
            std::cout << my_stack.size(); // Assuming size() returns the count as an int
        }
        else if (command == "stack_capacity") {
            // Capacity should just output the single value
            std::cout << my_stack.capacity(); // Assuming capacity() returns the max size as an int
        }
        else if (command == "stack_display") {
            std::cout << my_stack.get_data_string(); // Output data state
        }
        
        // --- Queue Operations ---
        
        else if (command == "queue_enqueue") {
            if (argc < 3 || !is_valid_int(argv[2])) throw std::runtime_error("Value required.");
            value = std::stoi(argv[2]);
            my_queue.enqueue(value);
            std::cout << my_queue.get_data_string(); // Output data state
        } 
        else if (command == "queue_dequeue") {
            my_queue.dequeue();
            std::cout << my_queue.get_data_string(); // Output data state
        } 
        else if (command == "queue_peek") {
            // Peek should just output the single value
            std::cout << my_queue.peek(); // Assuming peek() returns the element as an int
        }
        else if (command == "queue_size") {
            // Size should just output the single value
            std::cout << my_queue.size(); // Assuming size() returns the count as an int
        }
        else if (command == "queue_capacity") {
            // Capacity should just output the single value
            std::cout << my_queue.capacity(); // Assuming capacity() returns the max size as an int
        }
        else if (command == "queue_display") {
            std::cout << my_queue.get_data_string(); // Output data state
        } 
        else {
            std::cerr << "UNKNOWN_COMMAND\n";
            return 1;
        }

    } catch (const std::exception& e) {
        // Catch general errors (like underflow/overflow logic defined in headers)
        std::cerr << "ERROR: " << e.what() << "\n";
        return 1; 
    }

    return 0;
}