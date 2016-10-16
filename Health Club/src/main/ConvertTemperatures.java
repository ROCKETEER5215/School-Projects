package main;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.Arc2D;

/**
 * Created by Justin Wallace on 6/17/2016.
 */
public class ConvertTemperatures extends JFrame
{
 public final int windowWidth =300;
 public final int windowHeight=400;
 public JPanel pane;
 public JLabel temperatureLabel;
 public JTextField temperatureField;

 public JButton F2CButton;
 public JButton C2FButton;
 public JTextArea output;



 public ConvertTemperatures()
 {
  setTitle("Area of Rectangle");


  setSize(windowHeight,windowWidth);

  setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);


  buildPanel();
  add(pane);


  setVisible(true);
 }

 public void buildPanel()
 {
  temperatureLabel = new JLabel("Enter length of rectangle");

  temperatureField = new JTextField(20);

  F2CButton = new JButton("convert f to c");
  F2CButton.addActionListener(new ConvertTemperature());
  C2FButton= new JButton("Calculate Area");

  C2FButton.addActionListener(new ConvertTemperature());

  output = new JTextArea(3,20);




  pane = new JPanel();

  pane.add(temperatureLabel);
  pane.add(temperatureField);
  pane.add(F2CButton);
  pane.add(C2FButton);
  pane.add(output);



  return;
 }


 private class ConvertTemperature implements ActionListener
 {
  public void actionPerformed(ActionEvent e)
  {
   double temperature, convertedTemperature;
   temperature = Double.parseDouble(temperatureField.getText());

   if (e.getSource() == F2CButton)
   {
    convertedTemperature = (temperature-32)*5.0/9.0;

   }
   else
   {
    convertedTemperature = temperature * 9.0/5.0+32;
   }
   output.setText("Area of Rectangle is: " + convertedTemperature);
   //JOptionPane.showMessageDialog(null, "Area of Rectangle is: " + area);
   return;
  }

   /**output.setText("Area of Rectangle is: " + convertedTemperature);
   //JOptionPane.showMessageDialog(null, "Area of Rectangle is: " + area);
   return;**/
  }
 }


