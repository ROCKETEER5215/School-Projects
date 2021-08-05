package main;

/**
 * Created by Justin Wallace on 6/20/2016.
 */
public class TeamLeader extends ProductionWorker
{
 private double monthlyBonus;
 private int requiredTrainingHours;
 private int attendedTrainingHours;

 public TeamLeader()
 {
  monthlyBonus = 0.0;
  requiredTrainingHours = 0;
  attendedTrainingHours = 0;
 }

 public TeamLeader(double monthlyBonus,int requiredTrainingHours,int attendedTrainingHours)
 {
  this.monthlyBonus = monthlyBonus;
  this.requiredTrainingHours = requiredTrainingHours;
  this.attendedTrainingHours = attendedTrainingHours;
 }

 public TeamLeader(String name,String id,int hours,double rate,double monthlyBonus)
 {
  super(name,id,hours,rate);
  this.monthlyBonus = monthlyBonus;
 }

 public double getMonthlyBonus()
 {
  return monthlyBonus;
 }

 public void setMonthlyBonus(double monthlyBonus)
 {
  this.monthlyBonus = monthlyBonus;
 }

 public int getRequiredTrainingHours()
 {
  return requiredTrainingHours;
 }

 public void setRequiredTrainingHours(int requiredTrainingHours)
 {
  this.requiredTrainingHours = requiredTrainingHours;
 }

 public int getAttendedTrainingHours()
 {
  return attendedTrainingHours;
 }

 public void setAttendedTrainingHours(int attendedTrainingHours)
 {
  this.attendedTrainingHours = attendedTrainingHours;
 }

}
