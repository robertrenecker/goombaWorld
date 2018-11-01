package com.snowrentalsystem.RentalApp.Service;

import com.snowrentalsystem.RentalApp.Entity.Rentals;
import com.snowrentalsystem.RentalApp.Dao.RentalsDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import java.util.Collection;


@Service
public class RentalService {
    @Autowired
    @Qualifier("mongoData")
    private RentalsDao rentalDao;

    public Collection<Rentals> getAllRentals(){
        return rentalDao.getAllRentals();
    }
}
