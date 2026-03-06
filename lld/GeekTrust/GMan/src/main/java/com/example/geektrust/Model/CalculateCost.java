package com.example.geektrust.Model;

import com.example.geektrust.Entity.Destination;
import com.example.geektrust.Entity.Source;

public class CalculateCost {
    private Source source;
    private Destination destination;
    private int totalCost;

    public CalculateCost(Source source, Destination destination, int totalCost) {
        this.source = source;
        this.destination = destination;
        this.totalCost = totalCost;
    }

    public int getTotalCost() {
        return totalCost;
    }
}
