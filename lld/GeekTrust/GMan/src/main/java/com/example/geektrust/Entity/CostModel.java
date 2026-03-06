package com.example.geektrust.Entity;

public class CostModel {
    private int travellingCost;
    private int turningCost;
    private int totalAvailablePower;

    public CostModel(int travellingCost, int turningCost, int totalAvailablePower) {
        this.travellingCost = travellingCost;
        this.turningCost = turningCost;
        this.totalAvailablePower = totalAvailablePower;
    }

    public int getTotalAvailablePower() {
        return totalAvailablePower;
    }

    public void setTotalAvailablePower(int totalAvailablePower) {
        this.totalAvailablePower = totalAvailablePower;
    }

    public int getTravellingCost() {
        return travellingCost;
    }

    public void setTravellingCost(int travellingCost) {
        this.travellingCost = travellingCost;
    }

    public int getTurningCost() {
        return turningCost;
    }

    public void setTurningCost(int turningCost) {
        this.turningCost = turningCost;
    }
}
