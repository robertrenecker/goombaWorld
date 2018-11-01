package com.snowrentalsystem.RentalApp.Controller;
import com.snowrentalsystem.RentalApp.Entity.Rentals;
import com.snowrentalsystem.RentalApp.Service.RentalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collection;

@RestController
@RequestMapping("/rentals")
public class RentalsController {

    @Autowired
    private RentalService rentalService;
    @RequestMapping(method= RequestMethod.GET)
    public Collection<Rentals> getAllRentals(){
        return rentalService.getAllRentals();

    }


}
