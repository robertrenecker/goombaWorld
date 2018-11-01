package com.snowrentalsystem.RentalApp.Controller;

import com.snowrentalsystem.RentalApp.Dao.CustomerDao;
import com.snowrentalsystem.RentalApp.model.CustomerFacade;
import com.snowrentalsystem.RentalApp.views.AppCustomerForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class MainController {

    @Autowired
    private CustomerDao customerDao;
    /**
    @InitBinder
    protected void initBinder(WebDataBinder dataBinder){
        //form target
        Object target = dataBinder.getTarget();
        if(target==null){return;}
        System.out.println("Target="+target);

        if(target.getClass() == AppCustomerForm.class){

        }
    }
    **/
    @RequestMapping("/")
    public String viewHome(Model model){
        return "Welcome Page";
    }

    @RequestMapping("/rentals")
    public String viewMembers(Model model){

        return "This is the rentals page";
    }

    //register page
    @RequestMapping(value="/register", method= RequestMethod.GET)
    public String viewRegister(Model model){

        AppCustomerForm form = new AppCustomerForm();

        model.addAttribute("appCustomerForm", form);
        return "registerPage";

    }

    //save registry information


}
