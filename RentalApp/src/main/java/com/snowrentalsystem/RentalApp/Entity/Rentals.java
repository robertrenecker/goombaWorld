package com.snowrentalsystem.RentalApp.Entity;

public class Rentals {
    private int itemId;
    private String itemName;
    private float cost;

    public Rentals(int itemId, String itemName, float cost){
        this.itemId = itemId;
        this.itemName = itemName;
        this.cost = cost;
    }

    public String getItemName() {
        return itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public int getItemId() {
        return itemId;
    }

    public void setItemId(int itemId) {
        this.itemId = itemId;
    }

    public float getCost() {
        return cost;
    }

    public void setCost(float cost) {
        this.cost = cost;
    }
}
