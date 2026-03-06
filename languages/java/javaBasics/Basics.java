import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Scanner;




public class Basics {


    public boolean isPalindrome(String s){
        // if(s.length() == 0) return false;
        if(s.length() == 1) return true;
        int low = 0; 
        int high = s.length()-1;
        while(low<high){
            System.out.println("Comparing " + s.charAt(low) + " and " + s.charAt(high));
            if(s.charAt(low) != s.charAt(high)){
                return false;
            }
            low++;
            high--;
        }
        return true;
    }
    public String longestPalindrome(String s) {
        int n = s.length();
        if(n == 0) return "";
        if(n == 1) return s;
        String ans = "";
        int maxLen = Integer.MIN_VALUE;

        for(int i =0; i<n ; i++){
            for(int j = i; j<=n; j++){
                String curr = s.substring(i,j);
                System.out.println("current: " + curr);
                int currLen = curr.length();
                System.out.println("current length: " + currLen);
                if(isPalindrome(curr)){
                    System.out.println("Palindrome found: " + curr);
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
        int n = s.length();
        int leftSum = 0;
        int rightSum = 0;
        int left = 0;
        int right = n-1;
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
        System.out.println("Prefix sum array: ");
        for(int i =0; i<n; i++){
            System.out.print(preSum[i] + " ");
        }
        
        System.out.println("Post sum array: ");
        for(int i =0; i<n; i++){
            System.out.print(postSum[i] + " ");
        }
        for(int i =0; i<n; i++){
            if(preSum[i] == postSum[n-1-i]){
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        System.out.println("===="+input.substring(0,2));
        System.out.println("This is input: "+input);
        String ans = new Basics().longestPalindrome(input);
        System.out.println("Answer + " + ans);
        String config = "324";
        int x = 2;
        int y = 3;
        boolean res = new Basics().scoreBalance("abccba");
        // System.out.println(num % 2 == 0 ? "Even" : "Odd");
        scanner.close();

    }
}