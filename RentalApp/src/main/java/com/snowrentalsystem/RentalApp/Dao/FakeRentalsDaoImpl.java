package com.snowrentalsystem.RentalApp.Dao;

import com.snowrentalsystem.RentalApp.Entity.Rentals;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.Collection;
import java.util.Map;
import java.util.HashMap;

@Repository
public class FakeRentalsDaoImpl implements RentalsDao {

    private static Map<Integer, Rentals> rentals;

    static{

        rentals = new HashMap<Integer, Rentals>(){
            {
                put(1, new Rentals(1, "Armada Skis", 45));
                put(2, new Rentals(2, "Sleds", 10));
                put(3, new Rentals(3, "Burton Snowboard", 35));
            }
            };
    }

    @Override
    public Collection<Rentals> getAllRentals(){
        return this.rentals.values();
    }

}



