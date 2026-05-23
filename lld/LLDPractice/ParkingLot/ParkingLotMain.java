import Entities.ParkingLot;
import Entities.Vehicle;

class ParkingLotMain {
    public static void main(String[] args) {
        ParkingLot parkingLot = new ParkingLot(2); // Create a parking lot with 2 spaces

        Vehicle car1 = new Vehicle("Car1");
        Vehicle car2 = new Vehicle("Car2");
        Vehicle car3 = new Vehicle("Car3");

        parkingLot.parkVehicle(car1); // Park Car1
        parkingLot.parkVehicle(car2); // Park Car2
        parkingLot.parkVehicle(car3); // Attempt to park Car3 (should fail)

        parkingLot.unparkVehicle(car1); // Unpark Car1
        parkingLot.parkVehicle(car3); // Park Car3 (should succeed)
    }
}