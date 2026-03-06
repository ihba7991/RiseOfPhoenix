package com.example.geektrust.Utils;

import com.example.geektrust.Entity.*;

public class PowerConsumedCalculator {
    private Gman gman;
    private CostModel costModel;

    public PowerConsumedCalculator(Gman gman, CostModel costModel) {
        this.gman = gman;
        this.costModel = costModel;
    }

    public int calculatePowerConsumed() {
        int totalPowerConsumed = 0;
        int turningCost = costModel.getTurningCost();
        int travellingCost = costModel.getTravellingCost();

        // Calculate power consumed for turns
        totalPowerConsumed += getNumberOfTurns() * turningCost;

        // Calculate power consumed for distance travelled
        totalPowerConsumed += getDistanceTravelled(gman.getSource(), gman.getDestination()) * travellingCost;
        return totalPowerConsumed;
    }

    public int remainingPower() {
        int powerConsumed = calculatePowerConsumed();
        return costModel.getTotalAvailablePower() - powerConsumed;
    }

    private int getNumberOfTurns() {
        String directionFacing = gman.getDirectionFacing();
        int numberOfTurns = 0;
        int sourceX = gman.getSource().getCoordinateX();
        int sourceY = gman.getSource().getCoordinateY();
        int destinationX = gman.getDestination().getCoordinateX();
        int destinationY = gman.getDestination().getCoordinateY();

        if(sourceX != destinationX) {
            // Need to move in X direction
            if (sourceX < destinationX) {
                // Need to move East
                if (!directionFacing.equals("E")) {
                    numberOfTurns++;
                }
            } else {
                // Need to move West
                if (!directionFacing.equals("W")) {
                    numberOfTurns++;
                }
            }
        } else {
            if(sourceY != destinationY) {
                // Need to move in Y direction
                if(sourceY < destinationY) {
                    // Need to move North
                    if(!directionFacing.equals("N")) {
                        numberOfTurns++;
                    }
                } else {
                    // Need to move South
                    if(!directionFacing.equals("S")) {
                        numberOfTurns++;
                    }
                }
            }
        }


       if(sourceY != destinationY) {
           // Need to move in Y direction
            if(sourceY < destinationY) {
                 // Need to move North
                 if(!directionFacing.equals("N")) {
                     numberOfTurns++;
                 }
            } else {
                 // Need to move South
                 if(!directionFacing.equals("S")) {
                     numberOfTurns++;
                 }
            }
       } else{
              if(sourceX != destinationX) {
                // Need to move in X direction
                if (sourceX < destinationX) {
                     // Need to move East
                     if (!directionFacing.equals("E")) {
                          numberOfTurns++;
                     }
                } else {
                     // Need to move West
                     if (!directionFacing.equals("W")) {
                          numberOfTurns++;
                     }
                }
              }
       }



        return numberOfTurns;
    }

    private int getDistanceTravelled(Source source, Destination destination) {
        int distanceX = Math.abs(destination.getCoordinateX() - source.getCoordinateX());
        int distanceY = Math.abs(destination.getCoordinateY() - source.getCoordinateY());
        return distanceX + distanceY;
    }




}
