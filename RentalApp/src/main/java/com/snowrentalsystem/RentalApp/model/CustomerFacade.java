package com.snowrentalsystem.RentalApp.model;

public class CustomerFacade {
    private int userId;
    private String name;
    private String address;
    private String password;
    private String email;
    private int creditCardInfo;
    private String dob;

    public CustomerFacade(int userId, String name, String password, String address, String email) {
        this.userId = userId;
        this.name = name;
        this.address = address;
        this.email = email;
    }

    public int getUserId(){
        return userId;
    }
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getCreditCardInfo() {
        return creditCardInfo;
    }

    public void setCreditCardInfo(int creditCardInfo) {
        this.creditCardInfo = creditCardInfo;
    }

    public String getDob() {
        return dob;
    }

    public void setDob(String dob) {
        this.dob = dob;
    }

    //Create Shopping Cart

    //Create rental list


    public Boolean authenticateUser() {
        return true;
    }





}
