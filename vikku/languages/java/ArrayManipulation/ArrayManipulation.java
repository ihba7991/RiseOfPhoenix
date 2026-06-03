public class ArrayManipulation {
    public static void main(String[] args) {
        // Take input from user for searching element
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a number to search:");
        int searchElement = scanner.nextInt();

        int[] arr = {1,2,3,4,5};

        System.out.println("Print Original Array:");
        for(int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }

        System.out.println("Print Reversed Array:");
        for(int i = arr.length - 1; i >= 0; i--) {
            System.out.println(arr[i]);
        }

        System.out.println("Array after Sorting:");
        Arrays.sort(arr);
        for(int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }

        System.out.println("Searching for an element in an array:");
        for(int i = 0; i < arr.length; i++) {
            if(arr[i] == searchElement) {
                System.out.println("Element found at index: " + i);
            }
        }
    }
}