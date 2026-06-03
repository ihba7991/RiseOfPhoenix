import java.util.Scanner;

public class Calculator {
    public static void main(String[] args) {
        int a, b;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter first numbers:");
        a = scanner.nextInt();
        System.out.println("Enter second numbers:");
        b = scanner.nextInt();

        System.out.println("Select operation:");
        System.out.println("1. Addition");
        System.out.println("2. Subtraction");
        System.out.println("3. Multiplication");
        System.out.println("4. Division");
        int operation = scanner.nextInt();

        switch(operation) {
            case 1:
                System.out.println("Addition: " + (a + b));
                break;
            case 2:
                System.out.println("Subtraction: " + (a - b));
                break;
            case 3:
                System.out.println("Multiplication: " + (a * b));
                break;
            case 4:
                System.out.println("Division: " + (a / b));
                break;
        }

    }
}