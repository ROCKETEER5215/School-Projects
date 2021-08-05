package main;

import java.util.Scanner;
import javax.swing.JOptionPane;

/**
 * Created by Justin Wallace on 5/29/2016.
 */

public class MyAirline
{
 private final int rows = 6;
 private final int cols = 4;
 private final int firstClass = 2;
 private final int economy = 6;
 private int[][]airlineReservations = new int[rows][cols];

 public MyAirline()
 {

  for(int r = 0; r < rows; r++)
  {
   for(int c =0; c<cols; c++)
   {
    airlineReservations[r][c] = 0;
   }
  }
  getReservations();
 }

 private void getReservations()
 {
  Scanner keyboard = new Scanner(System.in);
  boolean done = false;
  String passClass ="";
  String end = "Next flight leaves in 2 hours";

  while (done != true)
  {
   System.out.println("What class would like to book seats in?(First or Economy)");
   passClass = keyboard.nextLine();

   //First
   if(passClass.equals("First") && checkFirstForSeats())
   {
    System.out.println("chose from rows 0-1");
    int tempRow = keyboard.nextInt();

    System.out.println("chose from seats 0-3");
    int tempSeat = keyboard.nextInt();

    if(airlineReservations[tempRow][tempSeat] == 1)
    {
     System.out.println("Sorry that seat is alreadly taken try again.");

     getReservations();

     done=true;
    }
    else
    {
     airlineReservations[tempRow][tempSeat] = 1;
     displayReservations();

     System.out.println("Would you like to book another seat?(Y or N)");

     if(keyboard.nextLine().equals("Y"))
     {
      getReservations();

      done=true;
     }
     if(keyboard.nextLine().equals("N"))
     {
      JOptionPane.showMessageDialog(null,end);
      done = true;
     }

    }
   }

   if(passClass.equals("First")&&!checkFirstForSeats())
   {
    System.out.println("First Class is full but you can book Economy instead(Y or N)");

    if(keyboard.nextLine().equals("N"))
    {
     displayReservations();
     JOptionPane.showMessageDialog(null,end);
     done = true;
    }
    else
    {
     System.out.println("chose from rows 2-5");
     int tempRow = keyboard.nextInt();

     System.out.println("chose from seats 0-3");
     int tempSeat = keyboard.nextInt();

     if(airlineReservations[tempRow][tempSeat] == 1)
     {
      System.out.println("Sorry that seat is alreadly taken try again.");
      getReservations();
      done=true;
     }
     else
     {
      airlineReservations[tempRow][tempSeat] = 1;
      displayReservations();

      System.out.println("Would you like to book another seat?(Y or N)");

      if(keyboard.nextLine().equals("Y"))
      {
       getReservations();
       done = true;
      }
      if(keyboard.nextLine().equals("N"))
      {
       JOptionPane.showMessageDialog(null,end);
       done = true;
      }
     }
    }
   }

   //Economy
   if(passClass.equals("Economy")&& checkEconomyForSeats())
   {
    System.out.println("chose from rows 2-5");
    int tempRow = keyboard.nextInt();

    System.out.println("chose from seats 0-3");
    int tempSeat = keyboard.nextInt();

    if(airlineReservations[tempRow][tempSeat] == 1)
    {
     System.out.println("Sorry that seat is alreadly taken try again.");

     getReservations();

     done = true;
    }
    else
    {
     airlineReservations[tempRow][tempSeat] = 1;
     displayReservations();

     System.out.println("Would you like to book another seat?(Y or N)");

     if(keyboard.nextLine().equals("Y"))
     {
      getReservations();
      done = true;
     }
     if(keyboard.nextLine().equals("N"))
     {
      JOptionPane.showMessageDialog(null,end);
      done = true;
     }
    }
   }

   if(passClass.equals("Economy")&& !checkEconomyForSeats())
   {
    System.out.println("Economy Class is full but you can book First instead(Y or N)");

    if(keyboard.nextLine().equals("N"))
    {
     displayReservations();
     JOptionPane.showMessageDialog(null,end);
     done = true;
    }
    else
    {
     System.out.println("chose from rows 0-1");
     int tempRow = keyboard.nextInt();

     System.out.println("chose from seats 0-3");
     int tempSeat = keyboard.nextInt();

     if(airlineReservations[tempRow][tempSeat] == 1)
     {
      System.out.println("Sorry that seat is alreadly taken try again.");
      getReservations();
      done=true;
     }
     else
     {
      airlineReservations[tempRow][tempSeat] = 1;
      displayReservations();

      System.out.println("Would you like to book another seat?(Y or N)");

      if(keyboard.nextLine().equals("Y"))
      {
       getReservations();
       done = true;
      }
      if(keyboard.nextLine().equals("N"))
      {
       JOptionPane.showMessageDialog(null,end);
       done = true;
      }
     }
    }
   }

  }
  keyboard.close();
 }

 private boolean checkFirstForSeats()
 {
  for(int r = 0; r < firstClass; r++)
  {
   for (int c = 0; c < cols; c++)
   {
    if(airlineReservations[r][c] == 0)
    {
     return true;
    }
   }
  }
  return false;
 }

 private boolean checkEconomyForSeats()
 {
  for(int r = 2; r < economy; r++)
  {
   for(int c = 0; c<cols; c++)
   {
    if(airlineReservations[r][c]== 0)
    {
     return true;
    }
   }
  }
  return false;
 }

 private void displayReservations()
 {
  //First Class
  System.out.println("First Class");
  System.out.print("   1|2|3|4");

  System.out.println("");
  System.out.print("1: "+airlineReservations[0][0]+" ");
  System.out.print(airlineReservations[0][1]+" ");
  System.out.print(airlineReservations[0][2]+" ");
  System.out.print(airlineReservations[0][3]+" ");
  System.out.println("");
  System.out.print("2: "+airlineReservations[1][0]+" ");
  System.out.print(airlineReservations[1][1]+" ");
  System.out.print(airlineReservations[1][2]+" ");
  System.out.print(airlineReservations[1][3]+" ");
  System.out.println("");

  //Economy Class
  System.out.println("Economy Class");
  System.out.print("   1|2|3|4");

  System.out.println("");
  System.out.print("3: "+airlineReservations[2][0]+" ");
  System.out.print(airlineReservations[2][1]+" ");
  System.out.print(airlineReservations[2][2]+" ");
  System.out.print(airlineReservations[2][3]+" ");
  System.out.println("");
  System.out.print("4: "+airlineReservations[3][0]+" ");
  System.out.print(airlineReservations[3][1]+" ");
  System.out.print(airlineReservations[3][2]+" ");
  System.out.print(airlineReservations[3][3]+" ");
  System.out.println("");
  System.out.print("5: "+airlineReservations[4][0]+" ");
  System.out.print(airlineReservations[4][1]+" ");
  System.out.print(airlineReservations[4][2]+" ");
  System.out.print(airlineReservations[4][3]+" ");
  System.out.println("");
  System.out.print("6: "+airlineReservations[5][0]+" ");
  System.out.print(airlineReservations[5][1]+" ");
  System.out.print(airlineReservations[5][2]+" ");
  System.out.print(airlineReservations[5][3]+" ");
  System.out.println("");
 }

}
