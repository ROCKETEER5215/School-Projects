package main;
// By Justin Wallace

import java.util.Random;
import java.util.Scanner;

public class Lottery
{
 private int Array_Size = 5;
 private int [] lotteryNumbers = new int[5];
 private int [] UsersNumbers = new int[5];
 private Random rand = new Random();

 public Lottery()
 {
  for(int index = 0; index < Array_Size; index++)
  {
   lotteryNumbers[index] = rand.nextInt(10);
  }
 }

 public int getAndCompareArray()
 {
  Scanner keyboard = new Scanner(System.in);
  int matchingDigits = 0;

  System.out.println("Please enter 5 array elements");

  for (int index = 0; index < Array_Size; index++)
  {
   System.out.println("Enter Array element "+(index+1)+": ");
   UsersNumbers[index] = keyboard.nextInt();

   if(lotteryNumbers[index] == UsersNumbers[index])
   {
    matchingDigits += 1;
   }
  }
  keyboard.close();
  return matchingDigits;
 }

 public int[] lotteryCopy()
 {
  return this.lotteryNumbers;
 }
}
