import java.util.*;

public class Player {
    private String name;
    private Card[] hand;
    private int numCards;

    public Player(String name) {
       this.name = name;
       this.hand = new Card[CardMatch.MAX_CARDS];
       this.numCards = 0;
    }

    public String getName(){
        return this.name;
    }

    public int getNumCards(){
        return numCards;
    }

    public String toString(){
        return this.name;
    }

    public void addCard(Card c1){
        if (c1 == null || this.numCards == CardMatch.MAX_CARDS){
            throw new IllegalArgumentException();
        }
        this.hand[this.numCards] = c1;
        this.numCards ++;
    }

    public Card getCard(int index){
        if (index >= this.numCards || index < -1){
            throw new IllegalArgumentException();
        }
        return this.hand[index];
    }

    public int getHandValue(){
        int HandValue = 0;
        for (int i = 0; i < this.numCards; i++){
            HandValue += this.hand[i].getValue();
        }
        if (this.numCards == CardMatch.MAX_CARDS){
            HandValue += CardMatch.MAX_CARDS_PENALTY;
        }
        return HandValue;
    }

    public void displayHand(){
        System.out.println(this.name + "'s " + "hand:");
        for (int i = 0; i < this.numCards; i ++){
                System.out.println("  " + i + ": " + this.hand[i].getColor() + " " + this.hand[i].getValue());
        }
    }

    public Card removeCard(int index){
        if (index >= this.numCards){
            throw new IndexOutOfBoundsException();
        }
        if (index == (this.numCards - 1)){
            Card store = this.hand[index];
            this.numCards --;
            return store;
        }
        else{
            Card store = this.hand[index];
            this.hand[index] = this.hand[this.numCards - 1];
            this.numCards --;
            return store;
        }
    }
    public int getPlay(Scanner console, Card topDiscard){
        System.out.print(name + ": number of card to play (-1 to draw)");
        int x = 0;
        while(true){
            x = console.nextInt();
            if (x == -1){
                return -1;
            }
            if (x >= 0 && x < this.numCards){
                return x;
            }
            else{
                System.out.print(name + ": number of card to play (-1 to draw)");
            }
        }
    }
}
