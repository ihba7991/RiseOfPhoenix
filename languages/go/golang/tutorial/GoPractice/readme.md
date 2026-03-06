# Go Programming Tutorial: Basic Commands and Structures

A comprehensive guide to learning Go fundamentals, including basic commands, syntax, and essential data structures.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Syntax](#basic-syntax)
3. [Data Types](#data-types)
4. [Functions](#functions)
5. [Control Structures](#control-structures)
6. [Data Structures](#data-structures)
7. [Packages and Imports](#packages-and-imports)
8. [Common Commands](#common-commands)
9. [Error Handling](#error-handling)
10. [Concurrency Basics](#concurrency-basics)

---

## Getting Started

### Installation

```bash
# macOS (using Homebrew)
brew install go

# Verify installation
go version
```

### Create Your First Go Program

```bash
# Create a new directory
mkdir my-go-project
cd my-go-project

# Initialize a Go module
go mod init example.com/my-go-project

# Create main.go file
cat > main.go << 'EOF'
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
EOF

# Run the program
go run main.go
```

---

## Basic Syntax

### Package Declaration

Every Go file starts with a package declaration:

```go
package main  // Executable packages must be named 'main'
package utils  // Library packages have custom names
```

### Imports

```go
// Single import
import "fmt"

// Multiple imports
import (
    "fmt"
    "math"
    "strings"
)
```

### Variable Declaration

```go
// Explicit type declaration
var name string = "Alice"
var age int = 30

// Short declaration (inside functions only)
name := "Bob"
count := 42

// Multiple declarations
var (
    name   string = "Charlie"
    age    int    = 25
    active bool   = true
)

// Blank identifier (discard value)
_, err := someFunction()
```

### Constants

```go
// Constant declaration
const Pi = 3.14159
const AppVersion = "1.0.0"

// Multiple constants
const (
    Sunday    = 0
    Monday    = 1
    Tuesday   = 2
)

// Constant expressions
const (
    Kilobyte = 1024
    Megabyte = Kilobyte * 1024
)
```

---

## Data Types

### Basic Types

```go
// Boolean
var active bool = true

// Integers (signed)
var small int8 = 127        // -128 to 127
var medium int16 = 32767    // -32768 to 32767
var large int32 = 2147483647
var huge int64 = 9223372036854775807
var general int = 42        // Platform-dependent (32 or 64 bit)

// Integers (unsigned)
var count uint = 100
var byte_val byte = 255     // 0 to 255
var rune_val rune = 'A'     // Unicode character

// Floating Point
var pi float32 = 3.14
var euler float64 = 2.71828

// Strings
var message string = "Hello, Go!"
```

### Type Conversion

```go
var intVal int = 42
var floatVal float64 = float64(intVal)

var str string = "123"
intVal, err := strconv.Atoi(str)

var numStr string = strconv.Itoa(intVal)
```

### Zero Values

```go
var i int        // 0
var f float64    // 0.0
var s string     // ""
var b bool       // false
var p *int       // <nil>
```

---

## Functions

### Basic Function

```go
func add(x int, y int) int {
    return x + y
}

// Shorthand for same-type parameters
func add(x, y int) int {
    return x + y
}
```

### Multiple Return Values

```go
func divide(dividend, divisor float64) (float64, error) {
    if divisor == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return dividend / divisor, nil
}

// Usage
result, err := divide(10, 2)
if err != nil {
    fmt.Println("Error:", err)
} else {
    fmt.Println("Result:", result)
}
```

### Named Return Values

```go
func swap(x, y string) (first, second string) {
    first = y
    second = x
    return  // Implicit return
}
```

### Variadic Functions

```go
func sum(numbers ...int) int {
    total := 0
    for _, num := range numbers {
        total += num
    }
    return total
}

// Usage
result := sum(1, 2, 3, 4, 5)  // 15
```

### Function Types and Callbacks

```go
// Function type
type Operation func(int, int) int

// Using function type
func apply(a, b int, op Operation) int {
    return op(a, b)
}

// Usage
multiply := func(x, y int) int { return x * y }
result := apply(5, 3, multiply)  // 15
```

---

## Control Structures

### If / Else

```go
// Basic if-else
if age >= 18 {
    fmt.Println("Adult")
} else {
    fmt.Println("Minor")
}

// If with initialization
if count := getCount(); count > 0 {
    fmt.Println("Count is positive:", count)
}

// Else-if chain
if score >= 90 {
    fmt.Println("A")
} else if score >= 80 {
    fmt.Println("B")
} else if score >= 70 {
    fmt.Println("C")
} else {
    fmt.Println("F")
}
```

### Switch Statement

```go
// Basic switch
switch day {
case "Monday":
    fmt.Println("Start of week")
case "Friday":
    fmt.Println("End of week")
case "Saturday", "Sunday":
    fmt.Println("Weekend")
default:
    fmt.Println("Midweek")
}

// Switch with expressions
switch {
case age < 13:
    fmt.Println("Child")
case age < 18:
    fmt.Println("Teen")
case age < 65:
    fmt.Println("Adult")
default:
    fmt.Println("Senior")
}

// Switch with type assertion
var x interface{} = 42
switch v := x.(type) {
case int:
    fmt.Println("Integer:", v)
case string:
    fmt.Println("String:", v)
default:
    fmt.Println("Unknown type")
}
```

### For Loop

```go
// Basic for loop
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// While-style loop
count := 0
for count < 5 {
    fmt.Println(count)
    count++
}

// Infinite loop
for {
    fmt.Println("Infinite")
    break  // Break out of the loop
}

// For-range loop
numbers := []int{1, 2, 3, 4, 5}
for i, num := range numbers {
    fmt.Printf("Index: %d, Value: %d\n", i, num)
}

// Range with strings (iterates over runes)
str := "Hello"
for i, ch := range str {
    fmt.Printf("Index: %d, Char: %c\n", i, ch)
}

// Iterate over map
scores := map[string]int{"Alice": 90, "Bob": 85}
for name, score := range scores {
    fmt.Printf("%s: %d\n", name, score)
}
```

### Break and Continue

```go
// Break
for i := 0; i < 10; i++ {
    if i == 5 {
        break  // Exit loop
    }
    fmt.Println(i)
}

// Continue
for i := 0; i < 5; i++ {
    if i == 2 {
        continue  // Skip to next iteration
    }
    fmt.Println(i)
}
```

---

## Data Structures

### Arrays

```go
// Array declaration
var arr [5]int                    // Array of 5 integers
var names [3]string = [3]string{"Alice", "Bob", "Charlie"}

// Array initialization
arr := [...]int{1, 2, 3, 4, 5}   // Length inferred
arr := [5]int{10, 20, 30}        // Rest are zero-valued

// Accessing elements
fmt.Println(arr[0])              // First element
arr[1] = 20                       // Modify element

// Array length
length := len(arr)

// Iterating arrays
for i, val := range arr {
    fmt.Printf("Index: %d, Value: %d\n", i, val)
}
```

### Slices

```go
// Slice declaration
var slice []int                           // Empty slice
slice := []int{1, 2, 3, 4, 5}             // Slice literal
slice := make([]int, 5)                   // Slice with length 5
slice := make([]int, 5, 10)               // Length 5, capacity 10

// Slice operations
slice = append(slice, 6, 7)               // Add elements
subSlice := slice[1:3]                    // Slice from index 1 to 2
subSlice := slice[:3]                     // From start to index 2
subSlice := slice[2:]                     // From index 2 to end

// Slice properties
len := len(slice)                         // Length of slice
cap := cap(slice)                         // Capacity of slice

// Copy slice
copySlice := make([]int, len(slice))
copy(copySlice, slice)

// Iterating slice
for i, val := range slice {
    fmt.Printf("Index: %d, Value: %d\n", i, val)
}
```

### Maps

```go
// Map declaration
var scores map[string]int                              // Nil map
scores := make(map[string]int)                         // Empty map
scores := map[string]int{"Alice": 90, "Bob": 85}       // Map literal

// Adding/updating elements
scores["Charlie"] = 95
scores["Alice"] = 92

// Accessing elements
score := scores["Bob"]                    // Returns 85
score, exists := scores["Unknown"]        // Returns 0, false

// Checking if key exists
if val, ok := scores["Alice"]; ok {
    fmt.Println("Alice's score:", val)
}

// Deleting elements
delete(scores, "Bob")

// Map length
length := len(scores)

// Iterating map
for name, score := range scores {
    fmt.Printf("%s: %d\n", name, score)
}

// Iterating only keys or values
for name := range scores {
    fmt.Println(name)
}

for _, score := range scores {
    fmt.Println(score)
}
```

### Structs

```go
// Struct definition
type Person struct {
    Name string
    Age  int
    City string
}

// Struct initialization
person := Person{Name: "Alice", Age: 30, City: "NYC"}
person := Person{"Bob", 25, "LA"}         // Positional
person := new(Person)                     // Pointer to new struct

// Accessing fields
fmt.Println(person.Name)
person.Age = 31

// Anonymous struct
config := struct {
    Host string
    Port int
}{
    Host: "localhost",
    Port: 8080,
}

// Struct embedding (composition)
type Employee struct {
    Person
    EmployeeID string
    Department string
}

emp := Employee{
    Person: Person{Name: "Charlie", Age: 35, City: "Boston"},
    EmployeeID: "E123",
    Department: "Engineering",
}

// Access embedded fields
fmt.Println(emp.Name)        // Alice "Charlie"
fmt.Println(emp.EmployeeID)  // E123
```

### Pointers

```go
// Declare pointer
var ptr *int
var name *string

// Address-of operator
value := 42
ptr = &value

// Dereference operator
fmt.Println(*ptr)        // 42
*ptr = 100               // Change value through pointer

// Pointer to struct
type Point struct {
    X, Y int
}

point := &Point{10, 20}
fmt.Println(point.X)     // Automatic dereferencing
(*point).X = 15

// Nil pointer
var emptyPtr *int
if emptyPtr == nil {
    fmt.Println("Pointer is nil")
}
```

---

## Packages and Imports

### Creating a Package

```go
// File: math/operations.go
package math

func Add(a, b int) int {
    return a + b
}

// Exported function (capital letter)
func Multiply(a, b int) int {
    return a * b
}

// private function (lowercase letter)
func helper() {
    // ...
}
```

### Using Packages

```go
package main

import (
    "fmt"
    "example.com/my-project/math"
)

func main() {
    result := math.Add(5, 3)
    fmt.Println(result)  // 8
}
```

### Aliasing Imports

```go
import (
    m "example.com/my-project/math"
    "fmt"
)

func main() {
    result := m.Add(5, 3)
    fmt.Println(result)
}
```

### Anonymous Import

```go
import (
    _ "example.com/my-project/init"  // Executes init functions
)
```

---

## Common Commands

### Go CLI Commands

```bash
# Initialize a new module
go mod init example.com/my-app

# Download dependencies
go mod download

# Tidy dependencies (remove unused ones)
go mod tidy

# Vendor dependencies
go mod vendor

# List dependencies
go list -m all

# Run a Go file
go run main.go

# Build executable
go build -o my-app
go build -o my-app ./cmd/main.go

# Install executable to $GOPATH/bin
go install

# Run tests
go test ./...
go test -v ./...

# Test with coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...

# Benchmark
go test -bench=. -benchmem

# Format code
go fmt ./...

# Lint code
go vet ./...

# Get dependencies
go get package/name

# Update package
go get -u package/name

# Remove unused dependencies
go mod tidy

# View package documentation
go doc package/name
go doc package/name.Function

# Check for security vulnerabilities
go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```

---

## Error Handling

### Basic Error Handling

```go
// Error interface
type error interface {
    Error() string
}

// Creating errors
import "errors"
import "fmt"

err := errors.New("something went wrong")
err := fmt.Errorf("invalid input: %s", userInput)

// Handling errors
result, err := someFunction()
if err != nil {
    fmt.Println("Error:", err)
    return
}
fmt.Println("Result:", result)
```

### Custom Error Types

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error in %s: %s", e.Field, e.Message)
}

// Using custom error
err := &ValidationError{Field: "email", Message: "invalid format"}
fmt.Println(err)
```

### Error Wrapping

```go
import "fmt"

if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

// Unwrapping errors
err := someOperation()
if errors.Is(err, targetError) {
    // Handle specific error
}

if errors.As(err, &varOfType) {
    // Handle error type
}
```

---

## Concurrency Basics

### Goroutines

```go
// Launch goroutine
go functionName()
go func() {
    fmt.Println("Running concurrently")
}()

// Goroutines with parameters
go func(name string) {
    fmt.Println("Hello", name)
}("Alice")
```

### Channels

```go
// Channel declaration
var ch chan int                       // Unbuffered channel
var sendCh chan<- int                 // Send-only channel
var recvCh <-chan int                 // Receive-only channel

// Create channel
ch := make(chan int)                  // Unbuffered
ch := make(chan int, 5)               // Buffered with capacity 5

// Send and receive
ch <- 42                              // Send value to channel
value := <-ch                         // Receive value from channel
value, ok := <-ch                     // Receive with ok check

// Close channel
close(ch)

// Check if channel is closed
value, ok := <-ch                     // ok = false if closed

// Range over channel
for value := range ch {
    fmt.Println(value)
}

// Select statement
select {
case msg1 := <-ch1:
    fmt.Println("Received:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received:", msg2)
case ch3 <- 42:
    fmt.Println("Sent value")
default:
    fmt.Println("No channel ready")
}
```

### Wait Groups

```go
import "sync"

var wg sync.WaitGroup

wg.Add(1)  // Add goroutine to wait group
go func() {
    defer wg.Done()  // Mark goroutine as done
    fmt.Println("Working...")
}()

wg.Wait()  // Wait for all goroutines to finish
```

### Mutex (Mutual Exclusion)

```go
import "sync"

type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *Counter) GetCount() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

---

## Practice Exercises

1. **Basic Program**: Write a program that calculates factorial using recursion
2. **Data Structures**: Create a simple to-do list using a slice of structs
3. **Maps**: Build a word frequency counter for a given text
4. **Error Handling**: Create a calculator that handles division by zero gracefully
5. **Goroutines**: Write a program that fetches multiple URLs concurrently
6. **File I/O**: Read a file, process its content, and write results to another file
7. **Interfaces**: Implement a `Shape` interface with `Area()` and `Perimeter()` methods

---

## Resources

- [Official Go Documentation](https://golang.org/doc/)
- [Go by Example](https://gobyexample.com/)
- [The Go Programming Language Book](https://www.gopl.io/)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Effective Go](https://golang.org/doc/effective_go)

---

## Tips for Learning Go

1. **Start Small**: Begin with simple programs before tackling complex projects
2. **Practice Regularly**: Write code every day to build muscle memory
3. **Read Others' Code**: Learn from open-source Go projects
4. **Use the Playground**: Try code at [go.dev/play](https://go.dev/play)
5. **Understand Goroutines**: Master concurrency early as it's a Go strength
6. **Follow Go Idioms**: Write code in the "Go way," not by translating from other languages
7. **Test Your Code**: Write tests alongside your code from the beginning
8. **Use Tools**: Leverage `go fmt`, `go vet`, and linters to maintain code quality

