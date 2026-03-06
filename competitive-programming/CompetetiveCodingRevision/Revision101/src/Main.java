import java.sql.SQLOutput;
import java.util.*;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {


    public int countPeaks(int num){
        List<Integer> list = new ArrayList<>();
        while(num != 0){
            list.add(num%10);
            num /= 10;
        }
        int len = list.size();
        int curr = 1;
        int prev = 0;
        int next = 2;
        int ct = 0;
        while(next < len){
            if( (list.get(curr) > list.get(prev) && list.get(curr) > list.get(next)) ){
                ct++;
            }
            if( (list.get(curr) < list.get(prev) && list.get(curr) < list.get(next)) ){
                ct++;
            }
            prev++;
            curr++;
            next++;
        }
        return ct;
    }

    private void bfsMatrix(){

    }

    public int totalWaviness(int num1, int num2) {
        if(num2%100 == num2){
            return 0;
        }
        int numOfPeak = 0;
        for(int i = num1; i <= num2; i++){
            if(i % 100 == i){
                continue;
            }
            numOfPeak += countPeaks(i);
        }
        return numOfPeak;
    }

    public static boolean isPeriodic(String s){
        int l =  s.length();
        String s1 = s + s;
        String s2 = s1.substring(1, 2*l-1);
        return s2.contains(s);
    }
    public static int findLeastNumOfUniqueInts(int[] arr, int k) {
        //brute force
        Map<Integer, Integer> mp = new HashMap<>();
        for(int i : arr){
            mp.put(i, mp.getOrDefault(i,0) + 1);
        }
        List<Integer> frequencies = new ArrayList<>(mp.values());
        Collections.sort(frequencies);

        int elementsRemoved = 0;
        for(int i = 0; i < frequencies.size(); i++){
            elementsRemoved += frequencies.get(i);
            if(elementsRemoved > k){
                return frequencies.size() - i;
            }
        }

        return 0;
    }

    public static void main(String[] args) {
        //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
        // to see how IntelliJ IDEA suggests fixing it.
        System.out.print("Hello and welcome!");
        String bStr = Integer.toBinaryString(7);
        String revStr = new StringBuilder(bStr).reverse().toString();

        System.out.println(isPeriodic("ababab"));

        System.out.println(findLeastNumOfUniqueInts(new int[]{4,3,1,1,3,3,2}, 1));
//        System.out.println(Integer.toBinaryString(7));;

//        String message = "12-10-2024";
//        int day = Integer.parseInt(message.substring(0, 2));
//        int month = Integer.parseInt(message.substring(3, 5));
//        int year = Integer.parseInt(message.substring(6, 10));
//
//        System.out.println(day);
//        System.out.println(month);
//        System.out.println(year);
//        System.out.println("Date: " + day + "/" + month + "/" + year);
//

    }




    private int add(String date, int days) {
        int day = Integer.parseInt(date.substring(0, 2));
        int month = Integer.parseInt(date.substring(3, 5));
        int year = Integer.parseInt(date.substring(6, 10));
        int[] dayMonth = {31,28,31,30,31,30,31,31,30,31,30,31}; // Simplified: assuming all months have 30 days
        int currentMonthDays = dayMonth[month - 1];
        while(days > 0) {
            day++;
            days--;

            if(day > currentMonthDays) { // Simplified: assuming all months have 30 days
                day = 1;
                month++;
                if(month > 12) {
                    month = 1;
                    year++;
                }
            }
        }
        return day;
    }
}