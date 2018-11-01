package com.snowrentalsystem.RentalApp.Dao;

import com.snowrentalsystem.RentalApp.model.CustomerFacade;
import com.snowrentalsystem.RentalApp.model.Rental;
import com.snowrentalsystem.RentalApp.views.AppCustomerForm;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class CustomerDao {
    private static Map<Integer, CustomerFacade> USERS_MAP = new HashMap<>();

    static{
        initDATA();
    }

    private static void initDATA(){
        CustomerFacade user = new CustomerFacade(1,"Robert", "dingus","5565 kieeit blvd", "sylvan.rrenecker10@gmail.com");

        USERS_MAP.put(user.getUserId(), user);

    }

    public Integer getMaxCustomerId(){
        int max = 0;
        for(Integer userId: USERS_MAP.keySet()){
            if(userId > max){
                max = userId;
            }
        }
        return max;
    }
    public CustomerFacade createCustomer(AppCustomerForm form){
        int userId = this.getMaxCustomerId() + 1;

        CustomerFacade user = new CustomerFacade(userId, form.getUserName(), form.getPassword(), form.getAddress(), form.getEmail());

        USERS_MAP.put(userId, user);

        return user;
    }



}
