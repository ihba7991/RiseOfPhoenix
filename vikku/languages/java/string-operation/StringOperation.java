public class StringOperation {
    public static void main(String[] args) {
        String str1 = "Hello";
        String str2 = "World";

        // Concatenation
        String result = str1 + " " + str2;
        System.out.println("Concatenation: " + result);

        // Length
        System.out.println("Length of str1: " + str1.length());

        // Substring
        System.out.println("Substring of str2: " + str2.substring(1, 4));

        // Character at index
        System.out.println("Character at index 2 of str1: " + str1.charAt(2));
    }

}