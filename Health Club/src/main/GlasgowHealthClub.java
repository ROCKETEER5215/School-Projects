package main;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class GlasgowHealthClub extends JFrame
{
 private final int windowWidth = 300;
 private final int windowHeight = 350;
 private JPanel pane;
 private CalculateClubFees actionListener;

 private String membership;
 private Box membershipBox;
 private ButtonGroup membershipGroup;
 private JRadioButton singleRB;
 private JRadioButton familyRB;

 private String additional;
 private Box additionalBox;
 private JCheckBox golfCB;
 private JCheckBox tennisCB;
 private JCheckBox racquetballCB;

 private JLabel basicFee;
 private JTextField basicFeesOutput;

 private JLabel additionalFee;
 private JTextField additionalFeesOutput;

 private JLabel monthlyDues;
 private JTextArea monthlyDuesOutput;

 private Box buttonBox;
 private JButton calculateButton;
 private JButton exitButton;

 public GlasgowHealthClub()
 {
  setTitle("Glasgow Health Club");

  setSize(windowWidth, windowHeight);

  setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

  buildPanel();

  add(pane);

  setVisible(true);
 }

 private void buildPanel()
 {
  actionListener = new CalculateClubFees();

  membership = "Membership";
  singleRB = new JRadioButton("Single");
  singleRB.addActionListener(actionListener);
  familyRB = new JRadioButton("Family");
  familyRB.addActionListener(actionListener);

  additional = "Additional";
  golfCB = new JCheckBox("Golf");
  golfCB.addActionListener(actionListener);
  tennisCB = new JCheckBox("Tennis");
  tennisCB.addActionListener(actionListener);
  racquetballCB = new JCheckBox("Racquetball");
  racquetballCB.addActionListener(actionListener);

  basicFee=new JLabel("Basic fee:");
  basicFeesOutput = new JTextField(10);

  additionalFee = new JLabel("Additional fee:");
  additionalFeesOutput = new JTextField(10);

  monthlyDues = new JLabel("Monthly dues:");
  monthlyDuesOutput = new JTextArea(3,10);

  calculateButton = new JButton("Calculate");
  calculateButton.addActionListener(actionListener);

  exitButton = new JButton("Exit");
  exitButton.addActionListener(actionListener);

  pane = new JPanel();
  pane.setLayout(new GridBagLayout());

  membershipBox = Box.createVerticalBox();
  membershipGroup = new ButtonGroup();
  membershipGroup.add(singleRB);
  membershipGroup.add(familyRB);

  membershipBox.add(singleRB);
  membershipBox.add(familyRB);
  membershipBox.setBorder(BorderFactory.createTitledBorder(membership));
  addItem(pane,membershipBox,0,0,20,20,GridBagConstraints.NORTHWEST);

  additionalBox = Box.createVerticalBox();
  additionalBox.add(golfCB);
  additionalBox.add(tennisCB);
  additionalBox.add(racquetballCB);
  additionalBox.setBorder(BorderFactory.createTitledBorder(additional));
  addItem(pane,additionalBox,2,2,1,1,GridBagConstraints.ABOVE_BASELINE);

  addItem(pane,basicFee,0,3,1,1,GridBagConstraints.NORTHWEST);
  addItem(pane,basicFeesOutput,0,3,1,1,GridBagConstraints.WEST);

  addItem(pane,additionalFee,2,3,1,1,GridBagConstraints.NORTHWEST);
  addItem(pane,additionalFeesOutput,2,3,1,1,GridBagConstraints.WEST);

  addItem(pane,monthlyDues,0,4,1,1,GridBagConstraints.NORTHWEST);
  addItem(pane,monthlyDuesOutput,0,4,1,2,GridBagConstraints.WEST);

  buttonBox = Box.createHorizontalBox();
  buttonBox.add(calculateButton);
  buttonBox.add(Box.createHorizontalGlue());
  buttonBox.add(exitButton);
  addItem(pane,buttonBox,2,5,1,1,GridBagConstraints.EAST);
 }

 private class CalculateClubFees implements ActionListener
 {
  private int single = 50;
  private int family = 90;
  private int golf = 0;
  private int tennis = 0;
  private int racquetball = 0;
  private int additionalTotal;
  private int monthlyTotal;

  public void actionPerformed(ActionEvent e)
  {

    // CalculateButton
    if (e.getSource() == calculateButton)
    {
     if (singleRB.isSelected())
     {
      if (golfCB.isSelected())
      {
       golf = 25;
      }
      else
      {
       golf=0;
      }
      if (tennisCB.isSelected())
      {
       tennis = 30;
      }
      else
      {
       tennis=0;
      }
      if (racquetballCB.isSelected())
      {
       racquetball = 20;
      }
      else
      {
       racquetball=0;
      }

      basicFeesOutput.setText("$" + single);

      additionalTotal = golf + tennis + racquetball;
      additionalFeesOutput.setText("$" + additionalTotal);

      monthlyTotal = single + additionalTotal;
      monthlyDuesOutput.setText("$" + monthlyTotal);
      additionalTotal=0;
      monthlyTotal=0;
     }

     if (familyRB.isSelected())
     {
      if (golfCB.isSelected())
      {
       golf = 35;
      }
      else
      {
       golf=0;
      }
      if (tennisCB.isSelected())
      {
       tennis = 50;
      }
      else
      {
       tennis=0;
      }
      if (racquetballCB.isSelected())
      {
       racquetball = 30;
      }
      else
      {
       racquetball=0;
      }

      basicFeesOutput.setText("$" + family);

      additionalTotal = golf + tennis + racquetball;
      additionalFeesOutput.setText("$" + additionalTotal);

      monthlyTotal = family + additionalTotal;
      monthlyDuesOutput.setText("$" + monthlyTotal);
      additionalTotal=0;
      monthlyTotal=0;
     }
    }

    // ExitButton
    if (e.getSource() == exitButton)
    {
     System.exit(0);
    }
  }
 }

 private void addItem(JPanel pane,JComponent comp,int x, int y, int width,int height,int align)
 {
  GridBagConstraints gc = new GridBagConstraints();

  gc.gridx = x;
  gc.gridy = y;
  gc.gridwidth = width;
  gc.gridheight = height;
  gc.weightx = 100.0;
  gc.weighty = 100.0;
  gc.insets = new Insets(5,5,5,5);
  gc.anchor = align;
  gc.fill = GridBagConstraints.NONE;
  pane.add(comp,gc);
 }
}
