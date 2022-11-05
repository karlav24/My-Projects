/*
 * Card.java
 * 
 * A blueprint class for objects that represent a single playing card 
 * for a game in which cards have both colors and numeric values.
 * 
 * starter code: CS 112 Staff (cs112-staff@cs.bu.edu)
 * completed by: Karla Vazquez
 */

public class Card{
    /* The smallest possible value that a Card can have. */
    public static final int MIN_VALUE = 0;
    
    /* The possible colors that a Card can have. */
    public static final String[] COLORS = {"blue", "green", "red", "yellow"};

    /* Define the third class constant here. */
    public static final int MAX_VALUE = 9;
    /* Put the rest of your class definition below. */
    private String color;
    private int value;

    public Card(String col, int val){
        this.setColor(col);
        this.setValue(val);
    }

    public String getColor(){
        return this.color;
    }

    public int getValue(){
        return this.value;
    }
    public static Boolean isValidColor(String color){
        for (int i = 0; i < COLORS.length; i++){
            if (COLORS[i] == color){
                return true;
            }
        }
    return false;
    }

    public void setColor(String col){
        if (isValidColor(col) == false){
            throw new IllegalArgumentException();
        }
        this.color = col;
    }

    public void setValue(int val){
        if(val < MIN_VALUE || val > MAX_VALUE ){
            throw new IllegalArgumentException();
        }
        this.value = val;
    }

    public String toString() {
        return this.color + " " + this.value;
    }

    public Boolean matches(Card other){
        if (other ==  null){
            return false;
        }
        if(other.color == this.color){
            return true;
        }
        else if(other.value == this.value){
            return true;
        }
        return false;
    }

    public Boolean equals(Card other){
        if (other == null){
            return false;
        }
        else if ((other.color == this.color) && (other.value == this.value)){
            return true;
        }
        return false;
    }
}
    
