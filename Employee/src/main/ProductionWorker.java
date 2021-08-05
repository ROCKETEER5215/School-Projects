package main;

/**
 * Created by Justin Wallace on 6/20/2016.
 */
public class ProductionWorker extends Employee
{
 private int hours;
 private double rate;

 public ProductionWorker()
 {
  hours = 0;
  rate = 0.0;
 }

 public ProductionWorker(int hours, double rate)
 {
  this.hours = hours;
  this.rate = rate;
 }

 public ProductionWorker(String name, String id,int hours,double rate)
 {
  super(name,id);
  this.hours =hours;
  this.rate=rate;
 }

 public int getHours()
 {
  return hours;
 }

 public void setHours(int hours)
 {
  this.hours = hours;
 }

 public double getRate()
 {
  return rate;
 }

 public void setRate(double rate)
 {
  this.rate = rate;
 }

}
