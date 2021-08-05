package main;


public class Main
{
 public static void main(String[] args)
 {
  //Employee
  Employee bob = new Employee("Bob Smith","345-12-6343");
  System.out.println(bob.getName() + ", ID: " + bob.getID());
  bob.setName("Bobby Smith");
  bob.setID("999-12-6343");
  System.out.println(bob.getName()+", ID: "+bob.getID());

  System.out.println("");

  //ProductionWorker
  ProductionWorker bill = new ProductionWorker("Bill Smith", "756-55-4488", 30, 2.50);
  System.out.println(bill.getName()+", ID: "+bill.getID()+", hours: "+bill.getHours()+", rate: "+bill.getRate());
  bill.setName("Billy The Smith");
  bill.setID("999-88-9999");
  bill.setHours(100);
  bill.setRate(0.1);
  System.out.println(bill.getName()+", ID: "+bill.getID()+", hours: "+bill.getHours()+", rate: "+bill.getRate());

  System.out.println("");

  //ShiftSupervisor
  ShiftSupervisor joe = new ShiftSupervisor("Joe IO", "111-99-2397", 6000.00, 9000.0);
  System.out.println(joe.getName()+", ID: "+joe.getID()+", salary: "+joe.getAnnualSalary()+
          ", bonus: "+joe.getAnnualProductionBonus());
  joe.setName("One Eyed Joe");
  joe.setID("777-00-1155");
  joe.setAnnualSalary(0.0);
  joe.setAnnualProductionBonus(1000000.0);
  System.out.println(joe.getName()+", ID: "+joe.getID()+", salary: "+joe.getAnnualSalary()+
          ", bonus: "+joe.getAnnualProductionBonus());

  System.out.println("");

  //TeamLeader
  TeamLeader jack = new TeamLeader("Jack IO","101-90-5057", 40, 20.50, 100.50);
  jack.setRequiredTrainingHours(5);
  jack.setAttendedTrainingHours(3);
  System.out.println(jack.getName()+", ID: "+jack.getID()+", hours: "+jack.getHours()+", rate: "+jack.getRate()+
          ", required training hours: "+jack.getRequiredTrainingHours()+
          ", attended training hours: "+jack.getAttendedTrainingHours()+
          ", bonus: "+jack.getMonthlyBonus());
  jack.setName("Jack Black");
  jack.setID("909-00-1117");
  jack.setHours(0);
  jack.setRate(1000.50);
  jack.setRequiredTrainingHours(100);
  jack.setAttendedTrainingHours(101);
  jack.setMonthlyBonus(-0.0);
  System.out.println(jack.getName()+", ID: "+jack.getID()+", hours: "+jack.getHours()+", rate: "+jack.getRate()+
          ", required training hours: "+jack.getRequiredTrainingHours()+
          ", attended training hours: "+jack.getAttendedTrainingHours()+
          ", bonus: "+jack.getMonthlyBonus());

 }
}
