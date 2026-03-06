package com.example.geektrust.Entity;

public class Gman {
    private Source source;
    private Destination destination;
    private String directionFacing;

    public Gman() {
    }

    public Gman(Source source, Destination destination, String directionFacing) {
        this.source = source;
        this.destination = destination;
        this.directionFacing = directionFacing;
    }

    public Source getSource() {
        return source;
    }

    public void setSource(Source source) {
        this.source = source;
    }

    public Destination getDestination() {
        return destination;
    }

    public void setDestination(Destination destination) {
        this.destination = destination;
    }

    public String getDirectionFacing() {
        return directionFacing;
    }

    public void setDirectionFacing(String directionFacing) {
        this.directionFacing = directionFacing;
    }
}
