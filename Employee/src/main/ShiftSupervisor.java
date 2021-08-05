package main;

/**
 * Created by Justin Wallace on 6/20/2016.
 */
public class ShiftSupervisor extends Employee
{
 private double annualSalary;
 private double annualProductionBonus;

 public ShiftSupervisor()
 {
  annualSalary = 0;
  annualProductionBonus= 0.0;
 }

 public ShiftSupervisor(double annualSalary, double bonus)
 {
  this.annualSalary = annualSalary;
  this.annualProductionBonus= bonus;
 }

 public ShiftSupervisor(String name, String id, double annualSalary, double bonus)
 {
  super(name,id);
  this.annualSalary =annualSalary;
  this.annualProductionBonus=bonus;
 }

 public double getAnnualSalary()
 {
  return annualSalary;
 }

 public void setAnnualSalary(double annualSalary)
 {
  this.annualSalary = annualSalary;
 }

 public double getAnnualProductionBonus()
 {
  return annualProductionBonus;
 }

 public void setAnnualProductionBonus(double bonus)
 {
  this.annualProductionBonus = bonus;
 }

}
