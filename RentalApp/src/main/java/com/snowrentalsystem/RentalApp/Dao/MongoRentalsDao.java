package com.snowrentalsystem.RentalApp.Dao;

import com.snowrentalsystem.RentalApp.Entity.Rentals;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.Collection;

@Repository
@Qualifier("mongoData")
public class MongoRentalsDao implements RentalsDao{

    @Override
    public Collection<Rentals> getAllRentals() {
        return new ArrayList<Rentals>(){
            {
                add(new Rentals(1, "Armada Skis", 45));
            }
            };
    }
}
