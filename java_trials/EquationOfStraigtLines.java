import java.io.*;
import static java.lang.Math.pow;

 
public class P{
 
    static void StraightLineFit(int x[], int y[])
    {
        int n = x.length;
        double m, c, sum_x = 0, sum_y = 0,
                     sum_xy = 0, sum_x2 = 0;
        for (int i = 0; i < n; i++) {
            sum_x += x[i];
            sum_y += y[i];
            sum_xy += x[i] * y[i];
            sum_x2 += pow(x[i], 2);
        }
 
        m = (n * sum_xy - (sum_x) * sum_y) / (n * sum_x2 - pow(sum_y, 2));
        c = (sum_y - m * sum_x) / n;
 
        System.out.println("m = " + m + "\n");System.out.println("c = " + c + "\n");
        System.out.println("The straight line equation for the given xi and yi");
        System.out.println("y=(" + m + ")x+" + c + "");
        
    }
 
    // Driver main function
    public static void main(String args[])
    {
        
        int x[] = {2,4};
        int y[] = {3,4};
        StraightLineFit(x, y);
    }
}