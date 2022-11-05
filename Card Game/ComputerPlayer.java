import java.util.*;

public class ComputerPlayer extends Player{
    public ComputerPlayer(String name){
        super(name);
    }
    
    public void displayHand(){
        System.out.println(getName() + "'s " + "hand:");
        if (getNumCards() == 1){
            System.out.println("  " + getNumCards() + " card");
        }
        else{
            System.out.println("  " +getNumCards() + " cards");
        }
    }

    public int getPlay(Scanner console, Card topDiscard){
        int count = 0;
        int index = 0;
        int store = 0;
        for(int i = 0; i < getNumCards(); i++){
            if (getCard(i).matches(topDiscard) == true){
                store = i;
                if (getCard(store).getValue() >= getCard(index).getValue()){
                    count += 1;
                    index = i;
                }
            }
        }
        if(count > 0){
            return index;
        }
        return -1;
    }
}
