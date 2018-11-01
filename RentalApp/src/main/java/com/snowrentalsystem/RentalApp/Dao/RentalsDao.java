package com.snowrentalsystem.RentalApp.Dao;

import com.snowrentalsystem.RentalApp.Entity.Rentals;

import java.util.Collection;

public interface RentalsDao {
    Collection<Rentals> getAllRentals();
}
