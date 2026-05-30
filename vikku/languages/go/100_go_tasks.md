# 100 Go Tasks - From Java/Spring Boot to Go Mastery

## Days 1-2: Core Fundamentals (Tasks 1-30)

### Basic Syntax & Types (1-10)
1. Write a "Hello, World!" program and run it
2. Declare variables using var, := and const for different types (int, string, bool, float64)
3. Create a program that converts Celsius to Fahrenheit
4. Write a function that takes two integers and returns their sum and difference (multiple returns)
5. Create an array of 5 integers and print each element using a for loop
6. Convert the array to a slice and append 3 more elements
7. Create a map[string]int to store student grades and add/retrieve/delete entries
8. Write a program using if-else to check if a number is positive, negative, or zero
9. Create a switch statement that prints the day name from a number (1-7)
10. Write a for loop that prints numbers 1-100, but print "Fizz" for multiples of 3, "Buzz" for 5, "FizzBuzz" for both

### Functions & Error Handling (11-20)
11. Write a function that divides two numbers and returns an error if divisor is zero
12. Create a function with variadic parameters that sums any number of integers
13. Write a function that returns a closure (function that increments a counter)
14. Create a recursive function to calculate factorial
15. Write a function that takes a slice and returns a new slice with duplicates removed
16. Implement a function that checks if a string is a palindrome
17. Create a defer example that demonstrates cleanup (open/close file simulation with prints)
18. Write a program demonstrating panic and recover
19. Create a custom error type with additional context fields
20. Write a function that validates email format and returns a descriptive error

### Pointers (21-25)
21. Write a function that swaps two integers using pointers
22. Create a struct and write a method that modifies its field using a pointer receiver
23. Demonstrate the difference between pointer and value receivers
24. Write a function that takes a pointer to a slice and appends elements
25. Create a program showing nil pointer checking

### Structs & Methods (26-30)
26. Define a Person struct with name, age, and email fields
27. Create a method on Person that returns a formatted greeting string
28. Write a constructor function NewPerson() that validates inputs
29. Create an Address struct and embed it in Person (composition)
30. Implement a String() method on Person (implements fmt.Stringer interface)

## Days 3-4: Go's Unique Features (Tasks 31-55)

### Interfaces (31-40)
31. Define a Shape interface with Area() method
32. Create Circle and Rectangle structs that implement Shape
33. Write a function that accepts Shape interface and prints the area
34. Implement the io.Reader interface for a custom type
35. Create an empty interface example that handles different types using type assertions
36. Use type switch to handle multiple types
37. Define an interface with multiple methods (e.g., ReadWriter)
38. Create a program demonstrating interface composition
39. Implement error interface with a custom error type
40. Write a program using interface{} to create a simple generic print function

### Goroutines & Channels (41-50)
41. Launch 5 goroutines that each print a number
42. Create a goroutine that calculates sum and sends result through a channel
43. Write a program with multiple goroutines sending to one channel
44. Implement a worker pool pattern with 3 workers processing 10 jobs
45. Create a program using buffered channels
46. Write a program that demonstrates channel closing and range over channels
47. Implement a timeout using select and time.After
48. Create a program with two channels and select to receive from whichever is ready
49. Write a goroutine that pings every second until told to stop (using quit channel)
50. Implement a simple producer-consumer pattern with channels

### Packages & Modules (51-55)
51. Create a custom package with exported and unexported functions
52. Initialize a Go module with go mod init
53. Import and use a third-party package (e.g., github.com/google/uuid)
54. Create multiple packages in your project and import between them
55. Write a package with init() function demonstrating initialization order

## Days 5-6: Web Services & Practical Go (Tasks 56-85)

### HTTP Basics (56-65)
56. Create a basic HTTP server that responds "Hello, World!" on port 8080
57. Add multiple route handlers for different paths
58. Write a handler that responds with JSON
59. Create a handler that parses URL query parameters
60. Implement a POST handler that reads JSON from request body
61. Add middleware that logs each request (path, method, timestamp)
62. Create middleware that adds CORS headers
63. Write a handler that serves static files
64. Implement basic authentication middleware
65. Create a handler with path parameters (using gorilla/mux or chi)

### JSON & Data Handling (66-72)
66. Define a struct and marshal it to JSON
67. Unmarshal JSON string into a struct
68. Handle JSON with custom field names using struct tags
69. Work with nested JSON structures
70. Parse JSON from an HTTP request and validate fields
71. Create a handler that returns different status codes based on input
72. Implement custom JSON marshaling for a type (MarshalJSON method)

### REST API Building (73-80)
73. Create a User struct with CRUD operations (in-memory slice for storage)
74. Implement GET /users endpoint (list all users)
75. Implement GET /users/{id} endpoint (get single user)
76. Implement POST /users endpoint (create user)
77. Implement PUT /users/{id} endpoint (update user)
78. Implement DELETE /users/{id} endpoint
79. Add input validation for user creation
80. Add error handling that returns proper JSON error responses

### Working with Files & I/O (81-85)
81. Write a program that reads a text file line by line
82. Create a program that writes data to a file
83. Implement a CSV reader that parses a file into structs
84. Write a program that copies a file
85. Create a program that walks a directory tree and lists all .go files

## Day 7: Integration & Advanced Patterns (Tasks 86-100)

### Database Integration (86-92)
86. Connect to SQLite database using database/sql
87. Create a table and insert records
88. Query records and scan into structs
89. Implement prepared statements for queries
90. Handle database transactions
91. Create a simple repository pattern for database operations
92. Add basic error handling for database operations

### Testing (93-97)
93. Write a unit test for a simple function using testing package
94. Create table-driven tests for multiple input scenarios
95. Write a test with setup and teardown (using defer)
96. Mock an interface for testing
97. Write a benchmark test for a function

### Final Mini-Project Tasks (98-100)
98. Build a TODO API with in-memory storage (GET, POST, PUT, DELETE)
99. Add persistence to the TODO API using JSON file storage
100. Create a simple CLI tool that makes HTTP requests to your API

---

## How to Use This List

**Progressive Learning**: Tasks build on each other, start from #1
**Hands-on**: Actually code each one, don't just read
**Experimentation**: Modify each task, break things, see what happens
**Time estimate**: ~30-45 min per task = ~50-75 hours total (matches your week timeline with 7-10 hours/day)

## Tips for Java/Spring Boot Developers

- **Task 26-30**: Structs are like POJOs, but simpler
- **Task 31-40**: Interfaces are implicit (no "implements" keyword)
- **Task 41-50**: This is where Go shines vs Java threads
- **Task 56-65**: Notice how much you can do without a framework like Spring
- **Task 73-80**: Your Spring Boot REST controller knowledge translates directly
- **Task 86-92**: Compare to Spring Data JPA - more explicit, less magic

## Validation Checklist Per Task
- [ ] Code compiles without errors
- [ ] Code runs and produces expected output
- [ ] You understand why it works
- [ ] You can explain it to someone else

Good luck! Remember: Go values simplicity and explicitness. Don't look for the "Spring way" - embrace the "Go way" of doing things simply and directly.
