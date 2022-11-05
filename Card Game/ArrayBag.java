/* 
 * ArrayBag.java
 *
 * A blueprint class for objects that represent a bag of other objects --
 * i.e., a collection of items in which the items do not have a position.
 * This implementation uses an array to store to objects in the bag.
 *
 * Computer Science 112
 *
 * modified by: <name>, <email>
 */

import java.util.*;

public class ArrayBag {
    /** 
     * The array used to store the items in the bag.
     */
    private Object[] items;
    
    /** 
     * The number of items in the bag.
     */
    private int numItems;
    
    public static final int DEFAULT_MAX_SIZE = 50;
    
    /**
     * Constructor with no parameters - creates a new, empty ArrayBag with 
     * the default maximum size.
     */
    public ArrayBag() {
        this.items = new Object[DEFAULT_MAX_SIZE];
        this.numItems = 0;
    }
    
    /** 
     * A constructor that creates a new, empty ArrayBag with the specified
     * maximum size.
     */
    public ArrayBag(int maxSize) {
        if (maxSize <= 0) {
            throw new IllegalArgumentException("maxSize must be > 0");
        }
        this.items = new Object[maxSize];
        this.numItems = 0;
    }
    
    /**
     * numItems - accessor method that returns the number of items 
     * in this ArrayBag.
     */
    public int numItems() {
        return this.numItems;
    }
    
    /** 
     * add - adds the specified item to this ArrayBag. Returns true if there 
     * is room to add it, and false otherwise.
     * Throws an IllegalArgumentException if the item is null.
     */
    public boolean add(Object item) {
        if (item == null) {
            throw new IllegalArgumentException("item must be non-null");
        } else if (this.numItems == this.items.length) {
            return false;    // no more room!
        } else {
            this.items[this.numItems] = item;
            this.numItems++;
            return true;
        }
    }
    
    /** 
     * remove - removes one occurrence of the specified item (if any)
     * from this ArrayBag.  Returns true on success and false if the
     * specified item (i.e., an object equal to item) is not in this ArrayBag.
     */
    public boolean remove(Object item) {
        for (int i = 0; i < this.numItems; i++) {
            if (this.items[i].equals(item)) {
                // Shift the remaining items left by one.
                for (int j = i; j < this.numItems - 1; j++) {
                    this.items[j] = this.items[j + 1];
                }
                this.items[this.numItems - 1] = null;
                
                this.numItems--;
                return true;
            }
        }
        
        return false;  // item not found
    }
    
    /**
     * contains - returns true if the specified item is in the Bag, and
     * false otherwise.
     */
    public boolean contains(Object item) {
        for (int i = 0; i < this.numItems; i++) {
            if (this.items[i].equals(item)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * grab - returns a reference to a randomly chosen item in this ArrayBag.
     */
    public Object grab() {
        if (this.numItems == 0) {
            throw new IllegalStateException("the bag is empty");
        }
        
        int whichOne = (int)(Math.random() * this.numItems);
        return this.items[whichOne];
    }
    
    /**
     * toArray - return an array containing the current contents of the bag
     */
    public Object[] toArray() {
        Object[] copy = new Object[this.numItems];
        
        for (int i = 0; i < this.numItems; i++) {
            copy[i] = this.items[i];
        }
        
        return copy;
    }
    
    /**
     * toString - converts this ArrayBag into a string that can be printed.
     * Overrides the version of this method inherited from the Object class.
     */
    public String toString() {
        String str = "{";
        
        for (int i = 0; i < this.numItems; i++) {
            str = str + this.items[i];
            if (i != this.numItems - 1) {
                str += ", ";
            }
        }
        
        str = str + "}";
        return str;
    }
    
    /* Test the ArrayBag implementation. */
    public static void main(String[] args) {
        ArrayBag b1 = new ArrayBag(10);
        String[] letters1 = {"a", "a", "b", "d", "f", "f", "f", "g"};
        for (String ltr: letters1) {
            b1.add(ltr);
        }
        System.out.println(b1);

        ArrayBag b2 = new ArrayBag(8);
        String[] letters2 = {"a", "b", "c", "d", "d", "e", "f"};
        for (String ltr: letters2) {
            b2.add(ltr);
        }
        System.out.println(b2);

        ArrayBag b3 = b1.intersectionWith(b2);
        System.out.println(b3);
        System.out.println(b3.numItems());
        System.out.println(b3.roomLeft());
        System.out.println(b1);   // make sure original bags are unchanged
        System.out.println(b2);
       
        // Create a Scanner object for user input.
        Scanner scan = new Scanner(System.in);
        
        // Create an ArrayBag named bag1.
        System.out.print("size of bag 1: ");
        int size = scan.nextInt();
        ArrayBag bag1 = new ArrayBag(size);
        scan.nextLine();    // consume the rest of the line
        
        // Read in strings, add them to bag1, and print out bag1.
        String itemStr;        
        for (int i = 0; i < size; i++) {
            System.out.print("item " + i + ": ");
            itemStr = scan.nextLine();
            bag1.add(itemStr);
        }
        System.out.println("bag 1 = " + bag1);
        System.out.println();
        
        // Select a random item and print it.
        Object item = bag1.grab();
        System.out.println("grabbed " + item);
        System.out.println();
        
        // Iterate over the objects in bag1, printing them one per
        // line.
        Object[] items = bag1.toArray();
        for (int i = 0; i < items.length; i++) {
            System.out.println(items[i]);
        }
        System.out.println();
        
        // Get an item to remove from bag1, remove it, and reprint the bag.
        System.out.print("item to remove: ");
        itemStr = scan.nextLine();
        if (bag1.contains(itemStr)) {
            bag1.remove(itemStr);
        }
        System.out.println("bag 1 = " + bag1);
        System.out.println();
    }

    public int roomLeft(){
        return this.items.length - this.numItems;
    }

    public boolean isFull(){
        if (this.items.length == this.numItems){
            return true;
        }
        return false;
    }

    public void increaseCapacity(int increment){
        if (increment == 0){
            return;
        }
        if (increment < 0){
            throw new IllegalArgumentException();
        }
        int newLength = this.items.length + increment;
        Object[] newArray = new Object[newLength];
        for (int i = 0; i < this.items.length; i++){
            newArray[i] = this.items[i];
        }
        this.items = newArray;
    }

    public boolean removeItems(ArrayBag other){
        int originalItems = this.numItems;
        Object[] arrayOther = other.toArray();
        for (int i = 0; i < arrayOther.length ; i ++){ 
            while(this.contains(arrayOther[i])){
                this.remove(arrayOther[i]);
            }
        }
        if (this.numItems < originalItems){
            return true;
        }
        return false;
    }
    public ArrayBag intersectionWith(ArrayBag Other){
        ArrayBag newBag;
        if (Other == null){
            throw new IllegalArgumentException();
        }
        if (Other.numItems == 0 && this.numItems == 0){
            return new ArrayBag(1);
        }
        else if (Other.numItems < this.numItems){
            newBag = new ArrayBag(Other.numItems);
        }
        else{
            newBag = new ArrayBag(this.numItems);
        }
        for (int i = 0; i < this.numItems; i++){
            if(Other.contains(this.items[i]) && !(newBag.contains(this.items[i]))){
                newBag.add(this.items[i]);
            }

        }
        return newBag;
        
    }

}   
