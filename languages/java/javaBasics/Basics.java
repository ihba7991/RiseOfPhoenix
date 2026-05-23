import java.util.Scanner;




public class Basics {


    public boolean isPalindrome(String s){
        if(s == null) return false;
        if(s.length() == 0) return false;
        if(s.length() == 1) return true;
        int low = 0; 
        int high = s.length()-1;
        while(low<high){
            // Reduced debug output for clarity
            if(s.charAt(low) != s.charAt(high)){
                return false;
            }
            low++;
            high--;
        }
        return true;
    }
    public String longestPalindrome(String s) {
        if(s == null) return "";
        int n = s.length();
        if(n == 0) return "";
        if(n == 1) return s;
        String ans = "";
        int maxLen = 0;

        for(int i =0; i<n ; i++){
            // ensure we consider substrings of length >= 1
            for(int j = i+1; j<=n; j++){
                String curr = s.substring(i,j);
                int currLen = curr.length();
                if(isPalindrome(curr)){
                    if(currLen>maxLen){
                        ans = curr;
                        maxLen = currLen;
                    }
                }
            }

        }
        return ans;
    }

    // public int validConfig(String config, int x, int y) {
    //     // Write your code here
    //     int curr = 0;
    //     //case 1 starting with x
    //     if(config.contains())
    //     //case 2 starting with y d
        
    //     return curr;
    // }

    public boolean scoreBalance(String s) {
        if(s == null) return false;
        int n = s.length();
        if(n < 2) return false; // cannot split
        int leftSum = 0;
        int rightSum = 0;
        int[] postSum = new int[n];
        int[] preSum = new int[n];
        for(int i =0; i<n; i++){
            leftSum += (s.charAt(i) - 'a') + 1;
            preSum[i] = leftSum;
        }
        for(int j = n-1; j>=0; j--){
            rightSum += (s.charAt(j) - 'a') + 1;
            postSum[j] = rightSum;
        }
        // compare prefix sum up to i with suffix sum starting at i+1
        for(int i =0; i<n-1; i++){
            if(preSum[i] == postSum[i+1]){
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = null;
        if(scanner.hasNextLine()){
            input = scanner.nextLine().trim();
        }
        if(input == null || input.length() == 0){
            // fallback/default
            input = "abccba";
            System.out.println("No input provided. Using default: " + input);
        }

        // Safe substring printing
        if(input.length() >= 2){
            System.out.println("===="+input.substring(0,2));
        } else {
            System.out.println("===="+input);
        }
        System.out.println("This is input: "+input);
        String ans = new Basics().longestPalindrome(input);
        System.out.println("Longest palindrome: " + (ans.isEmpty() ? "(none)" : ans));

        boolean res = new Basics().scoreBalance(input);
        System.out.println("scoreBalance result: " + res);
        scanner.close();

    }
}