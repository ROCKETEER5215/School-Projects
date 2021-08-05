package main;
//By Justin Wallace

import java.util.Random;

public class Main
{
    public static void main(String[] args)
    {
	 Lottery myLottery =  new Lottery();
     int numRight = myLottery.getAndCompareArray();
     int [] myCopy = myLottery.lotteryCopy();



     if(numRight == 5)
     {
      System.out.println("You Won The Lottery!");
     }
     else
     {
      System.out.println("You had "+numRight+" matches.");
     }

     System.out.print("Answer: ");
     for (int i = 0; i <5; i++)
     {
      System.out.print(myCopy[i]+" ");
     }
    }
}
