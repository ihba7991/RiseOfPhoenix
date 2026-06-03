public class HelloWorld {
    public static void main(String[] args) {
        
        /**
         * 1. Print "Hello, World!"
         */
        System.out.println("Hello, World!");

        /**
         * 2. Declare and initialize variables of different types
         */
        int a = 5;
        long b = 10L;
        float c = 5.5f;
        double d = 10.5;
        boolean ok = true;
        char ch = 'A';
        byte by = 100;
        short s = 1000;

        System.out.println("Integer: " + a);
        System.out.println("Long: " + b);
        System.out.println("Float: " + c);
        System.out.println("Double: " + d);
        System.out.println("Boolean: " + ok);
        System.out.println("Character: " + ch);
        System.out.println("Byte: " + by);
        System.out.println("Short: " + s);

        /**
         * 3. Create a program demonstrating type casting (implicit and explicit)
         */
        int intVal = 100;
        long longVal = intVal; // Implicit casting (widening)
        float floatVal = longVal; // Implicit casting (widening)
        double doubleVal = floatVal; // Implicit casting (widening)

        System.out.println("Implicit Casting:");
        System.out.println("Integer: " + intVal);
        System.out.println("Long: " + longVal);
        System.out.println("Float: " + floatVal);
        System.out.println("Double: " + doubleVal);

        doubleVal = 9.78;
        floatVal = (float) doubleVal; // Explicit casting (narrowing)
        longVal = (long) floatVal; // Explicit casting (narrowing)
        intVal = (int) longVal; // Explicit casting (narrowing)

        System.out.println("Explicit Casting:");
        System.out.println("Double: " + doubleVal);
        System.out.println("Float: " + floatVal);
        System.out.println("Long: " + longVal);
        System.out.println("Integer: " + intVal);

        /**
         * 4. Write a program using arithmetic, comparison, and logical operators
         */
        int x = 10, y = 20;
        System.out.println("Arithmetic Operators:");
        System.out.println("Addition: " + (x + y));
        System.out.println("Subtraction: " + (x - y));
        System.out.println("Multiplication: " + (x * y));
        System.out.println("Division: " + (y / x));
        System.out.println("Modulus: " + (y % x));

        System.out.println("Comparison Operators:");
        System.out.println("Equal to: " + (x == y));
        System.out.println("Not equal to: " + (x != y));
        System.out.println("Greater than: " + (x > y));
        System.out.println("Less than: " + (x < y));
        System.out.println("Greater than or equal to: " + (x >= y));
        System.out.println("Less than or equal to: " + (x <= y));

        System.out.println("Logical Operators:- && || !");
        System.out.println("AND: " + (x < y && x > 5));
        System.out.println("OR: " + (x < y || x > 5));
        System.out.println("NOT: " + !(x < y));
    }
}