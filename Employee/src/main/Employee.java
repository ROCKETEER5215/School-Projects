package main;

/**
 * Created by Justin Wallace on 6/20/2016.
 */
public class Employee
{
 private String name;
 private String id;

 public Employee()
 {
  name = "";
  id = "000-00-0000";
 }

 public Employee(String name)
 {
  this.name = name;
  this.id = "000-00-0000";
 }

 public Employee(String name,String id)
 {
  this.name = name;
  this.id = id;
 }

 public String getName()
 {
  return this.name;
 }

 public void setName(String name)
 {
  this.name = name;
 }

 public String getID()
 {
  return this.id;
 }

 public void setID(String id)
 {
  this.id = id;
 }

}
