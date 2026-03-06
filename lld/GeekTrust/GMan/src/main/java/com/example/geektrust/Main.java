package com.example.geektrust;

import com.example.geektrust.Entity.*;
import com.example.geektrust.Utils.PowerConsumedCalculator;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {

//        Sample code to referead from file passed as command line argument
        try {
            // the file to be opened for reading
            FileInputStream fis = new FileInputStream(args[0]);
            Scanner sc = new Scanner(fis); // file to be scanned
            // returns true if there is another line to read
            Gman gman = new Gman();
            while (sc.hasNextLine()) {
               //Add your code here to process input commands
                String line = sc.nextLine();
                String[] tokens = line.split(" ");
                switch (tokens[0]) {
                    case "SOURCE":
                        // process command 1
                        Source source = new Source(Integer.parseInt(tokens[1]), Integer.parseInt(tokens[2]));
                        gman.setSource(source);
                        gman.setDirectionFacing(tokens[3]);
                        break;
                    case "DESTINATION":
                        // process command 2
                        Destination destination = new Destination(Integer.parseInt(tokens[1]), Integer.parseInt(tokens[2]));
                        gman.setDestination(destination);
                        break;
                    case "PRINT_POWER":
                        CostModel costModel = new CostModel(10,5,200);
                        PowerConsumedCalculator powerConsumedCalculator = new PowerConsumedCalculator(gman, costModel);
                        System.out.println(powerConsumedCalculator.remainingPower());
                        break;
                    // add more cases as needed
                    default:
                        System.out.println("Invalid command: " + tokens[0]);
                }
            }
            sc.close(); // closes the scanner
        } catch (IOException e) {
        }

    }
}
